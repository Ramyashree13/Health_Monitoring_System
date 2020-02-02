from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
from PIL import ImageTk,Image
import webbrowser
import sqlite3
import smtplib

conn=sqlite3.connect('HMS.db')
print("opened")

main_screen=Tk()
main_screen.geometry("800x600")
main_screen.title("Health Monitoring System")

def doc_validate():
    global d_username1
    d_username1 = username_verify.get()
    password1 = password_verify.get()
    entry.delete(0, END)
    entry1.delete(0, END)
    flag=0
    query='''SELECT * FROM LOGIN '''
    rows=conn.execute(query)
    for row in rows:
        if(row[0]==d_username1 and row[1]==password1):
            l1=list(row[0])
            if(l1[0]=='d'):
                flag=1
    if(flag==1):
        doctor_homepage()
    else:
        messagebox.showerror("ERROR","Invalid Username or Password")
        
        

        
def pat_validate():
    global p_username1
    p_username1 = username_verify.get()
    password1 = password_verify.get()
    entry.delete(0, END)
    entry1.delete(0, END)
    flag=0
    query='''SELECT * FROM LOGIN '''
    rows=conn.execute(query)
    for row in rows:
        if(row[0]==p_username1 and row[1]==password1):
            l1=list(row[0])
            if(l1[0]=='p'):
                flag=1
    if(flag==1):
        patient_homepage()
    else:
        messagebox.showerror("ERROR","Invalid Username or Password")
        


def patient_detail_validate():
    global pd_username1
    pd_username1=username_verify.get()
    entry.delete(0,END)
    flag=0
    query='''SELECT * FROM PATIENT'''
    rows=conn.execute(query)
    for row in rows:
        if(row[0]==pd_username1):
            flag=1
    if(flag==1):
        patient_detail()
    else:
        doctor_homepage()
        main_screen.withdraw()
        messagebox.showinfo("ERROR","P_ID invalid")
       


def add_prescription():
    t_name=tablet_name.get()
    t_mg=tablet_mg.get()
    t_t=tablet_timings.get()
    entry.delete(0,END)
    entry1.delete(0,END)
    entry2.delete(0,END)
    query="UPDATE PRESCRIPTION SET tname='%s',tmg='%s',timing='%s' WHERE pid='%s'"%(t_name,t_mg,t_t,pd_username1)
    conn.execute(query)
    conn.commit()
    email="nrsy.hms@gmail.com"
    to="namrathav99@gmail.com"
    pswd="Nrsy1234"
    subject="New prescription added"
    message="The doctor has updated %s's medicine.\n\nTablet Name : %s\nTablet Mg : %s\nTimings : %s.\n\nPlease check."%(pd_username1,t_name,t_mg,t_t)
    try:
        with smtplib.SMTP('smtp.gmail.com:587') as server:
            server.ehlo()
            server.starttls()
            server.login(email,pswd)
            message='Subject : {}\n\n{}'.format(subject,message)
            server.sendmail(email,to,message)
            print("email sent")
    except Exception as e:
        print("Email failed e")
    messagebox.showinfo("Updated","Inserted the record successfully.")
    prescription()

    
