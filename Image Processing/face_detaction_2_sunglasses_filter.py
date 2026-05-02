# 1.transparent sunglasses chahiye hota h
# 2.usko transparent rkhne k liye IMREAD_UNCHANGED flag use krna hota h.
# 3.agar image transparent nhi h to usme alpha channel nhi hoga, aur agar image transparent h to usme alpha channel hoga.
# 4.alpha channel me transparency ki information hoti h, jisme 0 ka matlab h fully transparent, aur 255 ka matlab h fully opaque.

import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

face_mesh=mp_face_mesh.FaceMesh(
    static_image_mode=False, #yha static off h means video hi hoga.
    # max_num_faces=1, #ek hi face detect karna hai.
    refine_landmarks=True, #yeh true hoga to iris bhi detect hoga.
    # min_detection_confidence=0.5, #face detect karne ki confidence 50% se jyada honi chahiye.
    # min_tracking_confidence=0.5 #face tracking ki confidence 50% se jyada honi chahiye.
)

#Load image with transparency
sunglasses=cv2.imread("sunglasses.png",cv2.IMREAD_UNCHANGED) #sunglasses image ko transparent rkhne ke liye IMREAD_UNCHANGED flag use krna hota h.

cap=cv2.VideoCapture(0) #0 means webcam se video capture karna hai.
while True:
    flag,frame=cap.read() #video se frame read karna hai.
    if not flag:
        break
    rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) #frame ko RGB me convert karna hai.
    #Dectect face landmarks
    results=face_mesh.process(rgb_frame) #face landmarks detect karna hai.
    #Draw landmarks
    if results.multi_face_landmarks: #agar face landmarks detect hote hain to unhe draw karna hai.
        for face_landmarks in results.multi_face_landmarks:

            h,w,_=frame.shape #frame ki height, width aur channels nikalna hai.
            left_eye=face_landmarks.landmark[33] #face landmarks ke points nikalna hai. total 468 points hote hain, yaha 33rd point nikalna hai.
            right_eye=face_landmarks.landmark[263] #face landmarks ke points nikalna hai. total 468 points hote hain, yaha 263rd point nikalna hai.

            x1,y1=int(left_eye.x*w), int(left_eye.y*h) #x1,y1 coordinate nikalna hai.
            x2,y2=int(right_eye.x*w), int(right_eye.y*h) #x2,y2 coordinate nikalna hai.

            #Distance between two eyes
            glasses_width=int(np.hypot(x2-x1, y2-y1)) +100 #sunglasses ki width nikalna hai. +80 isliye kiya hai kyunki sunglasses ko thoda bada rkhna hai, taki wo dono aankhon ko cover kar sake. np.hypot function ka matlab h x2-x1 aur y2-y1 ke distance ko calculate karna hai, jisme x2-x1 ka matlab h dono aankhon ke beech ka horizontal distance, aur y2-y1 ka matlab h dono aankhon ke beech ka vertical distance. np.hypot function ka output h dono aankhon ke beech ka straight line distance, jisme Pythagorean theorem apply hota h, jisme distance = sqrt((x2-x1)^2 + (y2-y1)^2) hota h.
            glasses_height=int(glasses_width*0.4) #sunglasses ki height nikalna hai.
            
            


            resized_glasses=cv2.resize(sunglasses, (glasses_width, glasses_height)) #sunglasses ko resize karna hai.

            #Position of sunglasses CENTRE POINT SHOULD BE BETWEEN TWO EYES
            x_center=int((x1+x2)/2)
            y_center=int((y1+y2)/2)

            x_offset=int(x_center-glasses_width/2) #sunglasses ko frame par place karne ke liye x offset nikalna hai.
            y_offset=int(y_center-glasses_height/2) #sunglasses ko frame par place karne ke liye y offset nikalna hai.

            #split channels 
            overlay_img=resized_glasses[:,:,:3] #sunglasses ke RGB channels nikalna hai. [:,:,:3] ka matlab h all rows, all columns, aur first 3 channels (RGB) nikalna hai.
            mask=resized_glasses[:,:,3] #sunglasses ke alpha channel nikalna hai. [:,:,3] ka matlab h all rows, all columns, aur 4th channel (alpha) nikalna hai.
            #inverse mask
            mask_inv=cv2.bitwise_not(mask) #mask ka inverse nikalna hai. bitwise_not function ka matlab h mask ke pixels ko invert karna hai, jisme 0 ka matlab h 255, aur 255 ka matlab h 0.
            #ROI(Region of Interest) on frame
            roi=frame[y_offset:y_offset+glasses_height, x_offset:x_offset+glasses_width] #frame par sunglasses ko place karne ke liye ROI nikalna hai. y_offset se start hoga, aur y_offset+glasses_height tak jayega, aur x_offset se start hoga, aur x_offset+glasses_width tak jayega.

            background=cv2.bitwise_and(roi, roi, mask=mask_inv) #ROI se background nikalna hai. bitwise_and function ka matlab h ROI ke pixels ko mask_inv ke pixels ke saath AND operation karna hai, jisme mask_inv me 0 hoga to ROI ka pixel bhi 0 hoga, aur mask_inv me 255 hoga to ROI ka pixel bhi 255 hoga.
            foreground=cv2.bitwise_and(overlay_img, overlay_img, mask=mask) #sunglasses ke foreground nikalna hai. bitwise_and function ka matlab h overlay_img ke pixels ko mask ke pixels ke saath AND operation karna hai, jisme mask me 0 hoga to overlay_img ka pixel bhi 0 hoga, aur mask me 255 hoga to overlay_img ka pixel bhi 255 hoga.

            combined=cv2.add(background, foreground) #background aur foreground ko combine karna hai. add function ka matlab h background ke pixels aur foreground ke pixels ko add karna hai, jisme 0+0=0, 0+255=255, aur 255+255=255 hoga.
            frame[y_offset:y_offset+glasses_height, x_offset:x_offset+glasses_width]=combined #frame par combined image ko place karna hai. y_offset se start hoga, aur y_offset+glasses_height tak jayega, aur x_offset se start hoga, aur x_offset+glasses_width tak jayega.



            # mp_drawing.draw_landmarks(
            #     image=frame, #frame par landmarks draw karna hai.
            #     landmark_list=face_landmarks, #landmark list dena hai.
            #     connections=mp_face_mesh.FACEMESH_TESSELATION, #landmark connections dena hai.
            #     # landmark_drawing_spec=None, #landmark drawing specification dena hai.
            #     # connection_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0),thickness=1) #connection drawing specification dena hai.
            # )

    cv2.imshow("Face Mesh",frame) #frame ko display karna hai.
    key=cv2.waitKey(1)  & 0xFF #1 millisecond ke liye wait karna hai.
    if key==27: #agar ESC key press hoti hai to loop break karna
        break
cap.release() #video capture release karna hai.
cv2.destroyAllWindows() #sabhi windows destroy karna hai.