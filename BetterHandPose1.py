from dependencies.BothModule import HandDetector
from dependencies.BothModule import posedetector
import cv2

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

handDetect = HandDetector(detectionCon=0.5, maxHands=1)
poseDetect = posedetector()

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    img = cv2.flip(img,1)
    
    #Hand Detection
    hands, img = handDetect.findHands(img)
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        bbox = hand["bbox"]
        centerPoint = hand['center']
        handType = hand["type"]
        LM = lmList[9]

    #Pose Detection
    img = poseDetect.findPose(img)
    lmListPose, bboxInfo = poseDetect.findPosition(img, bboxWithHands=False)
    if bboxInfo:
        center = bboxInfo["center"]
        cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

        rightShoulder = lmListPose[11][1:3]

        start_point= [rightShoulder[0] - 1000, rightShoulder[1] - 1000]
        end_point = [rightShoulder[0] + 1000, rightShoulder[1] + 1000]
        color = (255, 0, 0)
        thickness = 2

        a = [rightShoulder[0]+1000, rightShoulder[1] - 1000]
        b = [rightShoulder[0]-1000, rightShoulder[1]+1000]

        img = cv2.rectangle(img, start_point, end_point,color,thickness)
        img = cv2.line(img, start_point, end_point, color, thickness)
        img = cv2.line(img, a, b, color, thickness)

        #print(rightShoulder)

    if LM[0] > rightShoulder[0]:
        if LM[0] > rightShoulder[0] and LM[1] < (LM[0]-rightShoulder[0]+rightShoulder[1]) and LM[1] > (-LM[0]+rightShoulder[0]+rightShoulder[1]):
            Position = "Right side"

    if LM[0] < rightShoulder[0]:
        if LM[0] < rightShoulder[0] and LM[1] > (LM[0]-rightShoulder[0]+rightShoulder[1]) and LM[1] < (-LM[0]+rightShoulder[0]+rightShoulder[1]):
            Position = "Left side"

    if LM[1] < rightShoulder[1]:
        if LM[1] < rightShoulder[1] and LM[0] > (LM[1]+rightShoulder[0]-rightShoulder[1]) and LM[0] < (-LM[1]+rightShoulder[0]+rightShoulder[1]):
            Position = "Up side"

    if LM[1] > rightShoulder[1]:
        if LM[1] > rightShoulder[1] and LM[0] < (LM[1]+rightShoulder[0]-rightShoulder[1]) and LM[0] > (-LM[1]+rightShoulder[0]+rightShoulder[1]):
            Postion = "Down side"

    Time = datetime.now().strftime("%Y-%m-%d %H-%M-%S\n")
    with open("patient.csv", 'w')as f:
        data = csv.writer(f)
        header=["Time", "Position"]
        data.writerow([Time, Positon])
            
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release("q")
cv2.destroyAllWindows()