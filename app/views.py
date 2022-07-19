from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from .models import *
from django.contrib.auth import login,logout,authenticate
from datetime import datetime,timedelta,date
import numpy as np
import pytz,dateutil.parser
import cv2,Attendance as atd
 
# Create your views here.

def home(request):
	return render(request,'home.html')

def signup(request):
	if request.method=="POST":
		fn = request.POST['firstname']
		ln = request.POST['lastname']
		rl = request.POST['roll']
		userpic = request.FILES['userpic']
		fs=FileSystemStorage()
		filePathName=fs.save(rl+'.jpg',userpic)
		filePathName=fs.url(filePathName)

		print(fn,ln,rl)

	return render(request,'index.html',locals())


def Logout(request):
	logout(request)
	return redirect('home')

# Admin Page

def adminlogin(request):
	if request.method == "POST":
		e = request.POST['admmail']
		p = request.POST['admpass']
		user=authenticate(username=e,password=p)
		if user:
			login(request.user)
			error="no"
		else:
			error="yes"

	return render(request, 'adminlogin.html',locals())

def adminregister(request):
	if request.method == "POST":
		fn = request.POST['fname']
		ln = request.POST['lname']
		em = request.POST['email']
		brh = request.POST['branch']
		admpic = request.FILES['adminpic']
		pwd = request.POST['pass']
		user = User.objects.create_user(first_name=fn,last_name=ln,username=em,password=pwd)
		Admin.objects.create(user=user,branch=brh,admpic=admpic)
		error="no"
	return render(request,'adminregister.html',locals())

def adminhome(request):
	if not request.user.is_authenticated:
		return redirect('adminlogin')

	staff = Staff.objects.all()
	student = Students.objects.all()
	subject = Subjects.objects.all()
	print(len(student))

	return render(request, 'adminhome.html',locals())

def admprofile(request):
	if not request.user.is_authenticated:
		return redirect('adminlogin')
	user=request.user
	admin = Admin.objects.get(user=user)
	return render(request,'admprofile.html',locals())

def admin_studetails(request):
	if not request.user.is_authenticated:
		return redirect('adminlogin')

	user = request.user
	adm = Admin.objects.get(user=user)

	student = Students.objects.filter(branch=adm.branch)
	return render(request,'admin_studetails.html',locals())

def admin_deletestu (request,pid):
	student = Students.objects.get(id=pid)
	student.delete()
	return redirect("admin_studetails")

def admin_viewstudetails (request,pid):
	if not request.user.is_authenticated:
		return redirect('admin_login')

	student = Students.objects.get(id=pid)
	return render(request,'admin_viewstudetails.html',locals())

def staffdetails(request):
	if not request.user.is_authenticated:
		return redirect('adminlogin')

	user = request.user
	adm = Admin.objects.get(user=user)

	staff = Staff.objects.filter(branch=adm.branch)
	return render(request,'staffdetails.html',locals())

def admin_viewstaff (request,pid):
	if not request.user.is_authenticated:
		return redirect('admin_login')

	staff = Staff.objects.get(id=pid)
	return render(request,'admin_viewstaff.html',locals())

def deletestaff (request,pid):
	if not request.user.is_authenticated:
		return redirect('admin_login')

	staff = Staff.objects.get(id=pid)
	print(staff)
	# staff.delete()
	return redirect("staffdetails")


def admin_addstu(request):
	if not request.user.is_authenticated:
		return redirect('admin_login')

	user=request.user
	item = Subjects.objects.all()
	error = ""

	if request.method == "POST":
		fn = request.POST['fname']
		ln = request.POST['lname']
		rl = request.POST['roll']
		fthn = request.POST['fthname']
		brh = request.POST['branch']
		sem = request.POST['sem']
		cnt = request.POST['contact']
		dob = request.POST['dob']
		gdr = request.POST['gender']
		fr = request.POST['feereceipt']
		rp = request.FILES['receiptpic']
		stupic = request.FILES['stupic']
		stupwd = request.POST['stupass']
		about = request.POST['about']
		sub = request.POST.getlist('subitem[]')
		print(sub)

		try:
			user = User.objects.create_user(first_name=fn,last_name=ln,username=rl,password=stupwd)
			student = Students.objects.create(user=user,fathername=fthn,branch=brh,semester=sem,contact=cnt,birthdate=dob,gender=gdr,feereceipt=fr,receiptpic=rp,userpic=stupic,about=about)

			for item in sub:
				subject=Subjects.objects.get(subject_id=item)
				Stumapping.objects.create(stu_id=student, subject_id=subject)
			error="no"
		except:
			error="Yes"
	return render(request,'admin_addstu.html',{'items':item,'error':error})



