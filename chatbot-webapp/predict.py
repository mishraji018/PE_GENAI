#Tokenisation
from nltk.tokenize import word_tokenize
#Stopwords list 
from nltk.corpus import stopwords
#Stemming
from nltk.stem import PorterStemmer
#Lemmatization
from nltk.stem import WordNetLemmatizer
import string
import joblib

def preprocess_text(documents):
    english_stopwords = stopwords.words("english")
    punctuations = string.punctuation
    cleaned_documents = []
    for doc in documents:
        # Step-1 : Lowercase
        raw_text = doc.lower()
        # print("After lowercase: ",raw_text)
        
        tokens = word_tokenize(raw_text)
        # print("Tokens:",tokens)

        filtered_tokens = []
        for word in tokens:
            if word not in english_stopwords:
                filtered_tokens.append(word)
        
        # print("Filtered Tokens :",filtered_tokens)

        clean_tokens = [word for word in filtered_tokens if word not in punctuations]
        # print("After removing punctuations:",clean_tokens)

        lemmatized_words = []
        wnet = WordNetLemmatizer()
        for word in clean_tokens:
            lemmatized_words.append(wnet.lemmatize(word,"v"))
        
        # print("After Lemmatization :",lemmatized_words)

        final_tokens = []
        for word in lemmatized_words:
            if word.isalpha():
                final_tokens.append(word)
        
        # print("Final Tokens:",final_tokens)

        cleaned_text = " ".join(final_tokens)
        # print("Cleaned Text:",cleaned_text)
        
        cleaned_documents.append(cleaned_text)
        # print("="*50)
    return cleaned_documents

def do_prediction(user_input):
    # Load the model and vectorizer
    model = joblib.load("chatbot_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")

    # Preprocess the user input
    cleaned_input = preprocess_text([user_input])

    # Vectorize the cleaned input
    input_vector = vectorizer.transform(cleaned_input)

    # Make a prediction using the loaded model
    prediction = model.predict(input_vector)

    return prediction[0]