import json
import numpy as np
from nltk_utils import tokenize,stem,bag_of_words
from training_model import NeuralNetwork
#pytorch 
import torch 
import torch.nn as nn
from torch.utils.data import Dataset,DataLoader



with open('intents.json','r') as f:
    intents = json.load(f)



all_words = []
tags = []
#a list of tuples : each tuple will associate the list of tokenized words specific to particular tag
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    
    for pattern in intent['patterns']:
        words = tokenize(pattern)
        all_words.extend(words)
        xy.append((words,tag))


ignore_words = ['?',':','!','.',',']
all_words = [stem(w) for w in all_words if w not in ignore_words]



all_words = sorted(set(all_words))
tags = sorted(set(tags))


X_train = []
Y_train = []
for (tokenized_pattern_sentence, tag) in xy:
    bag = bag_of_words(tokenized_pattern_sentence,all_words)
    X_train.append(bag)

    label = tags.index(tag)
    Y_train.append(label)

X_train = np.array(X_train)
Y_train = np.array(Y_train)

class ChatDataSet(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = Y_train

    #data[idx]
    def __getitem__(self, index):
        return self.x_data[index],self.y_data[index]
    
    def __len__(self):
        return self.n_samples
    
#Hyperparameters 
batch_size = 8
hidden_size = 8 
output_size = len(tags)
input_size = len(X_train[0])
learning_rate = 0.001
num_epochs = 1000


dataset = ChatDataSet()
train_loader = DataLoader(dataset=dataset,batch_size=batch_size,shuffle=True,num_workers=0)

device =torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNetwork(input_size,hidden_size,output_size).to(device)

#loss and optimizer 
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr = learning_rate)

for epoch in range(num_epochs):
    for(words,labels) in train_loader:
        words = words.to(device)
        labels = labels.to(device,dtype = torch.int64)

        #forward

        outputs = model(words)
        loss = criterion(outputs,labels)

        #backward and optimizer step 
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1)% 100 == 0:
        print(f'epoch {epoch + 1 } / {num_epochs}, loss = {loss.item():.4}')
    
print(f'final loss , loss ={loss.item():.4f}')

data = {
    "model_state" : model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags":tags
}

FILE = "data.pth"
torch.save(data,FILE)

print(f'training complete. file saved to {FILE}')