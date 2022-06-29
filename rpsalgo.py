import mediapipe as mp
import cv2
import random

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
tipIds = [4, 8, 12, 16, 20]


def set_color(color, t, r): # color - BGR, thickness, circle_radius
    return mp_drawing.DrawingSpec(color=color, thickness=t, circle_radius=r)


def fingersUp(lmList, hand):
    fingers = []

    if hand == 0:  # left hand
        fingers.append(0)  # denoting left hand
        # Thumb
        if lmList[tipIds[0]].x > lmList[tipIds[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)
    elif hand == 1:  # right hand
        fingers.append(1)  # denoting right hand
        # Thumb
        if lmList[tipIds[0]].x > lmList[tipIds[0] - 1].x:
            fingers.append(0)
        else:
            fingers.append(1)

    # 4 Fingers
    for id in range(1, 5):
        if lmList[tipIds[id]].y < lmList[tipIds[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


def findSymbol(fingers):
    if fingers != 0:
        fingers = fingers[1:]

        # rock
        if fingers == [0, 0, 0, 0, 0]:
            return 0
        # paper
        elif fingers == [1, 1, 1, 1, 1]:
            return 1
        # scissors
        elif fingers == [0, 1, 1, 0, 0]:
            return 2

        else:
            return -1

    return -1


def aiAlgo():
    rockImg = cv2.imread('assets/rock.png')
    paperImg = cv2.imread('assets/paper.png')
    scissorsImg = cv2.imread('assets/scissors.png')

    roles = ['rock', 'paper', 'scissors']

    role_image = random.choice(roles)
    role_val = roles.index(role_image)

    if role_image == 'rock':
        role_image = rockImg
    elif role_image == 'paper':
        role_image = paperImg
    elif role_image == 'scissors':
        role_image = scissorsImg

    return role_image, role_val
