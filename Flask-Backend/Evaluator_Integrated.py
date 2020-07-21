from itertools import product
from collections import defaultdict
import numpy as np
from scipy.spatial.distance import euclidean
import pulp
import gensim
import gensim.downloader as api
import pickle
from sklearn.metrics.pairwise import cosine_similarity as cosine
import json
from itertools import islice
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import re
import string
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from collections import Counter



def Load_Data():
    
    w2i = pickle.load(open("D:\\University\\Semester 10 Spring 2020\\GP\\GP_ESAE\\Flask-Backend\\word-index.pk","rb"))
    i2w = pickle.load(open("D:\\University\\Semester 10 Spring 2020\\GP\\GP_ESAE\\Flask-Backend\\index-word.pk","rb"))
    CentralEmbedding = np.load("D:\\University\\Semester 10 Spring 2020\\GP\\GP_ESAE\\Flask-Backend\\central_embeddings.npy")
    ContextEmbedding=np.load("D:\\University\\Semester 10 Spring 2020\\GP\\GP_ESAE\\Flask-Backend\\context_embeddings.npy")
    w2v=CentralEmbedding+ContextEmbedding 
    return w2v,w2i,i2w

def tokens_to_fracdict(tokens):
    cntdict = defaultdict(lambda : 0)
    for token in tokens:
        cntdict[token] += 1
    totalcnt = sum(cntdict.values())
    return {token: float(cnt)/totalcnt for token, cnt in cntdict.items()}

def word_mover_distance_probspec(first_sent_tokens, second_sent_tokens, w2v,w2i, lpFile=None):
    all_tokens = list(set(first_sent_tokens+second_sent_tokens))
    wordvecs = {token: w2v[w2i[token]] for token in all_tokens}

    first_sent_buckets = tokens_to_fracdict(first_sent_tokens)
    second_sent_buckets = tokens_to_fracdict(second_sent_tokens)

    T = pulp.LpVariable.dicts('T_matrix', list(product(all_tokens, all_tokens)), lowBound=0)

    prob = pulp.LpProblem('WMD', sense=pulp.LpMinimize)
    prob += pulp.lpSum([T[token1, token2]*euclidean(wordvecs[token1], wordvecs[token2])
                        for token1, token2 in product(all_tokens, all_tokens)])
    for token2 in second_sent_buckets:
        prob += pulp.lpSum([T[token1, token2] for token1 in first_sent_buckets])==second_sent_buckets[token2]
    for token1 in first_sent_buckets:
        prob += pulp.lpSum([T[token1, token2] for token2 in second_sent_buckets])==first_sent_buckets[token1]

    if lpFile!=None:
        prob.writeLP(lpFile)

    prob.solve()

    return prob

def word_mover_distance(first_sent_tokens, second_sent_tokens, w2v,w2i, lpFile=None):
    prob = word_mover_distance_probspec(first_sent_tokens, second_sent_tokens, w2v,w2i, lpFile=lpFile)
    return pulp.value(prob.objective)
  
def my_cos_similarity(vec1,vec2):
    sim = cosine(vec1.reshape(1,-1),vec2.reshape(1,-1))
    return round(float(sim),4)
    
#To lower case
def To_Lower_Text(Text):
    Text = Text.lower()
    return Text

#Split text and get unique words out of it
def Split_Text_Unique(Text): 
    #Text_Split   = re.split(" |\s|(?<!\d)[,.](?!\d)",Text) 
    Text_Split   = re.findall(r'\w+', Text) #split on punctuation marks and symbols
    # gives set of unique words 
    unique_words = set(Text_Split) 
    unique_words = [string for string in unique_words if string != ""]
    return unique_words

#Stemming of sentence
def Stem_Sentence(sentence):
    porter        = PorterStemmer()
    lancaster     = LancasterStemmer()
    token_words   = word_tokenize(sentence)
    stem_sentence = []
    for word in token_words:
        stem_sentence.append(porter.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)

#Lemmetization was better tha stemming to prevent removal of some letters in words as vowels at end
def Lemmetize_Sentence(sentence):
    wordnet_lemmatizer = WordNetLemmatizer()
    Lemm_words         = []
    nltk_tokens        = nltk.word_tokenize(sentence)
    for word in nltk_tokens:
        Lemm_words.append(wordnet_lemmatizer.lemmatize(word))
        #print("Actual: %s  Lemma: %s"  % (word,wordnet_lemmatizer.lemmatize(word)))  
    #return "".join(Lemm_sentence)
    return Lemm_words