def admin_addstaff (request):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	user=request.user
	item = Subjects.objects.all()
	error = ""

	if request.method == "POST":
		fn = request.POST['fname']
		ln = request.POST['lname']
		em = request.POST['email']
		contact = request.POST['contact']
		post = request.POST['post']
		brh = request.POST['branch']
		staffpic = request.FILES['staffpic']
		sub = request.POST.getlist('subitem[]')
		sem = request.POST.getlist('sem[]')
		print(sub)
		print(sem)

		pwd = request.POST['pass']

		try:
			user = User.objects.create_user(first_name=fn,last_name=ln,username=em,password=pwd)
			staff = Staff.objects.create(user=user,contact=contact,userpic=staffpic,post=post,branch=brh)
			temp = len(sub)
			for i in range(temp):
				subject=Subjects.objects.get(subject_id=sub[i])
				Staffmapping.objects.create(staff_id=staff, subject_id=subject, sem = sem[i] )
				error="no"
		except:
			error="Yes"
	return render(request,'admin_addstaff.html',{'items':item,'error':error})









# def staff_deletestu (request,pid):
# 	student = Students.objects.get(id=pid)
# 	student.delete()
# 	return redirect("staff_studetails")

# def view_studetails (request,pid):
# 	if not request.user.is_authenticated:
# 		return redirect('admin_login')

# 	student = Students.objects.get(id=pid)
# 	return render(request,'view_studetails.html',locals())











# Staff Page

def stafflogin(request):
	if request.method == "POST":
		e = request.POST['staffmail']
		p = request.POST['staffpass']
		user=authenticate(username=e,password=p)
		if user:
			login(request,user)
			error="no"
		else:
			error="yes"
	return render(request,'stafflogin.html',locals())

def staffregister(request):
	user=request.user
	item = Subjects.objects.all()
	error = ""

	if request.method == "POST":
		fn = request.POST['fname']
		ln = request.POST['lname']
		em = request.POST['email']
		contact = request.POST['contact']
		post = request.POST['post']
		brh = request.POST['branch']
		staffpic = request.FILES['staffpic']
		sub = request.POST.getlist('subitem[]')
		sem = request.POST.getlist('sem[]')
		print(sub)
		print(sem)

		pwd = request.POST['pass']

		try:
			user = User.objects.create_user(first_name=fn,last_name=ln,username=em,password=pwd)
			staff = Staff.objects.create(user=user,contact=contact,userpic=staffpic,post=post,branch=brh)
			temp = len(sub)
			for i in range(temp):
				subject=Subjects.objects.get(subject_id=sub[i])
				Staffmapping.objects.create(staff_id=staff, subject_id=subject, sem = sem[i] )
				error="no"
		except:
			error="Yes"
	return render(request,'staffregister.html',{'items':item,'error':error})

def staffhome(request):
	if not request.user.is_authenticated:
		return redirect('stafflogin')
	return render(request, 'staffhome.html')

def staffprofile(request):
	if not request.user.is_authenticated:
		return redirect('stafflogin')

	user=request.user
	staff = Staff.objects.get(user=user)
	return render(request,'staffprofile.html',locals())

def classes(request):
	if not request.user.is_authenticated:
		return redirect('stafflogin')
	user=request.user 
	staff = Staff.objects.get(user=user)
	mapp = Staffmapping.objects.filter(staff_id=staff)
	return render(request, 'classes.html',locals())

def staff_studetails(request):
	if not request.user.is_authenticated:
		return redirect('stafflogin')

	user = request.user
	stf = Staff.objects.get(user=user)

	staffmapping = Staffmapping.objects.filter(staff_id=stf)
	print(len(staffmapping))
	sm = []
	student = []
	for i in staffmapping:
		sm.append(i.sem)
	sm=np.unique(sm)
	for i in sm:
		student.append(Students.objects.filter(semester=i))
	return render(request,'staff_studetails.html',locals())

def staff_addstu(request):
	if not request.user.is_authenticated:
		return redirect('stafflogin')

	user=request.user
	item = Subjects.objects.all()
	error = ""

	if request.method == "POST":
		fn = request.POST['fname']
		ln = request.POST['lname']
		rl = request.POST['roll']
		fthn = request.POST['fthname']
		brh = request.POST['branch']
		sem = request.POST['sem']
		cnt = request.POST['contact']
		dob = request.POST['dob']
		gdr = request.POST['gender']
		fr = request.POST['feereceipt']
		rp = request.FILES['receiptpic']
		stupic = request.FILES['stupic']
		stupwd = request.POST['stupass']
		about = request.POST['about']
		sub = request.POST.getlist('subitem[]')
		print(sub)

		try:
			user = User.objects.create_user(first_name=fn,last_name=ln,username=rl,password=stupwd)
			student = Students.objects.create(user=user,fathername=fthn,branch=brh,semester=sem,contact=cnt,birthdate=dob,gender=gdr,feereceipt=fr,receiptpic=rp,userpic=stupic,about=about)

			for item in sub:
				subject=Subjects.objects.get(subject_id=item)
				Stumapping.objects.create(stu_id=student, subject_id=subject)
			error="no"
		except:
			error="Yes"
	return render(request,'staff_addstu.html',{'items':item,'error':error})

def staff_deletestu (request,pid):
	student = Students.objects.get(id=pid)
	student.delete()
	return redirect("staff_studetails")

