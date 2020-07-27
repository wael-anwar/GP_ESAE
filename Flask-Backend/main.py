import flask
import tensorflow as tf
from tensorflow.keras.models import load_model
import tensorflow.keras.backend as be
import string
import numpy as np
import pickle
import json

app=flask.Flask("__main__")

word2indexT = pickle.load(open("D:\\Anime\\Faculty Of Engineering\\GP\\Project\\WordEmbeddings\\word-index.pkl","rb"))
index2word = pickle.load(open("D:\\Anime\\Faculty Of Engineering\\GP\\Project\\WordEmbeddings\\index-word.pkl","rb"))
char2index = pickle.load(open("D:\\Anime\\Faculty Of Engineering\\GP\\Project\\WordEmbeddings\\char-index.pkl","rb"))
word2index =dict()
for key,value in word2indexT.items():
  if 1<=value < 100001:
    word2index[key]=value
    
word2index["UNK"] = 100001

embeddings1 = np.load("D:\\Anime\\Faculty Of Engineering\\GP\\Project\\WordEmbeddings\\central_embeddings.npy")
embeddings2 = np.load("D:\\Anime\\Faculty Of Engineering\\GP\\Project\\WordEmbeddings\\context_embeddings.npy")
embeddings = embeddings1 + embeddings2
zer = np.full((1,100),0.000001)
embeddings = np.append(embeddings,zer,axis=0)

def InputPreprocess(questions,contexts):
  questionList=[]
  contextList=[]
  for question in questions:
    for word in question.split():
      questionList.append(word.lower())
  for context in contexts:
    for word in context.split():
      contextList.append(word.lower())

  userQuestionEmbedded, userContextEmbedded, _,userQuestionCharEmbedded,userContextCharEmbedded = Embed([questionList],[contextList],["-"])

  for i in range(len(userQuestionCharEmbedded)):
    userQuestionCharEmbedded= tf.keras.preprocessing.sequence.pad_sequences(userQuestionCharEmbedded[i],padding='post',maxlen=16,value=len(char2index))
  userQuestionCharEmbedded = be.expand_dims(userQuestionCharEmbedded,axis=0)

  for i in range(len(userContextCharEmbedded)):
    userContextCharEmbedded= tf.keras.preprocessing.sequence.pad_sequences(userContextCharEmbedded[i],padding='post',maxlen=16,value=len(char2index))
  userContextCharEmbedded = be.expand_dims(userContextCharEmbedded,axis=0)

  # print("Before Padding")
  userQuestionEmbedded = tf.keras.preprocessing.sequence.pad_sequences(userQuestionEmbedded,padding='post',truncating="post",dtype='float32',maxlen=50)
  userContextEmbedded = tf.keras.preprocessing.sequence.pad_sequences(userContextEmbedded,padding='post',truncating="post",dtype='float32',maxlen=250)
  userQuestionCharEmbedded = tf.keras.preprocessing.sequence.pad_sequences(userQuestionCharEmbedded,padding='post',truncating="post",maxlen=50,value=len(char2index))
  userContextCharEmbedded = tf.keras.preprocessing.sequence.pad_sequences(userContextCharEmbedded,padding='post',truncating="post",maxlen=250,value=len(char2index))

  return userQuestionEmbedded,userContextEmbedded,userQuestionCharEmbedded,userContextCharEmbedded


def OutputProcess(p,context):
  answers =[]
  for index in range(len(p[0])):
    start = np.argmax(p[0][index])
    end = np.argmax(p[1][index])

    contextList = context[index].split()
    if start<=end:
      answers.append(" ".join(contextList[start:end+1]))

    else:
      maxPos=0
      answer=""
      for i in range(len(contextList)):
        for j in range(i,len(contextList)):
          if p[0][index][i]*p[1][index][j] >maxPos:
            maxPos = p[0][0][i]*p[1][0][j]
            answer = " ".join(contextList[i:j+1])

      answers.append(answer)
  return answers

def Embed(questions,contexts,answers):
    unk = 0
    nk = 0
    e_q=[]      #embedded question
    e_qC=[]     #embedded question Characters
    e_c=[]      #embedded context
    e_cC=[]      #embedded context Characters

    e_a=[]      #embedded answer

    for i in range(len(questions)):
      question=[]
      questionChars=[]
      for word in questions[i]:
        if word.strip(string.punctuation) in word2index:
          question.append(embeddings[word2index[word.strip(string.punctuation)]])
          nk+=1
        else:
          unk+=1          
          question.append(embeddings[word2index["UNK"]])

        chars=[]
        for char in word:
          if char in char2index:
            chars.append(char2index[char])
        questionChars.append(np.array(chars))

      context=[]
      contextChars=[]
      for word in contexts[i]:
        if word.strip(string.punctuation) in word2index:
          context.append(embeddings[word2index[word.strip(string.punctuation)]])
          nk+=1
        else:
          unk+=1
          context.append(embeddings[word2index["UNK"]])

        chars=[]
        for char in word:
          if char in char2index:
            chars.append(char2index[char])
        contextChars.append(np.array(chars))


      answer=[]
      for word in answers[i]:
        if word.strip(string.punctuation) in word2index:
          answer.append(embeddings[word2index[word.strip(string.punctuation)]])
          nk+=1
        else:
          unk+=1
          answer.append(embeddings[word2index["UNK"]])



      e_q.append(question)
      e_qC.append(questionChars)
         
      e_c.append(context)
      e_cC.append(contextChars)

      e_a.append(answer)

    print("Unk",unk,"nk",nk)

    return np.array(e_q), np.array(e_c), np.array(e_a),np.array(e_qC),np.array(e_cC)

# QWE,CWE,QCE,CCE = InputPreprocess(userQuestion,userContext)

# p=model.predict([QWE,CWE,QCE,CCE ])
# answer = OutputProcess(p,userContext[0])
# print(p)
# print("Context:\n",userContext[0],"\nQuestion:\n",userQuestion[0],"\nAnswer:\n",answer)
conte=""
start=0
model=""

@app.route("/")
def my_index():
    return flask.render_template("index.html",token="Hello Flask+React (GP ESAE)")

@app.route("/model/<string:question>")
def answerModel(question):
    global start
    global model
    global conte
    print("question:",question," context:",conte)
    if start==0:
        model = load_model("D:\\Anime\\Faculty Of Engineering\\GP\\Project\\QanetModel")
        start=1
    # print("loaded")
    userQuestion=[question]
    userContext = [conte]

    QWE,CWE,QCE,CCE = InputPreprocess(userQuestion,userContext)
    p=model.predict([QWE,CWE,QCE,CCE ])
    answer = OutputProcess(p,userContext)
    return {'ans': answer[0]}  


@app.route("/context/<string:cont>")
def getContext(cont):
    print(cont)
    global conte
    conte = cont
    return {'context':conte}
app.run(debug=True)
