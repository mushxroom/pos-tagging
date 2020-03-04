import nltk
import matplotlib.pyplot as plt
import math
import re
import numpy as np
import pickle


with open("wsj1-18.training", "r") as train_file:
    train_whole_lines = train_file.readlines()

with open("wsj1-18.training", "r") as train_file1:
    train_all=train_file1.read().split()
   

#####initial probability pi:
pi={}
#####transition probability A:
tt={}
#####observation probability B:
tw={}
all_words={}
unka=[]
uw=[]
ut=[]
it=0
print(len(train_all))

for word in train_all:
    if it==0 or it%2==0: 
        uw.append(word)
    else:
        ut.append(word)
    it=it+1
uniq_word=list(set(uw))
states=list(set(ut))
##Counting words
for word in uw:
    all_words[word]=all_words.get(word,0)
    all_words[word]=all_words[word]+1

print(len(uw))

        
#find unka
for k in all_words:
    #print(k)
    if all_words.get(k,0)<=1:
        unka.append(k)

uw_new=[]
for k in uw:
    if all_words.get(k,0)<=2:
        uw_new.append("UNKA")
    else:
        uw_new.append(k)




for i in range(len(ut)-1):
        this_tag=ut[i]
        next_tag=ut[i+1]
        this_word=uw_new[i]
        
        ##calculate A:
        tt[this_tag]=tt.get(this_tag,{})
        tt[this_tag][next_tag]=tt[this_tag].get(next_tag,0)
        tt[this_tag][next_tag]=tt[this_tag][next_tag]+1
for i in range(len(ut)):
        ##calculate B:
        this_word=uw_new[i]
        this_tag=ut[i]
        tw[this_tag]=tw.get(this_tag,{})
        tw[this_tag][this_word]=tw[this_tag].get(this_word,0)
        tw[this_tag][this_word]=tw[this_tag][this_word]+1




for train_whole in train_whole_lines:
    train_single = train_whole.split()
    #print(train_single)
    train_word=[]
    train_tag=[]

    iter=0
    for i in train_single:
        if iter==0 or iter%2==0: 
            train_word.append(i)
        else:
            train_tag.append(i)
        iter=iter+1
    start=train_tag[0]
    pi[start]=pi.get(start,0)
    pi[start]=pi[start]+1







#print("start probabilities")
##convert to probabilities
for i in tt:
    this_tt=tt[i]
    ss=sum(this_tt.values())
    for next in this_tt:
        this_tt[next]=math.log((this_tt[next]+1)/(ss+len(states)))
        #this_tt[next]=this_tt[next]/ss
    #sort_this=sorted(this_tt.items(), key = lambda d:d[1], reverse=True)
    tt[i]=this_tt

for i in tw:
    this_tw=tw[i]
    ss=sum(this_tw.values())
    for next in this_tw:
        this_tw[next]=math.log((this_tw[next]+1)/(ss+len(uniq_word)))
        #this_tw[next]=this_tw[next]/ss
    #sort_this=sorted(this_tw.items(), key = lambda d:d[1],reverse=True)
    tw[i]=this_tw


ss_pi=sum(pi.values())
for i in pi:
    #print(i) 
    pi[i]=math.log((pi[i]+1)/(ss_pi+len(pi.keys())))
    #pi[i]=pi[i]/ss_pi
    
  


#print(tw["VBZ"])
model1={}
model1["A"]=tt
model1["B"]=tw
model1["pi"]=pi
model1["states"]=states

pickle.dump(model1,open('model.pyc','wb'))