#Remove the stopping words in a sentence and ger unique words
def RemoveStoppingWords(text):
    Tokens = Split_Text_Unique(text)
    Words  = []
    for word in Tokens:
        if not word in stopwords.words():
            Words.append(word)
            Words.append(" ")
    return "".join(Words)

#Preprocess the input answer and return its unique, lemmitized, non stopping words
def PreprocessAnswer(Text):
    Text      = To_Lower_Text(Text)
    Text      = RemoveStoppingWords(Text)
    TextWords = Lemmetize_Sentence(Text)
    return TextWords

#Calculate cos similarity between Student answer and Model answer
def OverallCosSimilarity(StudentAnswer,ModelAnswer,w2v,w2i,i2w):
    rows = len(StudentAnswer)+1
    cols = len(ModelAnswer)+1

    EmbeddingMatrix = [[0] * cols for i in range(rows)]
    CheckNeighborsMatrix = [[0] * (cols-1) for i in range(rows-1)]
    GlobalAvg=0
    GlobalCount=0

    
    for word1 in range(len(StudentAnswer)): #Loop on Student Answer
        LocalAvg=0
        Count=0
        for word2 in range(len(ModelAnswer)): #Loop on Model Answer
            #Score = my_cos_similarity(Wt[vocab[StudentAnswer[word1]]],Wt[vocab[ModelAnswer[word2]]])
            Score = my_cos_similarity(w2v[w2i[StudentAnswer[word1]]],w2v[w2i[ModelAnswer[word2]]])
            EmbeddingMatrix[word1][word2] = Score
            #print(EmbeddingMatrix)
            if Score>=0.5:
                LocalAvg+=Score
                Count+=1
                
                #next will be ismaeel embedding criteria
                NeighborWordsStudent = ISM_EMB(StudentAnswer[word1],w2v, w2i, i2w)
                NeighborWordsModel   = ISM_EMB(ModelAnswer[word2]  ,w2v, w2i, i2w)
                if NeighborWordsStudent !=0 and NeighborWordsModel != 0 :
                    if StudentAnswer[word1] in NeighborWordsModel or ModelAnswer[word2] in NeighborWordsStudent:
                        CheckNeighborsMatrix[word1][word2] = 1

        if Count!=0:
            EmbeddingMatrix[word1][-1] = LocalAvg/Count
            GlobalAvg += (LocalAvg/Count)
            GlobalCount+=1
        else:
            EmbeddingMatrix[word1][-1] = 0

    if GlobalCount!=0:
        EmbeddingMatrix[-1][-1] = GlobalAvg/GlobalCount
    else:
        EmbeddingMatrix[-1][-1] = 0

    # ColIndex = list(ModelAnswer)
    # ColIndex.append('avg>=0.5')
    # RowIndex = list(StudentAnswer)
    # RowIndex.append('Overall similarity score')
    # CosSimDataFrame = pd.DataFrame(EmbeddingMatrix, columns=ColIndex, index=RowIndex)
    # print(CosSimDataFrame)
    # CheckNeighborsDataFrame = pd.DataFrame(CheckNeighborsMatrix, columns=list(ModelAnswer), index=list(StudentAnswer))
    # print(CheckNeighborsDataFrame)

    CheckNeighborsSum=np.sum(np.array(CheckNeighborsMatrix))
    NeighborsFlag=0
    if (CheckNeighborsSum>=4):
        NeighborsFlag=1
    return EmbeddingMatrix,NeighborsFlag

# function for calculating the frequency  
def Compute_Word_Frequency(Reference): #From the reference find its count badal ma3od ageb ml answer wa3ml for loop 3l reference,
                                       #kda asr3 w fl akher ashoof el answer word mawgoda fl return walla la2    
    Freq_Dict = Counter(Reference)
    # print(counts)
    # print(Freq_Dict[Answer[0]])
    return Freq_Dict

