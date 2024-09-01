from django.shortcuts import render,redirect
from django.http import HttpResponse
import mysql.connector
from .models import *
import sqlite3
from datetime import datetime, timedelta
from random import randint
import smtplib
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random


#generation funtions end
# Create your views here.

def timetable_view(request):
    return render(request,'timetable_view.html')

#admin funtions start
def login(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        uname = request.POST['username']
        pwd = request.POST['pass']
        query.execute("select * from admintable where username='"+uname+"' and password='"+pwd+"'")
        result=query.fetchone()
        if(result!=None):
            request.session["username"]=uname
            return render(request, 'index.html', {"name" : uname})
        
            #redirect('dashboard')
        else:
            return render(request,'login.html',{'status':'invalid credentials'})    
    else:
        return render(request,'login.html')
    
def logout(request):
    try:
        del request.session['username']
        request.session.modified = True
        return render(request,'login.html') 
    except KeyError:
        return redirect('login')    


def change_password(request):
   # return HttpResponse("<h3>Welcome hnc</h3>")
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234",
            database="timetable"
        )
        mycursor = conn.cursor()
        # retrive post details
        otp = request.POST['otp-code']
        npwd = request.POST['new-password']
        em = request.POST['email']
        mycursor.execute("select username from forget where otp='"+otp+"'")
        result=mycursor.fetchone()
        mail=em
       
        if(result!=None):
#            sql = "UPDATE registration SET u_password = %s WHERE email = %s"
            #mycursor.execute("UPDATE customers SET address = %s WHERE address = %s")
 #           val = (npwd, em)
            mycursor.execute("UPDATE admin SET password ='"+npwd+"' WHERE username ='"+mail+"'")
            conn.commit()
            return render(request, 'login.html', {'status':'success'})
            
        else:
            return render(request,'change_password.html',{'status':'invalid otp'})    


def forgot(request):

    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234",
            database="timetable"
        )
        mycursor = conn.cursor()
        # retrive post details
        email = request.POST['username']
        #for otp in range(0,4):
        otp=str(random.randint(100000,999999))
        uname=[]
        uname.append(email)

        mycursor.execute("insert into forget(username,otp) values('"+email+"','"+otp+"')")
        conn.commit()

        #result = mycursor.fetchone()
        #pwd=str(result)
        #if (result != None):
            # SMTP server configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'vishnutejakommera5@gmail.com'
# for App Password enable 2-step verification then u can create app password
        smtp_password = 'euhr qbmy eway tcqn'

# Email content
        subject = 'Password recovery'
        body = 'This is a Password recovery email sent from kits.'+'Your password as per registration is: '+ otp
        sender_email = 'vishnutejakommera5@gmail.com'
        receiver_email = email

# Create a message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            
            return render(request, 'change_password.html', {'un':uname})
     
    else:
        return render(request, 'forgot.html')

