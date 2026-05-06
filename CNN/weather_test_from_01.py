import cv2
import tensorflow as tf
import numpy as np

model=tf.keras.models.load_model("weather_classification_model.h5")
print("Model loaded successfully")


class_names=['dew', 'fogsmog', 'frost', 'glaze', 'hail', 'lightning', 'rain', 'rainbow', 'rime', 'sandstorm', 'snow']

cap = cv2.VideoCapture(0)

while True:
    flag,frame=cap.read()
    if not flag:
        break
    img=cv2.resize(frame,(128,128)) #128 is cuz images are trained on this size only 
    img_array=np.array(img)  #Convert frame into numpy array
    img_array=img_array/255.0   #Normalization - normalize pixel values(same as training data)
    img_array=np.expand_dims(img_array,axis=0) #Expand dimensions- (1,128,128,3) - 1 is for batch size, 128,128 is for image size and 3 is for color channels (RGB)
    prediction=model.predict(img_array)
    predicted_index=np.argmax(prediction[0]) #Get the index of the highest predicted class
    predicted_label=class_names[predicted_index] #Get the corresponding label from class_names
    confidence_score=np.max(prediction[0]) #Get the confidence score of the predicted class

    cv2.putText(frame,f"{predicted_label}:{confidence_score:.2f}",(20,40),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2) #Display predicted label and confidence score on the frame
    cv2.imshow("Weather Recognition",frame) #Display the frame

    key=cv2.waitKey(1) & 0xFF
    if key==27: #Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()