from django.shortcuts import render, redirect
from django.http import HttpResponse
from collections import defaultdict
import os, signal 
import shutil
from subprocess import run,PIPE
import sys

import face_recognition
import os
import cv2
import telegram

def termination():
        sys.exit()

def face_recog():   

    KNOWN_FACES_DIR = 'Face_recognition_sample/known_faces'
    # UNKNOWN_FACES_DIR = 'unknown_faces'
    TOLERANCE = 0.5
    FRAME_THICKNESS = 2
    FONT_THICKNESS = 1
    MODEL = 'cnn'

    token = "1171072467:AAHqz6QI90f1KjLRybL8uwYRZblIzAYSSnQ"
    bot = telegram.Bot(token)
    print(bot.get_me())
    chat_id = "573611170"

    video = cv2.VideoCapture('http://192.168.0.100:8080/video')
    video.set(3, 256)
    video.set(4, 144) 
    scale_percent = 200

    c = 0

    def name_to_color(name):
        # Take 3 first letters, tolower()
        # lowercased character ord() value rage is 97 to 122, substract 97, multiply by 8
        color = [(ord(c.lower())-97)*8 for c in name[:3]]
        return color


    print("Loading knowns faces.....")
    known_faces = []
    known_names= []
    for name in os.listdir(KNOWN_FACES_DIR):
        for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
            image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
            encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(encoding)
            known_names.append(name)

    count = 0

    print("Processing unknown faces...")
    while True:
        # print(f'Filename {filename}', end=" ")
        # image = face_recognition.load_image_file(f'{UNKNOWN_FACES_DIR}/{filename}')
        ret, image = video.read()
        width = int(image.shape[1]*scale_percent/100)
        height = int(image.shape[0]*scale_percent/100)
        dsize = (width, height)
        locations = face_recognition.face_locations(image, model=MODEL)
        encodings = face_recognition.face_encodings(image, locations)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        print(type(encodings))
        if(encodings==[]):
            print("No faces detected")
            message = "No faces detected"
            cv2.putText(image, message, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (200,200,200), FONT_THICKNESS)
            image = cv2.resize(image, dsize)
            cv2.imshow(filename, image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            continue
        else:
            print(f', found {len(encodings)} face(s)')
            for face_encoding, face_location in zip(encodings,  locations):
                results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
                
                match = None
                if True in results:
                    match = known_names[results.index(True)]
                    print(f' - {match} from {results}')

                    top_left = (face_location[3], face_location[0])
                    bottom_right = (face_location[1], face_location[2])

                    color = name_to_color(match)
                    cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

                    top_left = (face_location[3], face_location[2])
                    bottom_right = (face_location[1], face_location[2] + 22)

                    cv2.rectangle(image, top_left,bottom_right, color, cv2.FILLED)
                    cv2.putText(image, match, (face_location[3] + 5, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (200,200,200), FONT_THICKNESS)

                else:
                    count += 1 
                    
                    print("The person is outsides/intruder/potential threat")
                    match = "Intruder"
                    top_left = (face_location[3], face_location[0])
                    bottom_right = (face_location[1], face_location[2])

                    color = name_to_color(match)
                    cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

                    top_left = (face_location[3], face_location[2])
                    bottom_right = (face_location[1], face_location[2] + 22)

                    cv2.rectangle(image, top_left,bottom_right, color, cv2.FILLED)
                    cv2.putText(image, match, (face_location[3] + 5, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (200,200,200), FONT_THICKNESS)
                    
                    if(count==5):
                        count = 0
                        c += 1
                        cv2.imwrite('Face_recognition_sample/intruders'+'/intruder_'+str(c)+'.jpg', image)
                        photo = 'Face_recognition_sample/intruders'+'/intruder_'+str(c)+'.jpg'
                        bot.send_photo(chat_id, photo=open(photo, 'rb'))
                        text = "An intruder is trying to intrude."
                        bot.send_message(chat_id, text)

        image = cv2.resize(image, dsize)
        cv2.imshow(filename, image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        # cv2.waitKey(0)
        # cv2.destroyWindow(filename)        
