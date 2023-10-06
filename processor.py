import nltk
import tensorflow as tf
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
import pandas as pd

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('omw-1.4')

model = tf.keras.models.load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('job_intents.json', encoding='utf-8').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

lemmatizer = WordNetLemmatizer()

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    exclusive_intents = ["vm_count","profile_type","owner","batch_autotest_path","scratch"]
    for i in list_of_intents:
        if(i['tag']== tag):
            if(tag in exclusive_intents):
                if(tag == "vm_count"):
                    set_flag(1)
                elif(tag == "profile_type"):
                    set_flag(2)
                elif(tag == "owner"):
                    set_flag(3)
                elif(tag == "batch_autotest_path"):
                    set_flag(4)
                elif(tag == "scratch"):
                    set_flag(5)

                result = "Enter Profile Name"
                break
            else:
                result = random.choice(i['responses'])
                set_flag(0)
                break
        else:
            result = "You must ask the right questions"
    return result



def fetch_profile_data(msg):
    profile_data = pd.read_excel('./Profile_details.xlsx')

    try:
        profile = profile_data[profile_data['Profile Name'].str.contains(msg, case=False, na=False)]

        if not profile.empty:
            if not len(profile) == 1:
                res = profile['Profile Name'].tolist()
            else:
                res = fetch_single_value(profile)


    except Exception as e:
        return str(e)

    return res
    

def fetch_single_value(profile):
    context = get_flag()
    if context == 1:
        res = profile["VM's Count"].values[0]
        
    elif context == 2:
        res =  profile["Profile Type"].values[0]

    elif context == 3:
        res = profile["OWNER"].values[0]

    elif context == 4:
        res = profile["APT Batch name and Autotest TP path"].values[0]

    elif context == 5:
        res = profile["Scratch Installation Job"].values[0]
        
    set_flag(0)
    return res

    

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


flag = 0

# Function to change the global variable
def set_flag(value):
    global flag
    flag = value

# Function to get the global variable
def get_flag():
    return flag