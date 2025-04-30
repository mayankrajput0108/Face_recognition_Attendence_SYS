import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2
import os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import threading
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'piyushooo28@gmail.com' ")

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp = (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#3ece48", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

def update_registration_count():
    res = 0
    exists = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists:
        with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            lines = list(reader1)
            logging.debug(f"CSV contents: {lines}")
            res = len(lines) - 1  # Subtract 1 for header row
    logging.debug(f"Calculated registrations: {res}")
    message.config(text=f'Total Registrations till now: {res}')

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    
    # Get next serial number
    serial = 1  # Start at 1 if no file exists
    exists = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists:
        with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            lines = list(reader1)
            if len(lines) > 1:  # More than just header
                serial = len(lines)  # Next serial = total rows (header + registrations)
        csvFile1.close()
    else:
        with open("StudentDetails/StudentDetails.csv", 'a+', newline='') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
        csvFile1.close()

    Id = txt.get()
    name = txt2.get()
    if not ((name.isalpha()) or (' ' in name)):
        res = "Enter Correct name"
        message.configure(text=res)
        return

    # Flag to stop the thread
    stop_event = threading.Event()

    def capture_thread():
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            logging.error("Camera could not be opened")
            mess._show(title="Camera Error", message="Unable to access camera!")
            return
        
        harcascadePath = "haarcascade_frontalface_default.xml"
        if not os.path.isfile(harcascadePath):
            logging.error("Haar Cascade file not found")
            mess._show(title="File Error", message="Haar Cascade file missing!")
            return
        detector = cv2.CascadeClassifier(harcascadePath)
        if detector.empty():
            logging.error("Failed to load Haar Cascade classifier")
            mess._show(title="Classifier Error", message="Failed to load face detector!")
            return
        
        sampleNum = 0
        jpeg_quality = 85
        
        try:
            logging.info(f"Starting image capture for serial {serial}")
            while not stop_event.is_set():
                ret, img = cam.read()
                if not ret or img is None:
                    logging.error("Failed to read frame from camera")
                    mess._show(title="Camera Error", message="No frame captured from camera!")
                    break
                
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                
                if len(faces) == 0:
                    logging.debug("No faces detected in this frame")
                else:
                    logging.debug(f"Detected {len(faces)} face(s)")
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum += 1
                    file_path = os.path.join("TrainingImage", f"{name}.{serial}.{Id}.{sampleNum}.jpg")
                    logging.debug(f"Saving image: {file_path} with quality {jpeg_quality}")
                    success = cv2.imwrite(file_path, gray[y:y + h, x:x + w], [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
                    if not success:
                        logging.error(f"Failed to save image: {file_path}")
                
                cv2.imshow('Taking Images', img)
                if cv2.waitKey(100) & 0xFF == ord('q') or sampleNum >= 100:  # 'q' retained for TakeImages
                    break
        
        except Exception as e:
            logging.error(f"Error in capture thread: {e}")
            mess._show(title="Capture Error", message=f"An error occurred: {str(e)}")
        
        finally:
            logging.info("Cleaning up resources")
            cam.release()
            cv2.destroyAllWindows()
            if sampleNum > 0:
                res = f"Images Taken for ID: {Id} ({sampleNum} images)"
                message1.configure(text=res)
                row = [serial, '', Id, '', name]
                with open('StudentDetails/StudentDetails.csv', 'a+', newline='') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                csvFile.close()
                logging.debug(f"Added row to CSV: {row}")
                update_registration_count()
            else:
                message1.configure(text="No images captured - check logs")

    capture_thread_instance = threading.Thread(target=capture_thread, daemon=True)
    capture_thread_instance.start()

    def stop_capture():
        stop_event.set()
        capture_thread_instance.join(timeout=2)
    
    stop_button = ttk.Button(right_frame, text="Stop Capture", command=stop_capture)
    stop_button.place(x=250, y=200)

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

def update_treeview(date):
    """Helper function to update Treeview with attendance data from CSV"""
    for k in tv.get_children():
        tv.delete(k)
    with open(f"Attendance/Attendance_{date}.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        i = 0
        for lines in reader1:
            i += 1
            if i > 1 and i % 2 != 0:  # Skip header and handle data rows
                iidd = str(lines[0]) + '   '
                tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    
    # Flag to stop the thread
    stop_event = threading.Event()
    attendance = None  # To store attendance data
    
    def attendance_thread():
        nonlocal attendance
        recognizer = cv2.face.LBPHFaceRecognizer.create()
        exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
        if exists3:
            recognizer.read("TrainingImageLabel\Trainner.yml")
        else:
            mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
            return
        
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            logging.error("Camera could not be opened")
            mess._show(title="Camera Error", message="Unable to access camera!")
            return
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
        exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
        if exists1:
            df = pd.read_csv("StudentDetails\StudentDetails.csv")
        else:
            mess._show(title='Details Missing', message='Students details are missing, please check!')
            cam.release()
            cv2.destroyAllWindows()
            return
        
        try:
            logging.info("Starting attendance capture")
            while not stop_event.is_set():
                ret, im = cam.read()
                if not ret or im is None:
                    logging.error("Failed to read frame from camera")
                    mess._show(title="Camera Error", message="No frame captured from camera!")
                    break
                
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, 1.2, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
                    serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
                    if (conf < 50):
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                        ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                        ID = str(ID)
                        ID = ID[1:-1]
                        bb = str(aa)
                        bb = bb[2:-2]
                        attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]
                    else:
                        Id = 'Unknown'
                        bb = str(Id)
                    cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
                cv2.imshow('Taking Attendance', im)
                cv2.waitKey(1)  # No 'q' check here
        
        except Exception as e:
            logging.error(f"Error in attendance thread: {e}")
            mess._show(title="Attendance Error", message=f"An error occurred: {str(e)}")
        
        finally:
            logging.info("Cleaning up attendance resources")
            cam.release()
            cv2.destroyAllWindows()

    def stop_attendance():
        stop_event.set()
        attendance_thread_instance.join(timeout=2)
        # After thread stops, log attendance and update GUI
        if attendance:
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
            exists = os.path.isfile(f"Attendance/Attendance_{date}.csv")
            if exists:
                with open(f"Attendance/Attendance_{date}.csv", 'a+', newline='') as csvFile1:
                    writer = csv.writer(csvFile1)
                    writer.writerow(attendance)
            else:
                with open(f"Attendance/Attendance_{date}.csv", 'a+', newline='') as csvFile1:
                    writer = csv.writer(csvFile1)
                    writer.writerow(['Id', '', 'Name', '', 'Date', '', 'Time'])  # Header
                    writer.writerow(attendance)
            update_treeview(date)  # Update GUI after stopping
        else:
            logging.debug("No attendance recorded")

    attendance_thread_instance = threading.Thread(target=attendance_thread, daemon=True)
    attendance_thread_instance.start()

    stop_attendance_button = ttk.Button(left_frame, text="Stop Attendance", command=stop_attendance)
    stop_attendance_button.place(x=250, y=60)

######################################## USED STUFFS ############################################

global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = {'01':'January', '02':'February', '03':'March', '04':'April', '05':'May', '06':'June',
        '07':'July', '08':'August', '09':'September', '10':'October', '11':'November', '12':'December'}

######################################## GUI SETUP ############################################

window = tk.Tk()
window.geometry("1280x720")
window.resizable(False, False)
window.title("Attendance System")
window.configure(bg="#2c2f33")

header = ttk.Label(window, text="Face Recognition Attendance System", font=('Helvetica', 24, 'bold'), foreground="white", background="#23272a")
header.pack(pady=10)

left_frame = ttk.Frame(window, style="Card.TFrame")
left_frame.place(relx=0.05, rely=0.15, relwidth=0.45, relheight=0.75)

right_frame = ttk.Frame(window, style="Card.TFrame")
right_frame.place(relx=0.52, rely=0.15, relwidth=0.43, relheight=0.75)

date_label = ttk.Label(window, text=f"{day}-{mont[month]}-{year}", font=('Helvetica', 14), foreground="white", background="#2c2f33")
date_label.place(relx=0.05, rely=0.05)

clock = ttk.Label(window, font=('Helvetica', 14), foreground="white", background="#2c2f33")
clock.place(relx=0.85, rely=0.05)
tick()

ttk.Label(left_frame, text="Attendance", font=('Helvetica', 16, 'bold')).place(x=20, y=20)
trackImg = ttk.Button(left_frame, text="Capture Attendance", command=TrackImages, width=20)
trackImg.place(x=20, y=60)

tv = ttk.Treeview(left_frame, columns=('name', 'date', 'time'), height=15)
tv.column('#0', width=80)
tv.column('name', width=150)
tv.column('date', width=150)
tv.column('time', width=150)
tv.heading('#0', text='ID')
tv.heading('name', text='NAME')
tv.heading('date', text='DATE')
tv.heading('time', text='TIME')
tv.place(x=20, y=100)

scroll = ttk.Scrollbar(left_frame, orient='vertical', command=tv.yview)
scroll.place(x=550, y=100, height=325)
tv.configure(yscrollcommand=scroll.set)

quitWindow = ttk.Button(left_frame, text="Quit", command=window.destroy, width=20)
quitWindow.place(x=20, y=450)

ttk.Label(right_frame, text="New Registration", font=('Helvetica', 16, 'bold')).place(x=20, y=20)

ttk.Label(right_frame, text="Enter ID").place(x=20, y=60)
txt = ttk.Entry(right_frame, width=25)
txt.place(x=120, y=60)
clearButton = ttk.Button(right_frame, text="Clear", command=clear, width=10)
clearButton.place(x=350, y=60)

ttk.Label(right_frame, text="Enter Name").place(x=20, y=100)
txt2 = ttk.Entry(right_frame, width=25)
txt2.place(x=120, y=100)
clearButton2 = ttk.Button(right_frame, text="Clear", command=clear2, width=10)
clearButton2.place(x=350, y=100)

message1 = ttk.Label(right_frame, text="1) Take Images  >>>  2) Save Profile", font=('Helvetica', 12))
message1.place(x=20, y=150)

takeImg = ttk.Button(right_frame, text="Take Images", command=TakeImages, width=20)
takeImg.place(x=20, y=200)
trainImg = ttk.Button(right_frame, text="Save Profile", command=psw, width=20)
trainImg.place(x=20, y=250)

message = ttk.Label(right_frame, text="Total Registrations till now: 0", font=('Helvetica', 12))
message.place(x=20, y=300)
update_registration_count()  # Set initial count

menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Change Password', command=change_pass)
filemenu.add_command(label='Contact Us', command=contact)
filemenu.add_command(label='Exit', command=window.destroy)
menubar.add_cascade(label='Help', menu=filemenu)
window.config(menu=menubar)

style = ttk.Style()
style.theme_use('clam')
style.configure("Card.TFrame", background="#ffffff", relief="flat")
style.configure("TButton", font=('Helvetica', 10), padding=5)
style.configure("TLabel", background="#ffffff", font=('Helvetica', 10))

window.mainloop()