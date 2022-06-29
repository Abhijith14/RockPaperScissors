import random
import time
import cv2
import mediapipe as mp
from rpsalgo import set_color, fingersUp, findSymbol, aiAlgo


cap = cv2.VideoCapture(0)

cap.set(3, 1080)
cap.set(4, 720)

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
startGame = False
stateResult = False
curr_ai_img = False
Pscore, Ascore = 0, 0


def evaluate(AI, Player):
    global Pscore, Ascore

    if Player >= 0:
        if AI == 0 and Player == 1 or AI == 1 and Player == 2 or AI == 2 and Player == 0:
            Pscore = Pscore + 1
        elif AI == 0 and Player == 2 or AI == 1 and Player == 0 or AI == 2 and Player == 1:
            Ascore = Ascore + 1


def main():
    global mp_drawing, mp_holistic, startGame, stateResult, curr_ai_img, Pscore, Ascore
    with mp_holistic.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.7) as holistic:
        while cap.isOpened():
            bg_main = cv2.imread('assets/BG.png')  # 515 x 515
            success, img = cap.read()

            img = cv2.flip(img, 1)

            imgScaled = cv2.resize(img, (0, 0), None, 0.7222, 0.7222)
            imgScaled = imgScaled[:, 3:515]

            imgScaled = cv2.cvtColor(imgScaled, cv2.COLOR_BGR2RGB)
            results = holistic.process(imgScaled)
            imgScaled = cv2.cvtColor(imgScaled, cv2.COLOR_RGB2BGR)

            mp_drawing.draw_landmarks(imgScaled, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                      set_color((121, 22, 76), 2, 4),
                                      set_color((121, 44, 250), 2, 2))
            mp_drawing.draw_landmarks(imgScaled, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                      set_color((121, 22, 76), 2, 4),
                                      set_color((121, 44, 250), 2, 2))

            bg_main[227:747, 1168:1680] = imgScaled

            raised_fingers = 0

            if startGame:
                AI_image, AI_val = aiAlgo()

                cv2.putText(bg_main, '(' + str(Ascore) + ')', (530, 800), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 4)
                cv2.putText(bg_main, '(' + str(Pscore) + ')', (1530, 800), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 4)
                time1 = cv2.imread('assets/time1.png')  # 300 x 200
                time2 = cv2.imread('assets/time2.png')
                time3 = cv2.imread('assets/time3.png')
                time0 = cv2.imread('assets/time0.png')

                if stateResult is False:
                    timer = int(time.time() - initialTime)
                    if timer == 0:
                        bg_main[850:1050, 800:1100] = time3
                    elif timer == 1:
                        bg_main[850:1050, 800:1100] = time2
                    elif timer == 2:
                        bg_main[850:1050, 800:1100] = time1
                    elif timer == 3:
                        bg_main[850:1050, 800:1100] = time0
                        stateResult = True
                    #else:
                    #    stateResult = True
                    if type(curr_ai_img) is not bool:
                        bg_main[230:750, 240:760] = curr_ai_img

                if stateResult:
                    # if both hands detected or no hands detected
                    if results.left_hand_landmarks and results.right_hand_landmarks:
                        raised_fingers = 0
                        print("BOTH RAISED !!")
                        pass

                    # right hand
                    elif results.left_hand_landmarks:
                        raised_fingers = fingersUp(results.left_hand_landmarks.landmark, 1)

                    # left hand
                    elif results.right_hand_landmarks:
                        raised_fingers = fingersUp(results.right_hand_landmarks.landmark, 0)

                    else:
                        print("TRY AGAIN")

                    print(raised_fingers)

                    curr_ai_img = AI_image
                    curr_ai_val = AI_val

                    bg_main[230:750, 240:760] = curr_ai_img

                    evaluate(curr_ai_val, findSymbol(raised_fingers))

                    # Reset the game
                    stateResult = False
                    initialTime = time.time()

            cv2.imshow("RPS Game", bg_main)

            key = cv2.waitKey(1)
            if key == ord('s'):
                startGame = True
                initialTime = time.time()
                Pscore, Ascore = 0, 0


main()
