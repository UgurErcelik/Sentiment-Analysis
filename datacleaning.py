import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk 
import string
import re



data = pd.read_csv('lemessi.csv')

df = pd.DataFrame(data['tweet'])

stop_word_list = stopwords.words('english')


#print(df)

def cleanTxt(text):
    text = re.sub(r'@[A-Za-z0-9]+','',text)
    text = re.sub(r'#','',text)
    text = re.sub(r'RT[\s]+','',text)
    text = re.sub(r'https?:\/\/\S+','',text)
    text = re.sub("["u"\U0001F600-\U0001F64F""]",'',text)
    text = "".join(u for u in text if u not in ("?", ".", ";", ":", "!",",","\n",")","'",'"',"(","[","]","-","...","/","_",">","@","|","’","+","“","&","%"))
    text = re.sub('[0-9]', '', text)
    text = ''.join([i for i in text if not i.isdigit()])
    text = re.sub('[\d\s]',' ',str(text))
    text = re.sub('[^\w\s]',' ',str(text))
    text = re.sub(r'\s+',' ',text)
    text = re.sub('[^\w\s]',' ',str(text))
    
    WPT = nltk.WordPunctTokenizer()
    tokens=WPT.tokenize(text)
    filtered_tokens = [token for token in tokens if token not in stop_word_list]
    single_doc=' '.join(filtered_tokens)
    text = single_doc
    
    text = single_doc.lower()
    
    

    return text

df['tweet'] = df['tweet'].apply(cleanTxt)
dframe = pd.DataFrame(df['tweet'])
dframe.to_csv("lemessi10.csv",encoding="utf-8-sig")




    