#Smooth Inverse Frequency measure
def Compute_Answer_SIF(Answer,Reference):
    Reference_Freq_Dict = dict(Compute_Word_Frequency(Reference))
    Answer_SIF_Dict     = {}
    # print([str( 0.001 / ( np.asarray(0.001) + np.asarray([val if key in Answer_unique_words else 0 for key,val in Reference_Freq_Dict.items()] ) ) ) ])
    # x if x%2 else x*100 for x in range(1, 10) 
    # SIF= dict(zip(Answer_unique_words , str( 0.001 / ( np.asarray(0.001) + 
    #                                     np.asarray([val if key in Answer_unique_words else 0 for key,val in Reference_Freq_Dict.items()] ) ) )
    # ) )
    for word in Answer:
        if word in Reference_Freq_Dict:
            Answer_SIF_Dict[word] = 0.001 / (0.001 + Reference_Freq_Dict[word])
        else:
            Answer_SIF_Dict[word] = 1
    return Answer_SIF_Dict

#Length of Document measure, 1 means logical, 0 means not logical
def Document_Length(StudentAnswer,ModelAnswer):
    StudentAnswerCount = len(re.findall(r'\w+', StudentAnswer)) #split on punctuation marks and symbols
    ModelAnswerCount   = len(re.findall(r'\w+', ModelAnswer))
    Len_Score          = StudentAnswerCount / ModelAnswerCount
    #Assume if model ans is 20 words then ans will be nearly 15-30 words
    if (Len_Score <= 1.5 and Len_Score >= 0.75): # 30/20 = 1.5 , 15/20=0.75
        return 1
    else:
        return 0

#Ismaeel's embedding measure, input is a word, output is most similar 10 words to input
def ISM_EMB(WordInput,embeddings,word2index, index2word):
    if WordInput not in word2index: #Out OF Vocabulary
        return 0
    target=embeddings[word2index[WordInput]]
    word_sim={}
    for i in range(1,100000):
        word=embeddings[i]
        theta_sum=np.dot(target,word)
        theta_den=np.linalg.norm(target) * np.linalg.norm(word)
        theta=theta_sum/theta_den
        word=index2word[i]
        word_sim[word]=theta

    words_sorted=sorted(word_sim.items(),key=lambda kv:kv[1],reverse=True)
    #for word,sim in words_sorted[:10]:
        #print(word,sim)
    words_sorted=dict(words_sorted)
    #print(list(words_sorted.keys())[:10])
    return list(words_sorted.keys())[:10]

def WMDNormalization(WMD):
    Max_WMD=max(WMD)
    # if (WMD == None):
    #     WMD=0
    WMDNormalized = [(Max_WMD-element)/Max_WMD for element in WMD]
    
    return WMDNormalized

def EvaluateEssay(StudentsAnswers,ModelAnswer,ModelGrades):
    #embbedding.pk, word2index and index2word files must be in same directory as this file
    w2v,w2i,i2w=Load_Data()
    WMDGrade=[]
    CosSimGrade=[]
    NeighborsGrade=[]
    DocLengthGrade=[]
    OverallGrade=[]
    for StudentAnswer in StudentsAnswers:
        
    #StudentAnswer   = 'FootbALl is similar sports. be keen on practising it'
    #ModelAnswer     = 'you shall Play different sports from time to time'
    #ModelAnswer=StudentAnswer
    #StudentAnswer  = 'i ate pizza yesterday'
    #ModelAnswer    = 'football is good sports. learn to practice it'
    #StudentAnswer  = 'Film action suspense but horror'
    #ModelAnswer    = 'i used to watch movies more frequently'
        StudentAnswerWords  = PreprocessAnswer(StudentAnswer)
        ModelAnswerWords    = PreprocessAnswer(ModelAnswer)

    #example wmd 
    #hint all words passed through the wmd must be preprocessed (lowercase ,not prural and so on)
        WMDGrade.append(word_mover_distance(StudentAnswerWords, ModelAnswerWords, w2v,w2i)) 
    
    #print(WMD) #the less the number the stronger the relation

    #CosSimDataFrame,CheckNeighborsDataFrame     = OverallCosSimilarity(StudentAnswerWords,ModelAnswerWords,w2v,w2i,i2w)
        EmbeddingMatrix,NeighborsFlag = OverallCosSimilarity(StudentAnswerWords,ModelAnswerWords,w2v,w2i,i2w)
    #print(EmbeddingMatrix[-1][-1])
    #print(CosSimDataFrame)
    #print(CheckNeighborsMatrix)
    #print(CheckNeighborsDataFrame)

    #Answer_SIF_Dict = Compute_Answer_SIF(StudentAnswerWords,ModelAnswerWords)
    #print(Answer_SIF_Dict)

        Doc_Length = Document_Length(StudentAnswer,ModelAnswer)
        CosSimGrade.append(0.6 * EmbeddingMatrix[-1][-1])      
        NeighborsGrade.append(0.1  * NeighborsFlag)  
        DocLengthGrade.append(0.05 * Doc_Length)   
    #print(Doc_Length)
    WMD = WMDNormalization(WMDGrade)
    multiplied_WMD = [element * 0.25 for element in WMD]
    #WMDGrade        = 0.4  * WMD
    zipped_lists = zip(CosSimGrade, NeighborsGrade,DocLengthGrade,multiplied_WMD)

    OverallGrade = [x + y +z+w for (x, y,z,w) in zipped_lists]
    
    return OverallGrade

