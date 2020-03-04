eecs595.py stores the code that trains the model.
pos.py stores the code that tests and gives the accuracy.
Model.pyc stores a dictionary that includes the initial("pi"), transition("A") and emmission("B") probabilities, along with a dictonary of tags. The probabilities are calculated into log, and for the case of not found, the probability is specified as float("-Inf").
Laplace smoothing is also applied to the model, with the number of unique words and tags as the additional number for tag-word and tag-tag.
In addition, words that occur less than three times are marked as UNKA.
During implementation, I also found NOT using log can also achieve a good accuracy using the test file and it also saves running time. However, log should be adapted to accomodate other circumstances and is worth sacrificing the time. Using this model, the accuracy is about 92.1 and the running time takes around 10min. 
