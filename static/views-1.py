from django.shortcuts import render,redirect
from django.http import HttpResponse
import mysql.connector
from .models import Branch,Subject
import smtplib
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create your views here.
def index(request):
    return render(request,'registration.html')

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
            return render(request, 'dashboard.html', {"name" : uname})
        
            #redirect('dashboard')
        else:
            return render(request,'login.html',{'status':'invalid credentials'})    
    else:
        return render(request,'login.html')
    

def dashboard(request):
    if "username" in request.session:
        uname = request.session['username']
        return render(request,'dashboard.html',{'name':uname})
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
        
        return render(request,'managedep.html')
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
            br=Branch()
            br.bid=row[0]
            br.bname=row[1]
            branch.append(br)  
        return render(request,'managedep.html',{"branches":branch})#{ key:list}
        

def submanage(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        
        return render(request,'managesub.html',{'status':'invalid credentials'})
    else:
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        query.execute("select * from subjects")
        result= query.fetchall()
        subjects=[]
        for row in result:
            s=Subject()
            s.subid=row[0]
            s.subname=row[1]
            s.subcode=row[2]
            s.subncpw=row[3]
            s.subdep=row[4]
            s.subyear=row[5]
            s.subreg=row[6]
            subjects.append(s)  
        return render(request,'managesub.html',{"subject":subjects})#{ key:list}




    
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
        
def add_sub(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        sname=request.POST['sname']
        scode=request.POST['scode']
        ncpw=request.POST['ncpw']
        branch=request.POST['branch']
        year=request.POST['year']
        ar=request.POST['ar']
        query.execute("select * from subjects where sname='"+sname+"'")
        result= query.fetchone()
        if(result==None):
               
            query.execute("insert into subjects(sname,scode,ncpw,department,year,regulation) values('"+sname+"','"+scode+"','"+ncpw+"','"+branch+"','"+year+"','"+ar+"')")
            conn.commit()
            return render(request, 'add_sub.html',{'status': 'subject added successfully.'})
            
        else:
            return render(request, 'add_sub.html', {'status': 'subject already exists!'})
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
            br=Branch()
            br.bid=row[0]
            br.bname=row[1]
            branch.append(br)  
        return render(request,'add_sub.html',{"branches":branch})#{ key:list}


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

def del_sub(request,subid):
    conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'root1234',
        database = 'timetable'
    )
    query = conn.cursor()
    query.execute("DELETE FROM subjects where sid='"+subid+"'")
    conn.commit()
    return render(request, 'del_dep.html',{'status': 'subject deleted successfully.'})


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
        return render(request,'edit_dep.html')
    else:
        return render(request,'edit_dep.html',{'status': 'Department editing failed.'})    
        
               
def edit_sub(request,subid):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        subname = request.POST['sname']
        subcode = request.POST['scode']
        subncpw = request.POST['ncpw']
        subdep = request.POST['branch']
        subyear = request.POST['year']
        subreg = request.POST['ar']
        query.execute("update subjects set sname ='"+subname+"',scode ='"+subcode+"',ncpw ='"+subncpw+"',department ='"+subdep+"',year ='"+subyear+"',regulation ='"+subreg+"' where sid='"+subid+"'")
        conn.commit()
        return render(request, 'edit_sub.html',{'status': 'Subject edited successfully.'})
    
    
    else:
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        query.execute("select * from subjects")
        result= query.fetchall()
        subjects=[]
        for row in result:
            s=Subject()
            s.subid=row[0]
            s.subname=row[1]
            s.subcode=row[2]
            s.subncpw=row[3]
            s.subdep=row[4]
            s.subyear=row[5]
            s.subreg=row[6]
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
    
def logout(request):
    try:
        del request.session['username']
        request.session.modified = True
        return render(request,'login.html') 
    except KeyError:
        return redirect('login')       


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

        mycursor.execute("select password from admintable where username='"+email+"'")

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
            
            return render(request, 'forgot.html', {'status': 'Password sent to given mail ID'})
        else:
            return render(request, 'forgot.html', {'status': 'Wrong Username!'})
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
        query.execute("insert into admintable(username,password) values('"+username+"','"+pwd+"')")
        conn.commit()
        return redirect('login')
    else:
        return render(request,'admin_registration.html')#{ key:list}
        

#admin funtions end

#-------------------------------------------------

#faculty funtion start

def dashboardf():
    return render(request,'dashboard.html')

def loginf(request):
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
        query.execute("select * from faculty where funame='"+uname+"' and fpass='"+pwd+"'")
        result=query.fetchone()
        if(result!=None):
            request.session["username"]=uname
            return render(request, 'dashboardf.html', {"username" : uname})
            #redirect('dashboard')
        else:
            return render(request,'loginf.html',{'status':'invalid credentials'})    
    else:
        return render(request,'loginf.html')

def logoutf(request):
    try:
        del request.session['username']
        request.session.modified = True
        return render(request,'login.html') 
    except KeyError:
        return redirect('login')       



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
            
            return render(request, 'forgot.html', {'status': 'Password sent to given mail ID'})
        else:
            return render(request, 'forgot.html', {'status': 'Wrong Username!'})
    else:
        return render(request, 'forgot.html')



def register(request):
    if request.method=='POST':
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root1234',
            database = 'timetable'
        )
        query = conn.cursor()
        name=request.POST['fname'] 
        username=request.POST['uname']
        pwd=request.POST['pass']     
        branch=request.POST['branch']
        contact=request.POST['contact']
        subject=request.POST['subjects']
        query.execute("insert into faculty(fname,funame,fpass,contact,fsubject,branch) values('"+name+"','"+username+"','"+pwd+"','"+contact +"','"+subject+"','"+branch+"')")
        conn.commit()
        return redirect('loginf')
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
            br=Branch()
            br.bid=row[0]
            br.bname=row[1]
            branch.append(br)  
        return render(request,'registration.html',{"branches":branch})#{ key:list}
    
    