def view_prescription():   
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Health Monitoring System")
    login_screen.geometry("800x600")

    c=Canvas(login_screen,width=800,height=600)
    c.pack()
    image=PhotoImage(file="C:\\Users\\lenovo\\Documents\\PROJECTS\\PYTHON\\globe.png")
    c.create_image(400,300,anchor="center",image=image)
    background_label = Label(login_screen, image=image)
    background_label.image = image

    query="SELECT tname,tmg,timing FROM PRESCRIPTION WHERE pid='%s'"%(p_username1)
    rows=conn.execute(query)
    for row in rows:
        t_name=row[0]
        t_mg=row[1]
        t_t=row[2]

    label4=Label(login_screen, text=t_name,anchor=CENTER,justify=CENTER,font=('Times New Roman',14,'bold'),state=NORMAL,bg='white',relief=FLAT)
    label4.configure(width=25,height=2)
    label4=c.create_window(650,250,anchor=SE,window=label4)

    label5=Label(login_screen, text=t_mg,anchor=CENTER,justify=CENTER,font=('Times New Roman',14,'bold'),state=NORMAL,bg='white',relief=FLAT)
    label5.configure(width=25,height=2)
    label5=c.create_window(650,350,anchor=SE,window=label5)

    label6=Label(login_screen, text=t_t,anchor=CENTER,justify=CENTER,font=('Times New Roman',14,'bold'),state=NORMAL,bg='white',relief=FLAT)
    label6.configure(width=25,height=2)
    label6=c.create_window(650,450,anchor=SE,window=label6)

    label=Label(login_screen, text="PRESCRIPTION",anchor=CENTER,justify=CENTER,font=('Times New Roman',18,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label.configure(width=25,height=2)
    label=c.create_window(570,130,anchor=SE,window=label)

    label=Label(login_screen, text="Medicine Name",anchor=CENTER,justify=CENTER,font=('Times New Roman',14,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label.configure(width=15,height=2)
    label=c.create_window(320,250,anchor=SE,window=label)

    label1=Label(login_screen, text="Mg",anchor=CENTER,justify=CENTER,font=('Times New Roman',14,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label1.configure(width=15,height=2)
    label1=c.create_window(320,350,anchor=SE,window=label1)

    label2=Label(login_screen, text="Timings",anchor=CENTER,justify=CENTER,font=('Times New Roman',14,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label2.configure(width=15,height=2)
    label2=c.create_window(320,450,anchor=SE,window=label2)

    button13=Button(login_screen, text="Back",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,command=lambda :[login_screen.destroy(),patient_homepage()],bg='#F0FFFF',relief=RIDGE,bd=2)
    button13.configure(width=12,height=2)
    button_window13=c.create_window(110,56,anchor=SE,window=button13)

    button14=Button(login_screen, text="Logout",anchor=CENTER,command=login_screen.destroy,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,bg='#F0FFFF',relief=RIDGE,bd=2)
    button14.configure(width=12,height=2)
    button_window14=c.create_window(795,56,anchor=SE,window=button14)


def view_all_patient_details():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Health Monitoring System")
    login_screen.geometry("800x600")

    c=Canvas(login_screen,width=800,height=600)
    c.pack()
    image=PhotoImage(file="C:\\Users\\lenovo\\Documents\\PROJECTS\\PYTHON\\globe.png")
    c.create_image(400,300,anchor="center",image=image)
    background_label = Label(login_screen, image=image)
    background_label.image = image

    label=Label(login_screen, text="SOLDIERS DETAILS",anchor=CENTER,justify=CENTER,font=('Times New Roman',18,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label.configure(width=25,height=2)
    label=c.create_window(570,130,anchor=SE,window=label)

    query="SELECT * FROM PATIENT"
    rows=conn.execute(query)
    

    listbox=Text(login_screen,bg='#F0FFFF')
    listbox.configure(width=50,height=20)
    listbox.insert(INSERT,"  PATIENT ID | NAME \t\t\t|  AGE   | GENDER\n")
    listbox.insert(END,"  ------------------------------------------")
    listbox.insert(END,"\n")
    for row in rows:
        listbox.insert(END,"  ")
        listbox.insert(END,row[0])
        listbox.insert(END,"\t     | ")
        listbox.insert(END,row[1])
        listbox.insert(END,"\t\t| ")
        listbox.insert(END,row[2])
        listbox.insert(END,"\t | ")
        listbox.insert(END,row[3])
        listbox.insert(END,"\n")

    listbox=c.create_window(600,500,anchor=SE,window=listbox)
   
    button13=Button(login_screen, text="Back",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,command=lambda :[login_screen.destroy(),doctor_homepage()],bg='#F0FFFF',relief=RIDGE,bd=2)
    button13.configure(width=12,height=2)
    button_window13=c.create_window(110,56,anchor=SE,window=button13)

    button14=Button(login_screen, text="Logout",command=login_screen.destroy,anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,bg='#F0FFFF',relief=RIDGE,bd=2)
    button14.configure(width=12,height=2)
    button_window14=c.create_window(795,56,anchor=SE,window=button14)

    
def patient_homepage():

    global ph_login_screen
    ph_login_screen = Toplevel(main_screen)
    ph_login_screen.title("Health Monitoring System")
    ph_login_screen.geometry("800x600")

    c=Canvas(ph_login_screen,width=800,height=600)
    c.pack()
    image=PhotoImage(file="C:\\Users\\lenovo\\Documents\\PROJECTS\\PYTHON\\globe.png")
    c.create_image(400,300,anchor="center",image=image)
    background_label = Label(ph_login_screen, image=image)
    background_label.image = image

    new=1
    url="https://thingspeak.com/channels/918595"
    url1="https://thingspeak.com/channels/915972"

    def openweb1():
        webbrowser.open(url,new=new)
    def openweb2():
        webbrowser.open(url1,new=new)

    label=Label(ph_login_screen, text="HOMEPAGE",anchor=CENTER,justify=CENTER,font=('Times New Roman',18,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label.configure(width=25,height=2)
    label=c.create_window(570,150,anchor=SE,window=label)
    
    button11=Button(ph_login_screen, text="View Prescription",anchor=CENTER,command=lambda :[view_prescription(),ph_login_screen.destroy()],justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,bg='#F0FFFF',relief=RIDGE,bd=4)
    button11.configure(width=22,height=2)
    button_window11=c.create_window(480,250,anchor=SE,window=button11)

    button12=Button(ph_login_screen, text="View Pulse rate Graph",command=openweb1,anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,bg='#F0FFFF',relief=RIDGE,bd=4)
    button12.configure(width=22,height=2)
    button_window12=c.create_window(480,350,anchor=SE,window=button12)

    button12=Button(ph_login_screen, text="View Temperature Graph",command=openweb2,anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,bg='#F0FFFF',relief=RIDGE,bd=4)
    button12.configure(width=22,height=2)
    button_window12=c.create_window(480,450,anchor=SE,window=button12)

    button13=Button(ph_login_screen, text="Back",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,command=lambda :[ph_login_screen.destroy(),patient_login()],bg='#F0FFFF',relief=RIDGE,bd=2)
    button13.configure(width=12,height=2)
    button_window13=c.create_window(110,56,anchor=SE,window=button13)

    button14=Button(ph_login_screen, text="Logout",anchor=CENTER,command=ph_login_screen.destroy,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,bg='#F0FFFF',relief=RIDGE,bd=2)
    button14.configure(width=12,height=2)
    button_window14=c.create_window(795,56,anchor=SE,window=button14)

   
def prescription():
    global plogin_screen
    global pd_username1
    plogin_screen = Toplevel(main_screen)
    plogin_screen.title("Health Monitoring System")
    plogin_screen.geometry("800x600")

    c=Canvas(plogin_screen,width=800,height=600)
    c.pack()
    image=PhotoImage(file="C:\\Users\\lenovo\\Documents\\PROJECTS\\PYTHON\\globe.png")
    c.create_image(400,300,anchor="center",image=image)
    background_label = Label(plogin_screen, image=image)
    background_label.image = image

    label=Label(plogin_screen, text="Medicine Name",anchor=CENTER,justify=CENTER,font=('Times New Roman',14,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label.configure(width=15,height=2)
    label=c.create_window(350,150,anchor=SE,window=label)

    label1=Label(plogin_screen, text="Mg",anchor=CENTER,justify=CENTER,font=('Times New Roman',14,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label1.configure(width=15,height=2)
    label1=c.create_window(350,250,anchor=SE,window=label1)

    label2=Label(plogin_screen, text="Timings",anchor=CENTER,justify=CENTER,font=('Times New Roman',14,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label2.configure(width=15,height=2)
    label2=c.create_window(350,350,anchor=SE,window=label2)

    global entry
    global entry1
    global entry2
    global tablet_name
    global tablet_mg
    global tablet_timings

    tablet_name=StringVar()
    tablet_mg=StringVar()
    tablet_timings=StringVar()
    
    entry=Entry(c,textvariable=tablet_name)
    c.create_window(500,125,window=entry,height=25,width=200)

    entry1=Entry(c, textvariable=tablet_mg)
    c.create_window(500,225,window=entry1,height=25,width=200)

    entry2=Entry(c, textvariable=tablet_timings)
    c.create_window(500,325,window=entry2,height=25,width=200)

    button1=Button(plogin_screen, text="Submit",anchor=CENTER,command=add_prescription,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,bg='#F0FFFF',relief=RIDGE,bd=4)
    button1.configure(width=15,height=2)
    button_window1=c.create_window(475,450,anchor=SE,window=button1)

    button13=Button(plogin_screen, text="Back",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,command=lambda :[plogin_screen.destroy(),patient_detail()],bg='#F0FFFF',relief=RIDGE,bd=2)
    button13.configure(width=12,height=2)
    button_window13=c.create_window(110,56,anchor=SE,window=button13)

    button14=Button(plogin_screen, text="Logout",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,command=plogin_screen.destroy,bg='#F0FFFF',relief=RIDGE,bd=2)
    button14.configure(width=12,height=2)
    button_window14=c.create_window(795,56,anchor=SE,window=button14)


def patient_detail():
    
    global pd_login_screen
    pd_login_screen = Toplevel(main_screen)
    pd_login_screen.title("Health Monitoring System")
    pd_login_screen.geometry("800x600")

    c=Canvas(pd_login_screen,width=800,height=600)
    c.pack()
    image=PhotoImage(file="C:\\Users\\lenovo\\Documents\\PROJECTS\\PYTHON\\globe.png")
    c.create_image(400,300,anchor="center",image=image)
    background_label = Label(pd_login_screen, image=image)
    background_label.image = image

    new=1
    url="https://thingspeak.com/channels/918595"
    url1="https://thingspeak.com/channels/915972"

    def openweb1():
        webbrowser.open(url,new=new)
    def openweb2():
        webbrowser.open(url1,new=new)

    button=Button(pd_login_screen, text="View Pulse rate Graph",command=openweb1,anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,bg='#F0FFFF',relief=RIDGE,bd=4)
    button.configure(width=22,height=2)
    button_window1=c.create_window(475,250,anchor=SE,window=button)

    button=Button(pd_login_screen, text="View Temperature Graph",command=openweb2,anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,bg='#F0FFFF',relief=RIDGE,bd=4)
    button.configure(width=22,height=2)
    button_window1=c.create_window(475,350,anchor=SE,window=button)

    button1=Button(pd_login_screen, text="Add Prescription",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,command=lambda :[prescription(),pd_login_screen.destroy()],bg='#F0FFFF',relief=RIDGE,bd=4)
    button1.configure(width=22,height=2)
    button_window1=c.create_window(475,450,anchor=SE,window=button1)

    button13=Button(pd_login_screen, text="Back",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,command=lambda :[pd_login_screen.destroy(),doctor_homepage()],bg='#F0FFFF',relief=RIDGE,bd=2)
    button13.configure(width=12,height=2)
    button_window13=c.create_window(110,56,anchor=SE,window=button13)

    button14=Button(pd_login_screen, text="Logout",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,command=pd_login_screen.destroy,bg='#F0FFFF',relief=RIDGE,bd=2)
    button14.configure(width=12,height=2)
    button_window14=c.create_window(795,56,anchor=SE,window=button14)
 
    
def doctor_homepage():
    global dh_login_screen
    dh_login_screen = Toplevel(main_screen)
    dh_login_screen.title("Health Monitoring System")
    dh_login_screen.geometry("800x600")

    c=Canvas(dh_login_screen,width=800,height=600)
    c.pack()
    image=PhotoImage(file="C:\\Users\\lenovo\\Documents\\PROJECTS\\PYTHON\\globe.png")
    c.create_image(400,300,anchor="center",image=image)
    background_label = Label(dh_login_screen, image=image)
    background_label.image = image

    label=Label(dh_login_screen, text="DOCTOR HOMEPAGE",anchor=CENTER,justify=CENTER,font=('Times New Roman',18,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label.configure(width=25,height=2)
    label=c.create_window(570,150,anchor=SE,window=label)

    label1=Label(dh_login_screen, text="Soldier Id",anchor=CENTER,justify=CENTER,font=('Times New Roman',14,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label1.configure(width=17,height=2)
    label1=c.create_window(350,400,anchor=SE,window=label1)

    global username_verify
    global entry

    entry=Entry(c, textvariable=username_verify)
    c.create_window(500,375,window=entry,height=25,width=200)

    button1=Button(dh_login_screen, text="OK",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,command=lambda :[patient_detail_validate(),dh_login_screen.destroy()],bg='#F0FFFF',relief=RIDGE,bd=4)
    button1.configure(width=8,height=1)
    button_window1=c.create_window(425,470,anchor=SE,window=button1)
 

    button1=Button(dh_login_screen, text="View All SOLIDERS DETAILS",anchor=CENTER,command=lambda :[view_all_patient_details(),dh_login_screen.destroy()],justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,bg='#F0FFFF',relief=RIDGE,bd=4)
    button1.configure(width=15,height=2)
    button_window1=c.create_window(450,300,anchor=SE,window=button1)
 

    button13=Button(dh_login_screen, text="Back",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,command=lambda :[dh_login_screen.destroy(),doctor_login()],bg='#F0FFFF',relief=RIDGE,bd=2)
    button13.configure(width=12,height=2)
    button_window13=c.create_window(110,56,anchor=SE,window=button13)

    button14=Button(dh_login_screen, text="Logout",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,command=dh_login_screen.destroy,bg='#F0FFFF',relief=RIDGE,bd=2)
    button14.configure(width=12,height=2)
    button_window14=c.create_window(795,56,anchor=SE,window=button14)

 
def patient_login():
    global p_login_screen
    p_login_screen = Toplevel(main_screen)
    p_login_screen.title("Health Monitoring System")
    p_login_screen.geometry("800x600")

    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    c=Canvas(p_login_screen,width=800,height=600)
    c.pack()
    image=PhotoImage(file="C:\\Users\\lenovo\\Documents\\PROJECTS\\PYTHON\\globe.png")
    c.create_image(400,300,anchor="center",image=image)
    background_label = Label(p_login_screen, image=image)
    background_label.image = image

    label=Label(p_login_screen, text="Username",anchor=CENTER,justify=CENTER,font=('Times New Roman',14,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label.configure(width=15,height=2)
    label=c.create_window(350,250,anchor=SE,window=label)

    label1=Label(p_login_screen, text="Password",anchor=CENTER,justify=CENTER,font=('Times New Roman',14,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label1.configure(width=15,height=2)
    label1=c.create_window(350,350,anchor=SE,window=label1)
    
    label2=Label(p_login_screen, text="SOLDIER LOGIN",anchor=CENTER,justify=CENTER,font=('Times New Roman',18,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label2.configure(width=25,height=2)
    label2=c.create_window(570,150,anchor=SE,window=label2)

    global entry
    global entry1
    
    entry=Entry(c, textvariable=username_verify)
    c.create_window(500,225,window=entry,height=25,width=200)
    
    entry1=Entry(c, textvariable=password_verify,show="*")
    c.create_window(500,325,window=entry1,height=25,width=200)

    b=Button(p_login_screen, text="LOG IN",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),command=lambda :[pat_validate(),p_login_screen.destroy()],bg='#F0FFFF',relief=RIDGE,bd=4)
    b.configure(width=20,height=2)
    b_w=c.create_window(400,425,anchor=CENTER,window=b)

    button13=Button(p_login_screen, text="Back",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,command=lambda :[p_login_screen.destroy(),login_page()],bg='#F0FFFF',relief=RIDGE,bd=2)
    button13.configure(width=12,height=2)
    button_window13=c.create_window(110,56,anchor=SE,window=button13)
    

def doctor_login():
    global d_login_screen
    d_login_screen = Toplevel(main_screen)
    d_login_screen.title("Health Monitoring System")
    d_login_screen.geometry("800x600")

    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    c=Canvas(d_login_screen,width=800,height=600)
    c.pack()
    image=PhotoImage(file="C:\\Users\\lenovo\\Documents\\PROJECTS\\PYTHON\\globe.png")
    c.create_image(400,300,anchor="center",image=image)
    background_label = Label(d_login_screen, image=image)
    background_label.image = image

    label=Label(d_login_screen, text="Username",anchor=CENTER,justify=CENTER,font=('Times New Roman',14,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label.configure(width=15,height=2)
    label=c.create_window(350,250,anchor=SE,window=label)

    label1=Label(d_login_screen, text="Password",anchor=CENTER,justify=CENTER,font=('Times New Roman',14,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label1.configure(width=15,height=2)
    label1=c.create_window(350,350,anchor=SE,window=label1)
    
    label2=Label(d_login_screen, text="DOCTOR LOGIN",anchor=CENTER,justify=CENTER,font=('Times New Roman',18,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label2.configure(width=25,height=2)
    label2=c.create_window(570,150,anchor=SE,window=label2)

    global entry
    global entry1

    entry=Entry(c, textvariable=username_verify)
    c.create_window(500,225,window=entry,height=25,width=200)
    
    entry1=Entry(c, textvariable=password_verify,show="*")
    c.create_window(500,325,window=entry1,height=25,width=200)

    b=Button(d_login_screen, text="LOG IN",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),command=lambda :[doc_validate(),d_login_screen.destroy()],bg='#F0FFFF',relief=RIDGE,bd=4)
    b.configure(width=20,height=2)
    b_w=c.create_window(400,425,anchor=CENTER,window=b)

    button13=Button(d_login_screen, text="Back",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,command=lambda :[d_login_screen.destroy(),login_page()],bg='#F0FFFF',relief=RIDGE,bd=2)
    button13.configure(width=12,height=2)
    button_window13=c.create_window(110,56,anchor=SE,window=button13)

 
def login_page():
    
    global l_login_screen
    l_login_screen = Toplevel(main_screen)
    l_login_screen.title("Health Monitoring System")
    l_login_screen.geometry("800x600")
    
    c1=Canvas(l_login_screen,width=800,height=600)
    c1.pack()
    image=PhotoImage(file="C:\\Users\\lenovo\\Documents\\PROJECTS\\PYTHON\\globe.png")
    background_label = Label(l_login_screen, image=image)
    background_label.image = image      
    c1.create_image(400,300,anchor="center",image=image)
    
    button11=Button(l_login_screen, text="DOCTOR LOGIN",command=lambda :[doctor_login(),l_login_screen.destroy()],anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,bg='#F0FFFF',relief=RIDGE,bd=4)
    button11.configure(width=20,height=2)
    button_window11=c1.create_window(480,250,anchor=SE,window=button11)

    button12=Button(l_login_screen, text="SOLDIER LOGIN",command=lambda :[patient_login(),l_login_screen.destroy()],anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,bg='#F0FFFF',relief=RIDGE,bd=4)
    button12.configure(width=20,height=2)
    button_window12=c1.create_window(480,350,anchor=SE,window=button12)

    button13=Button(l_login_screen, text="Back",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,command=l_login_screen.destroy,bg='#F0FFFF',relief=RIDGE,bd=2)
    button13.configure(width=12,height=2)
    button_window13=c1.create_window(110,56,anchor=SE,window=button13)

def about_page():
    global a_login_screen
    a_login_screen = Toplevel(main_screen)
    a_login_screen.title("Health Monitoring System")
    a_login_screen.geometry("800x600")
    
    c1=Canvas(a_login_screen,width=800,height=600)
    c1.pack()
    image=PhotoImage(file="C:\\Users\\lenovo\\Documents\\PROJECTS\\PYTHON\\globe.png")
    background_label = Label(a_login_screen, image=image)
    background_label.image = image      
    c1.create_image(400,300,anchor="center",image=image)

    label=Label(a_login_screen, text="ABOUT",anchor=CENTER,justify=CENTER,font=('Times New Roman',18,'bold'),state=NORMAL,bg='#F0FFFF',relief=SOLID,bd=1)
    label.configure(width=15,height=2)
    label=c1.create_window(520,120,anchor=SE,window=label)

    explanation="Health Monitoring System measures the Pulse rate(BP) and Body Temperature of patients. \nIt provides an online platform for communication between the doctor and the patient. \nThe patient can measure the BP and temperature at home \nand an alert will be sent to the doctor in case of any emergency.\nThe doctor can add priscription through the online platform.\n\n\n\nCONTACT NUMBER\nNamratha : 9482141788\nRamya : 9538536898\nYashita : 8970736699\nSanjay : 9742722370\nEmail :health_monitoring@bmsce.ac.in"

    label1=Label(a_login_screen, text=explanation,anchor=CENTER,justify=CENTER,font=('Times New Roman',13),state=NORMAL,bg='#F0FFFF',fg="#000000",relief=FLAT,bd=1)
    label1.configure(width=80,height=20)
    label1=c1.create_window(400,350,window=label1)

    button13=Button(a_login_screen, text="Back",anchor=CENTER,justify=CENTER,font=('calibri',12,'bold'),state=NORMAL,command=a_login_screen.destroy,bg='#F0FFFF',relief=RIDGE,bd=2)
    button13.configure(width=12,height=2)
    button_window13=c1.create_window(110,56,anchor=SE,window=button13)

c=Canvas(main_screen,width=800,height=600,bg="white")
c.pack()
image8=PhotoImage(file = "C:\\Users\\lenovo\\Documents\\PROJECTS\\PYTHON\\home.png")
c.create_image(400,300,anchor="center",image=image8)

button=Button(main_screen, text="LOGIN",relief=FLAT,anchor=S,justify=CENTER,font=('calibri',12,'bold'),command=login_page,bg='#EBF4FA',activebackground='#add8e6',bd=0)
button.configure(width=10,height=2)
button_window=c.create_window(800,30,anchor=SE,window=button)

button1=Button(main_screen, text="ABOUT",relief=FLAT,anchor=S,justify=CENTER,font=('calibri',12,'bold'),command=about_page,state=NORMAL,bg='#EBF4FA',activebackground='#add8e6',bd=0)
button1.configure(width=10,height=2)
button_window1=c.create_window(700,30,anchor=SE,window=button1)



main_screen.mainloop()