def admin_register(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        username=request.POST['uname']
        pwd=request.POST['pass']     
        query.execute("insert into admin(username,password) values('"+username+"','"+pwd+"')")
        conn.commit()
        return redirect('login')
    else:
        return render(request,'admin_registration.html')#{ key:list}


def index(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        query.execute("select username from admintable Limit 1")
        result=query.fetchone()
        context = {'username': result[0] if result else None}
        return render(request,'index.html',context)
    if "username" in request.session:
        uname = request.session['username']
        return render(request,'index.html',{'name':uname})
    else:
        return render(request,'login.html') 



def depmanage(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        
        return render(request,'add_dep.html')
    elif "username" in request.session:
        uname = request.session['username']
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        
        query = conn.cursor()
        query.execute("select * from department")
        result= query.fetchall()
        branch=[]
        for row in result:
            br=Branch()
            br.bid=row[0]
            br.bname=row[1]
            branch.append(br)  
        return render(request,'managedep.html',{"branches":branch})#{ key:list}
    else:
        return render(request,'login.html')    
        
    
def add_dep(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        depname=request.POST['dname']
        query.execute("select * from department where depcode='"+depname+"'")
        result= query.fetchone()
        if(result==None):
               
            query.execute("insert into department(depcode) values('"+depname+"')")
            conn.commit()
            return render(request, 'add_dep.html',{'status': 'Department added successfully.'})
            
        else:
            return render(request, 'add_dep.html', {'status': 'Department already exists!'})
    elif "username" in request.session:
        uname = request.session['username']
        return render(request,'add_dep.html')
    else:
        return render(request,'login.html')
        

def del_dep(request,bname):
    conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'root1234',
        database = 'timetable'
    )
    query = conn.cursor()
    query.execute("DELETE FROM department where depcode='"+bname+"'")
    conn.commit()
    return render(request, 'del_dep.html',{'status': 'Department deleted successfully.'})


def edit_dep(request,bname):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        depname = request.POST['dname']
        query.execute("update department set depcode ='"+depname+"' where depcode='"+bname+"'")
        conn.commit()
        return render(request, 'edit_dep.html',{'status': 'Department edited successfully.'})
    elif "username" in request.session:
        uname = request.session['username']
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        query.execute("select * from department where depcode='"+bname+"'")
        result= query.fetchall()
        branch=[]
        for row in result:
            br=Branch()
            br.bid=row[0]
            br.bname=row[1]
            branch.append(br)
        return render(request,'edit_dep.html',{"branches":branch})
    else:
        return render(request,'login.html')    

def subject(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        
        return render(request,'add_sub.html')
    elif "username" in request.session:
        uname = request.session['username']
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        
        query = conn.cursor()
        query.execute("select * from subject")
        result= query.fetchall()
        subjects=[]
        for row in result:
            s=Subject()
            s.subid=row[0]
            s.subcode=row[1]
            s.subname=row[2]
            s.subl=row[3]
            s.subt=row[4]
            s.subp=row[5]
            s.subdep=row[6]
            s.subyear=row[7]
            s.subsem=row[8]
            s.subreg=row[9]
            subjects.append(s)  
        return render(request,'subject.html',{"subject":subjects})#{ key:list}
    else:
        return render(request,'login.html')

def add_sub(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        sn=request.POST['sname']
        sc=request.POST['scode']
        le=request.POST['lectures']
        pa=request.POST['practicals']
        branch=request.POST['branch']
        year=request.POST['year']
        sem=request.POST['semester']
        reg=request.POST['ar']
        query.execute("select * from subject where scode='"+sc+"' and regulation='"+reg+"'")
        result= query.fetchone()
        if(result==None):
               
            query.execute("insert into subject(scode,sname,lectures,practicals,department,year,semester,regulation) values('"+sc+"','"+sn+"','"+le+"','"+pa+"','"+branch+"','"+year+"','"+sem+"','"+reg+"')")
            conn.commit()
            return render(request, 'add_sub.html',{'status': 'subject added successfully.'})
            
        else:
            return render(request, 'add_sub.html', {'status': 'subject adding failed or subject already exists '})
    elif "username" in request.session:
        uname = request.session['username']
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        query.execute("select * from department")
        result= query.fetchall()
        branch=[]
        for row in result:
            br=Branch()
            br.bid=row[0]
            br.bname=row[1]
            branch.append(br)  
        return render(request,'add_sub.html',{"branches":branch})#{ key:list}
    else:
        return render(request,'login.html')

def del_sub(request,subid):
    conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'root1234',
        database = 'timetable'
    )
    query = conn.cursor()
    query.execute("DELETE FROM subject where sid='"+subid+"'")
    conn.commit()
    return render(request, 'del_dep.html',{'status': 'subject deleted successfully.'})

def edit_sub(request,subid):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        sn=request.POST['sname']
        co=request.POST['scode']
        le=request.POST['lecture']
        tu=request.POST['tutorial']
        pa=request.POST['practical']
        branch=request.POST['branch']
        year=request.POST['year']
        sem=request.POST['semester']
        reg=request.POST['ar']
        query.execute("update subject set sname ='"+sn+"',scode ='"+co+"',lectures ='"+le+"',tutorials ='"+tu+"',practicals ='"+pa+"',department ='"+branch+"',year ='"+year+"',semester ='"+sem+"',regulation ='"+reg+"' where sid='"+subid+"'")
        conn.commit()
        return render(request, 'edit_sub.html',{'status': 'Subject edited successfully.'})
    
    
    elif "username" in request.session:
        uname = request.session['username']
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        query.execute("select * from subject where sid='"+subid+"'")
        result= query.fetchall()
        subjects=[]
        for row in result:
            s=Subject()
            s.subid=row[0]
            s.subcode=row[1]
            s.subname=row[2]
            s.subl=row[3]
            s.subt=row[4]
            s.subp=row[5]
            s.subdep=row[6]
            s.subyear=row[7]
            s.subsem=row[8]
            s.subreg=row[9]
            subjects.append(s)  
        query1 = conn.cursor()
        query1.execute("select * from department")
        result= query1.fetchall()
        branch=[]
        for row in result:
            br=Branch()
            br.bid=row[0]
            br.bname=row[1]
            branch.append(br)  
        return render(request,'edit_sub.html',{"subject":subjects,"branches":branch})#{ key:list}            
    else:
        return render(request,'login.html') 
        
def faculty(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        return render(request,'add_fac.html')
    elif "username" in request.session:
        uname = request.session['username']
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        query.execute("select * from faculty_subject")
        result= query.fetchall()
        faculty_sub=[]
        for row in result:
            fs=FS()
            fs.fsid=row[0]
            fs.fname=row[1]
            fs.sname=row[2]
            fs.dep=row[3]
            fs.year=row[4]
            fs.sec=row[5]
            fs.ay=row[6]
            faculty_sub.append(fs)
              
        return render(request,'faculty.html',{"faculty":faculty_sub})#{ key:list}
    else:
        return render(request,'login.html')  
        
    
def add_fac(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        fn=request.POST['fname']
        sn=request.POST['sname']
        b=request.POST['branch']
        y=request.POST['year']
        sec=request.POST['section']
        a=request.POST['ar']
        query.execute("select * from faculty_subject where faculty_name='"+fn+"'")
        result= query.fetchone()
        if(result==None):
            query.execute("insert into faculty_subject(faculty_name,subject_name,department,year,section,academic_year) values('"+fn+"','"+sn+"','"+b+"','"+y+"','"+sec+"','"+a+"')")
            conn.commit()
            return render(request, 'add_fac.html',{'status': 'Faculty added successfully.'})
           

        else:
            return render(request, 'add_fac.html', {'status': 'Faculty already exists!'})

    elif "username" in request.session:
        uname = request.session['username']
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        query.execute("select * from department")
        result= query.fetchall()
        branch=[]
        for row in result:
            br=Branch()
            br.bid=row[0]
            br.bname=row[1]
            branch.append(br)
        return render(request,'add_fac.html',{"branches":branch})
    else:
        return render(request,'login.html')
       

def del_fac(request,fsid):
    conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'root1234',
        database = 'timetable'
    )
    query = conn.cursor()
    query.execute("DELETE FROM faculty_subject where sfid='"+fsid+"'")
    conn.commit()
    return render(request, 'del_fac.html',{'status': 'Faculty deleted successfully.'})
 

def edit_fac(request,fsid):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        fn = request.POST['fname']
        sn=request.POST['sname']
        b=request.POST['branch']
        y=request.POST['year']
        sec=request.POST['section']
        a=request.POST['ar']
        query.execute("update faculty_subject set faculty_name ='"+fn+"',subject_name='"+sn+"' ,department='"+b+"',year='"+y+"',section='"+sec+"',academic_year='"+a+"' where sfid='"+fsid+"'")
        conn.commit()
        return render(request, 'edit_fac.html',{'status': 'Faculty edited successfully.'})
    elif "username" in request.session:
        uname = request.session['username']
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        query.execute("select * from faculty_subject where sfid='"+fsid+"'")
        result= query.fetchall()
        faculty_sub=[]
        for row in result:
            fs=FS()
            fs.fsid=row[0]
            fs.fname=row[1]
            fs.sname=row[2]
            fs.dep=row[3]
            fs.year=row[4]
            fs.sec=row[5]
            fs.ay=row[6]
            faculty_sub.append(fs)
        query.execute("select * from department")
        result= query.fetchall()
        branch=[]
        for row in result:
            br=Branch()
            br.bid=row[0]
            br.bname=row[1]
            branch.append(br) 
        return render(request,'edit_fac.html',{"faculty":faculty_sub,"branches":branch})#{ key:list}
    else:
        return render(request,'login.html')
    
def create_tt(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        b=request.POST['branch']
        y=request.POST['year']
        sem=request.POST['semester']
        reg=request.POST['regulation']
        ay=request.POST['ay']
        sec=request.POST['sec']
        a_year=[]
        a_year.append(ay)
        section=[]
        section.append(sec)
        
        query.execute("select * from subject where department='"+b+"' and year='"+y+"' and semester='"+sem+"' and regulation='"+reg+"'")
        result=query.fetchall()
        subjects=[]
        for row in result:
            s=Subject()
            s.subid=row[0]
            s.subcode=row[1]
            s.subname=row[2]
            s.subl=row[3]
            s.subt=row[4]
            s.subp=row[5]
            s.subdep=row[6]
            s.subyear=row[7]
            s.subsem=row[8]
            s.subreg=row[9]
            subjects.append(s)
        return render(request,'select_sub.html',{"subject":subjects,"a":a_year,"se":section})
    
    elif "username" in request.session:
        uname = request.session['username']
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        
        query = conn.cursor() 
        query.execute("select * from department")
        result= query.fetchall()
        branch=[]
        for row in result:
            br=Branch()
            br.bid=row[0]
            br.bname=row[1]
            branch.append(br)  
        return render(request,'create_tt.html',{"branches":branch})#{ key:list}
    else:
        return render(request,'login.html')
    
def gen_tt(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor(buffered=True)
        sub=request.POST['selectedsubjects']
        b=request.POST['branch']
        branch=[]
        branch.append(b)
        y=request.POST['year']
        year=[]
        year.append(y)
        s=request.POST['semester']
        sem=[]
        sem.append(s)
        r=request.POST['regulation']
        reg=[]
        reg.append(r)
        a=request.POST['ay']
        academic=[]
        academic.append(a)
        sec=request.POST['sec']
        section=[]
        section.append(sec)
        sub_list=sub.split(',')
        subf_list=list(filter(None,sub_list))
        sub_fac={}
        fac=[]
        facle=[]
        subl=[]
        suble=[]
        lab=[]
        week=['MON','TUE','WED','THU','FRI','SAT']
        time=['t1','t2','t3','t4','t5','t6','t7']
        print(subf_list)
        query.execute("select * from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' ")
        schedule=query.fetchone()
        if schedule==None:
            for day in week:
                query.execute("Insert into time_table(department,regulation,academic_year,year,semester,section,weekday) values('"+b+"','"+r+"','"+a+"','"+y+"','"+s+"','"+sec+"','"+day+"')")
        
        #lab section starts----------------
          
        for sub in subf_list:
            query.execute('SELECT faculty_name FROM faculty_subject where FIND_IN_SET("'+sub+'",subject_name) > 0  and department="'+b+'" and year="'+y+'" and 	academic_year="'+a+'" and FIND_IN_SET("'+sec+'",section) > 0 ')
            resultf=query.fetchall()
            fac.append(resultf[0][0])
            query.execute("select scode,is_lab from subject where sname='"+sub+"' and department='"+b+"' and year='"+y+"' and semester='"+s+"'")
            result=query.fetchone()
            subl.append(result[1])
            
            if result[1]==1:
                flag = 20
                while flag > 0:
                    ran=randint(0, 1)
                    if ran==1:
                        w=randint(1,4)
                        we=week[w]
                        sc=result[0]
                        fl=0
                        lab_asm=0
                        lab_asa=0
                        query.execute("select * from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"'")
                        resultl=query.fetchone()
                        if resultl==None:
                            for day in week:
                                query.execute("Insert into faculty_load(faculty_name,department,weekday) values('"+resultf[0][0]+"','"+b+"','"+day+"')")
                        
                        query.execute("select FIND_IN_SET('"+sc+"',t2) > 0,FIND_IN_SET('"+sc+"',t3) > 0,FIND_IN_SET('"+sc+"',t4) > 0 from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"'")
                        facl=query.fetchall()
                        print(facl[0],'facl FN',sc,we)
                        for f in facl[0]:
                            if f==1:
                                fl=2
                                print(sc,' already assigned on FN',we)
                                break
                            if f==0:
                                fl=1
                                print(' cannot assign as faclty is assigned for other class on FN',we)
                                break
                            else:
                                pass
                        if fl==0:
                            query.execute("select FIND_IN_SET('"+sc+"',t2) > 0,FIND_IN_SET('"+sc+"',t5) > 0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"'") 
                            sh=query.fetchall()
                            print(sh)
                            for q in sh:
                                if q[0]==1:
                                    lab_asm=2
                                    break
                            for q in sh:
                                if q[1]==1:
                                    lab_asa=2
                                    break
                            if lab_asm==2 or lab_asa==2:
                                flag=0
                                break
                            if lab_asm==0 and lab_asa==0:
                                query.execute("select FIND_IN_SET('"+sc+"',t2) > 0,FIND_IN_SET('"+sc+"',t5) > 0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'") 
                                sh=query.fetchall()
                                print(sh)
                                for q in sh:
                                    if q[0]==None:
                                        lab_asm=1
                                        break
                                for q in sh:
                                    if q[1]==None:
                                        lab_asa=1
                                        break
                                if lab_asm==1 and lab_asa==1:
                                    
                                    query.execute("select FIND_IN_SET('"+sc+"',t2) > 0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and weekday='"+we+"'") 
                                    ssh=query.fetchone()
                                    con=ssh[0]
                                    print(ssh[0],'SECOND HOUR')
                                    if con == None:
                                        print('assigned FN')
                                        query.execute("update faculty_load set t2='"+sc+"',t3='"+sc+"',t4='"+sc+"' where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"'")
                                        query.execute("update time_table set t2='"+sc+"',t3='"+sc+"',t4='"+sc+"' where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                        flag = 0
                                        break
                                    if con == 0:
                                        print('assigned FN')
                                        query.execute("update faculty_load set t5='"+sc+"',t6='"+sc+"',t7='"+sc+"' where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"'")
                                        query.execute("update time_table set t5='"+sc+"',t6='"+sc+"',t7='"+sc+"' where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                        flag = 0
                                        break
                        flag=flag-2
                    else:
                        w=randint(1,4)
                        we=week[w]
                        sc=result[0]
                        fl=0
                        lab_asm=0
                        lab_asa=0
                        query.execute("select * from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"'")
                        resultl=query.fetchone()
                        if resultl==None:
                            for day in week:
                                query.execute("Insert into faculty_load(faculty_name,department,weekday) values('"+resultf[0][0]+"','"+b+"','"+day+"')")

                        query.execute("select FIND_IN_SET('"+sc+"',t5) > 0,FIND_IN_SET('"+sc+"',t6) > 0,FIND_IN_SET('"+sc+"',t7) > 0 from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"'")
                        facl=query.fetchall()
                        print(facl[0],'facl AN',sc,we)
                        for f in facl[0]:
                            if f==1:
                                fl=2
                                print(sc,' already assigned on AN',we)
                                break
                            if f==0:
                                fl=1
                                print(' cannot assign as faclty is assigned for other class on AN',we)
                                break

                        if fl==0:
                            query.execute("select FIND_IN_SET('"+sc+"',t2) > 0,FIND_IN_SET('"+sc+"',t5) > 0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"'") 
                            sh=query.fetchall()
                            print(sh)
                            for q in sh:
                                if q[0]==1:
                                    lab_asm=2
                                    break
                            for q in sh:
                                if q[1]==1:
                                    lab_asa=2
                                    break
                            if lab_asm==2 or lab_asa==2:
                                flag=0
                                break
                            if lab_asm==0 and lab_asa==0:
                                query.execute("select FIND_IN_SET('"+sc+"',t2) > 0,FIND_IN_SET('"+sc+"',t5) > 0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'") 
                                sh=query.fetchall()
                                print(sh)
                                for q in sh:
                                    if q[0]==None:
                                        lab_asm=1
                                        break
                                for q in sh:
                                    if q[1]==None:
                                        lab_asa=1
                                        break
                                if lab_asm==1 and lab_asa==1:
                                    
                                    query.execute("select FIND_IN_SET('"+sc+"',t5) > 0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and weekday='"+we+"'") 
                                    ssh=query.fetchone()
                                    con=ssh[0]
                                    print(ssh[0],'FIFTH HOUR')
                                    if con==None:
                                        print('assigned AN')
                                        query.execute("update faculty_load set t5='"+sc+"',t6='"+sc+"',t7='"+sc+"'where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"'")
                                        query.execute("update time_table set t5='"+sc+"',t6='"+sc+"',t7='"+sc+"' where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                        flag=0
                                        break
                                    if con == 0:
                                        print('assigned FN')
                                        query.execute("update faculty_load set t2='"+sc+"',t3='"+sc+"',t4='"+sc+"' where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"'")
                                        query.execute("update time_table set t2='"+sc+"',t3='"+sc+"',t4='"+sc+"' where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                        flag = 0
                                        break
                             
                                                                     
                        flag-=1
                    flag=flag-2
        
        #lab section ends------------
        
        #first class assign start----------------
        
        for sub in subf_list:
            query.execute('SELECT faculty_name FROM faculty_subject where FIND_IN_SET("'+sub+'",subject_name) > 0  and department="'+b+'" and year="'+y+'" and 	academic_year="'+a+'" and FIND_IN_SET("'+sec+'",section) > 0 ')
            resultf=query.fetchall()
            fac.append(resultf[0][0])
            query.execute("select scode,is_lab from subject where sname='"+sub+"' and department='"+b+"' and year='"+y+"' and semester='"+s+"'")
            result=query.fetchone()
            subl.append(result[1])
            if result[1]==0:
                query.execute("select lectures from subject where sname='"+sub+"' and department='"+b+"' and year='"+y+"' and semester='"+s+"' and regulation='"+r+"'")
                lect=query.fetchone()
                le=lect[0]
                le1=le-1
                sc=result[0]
                flag=10
                
                class_assigned=0
                
                while flag>0 :   
                    while le>0 :
                        first_class=5
                        query.execute("select FIND_IN_SET('"+sc+"',t1)>0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' ")
                        h1=query.fetchall()
                        for h in h1:
                            if h[0]==1:
                                first_class=0
                                flag=0
                                break
                            
                                                        
                        if first_class!=0:
                            while first_class>0:
                                w=randint(0,5)
                                we=week[w]
                                print(resultf[0][0],b,we)
                                query.execute("select * from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"'")
                                resultl=query.fetchone()
                                if resultl==None:
                                    for day in week:
                                        query.execute("Insert into faculty_load(faculty_name,department,weekday) values('"+resultf[0][0]+"','"+b+"','"+day+"')")
                                query.execute("select FIND_IN_SET('"+sc+"',t1)>0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                empty_tt=query.fetchone()
                                query.execute("select FIND_IN_SET('"+sc+"',t1)>0 from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"'")
                                empty_fac=query.fetchone()
                                print(empty_fac[0],empty_tt[0])
                                if empty_fac[0]==None and empty_tt[0]==None:
                                    query.execute("update faculty_load set t1='"+sc+"' where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"'")
                                    query.execute("update time_table set t1='"+sc+"' where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                    le=le-1
                                    first_class=0
                                    flag=0
                                else:
                                    flag=flag-1
                                               
                        if first_class==0:
                            print(sc,'already exist')
                            flag=0
                            le=0
                        else:
                            flag=flag-1
        
        #first class assign end--------------
        
        #regular class assign start---------------
        
        for sub in subf_list:
            query.execute('SELECT faculty_name FROM faculty_subject where FIND_IN_SET("'+sub+'",subject_name) > 0  and department="'+b+'" and year="'+y+'" and 	academic_year="'+a+'" and FIND_IN_SET("'+sec+'",section) > 0 ')
            resultf=query.fetchall()
            fac.append(resultf[0][0])
            query.execute("select scode,is_lab from subject where sname='"+sub+"' and department='"+b+"' and year='"+y+"' and semester='"+s+"'")
            result=query.fetchone()
            subl.append(result[1])
            if result[1]==0:
                query.execute("select lectures from subject where sname='"+sub+"' and department='"+b+"' and year='"+y+"' and semester='"+s+"' and regulation='"+r+"'")
                lect=query.fetchone()
                le=lect[0]
                le1=le-1
                sc=result[0]
                flag=10
                
                class_assigned=0
                class_assigned_mon=0
                class_assigned_tue=0
                class_assigned_wed=0
                class_assigned_thu=0
                class_assigned_fri=0
                class_assigned_sat=0        
                while le1>0:
                    flag1=10
                    while flag1>0:
                        w=randint(0,5)
                        we=week[w]
                        query.execute("SELECT * FROM time_table WHERE '"+sc+"' IN(department,regulation,academic_year,year,semester,section,weekday,t1,t2,t3,t4,t5,t6,t7) and department='"+b+"' AND regulation='"+r+"' AND academic_year='"+a+"' AND year='"+y+"' AND semester='"+s+"' AND section='"+sec+"' AND weekday='"+we+"'")
                        count=query.fetchone()
                        if count==None  :
                            if we=='MON':
                                slot_t1 = slot_t2 = slot_t3 = slot_t4 = slot_t5 = slot_t6 = slot_t7 = 0
                                while class_assigned_mon<4:
                                    
                                    tym=randint(0, 3)
                                    time_slot=time[tym] 
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                    factt=query.fetchone()
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                    tt=query.fetchone()
                                    print(factt[0],tt[0],'HI MON')
                                    if factt[0]==None and tt[0]== None:
                                        query.execute("update time_table set "+time_slot+"='"+sc+"' where department='"+b+"' AND regulation='"+r+"' AND academic_year='"+a+"' AND year='"+y+"' AND semester='"+s+"' AND section='"+sec+"' AND weekday='"+we+"'")
                                        query.execute("update faculty_load set "+time_slot+"='"+sc+"' where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                        print(sc,'Assigned FN on',we,time_slot)
                                        le1-=1
                                        flag1=0
                                        break
                                    if tt[0]!=None :
                                        if time_slot=='t1' :
                                            slot_t1=1
                                            break
                                        if time_slot=='t2' :
                                            slot_t2=1
                                            break
                                        if time_slot=='t3' :
                                            slot_t3=1
                                            break
                                        if time_slot=='t4' :
                                            slot_t4=1
                                            break
                                    
                                    if slot_t1==1 and slot_t2==1 and slot_t3==1 and slot_t4==1:
                                        class_assigned_mon=4
                                        break
                                    else:
                                        flag1-=1
                                while class_assigned_mon>3 and class_assigned_mon<7:
                                    tym=randint(4,5)
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                    factt=query.fetchone()
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                    tt=query.fetchone()
                                    print(factt[0],tt[0],'HI MON')
                                    if factt[0]==None and tt[0]== None:
                                        query.execute("update time_table set "+time_slot+"='"+sc+"' where department='"+b+"' AND regulation='"+r+"' AND academic_year='"+a+"' AND year='"+y+"' AND semester='"+s+"' AND section='"+sec+"' AND weekday='"+we+"'")
                                        query.execute("update faculty_load set "+time_slot+"='"+sc+"' where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                        print(sc,'Assigned AN on',we,time_slot)
                                        le1-=1
                                        flag1=0
                                        break
                                    if tt[0]!= None :
                                        if time_slot=='t5' :
                                            slot_t5=1
                                            break
                                        if time_slot=='t6' :
                                            slot_t6=1
                                            break
                                    if slot_t5==1 and slot_t6==1:
                                        class_assigned_mon=8
                                        break
                                    else:
                                        flag1-=1
                            if we=='TUE':
                                slot_t1=slot_t2=slot_t3=slot_t4=slot_t5=slot_t6=slot_t7=0
                                while class_assigned_tue<4:
                                    
                                    tym=randint(0, 3)
                                    time_slot=time[tym] 
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                    factt=query.fetchone()
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                    tt=query.fetchone()
                                    print(factt[0],tt[0],'HI TUE')
                                    if factt[0]==None and tt[0]== None:
                                        query.execute("update time_table set "+time_slot+"='"+sc+"' where department='"+b+"' AND regulation='"+r+"' AND academic_year='"+a+"' AND year='"+y+"' AND semester='"+s+"' AND section='"+sec+"' AND weekday='"+we+"'")
                                        query.execute("update faculty_load set "+time_slot+"='"+sc+"' where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                        print(sc,'Assigned FN on',we,time_slot)
                                        le1-=1
                                        flag1=0
                                        break
                                    if tt[0]!= None :
                                        if time_slot=='t1' :
                                            slot_t1=1
                                            break
                                        if time_slot=='t2' :
                                            slot_t2=1
                                            break
                                        if time_slot=='t3' :
                                            slot_t3=1
                                            break
                                        if time_slot=='t4' :
                                            slot_t4=1
                                            break
                                    if slot_t1==1 and slot_t2==1 and slot_t3==1 and slot_t4==1:
                                        class_assigned_tue=4
                                        break
                                    else:
                                        flag1-=1
                                while class_assigned_tue>3 and class_assigned_tue<7:
                                    tym=randint(4,5)
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                    factt=query.fetchone()
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                    tt=query.fetchone()
                                    print(factt[0],tt[0],'HI TUE')
                                    if factt[0]==None and tt[0]== None:
                                        query.execute("update time_table set "+time_slot+"='"+sc+"' where department='"+b+"' AND regulation='"+r+"' AND academic_year='"+a+"' AND year='"+y+"' AND semester='"+s+"' AND section='"+sec+"' AND weekday='"+we+"'")
                                        query.execute("update faculty_load set "+time_slot+"='"+sc+"' where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                        print(sc,'Assigned AN on',we,time_slot)
                                        le1-=1
                                        flag1=0
                                        break
                                    if tt[0]!= None :
                                        if time_slot=='t5' :
                                            slot_t5=1
                                            break
                                        if time_slot=='t6' :
                                            slot_t6=1
                                            break
                                    if slot_t5==1 and slot_t6==1:
                                        class_assigned_tue=8
                                        break
                                    else:
                                        flag1-=1
                            if we=='WED':
                                slot_t1 = slot_t2 = slot_t3 = slot_t4 = slot_t5 = slot_t6 = slot_t7 = 0
                                while class_assigned_wed<4:
                                    
                                    tym=randint(0, 3)
                                    time_slot=time[tym] 
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                    factt=query.fetchone()
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                    tt=query.fetchone()
                                    print(factt[0],tt[0],'HI WED')
                                    if factt[0]==None and tt[0]== None:
                                        query.execute("update time_table set "+time_slot+"='"+sc+"' where department='"+b+"' AND regulation='"+r+"' AND academic_year='"+a+"' AND year='"+y+"' AND semester='"+s+"' AND section='"+sec+"' AND weekday='"+we+"'")
                                        query.execute("update faculty_load set "+time_slot+"='"+sc+"' where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                        print(sc,'Assigned FN on',we,time_slot)
                                        le1-=1
                                        flag1=0
                                        break
                                    if tt[0]!= None :
                                        if time_slot=='t1' :
                                            slot_t1=1
                                            break
                                        if time_slot=='t2' :
                                            slot_t2=1
                                            break
                                        if time_slot=='t3' :
                                            slot_t3=1
                                            break
                                        if time_slot=='t4' :
                                            slot_t4=1
                                            break
                                    if slot_t1==1 and slot_t2==1 and slot_t3==1 and slot_t4==1:
                                        class_assigned_wed=4
                                        break
                                    else:
                                        flag1-=1
                                while class_assigned_wed>3 and class_assigned_wed<7:
                                    tym=randint(4,5)
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                    factt=query.fetchone()
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                    tt=query.fetchone()
                                    print(factt[0],tt[0],'HI WED')
                                    if factt[0]==None and tt[0]== None:
                                        query.execute("update time_table set "+time_slot+"='"+sc+"' where department='"+b+"' AND regulation='"+r+"' AND academic_year='"+a+"' AND year='"+y+"' AND semester='"+s+"' AND section='"+sec+"' AND weekday='"+we+"'")
                                        query.execute("update faculty_load set "+time_slot+"='"+sc+"' where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                        print(sc,'Assigned AN on',we,time_slot)
                                        le1-=1
                                        flag1=0
                                        break
                                    if tt[0]!= None :
                                        if time_slot=='t5' :
                                            slot_t5=1
                                            break
                                        if time_slot=='t6' :
                                            slot_t6=1
                                            break
                                    if slot_t5==1 and slot_t6==1:
                                        class_assigned_wed=8
                                        break
                                    else:
                                        flag1-=1
                            if we=='THU':
                                slot_t1=slot_t2=slot_t3=slot_t4=slot_t5=slot_t6=slot_t7=0
                                while class_assigned_thu<4:
                                    
                                    tym=randint(0, 3)
                                    time_slot=time[tym] 
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                    factt=query.fetchone()
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                    tt=query.fetchone()
                                    print(factt[0],tt[0],'HI THU')
                                    if factt[0]==None and tt[0]== None:
                                        query.execute("update time_table set "+time_slot+"='"+sc+"' where department='"+b+"' AND regulation='"+r+"' AND academic_year='"+a+"' AND year='"+y+"' AND semester='"+s+"' AND section='"+sec+"' AND weekday='"+we+"'")
                                        query.execute("update faculty_load set "+time_slot+"='"+sc+"' where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                        print(sc,'Assigned FN on',we,time_slot)
                                        le1-=1
                                        flag1=0
                                        break
                                    if tt[0]!= None :
                                        if time_slot=='t1' :
                                            slot_t1=1
                                            break
                                        if time_slot=='t2' :
                                            slot_t2=1
                                            break
                                        if time_slot=='t3' :
                                            slot_t3=1
                                            break
                                        if time_slot=='t4' :
                                            slot_t4=1
                                            break
                                    if slot_t1==1 and slot_t2==1 and slot_t3==1 and slot_t4==1:
                                        class_assigned_thu=4
                                        break
                                    else:
                                        flag1-=1
                                while class_assigned_thu>3 and class_assigned_thu<7:
                                    tym=randint(4,5)
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                    factt=query.fetchone()
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                    tt=query.fetchone()
                                    print(factt[0],tt[0],'HI THU')
                                    if factt[0]==None and tt[0]== None:
                                        query.execute("update time_table set "+time_slot+"='"+sc+"' where department='"+b+"' AND regulation='"+r+"' AND academic_year='"+a+"' AND year='"+y+"' AND semester='"+s+"' AND section='"+sec+"' AND weekday='"+we+"'")
                                        query.execute("update faculty_load set "+time_slot+"='"+sc+"' where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                        print(sc,'Assigned AN on',we,time_slot)
                                        le1-=1
                                        flag1=0
                                        break
                                    if tt[0]!= None :
                                        if time_slot=='t5' :
                                            slot_t5=1
                                            break
                                        if time_slot=='t6' :
                                            slot_t6=1
                                            break
                                    if slot_t5==1 and slot_t6==1:
                                        class_assigned_thu=8
                                        break
                                    else:
                                        flag1-=1
                            if we=='FRI':
                                slot_t1=slot_t2=slot_t3=slot_t4=slot_t5=slot_t6=slot_t7=0
                                while class_assigned_fri<4:
                                    
                                    tym=randint(0, 3)
                                    time_slot=time[tym] 
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                    factt=query.fetchone()
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                    tt=query.fetchone()
                                    print(factt[0],tt[0],'HI FRI')
                                    if factt[0]==None and tt[0]== None:
                                        query.execute("update time_table set "+time_slot+"='"+sc+"' where department='"+b+"' AND regulation='"+r+"' AND academic_year='"+a+"' AND year='"+y+"' AND semester='"+s+"' AND section='"+sec+"' AND weekday='"+we+"'")
                                        query.execute("update faculty_load set "+time_slot+"='"+sc+"' where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                        print(sc,'Assigned FN on',we,time_slot)
                                        le1-=1
                                        flag1=0
                                        break
                                    if tt[0]!= None :
                                        if time_slot=='t1' :
                                            slot_t1=1
                                            break
                                        if time_slot=='t2' :
                                            slot_t2=1
                                            break
                                        if time_slot=='t3' :
                                            slot_t3=1
                                            break
                                        if time_slot=='t4' :
                                            slot_t4=1
                                            break
                                    if slot_t1==1 and slot_t2==1 and slot_t3==1 and slot_t4==1:
                                        class_assigned_fri=4
                                        break
                                    else:
                                        flag1-=1
                                while class_assigned_fri>3 and class_assigned_fri<7:
                                    tym=randint(4,5)
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                    factt=query.fetchone()
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                    tt=query.fetchone()
                                    print(factt[0],tt[0],'HI FRI')
                                    if factt[0]==None and tt[0]== None:
                                        query.execute("update time_table set "+time_slot+"='"+sc+"' where department='"+b+"' AND regulation='"+r+"' AND academic_year='"+a+"' AND year='"+y+"' AND semester='"+s+"' AND section='"+sec+"' AND weekday='"+we+"'")
                                        query.execute("update faculty_load set "+time_slot+"='"+sc+"' where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                        print(sc,'Assigned AN on',we,time_slot)
                                        le1-=1
                                        flag1=0
                                        break
                                    if tt[0]!= None :
                                        if time_slot=='t5' :
                                            slot_t5=1
                                            break
                                        if time_slot=='t6' :
                                            slot_t6=1
                                            break
                                    if slot_t5==1 and slot_t6==1:
                                        class_assigned_fri=8
                                        break
                                    else:
                                        flag1-=1
                            if we=='SAT':
                                slot_t1 = slot_t2 = slot_t3 = slot_t4 = slot_t5 = slot_t6 = slot_t7 = 0
                                while class_assigned_sat<4:
                                    
                                    tym=randint(0, 3)
                                    time_slot=time[tym] 
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                    factt=query.fetchone()
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                    tt=query.fetchone()
                                    print(factt[0],tt[0],'HI SAT')
                                    if factt[0]==None and tt[0]== None:
                                        query.execute("update time_table set "+time_slot+"='"+sc+"' where department='"+b+"' AND regulation='"+r+"' AND academic_year='"+a+"' AND year='"+y+"' AND semester='"+s+"' AND section='"+sec+"' AND weekday='"+we+"'")
                                        query.execute("update faculty_load set "+time_slot+"='"+sc+"' where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                        print(sc,'Assigned FN on',we,time_slot)
                                        le1-=1
                                        flag1=0
                                        break
                                    if tt[0]!= None :
                                        if time_slot=='t1' :
                                            slot_t1=1
                                            break
                                        if time_slot=='t2' :
                                            slot_t2=1
                                            break
                                        if time_slot=='t3' :
                                            slot_t3=1
                                            break
                                        if time_slot=='t4' :
                                            slot_t4=1
                                            break
                                    if slot_t1==1 and slot_t2==1 and slot_t3==1 and slot_t4==1:
                                        class_assigned_sat=4
                                        break
                                    else:
                                        flag1-=1
                                while class_assigned_sat>3 and class_assigned_sat<7:
                                    tym=randint(4,5)
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from faculty_load where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                    factt=query.fetchone()
                                    query.execute("select FIND_IN_SET('"+sc+"',"+time_slot+")>0 from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"' and weekday='"+we+"'")
                                    tt=query.fetchone()
                                    print(factt[0],tt[0],'HI SAT')
                                    if factt[0]==None and tt[0]== None:
                                        query.execute("update time_table set "+time_slot+"='"+sc+"' where department='"+b+"' AND regulation='"+r+"' AND academic_year='"+a+"' AND year='"+y+"' AND semester='"+s+"' AND section='"+sec+"' AND weekday='"+we+"'")
                                        query.execute("update faculty_load set "+time_slot+"='"+sc+"' where faculty_name='"+resultf[0][0]+"' and department='"+b+"' and weekday='"+we+"' ")
                                        print(sc,'Assigned AN on',we,time_slot)
                                        le1-=1
                                        flag1=0
                                        break
                                    if tt[0]!= None :
                                        if time_slot=='t5' :
                                            slot_t5=1
                                            break
                                        if time_slot=='t6' :
                                            slot_t6=1
                                            break
                                    if slot_t5==1 and slot_t6==1:
                                        class_assigned_sat=8
                                        break
                                    else:
                                        flag1-=1
                            
                            else:
                                flag1-=1
                                break
                        else:
                            print(sc,' subject already exist')
                            flag1=0
        
        # regular class assign end-----------------
        conn.commit()           
        return render(request,'sub_dis.html',{"s":subf_list,"b":branch,"r":reg,"y":year,"a":academic,"sec":sec,"sem":sem})
    else:
        return HttpResponse("<p>fail</p>")

def view_gen_tt(request):
    conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'root1234',
        database = 'timetable'
    )
    query = conn.cursor()
    b=request.POST['branch']
    branch=[]
    branch.append(b)
    y=request.POST['year']
    year=[]
    year.append(y)
    s=request.POST['sem']
    sem=[]
    sem.append(s)
    r=request.POST['regulation']
    a=request.POST['ay']
    sec=request.POST['sec']
    section=[]
    section.append(sec)
    timetable=[]
    query.execute("select * from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"'")
    result=query.fetchall()  
    for row in result:
        tt=Timetable()
        tt.tid=row[0]
        tt.dep=row[1]
        tt.reg=row[2]
        tt.ac=row[3]
        tt.year=row[4]
        tt.sem=row[5]
        tt.sec=row[6]
        tt.week=row[7]
        tt.t1=row[8]
        tt.t2=row[9]
        tt.t3=row[10]
        tt.t4=row[11]
        tt.t5=row[12]
        tt.t6=row[13]
        tt.t7=row[14]
        timetable.append(tt)
    return render(request, 'view_gen_tt.html',{"t":timetable,"b":branch,"y":year,"sec":sec,"sem":sem})
        
def view_tt(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        b=request.POST['branch']
        branch=[]
        branch.append(b)
        y=request.POST['year']
        year=[]
        year.append(y)
        s=request.POST['semester']
        sem=[]
        sem.append(s)
        r=request.POST['regulation']
        a=request.POST['ay']
        sec=request.POST['sec']
        section=[]
        section.append(sec)
        timetable=[]
        query.execute("select * from time_table where department='"+b+"' and regulation='"+r+"' and academic_year='"+a+"' and year='"+y+"' and semester='"+s+"' and section='"+sec+"'")
        result=query.fetchall()  
        for row in result:
            tt=Timetable()
            tt.tid=row[0]
            tt.dep=row[1]
            tt.reg=row[2]
            tt.ac=row[3]
            tt.year=row[4]
            tt.sem=row[5]
            tt.sec=row[6]
            tt.week=row[7]
            tt.t1=row[8]
            tt.t2=row[9]
            tt.t3=row[10]
            tt.t4=row[11]
            tt.t5=row[12]
            tt.t6=row[13]
            tt.t7=row[14]
            timetable.append(tt)
        return render(request, 'view.html',{"t":timetable,"b":branch,"y":year,"sec":sec,"sem":sem})
    
        
    elif "username" in request.session:
        uname = request.session['username']
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        
        query = conn.cursor() 
        query.execute("select * from department")
        result= query.fetchall()
        branch=[]
        for row in result:
            br=Branch()
            br.bid=row[0]
            br.bname=row[1]
            branch.append(br)  
        return render(request,'viewtt.html',{"branches":branch})#{ key:list}
    else:
        return render(request,'login.html')
 
      
def users_profile(request):
    return render(request,'users_profile.html')


def edit_admin_profile(request,aid):
    
    return render(request,'edit_admin_profile.html')#{ key:list}            
 
    

#admin funtions end

#-------------------------------------------------

#faculty funtion start    
def faculty_login(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        funame = request.POST['username']
        fpass = request.POST['pass']
        query.execute("select * from faculty where funame='"+funame+"' and fpass='"+fpass+"'")
        result=query.fetchone()
        if(result!=None):
            request.session["username"]=funame
            return render(request, 'view_fac.html', {"name" : funame})
        
            #redirect('dashboard')
        else:
            return render(request,'faculty_login.html',{'status':'invalid credentials'})    
    else:
        return render(request,'faculty_login.html')
    
def dashboard_f(request):
    return render(request,'dashboard_f.html')

def view_fac(request):
    if "username" in request.session:
        uname = request.session['username']
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor(buffered=True)
        query.execute("select fname,branch from faculty where funame='"+uname+"'")
        result=query.fetchone()
        print(result)
        query.execute("select * from faculty_load where faculty_name='"+result[0]+"' and department='"+result[1]+"'")
        resultt=query.fetchall()
        print(resultt)
        facultyload=[]
        name=[]
        name.append(result[0])
        for row in resultt:
            fl = Facultyload()
            fl.lid=row[0]
            fl.fname=row[1]
            fl.dep=row[2]
            fl.week=row[3]
            fl.t1=row[4]
            fl.t2=row[5]
            fl.t3=row[6]
            fl.t4=row[7]
            fl.t5=row[8]
            fl.t6=row[9]
            fl.t7=row[10]
            facultyload.append(fl)
        
        return render(request,'view_fac.html',{"fl":facultyload,"n":name})
    else:
        return render(request,'faculty_login.html') 

def faculty_reg(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        name=request.POST['fname'] 
        username=request.POST['funame']
        pwd = request.POST['fpass']
        contact=request.POST['contact']
        branch=request.POST['branch']
        subject=request.POST['subject']
        query.execute("insert into faculty(fname,funame,fpass,contact,subject,branch) values('"+name+"','"+username+"','"+pwd+"','"+contact +"','"+subject+"','"+branch+"')")
        conn.commit()
        return redirect(faculty_login)
    else:
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        query.execute("select * from department")
        result= query.fetchall()
        branch=[]
        for row in result:
            br=Branch(1,'Main Branch')
            br.bid=row[0]
            br.bname=row[1]
            branch.append(br)  
        return render(request,'faculty_reg.html',{"branches":branch})#{ key:list}
    
def forgotf(request):

    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234",
            database="timetable"
        )
        mycursor = conn.cursor()
        # retrive post details
        email = request.POST['username']

        mycursor.execute("select fpass from faculty where funame='"+email+"'")

        result = mycursor.fetchone()
        pwd=str(result)
        if (result != None):
            # SMTP server configuration
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_username = 'vishnutejakommera5@gmail.com'
# for App Password enable 2-step verification then u can create app password
            smtp_password = 'euhr qbmy eway tcqn'

# Email content
            subject = 'Password recovery'
            body = 'This is a Password recovery email sent from kits.'+'Your password as per registration is: '+ pwd[2:len(pwd)-3]
            sender_email = 'vishnutejakommera5@gmail.com'
            receiver_email = email

# Create a message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            
            return render(request, 'forgotf.html', {'status': 'Password sent to given mail ID'})
        else:
            return render(request, 'forgotf.html', {'status': 'Wrong Username!'})
    else:
        return render(request, 'forgotf.html')
    

def logoutf(request):
    try:
        del request.session['username']
        request.session.modified = True
        return render(request,'faculty_login.html') 
    except KeyError:
        return redirect('faculty_login')       
  
