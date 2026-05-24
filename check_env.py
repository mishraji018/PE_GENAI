import sys
import importlib.util
import json

pkgs = ['joblib', 'sklearn', 'nltk', 'streamlit', 'speech_recognition', 'requests', 'pyttsx3', 'numpy', 'pandas', 'tensorflow', 'matplotlib', 'gensim', 'cv2', 'mediapipe', 'yt_dlp']
res = {}
for p in pkgs:
    try:
        res[p] = importlib.util.find_spec(p) is not None
    except:
        res[p] = False
print(json.dumps(res))
