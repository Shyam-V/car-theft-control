from django.shortcuts import render, redirect
from django.http import HttpResponse
from collections import defaultdict
import os, signal 
import shutil
from subprocess import run,PIPE
import sys
from Face_recognition_sample import sample_video

import subprocess
import face_recognition
import os
import cv2
import telegram
from basic import settings

a=0
data=defaultdict()
data['ritesh']='lalu'
def home(request):
    for key in data.keys():
        if key == '' or data[key]== '':
            del data[key]
    return render(request,'index.html')
def login(request):
    if request.method=="POST":
        if request.POST['Username'] in data and request.POST['Password']==data[request.POST['Username']]:
            return redirect('/mainpage')
        else:
            return redirect('/signup')
    else:
        return redirect('/mainpage')

def signup(request):
    return render(request,'signup.html')
def mainpage(request):
    return render(request, 'mainpage.html')
def register(request):
    if request.method=="POST":
        print(request.POST)
        if request.POST['Password']==request.POST['Confirm_password']:
            data[request.POST['Username']]=request.POST['Password']
            return render(request, 'register.html')
        else:
            return HttpResponse("Password Not Matched")

def dataset(request):
    if request.method == 'POST':
        for afile in request.FILES.getlist('files'):
            handle_uploaded_file(afile, str(afile),str(request.POST['foldername']))
        return HttpResponse("Successful")

    return HttpResponse("Failed")

def handle_uploaded_file(file, filename,foldername):
    if not os.path.exists(os.path.join("app1/dataset/",foldername,"")):
        os.mkdir(os.path.join("app1/dataset/",foldername,""))
        print(os.getcwd())

    with open(os.path.join('app1/dataset/',foldername,"") + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def delete(request):
    foldername=str(request.POST['foldername'])
    if os.path.exists(os.path.join("app1/dataset/", foldername, "")):
        path = os.path.join("app1/dataset/", foldername)
        shutil.rmtree(path)
        return HttpResponse("User Account Deleted")
    else:
        return HttpResponse("No User Found ")
   
def control(request):
    global a
    a = 1 - a
    print(a)
    # print("cp = " + str(settings.child_process))
    if a == 1:
        # if settings.child_process!=0:
        #     settings.child_process.terminate()
        return  HttpResponse("USER MODE SWITCHED")
    else:
        sample_video.face_recog()
        # settings.child_process = subprocess.Popen(sample_video.face_recog())
        # print("cp2 = " + str(settings.child_process))
        # exec(open("Face_recognition_sample/sample_video.py").read())
        # os.system('Face_recognition_sample/sample_video.py')
        #file = os.startfile(r'Face_recognition_sample/sample_video.py')
        return  HttpResponse("THEFT MODE SWITCHED")