def view_studetails (request,pid):
	if not request.user.is_authenticated:
		return redirect('admin_login')

	student = Students.objects.get(id=pid)
	return render(request,'view_studetails.html',locals())

def staff_viewattendance(request,pid):
	if not request.user.is_authenticated:
		return redirect('studentlogin')
	attendance = []
	subid = Subjects.objects.get(subjects=pid)
	mapp = Stumapping.objects.filter(subject_id=subid)
	for item in mapp:
		attendance.append(Attendance.objects.filter(stu_map=item))
	return render(request,'staff_viewattendance.html',locals())

def staff_startattendance(request,pid):
	if not request.user.is_authenticated:
		return redirect('studentlogin')
	n = 5
	final_time = datetime.now() + timedelta(minutes=n)
	subid = Subjects.objects.get(subjects=pid)
	try:
		port = Portal.objects.get(subject_id=subid)
		port.starttime=datetime.now()
		port.endtime=final_time
		port.save()
		print('portal opened........... ONE')

	except Portal.DoesNotExist:
		Portal.objects.create(starttime=datetime.now(),endtime=final_time,subject_id=subid)
		print('portal opened........... TWO')

	return redirect('classes')









# Student Page

def studentlogin(request):
	if request.method == "POST":
		r = request.POST['roll']
		p = request.POST['pass']
		user=authenticate(username=r,password=p)
		if user:
			login(request,user)
			error="no"
		else:
			error="yes"
	return render(request, 'studentlogin.html',locals())
def sturegister(request):
	user=request.user
	item = Subjects.objects.all()
	error = ""

	if request.method == "POST":
		fn = request.POST['fname']
		ln = request.POST['lname']
		rl = request.POST['roll']
		fthn = request.POST['fthname']
		brh = request.POST['branch']
		sem = request.POST['sem']
		cnt = request.POST['contact']
		dob = request.POST['dob']
		gdr = request.POST['gender']
		fr = request.POST['feereceipt']
		rp = request.FILES['receiptpic']
		stupic = request.FILES['stupic']
		stupwd = request.POST['stupass']
		about = request.POST['about']
		sub = request.POST.getlist('subitem[]')

		if(len(sub)<4):
			error = "lesssub"

			print(sub)
		else:
			try:
				user = User.objects.create_user(first_name=fn,last_name=ln,username=rl,password=stupwd)
				student = Students.objects.create(user=user,fathername=fthn,branch=brh,semester=sem,contact=cnt,birthdate=dob,gender=gdr,feereceipt=fr,receiptpic=rp,userpic=stupic,about=about)

				for item in sub:
					subject=Subjects.objects.get(subject_id=item)
					Stumapping.objects.create(stu_id=student, subject_id=subject)
				error="no"
			except:
				error="Yes"
	return render(request,'sturegister.html',{'items':item,'error':error})


def stuhome(request):
	if not request.user.is_authenticated:
		return redirect('studentlogin')
	user=request.user 
	student = Students.objects.get(user=user)
	mapp = Stumapping.objects.filter(stu_id=student)
	return render(request,'stuhome.html',locals())

def stuprofile(request):
	if not request.user.is_authenticated:
		return redirect('studentlogin')
	user=request.user
	student = Students.objects.get(user=user)
	return render(request,'stuprofile.html',locals())

def stu_markattendance(request,pid):
	if not request.user.is_authenticated:
		return redirect('studentlogin')
	subid = Subjects.objects.get(subjects=pid)
	user=request.user
	student = Students.objects.get(user=user)


	try:
		mapp = Stumapping.objects.filter(subject_id=subid)
		port = Portal.objects.get(subject_id=subid)
		image = str(student.userpic.url)
		utc = pytz.UTC
		now = datetime.now()
		# now = now.replace(tzinfo=utc)
		endtime = port.endtime
		starttime = port.starttime

		for item in mapp:
			if item.stu_id == student:
				if endtime>=now>=starttime:
					if atd.markscan(image[1:]):
						Attendance.objects.create(stu_map=item,date=datetime.now())
					
						print('Attendance Marked...........')
					else:
						
						print('face not detected!!!!')
					break
				else:
				
					print('portal closed...')
					break
			
	except:
		print('something went wrong...')
	return redirect('stuhome')

# def stu_markattendance(request,pid):
# 	if not request.user.is_authenticated:
# 		return redirect('studentlogin')
# 	subid = Subjects.objects.get(subjects=pid)
# 	user=request.user
# 	student = Students.objects.get(user=user)
# 	image = str(student.userpic.url)
# 	temp = atd.markscan(image[1:])
# 	print(temp)
# 	return redirect('stuhome')


def stu_viewattendance(request,pid):
	if not request.user.is_authenticated:
		return redirect('studentlogin')
	subid = Subjects.objects.get(subjects=pid)
	mapp = Stumapping.objects.filter(subject_id=subid)
	user=request.user
	student = Students.objects.get(user=user)
	for item in mapp:
		if item.stu_id == student:
			attendance = Attendance.objects.filter(stu_map=item)
			break
	return render(request,'stu_viewattendance.html',locals())

