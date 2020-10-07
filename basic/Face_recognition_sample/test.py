import os
import face_recognition

KNOWN_FACES_DIR = 'known_faces'
UNKNOWN_FACES_DIR = 'unknown_faces'

known_faces = []
known_names= []
for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
        print(f'{KNOWN_FACES_DIR}/{name}/{filename}')
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)
print(known_faces)
print(known_names)

print("My name is Khan and i am not a terrorist but i am counter terrorist in CS:GO")
print("My name is Shyam and i love coding and to typing very much. If not always then atleast now i am loving it.")
 