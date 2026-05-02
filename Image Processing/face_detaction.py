import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

face_mesh=mp_face_mesh.FaceMesh(
    static_image_mode=False, #yha static off h means video hi hoga.
    max_num_faces=1, #ek hi face detect karna hai.
    refine_landmarks=True, #yeh true hoga to iris bhi detect hoga.
    min_detection_confidence=0.5, #face detect karne ki confidence 50% se jyada honi chahiye.
    min_tracking_confidence=0.5 #face tracking ki confidence 50% se jyada honi chahiye.
)

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
            mp_drawing.draw_landmarks(
                image=frame, #frame par landmarks draw karna hai.
                landmark_list=face_landmarks, #landmark list dena hai.
                connections=mp_face_mesh.FACEMESH_TESSELATION, #landmark connections dena hai.
                # landmark_drawing_spec=None, #landmark drawing specification dena hai.
                # connection_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0),thickness=1) #connection drawing specification dena hai.
            )

    cv2.imshow("Face Mesh",frame) #frame ko display karna hai.
    key=cv2.waitKey(1)  & 0xFF #1 millisecond ke liye wait karna hai.
    if key==27: #agar ESC key press hoti hai to loop break karna
        break
cap.release() #video capture release karna hai.
cv2.destroyAllWindows() #sabhi windows destroy karna hai.