def EvaluateMCQ (StudentAnswer,ModelAnswer,ModelGrade):
    Grade=0
    if StudentAnswer==ModelAnswer:
        Grade=1
    
    return Grade

def EvaluateTF (StudentAnswer,ModelAnswer,ModelGrade):
    Grade=0
    if StudentAnswer==ModelAnswer:
        Grade=1
    else:
        Grade=0
    
    return Grade

def EvaluateComplete (StudentAnswer,ModelAnswer,ModelGrade):
    Grade=0
    w2v,w2i,i2w=Load_Data()
    if StudentAnswer==ModelAnswer:
        Grade=1
    else:
        EmbeddingMatrix,NeighborsFlag = OverallCosSimilarity(StudentAnswer,ModelAnswer,w2v,w2i,i2w)
        Grade =  EmbeddingMatrix[-1][-1]
    
    return Grade
# StudentAnswer   = 'the boy play football daily.'
# ModelAnswer     = 'practice sports more often is useful to the body'

# #StudentAnswer   = 'FootbALl is similar sports. be keen on practising it'
# #ModelAnswer     = 'you shall Play different sports from time to time'

# x=EvaluateAns(StudentAnswer,ModelAnswer)
# print(x)
# x=5
def Evaluator(QuestionType,StudentIDList,StudentsAnswers,ModelAnswers,ModelGrades):
    
    StudentList=[]
    GradeList=[]
    
    if QuestionType=="MCQ":
        for Answers,ModelAns,ModelGrade in zip(StudentsAnswers,ModelAnswers,ModelGrades):
            StudentList=[]
            for Student in (Answers):       
                StudentList.append(EvaluateMCQ(Student,ModelAns,ModelGrade))
            GradeList.append(StudentList)   
        print('MCQ grade list')
        print(GradeList)
        return GradeList
     
    elif QuestionType=="TF":
        for Answers,ModelAns,ModelGrade in zip(StudentsAnswers,ModelAnswers,ModelGrades):
            StudentList=[]
            for Student in (Answers):       
                StudentList.append(EvaluateTF(Student,ModelAns,ModelGrade))
            GradeList.append(StudentList)
        print('tf grade list')
        print(GradeList)
        return GradeList
      
    elif QuestionType=="Complete":
        for Answers,ModelAns,ModelGrade in zip(StudentsAnswers,ModelAnswers,ModelGrades):
            StudentList=[]
            for Student in (Answers):    
                Val = EvaluateComplete(Student,ModelAns,ModelGrade)
                #print('Comp val is ' + str(Val))
                if (Val<0.5):
                    Val=0
                else:
                    Val=1 
                StudentList.append(Val)
            GradeList.append(StudentList)
        print('comp grade list')
        print(GradeList)  
        return GradeList
    
    elif QuestionType=="Essay":
        for Answers,ModelAns,ModelGrade in zip(StudentsAnswers,ModelAnswers,ModelGrades):
            GradeList.append(EvaluateEssay(Answers,ModelAns,ModelGrade))
        print('ess grade list')
        print(GradeList)
        return GradeList
       
    else:
        print("Error Question Type")
        
    return GradeList    

# QuestionType="Essay"
# StudentIDList=[1,2]
# StudentsAnswers=[['Football is a good game i love to play sports from time to time','i ate vegetables and fruit because i was hungry']]
# ModelAnswers=['You shall play sports always because it is good to health']
# ModelGrades=[1]

# Grade=Evaluator(QuestionType,StudentIDList,StudentsAnswers,ModelAnswers,ModelGrades)


#Evaluator()
