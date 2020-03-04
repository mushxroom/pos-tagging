import nltk
import matplotlib.pyplot as plt
import math
import re
import numpy as np
import pickle

import pickle

model = pickle.load(open('model.pyc', 'rb'))
ini_pro=model["pi"]
trans_pro=model["A"]
obs_pro=model["B"]
states=model["states"]
#print(obs_pro["POS"])
print(type(obs_pro))
with open("wsj19-21.testing", 'r') as TestFile:
    test_file=TestFile.read().split()
with open("wsj19-21.truth",'r') as AnswerFile:
    ans_file=AnswerFile.read().split()
with open("wsj19-21.testing", 'r') as TestFile:
    test_sentences=TestFile.readlines()


itt=0
ans_uw=[]
ans_ut=[]
#print(len(test_file),len(ans_file))

for word in ans_file:
    if itt==0 or itt%2==0: 
        ans_uw.append(word)
    else:
        ans_ut.append(word)
    itt=itt+1
#print(len(ans_uw))


test_uw=[]
for word in test_file:
    test_uw.append(word)

iterator=0
#print(len(test_uw))
tag_seq=[]
for sent in test_sentences:
    state_seq=[]  
    alpha={}
    observation=sent.split()
    length_sent=len(observation)
    
   
    for obs in range(length_sent):

        if obs==0:
            alpha[0]={}
            for tag in states:
                #alpha[0][tag]=ini_pro.get(tag,0)*obs_pro[tag].get(observation[0],0)
                alpha[0][tag]=math.exp(ini_pro.get(tag,float("-Inf"))+obs_pro[tag].get(observation[0],float("-Inf")))
                #print(ini_pro.get(tag,0),obs_pro[tag].get(observation[0],0))
            #print(observation[obs])
        else:
            alpha[obs]={}
            for tag in states:
                prev_alpha_sum=0
                for prev in states:
                    #prev_alpha_sum+=alpha[obs-1][prev]*trans_pro[prev].get(tag,0)
                    if trans_pro[prev].get(tag,float("-Inf"))==float("Inf"):
                        prev_alpha_sum+=0
                    else:
                        prev_alpha_sum+=alpha[obs-1][prev]*math.exp(trans_pro[prev].get(tag,float("-Inf")))
                #alpha[obs][tag]=prev_alpha_sum*obs_pro[tag].get(observation[obs],0)
                if obs_pro[tag].get(observation[obs],float("-Inf"))==float("-Inf"):
                    alpha[obs][tag]=0
                else:
                    alpha[obs][tag]=prev_alpha_sum*math.exp(obs_pro[tag].get(observation[obs],float("-Inf")))
                #print(prev_alpha_sum,obs_pro[tag].get(observation[obs],0))
                #this_obs=observation[i]
                #print(alpha[obs][tag])
           # print(observation[obs],alpha[obs])
    #print(alpha)
    for integ in range(length_sent):
        #print(length_sent)
        index=length_sent-1-integ
        st=max(alpha[index],key=alpha[index].get)
        #print(st)
        state_seq.append(st)

    tag_seq=state_seq+tag_seq
    #print(state_seq)

        #for tag in states:

tag_seq.reverse()
print(len(tag_seq))
print(len(ans_ut))
correct=0
for i in range(len(ans_ut)):
    if tag_seq[i]==ans_ut[i]:
        correct+=1
print(correct/len(ans_ut))


