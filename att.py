# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 12:54:37 2020

@author: admin
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 2018

@author: Ashish Kumar
"""

import tkinter as tk
from tkinter import Message, Text
import cv2, os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import telepot
import tkinter.font as font


# from pynput.keyboard import Key, Controller
# from ubidots import ApiClient
# keyboard = Controller()
# api=ApiClient(token='BBFF-6KkdwRkR7Xizc1I8ko59brdVf6llTl')
# var=api.get_variable("629afcff62f7bc013f1197c0")
def clear():
    txt.delete(0, 'end')
    res = ""
    message.configure(text=res)
    clear2()


def clear2():
    txt2.delete(0, 'end')
    res = ""
    message.configure(text=res)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def TakeImages():
    Id = (txt.get())
    name = (txt2.get())
    if (is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + Id + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('frame', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 60:
                break
        cam.release()
        cv2.destroyAllWindows()

    else:
        if (is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text=res)
        if (name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text=res)


def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()  # recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    # cv2.face_LBPHFaceRecognizer.cre
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Id = getImagesAndLabels("TrainingImage")
    print(Id)
    recognizer.train(faces, np.array(Id))
    recognizer.save("Trainner.yml")
    res = "Image Trained"
    message.configure(text=res, justify='left')


def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    ids = []
    for i_path in image_paths:
        pil_image = Image.open(i_path).convert('L')
        image_np = np.array(pil_image, 'uint8')
        id = int(os.path.split(i_path)[-1].split(".")[1])
        faces.append(image_np)
        ids.append(id)
    return faces, ids


def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    count = 0
    # response=var.save_value({"value":0})
    while True:
        ret, im = cam.read()
        print(im)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                print(Id)
                # print("sachin")
                token = '********'  # telegram token
                receiver_id = 1315745356  # https://api.telegram.org/bot<TOKEN>/getUpdates
                bot = telepot.Bot(token)
                bot.sendMessage(receiver_id,
                                'OTP from bank Server OTP=1234')  # send a activation message to telegram receiver id


            else:
                Id = 'Unknown'
                tt = str(Id)
                # cv2.imwrite("unknown.png", im)
                # response=var.save_value({"value":0})
                # sendmail()
                # response
                # keyboard.press('q')

        cv2.imshow('im', im)
        if (cv2.waitKey(1) == ord('q')):
            break

    cam.release()
    cv2.destroyAllWindows()


def sendmail():
    import boto3
    from botocore.exceptions import (NoCredentialsError)

    ACCESS_KEY = '******'
    SECRET_KEY = '*******'

    def upload_to_aws(local_file, bucket, s3_file):
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY)

        try:
            s3.upload_file(local_file, bucket, s3_file)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

    uploaded = upload_to_aws('unknown.png', 'radhakrishna', 'unknown_person.png')


def att():
    global window, message, txt, txt2
    window = tk.Tk()
    # helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
    window.title("IDENTITY AUTHENTICATION MANAGEMENT STUDIO")

    dialog_title = 'QUIT'
    dialog_text = 'Are you sure?'
    # answer = messagebox.askquestion(dialog_title, dialog_text)

    # window.geometry('1280x720')
    window.configure(background='#FFFBF5')

    # window.attributes('-fullscreen', True)

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.geometry('1600x800')

    def click(*args):
        txt.delete(0, 'end')

    def leave(*args):
        txt.delete(0, 'end')

    def caps(event):
        v.set(v.get().upper())

    border_color = tk.Frame(window, background="grey")

    message = tk.Label(window, text="IDENTITY AUTHENTICATION MANAGEMENT STUDIO", bg="#FFFBF5", fg="#39A7FF", width=50,
                       height=2, font=('arial', 30, 'bold'), )

    message.place(x=200, y=20)

    lbl = tk.Label(window, text="USN", width=15, height=1, fg="#87C4FF", bg="#FFFBF5", font=('Calibri', 20))
    lbl.place(x=400, y=200)

    v = tk.StringVar()
    txt = tk.Entry(window, width=20, borderwidth="1.2", bg="#F5F7F8", fg="red", font=('Calibri', 13), textvariable=v,
                   selectforeground="orange")
    txt.place(x=570, y=206)
    txt.bind("<KeyRelease>", caps)
    # txt.insert(0, '4MC20CS074',)
    # txt.bind("<Button-1>", click)  # Clears the placeholder when clicked
    # txt.bind("<Leave>", leave)

    lbl2 = tk.Label(window, text="NAME", width=15, height=1, fg="#87C4FF", bg="#FFFBF5", font=('Calibri', 20))
    lbl2.place(x=392, y=258)

    txt2 = tk.Entry(window, width=20, borderwidth="1.2", bg="#F5F7F8", fg="red", font=('Calibri', 13), )
    txt2.place(x=570, y=265)

    lbl3 = tk.Label(window, text="Log's : ", width=20, fg="#0174BE", bg="#FFFBF5", height=2,
                    font=('Calibri', 18, 'bold'))
    lbl3.place(x=360, y=400)

    message = tk.Label(window, text="", justify="left", bg="#FFFBF5", fg="green", width=20, height=2,
                       activebackground="yellow", font=('roboto', 14))
    message.place(x=540, y=405)

    clearButton = tk.Button(window, text="Clear", command=clear, fg="black", bg="#EEEEEE", width=10, height=1,
                            activebackground="#BDCDD6", font=('roboto', 13), border=2, padx=0, pady=0, cursor="hand2")
    clearButton.place(x=570, y=325)
    # clearButton2 = tk.Button(window, text="Clear", command=clear2, fg="black", bg="#EEEEEE"  ,width=10  ,height=1, activebackground = "#BDCDD6" ,font=('roboto', 14), border=3)
    # clearButton2.place(x=800, y=298)
    takeImg = tk.Button(window, text="Take Images", command=TakeImages, fg="black", bg="#f7b856", width=20, height=2,
                        activebackground="#faab30", font=('roboto', 15, ' bold '), cursor="hand2", border=2, padx=0,
                        pady=0)
    takeImg.place(x=200, y=500)
    trainImg = tk.Button(window, text="Train Images", command=TrainImages, fg="black", bg="#f7b856", width=20, height=2,
                         activebackground="#faab30", font=('roboto', 15, ' bold '), cursor="hand2", border=2, padx=0,
                         pady=0)
    trainImg.place(x=500, y=500)
    trackImg = tk.Button(window, text="Track Images", command=TrackImages, fg="black", bg="#f7b856", width=20, height=2,
                         activebackground="#faab30", font=('roboto', 15, ' bold '), cursor="hand2", border=2, padx=0,
                         pady=0)
    trackImg.place(x=800, y=500)
    quitWindow = tk.Button(window, text="Quit", command=window.destroy, fg="black", bg="#f7b856", width=20, height=2,
                           activebackground="#faab30", font=('roboto', 15, ' bold '), cursor="hand2", border=2, padx=0,
                           pady=0)
    quitWindow.place(x=1100, y=500)

    window.mainloop()


att()
