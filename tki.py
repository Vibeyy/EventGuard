import tkinter as tk
import sqlite3
from tkinter import messagebox
import pickle
import numpy as np
import asyncio
import winsdk.windows.devices.geolocation as wdg
import cv2
import face_recognition
import winsound
import smtplib

conn = sqlite3.connect('faces.db')
c = conn.cursor()

c.execute("SELECT name, username, password ,encoding, rgb FROM KnownFaces3")
global userpass
userpass=[]
known_faces_data = c.fetchall()
conn.close()
for name, username , password, encoding_blob, rgb_blob in known_faces_data:
    encoding = pickle.loads(encoding_blob)
    rgb = pickle.loads(rgb_blob)
    rgb_image = np.array(rgb)
    userpass.append([username,password,name,encoding,rgb_image])
    
async def getCoords():
    locator = wdg.Geolocator()
    pos = await locator.get_geoposition_async()
    return [pos.coordinate.latitude, pos.coordinate.longitude]


def getLoc():
    try:
        return asyncio.run(getCoords())
    except PermissionError:
        messagebox.showerror(title="Error",message="You need to allow applications to access you location in Windows settings")

def triangle_area(a, b, c):
    result = (c[1] * b[0] - b[1] * c[0]) - (c[1] * a[0] - a[1] * c[0]) + (b[1] * a[0] - a[1] * b[0])
    return result
def is_inside_square(a, b, c, d, p):
    if triangle_area(a, b, p) > 0 or triangle_area(b, c, p) > 0 or triangle_area(c, d, p) > 0 or triangle_area(d, a, p) > 0:
        return False
    else:
        return True


def clip():
    a=(12.846992,80.146598)
    b=(12.834356,80.146770)
    c=(12.834356,80.161886)
    d=(12.850339,80.163518)
    p=getLoc()
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True
    while True:
        ret, frame = video_capture.read()

        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            rgb_small_frame = small_frame[:, :, ::-1]
            
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces([encoding1], face_encoding)
                video_capture.release()
                cv2.destroyAllWindows()
        if matches[0]==True and is_inside_square(a,b,c,d,p):
            frequency = 440  
            duration = 1000  
            winsound.Beep(frequency, duration)
            content = name1+" "+user+" has attended the event."
            mail = smtplib.SMTP('smtp.gmail.com',587)
            mail.ehlo()
            mail.starttls()
            mail.login('#username','#password')#change the username pasword into your mail's username and password
            mail.sendmail('#username','#receivers username',content)#similarly change here
            mail.close
        elif matches[0]==True and not is_inside_square(a,b,c,d,p):
            frequency = 220
            duration = 1000  
            winsound.Beep(frequency, duration)
            winsound.Beep(frequency, duration)
            winsound.Beep(frequency, duration)
            messagebox.showerror(title="Sorry",message="You are not inside the campus, please try again after entering the campus")
            window.destroy
        else:
            frequency = 220
            duration = 1000  
            winsound.Beep(frequency, duration)
            winsound.Beep(frequency, duration)
            winsound.Beep(frequency, duration)
            messagebox.showerror(title="Sorry",message="You're face is not recognised, Please try again.")
                

       
def login():
    token = 0
    username = username_entry.get()
    password = password_entry.get()
    for i in range(0,len(userpass)):
        if username == userpass[i][0] and password == userpass[i][1]:
            token = 1
            global name1,user,encoding1,rgb1
            name1 = userpass[i][2]
            user = userpass[i][0]
            encoding1 = userpass[i][3]
            rgb1 = userpass[i][4]
            messagebox.showinfo(title="Successfull Login",message="Welcome student")
            root.destroy()
            global window
            window = tk.Tk()
            window.configure(bg="#343a40")
            window.geometry("1100x600")
            window.title("Attendance")
            title = tk.Label(window,text='Hello '+name1+"!!!",font=("Georgia",18),bg="#343a40",fg="#FFFFFF")
            title.pack(padx=20,pady=20)
            label = tk.Label(window,text="Please Click On The Button And Stand In A Well Lit BackGround To Recognize Your Face",font=("Georgia",16),bg="#343a40",fg="#FFFFFF")
            label.pack(padx=20,pady=20)
            label1 = tk.Label(window,text="It Will Take A Moment Once You Click The Button, So please Be Patient.",font=("Georgia",16),bg="#343a40",fg="#FFFFFF")
            label1.pack(padx=20,pady=20)
            Pic_btn1 = tk.Button(window,text="Start Clipping",font=("Georgia",16),bg="#343a40",fg="#FFFFFF",command = clip)
            Pic_btn1.pack(padx=20,pady=20)
            window.mainloop()
    if token == 0:
        messagebox.showerror(title="Invalid Login",message="Bad Credentials")

def shortcut(event):
    if event.keysym == "Return":
        login()


root = tk.Tk()   
root.configure(bg="#343a40")
frame = tk.Frame(bg="#343a40")
root.geometry("500x300")
root.title("Event Attendance")

title = tk.Label(frame,text='Login',font=("Georgia",18),bg="#343a40",fg="#FFFFFF")
title.grid(row=0,column = 0,padx=20,pady=20,columnspan=2)

username_label = tk.Label(frame,text='Username',font=("Georgia",16),bg="#343a40",fg="#FFFFFF")
username_label.grid(row=1,column=0,padx=10,pady=10)

username_entry = tk.Entry(frame)
username_entry.grid(row=1,column=1,padx=10,pady=10)


password_label = tk.Label(frame,text='Password',font=("Georgia",16),bg="#343a40",fg="#FFFFFF")
password_label.grid(row=2,column=0,padx=10,pady=10)

password_entry = tk.Entry(frame,show = "*")
password_entry.bind("<KeyPress>",shortcut)
password_entry.grid(row=2,column=1,padx=10,pady=10)

login_btn = tk.Button(frame,text="Login",font=("Georgia",16),bg="#343a40",fg="#FFFFFF",command = login)
login_btn.grid(row=3,column=1,padx=20,pady=20)
frame.pack()
root.mainloop()



