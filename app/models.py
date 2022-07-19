from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#user
	# username
	# firstname
	# lastname
	# email

class Students (models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	fathername = models.CharField(max_length=30,null=True)
	branch = models.CharField(max_length=15,null=True)
	semester = models.CharField(max_length=1,null=True)
	contact = models.CharField(max_length=15,null=True)
	birthdate = models.DateField(null=True)
	gender = models.CharField(max_length=15,null=True)
	feereceipt = models.CharField(max_length=15,null=True)
	receiptpic = models.FileField(null=True)
	userpic = models.FileField(null=True)
	about = models.CharField(max_length=300,null=True)
	regdate = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.user.username


class Staff (models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	contact = models.CharField(max_length=15,null=True)
	post = models.CharField(max_length=15,null=True)
	branch = models.CharField(max_length=15,null=True)
	student = models.ForeignKey(Students,null=True,on_delete=models.CASCADE)
	userpic = models.FileField(null=True)
	def __str__(self):
		return self.user.username

class Admin (models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	student = models.ForeignKey(Students,null=True,on_delete=models.CASCADE)
	staff = models.ForeignKey(Staff,null=True,on_delete=models.CASCADE)
	branch = models.CharField(max_length=15,null=True)
	admpic = models.FileField(null=True)
	def __str__(self):
		return self.user.username

class Subjects (models.Model):
	subject_id = models.AutoField(primary_key=True)
	subjects = models.CharField(max_length=100,null=True)


class Stumapping (models.Model):
	stu_id = models.ForeignKey(Students,null=True,on_delete=models.CASCADE)
	subject_id = models.ForeignKey(Subjects,null=True,on_delete=models.CASCADE)

class Staffmapping (models.Model):
	staff_id = models.ForeignKey(Staff,null=True,on_delete=models.CASCADE)
	subject_id = models.ForeignKey(Subjects,null=True,on_delete=models.CASCADE)
	sem = models.IntegerField()

class Attendance (models.Model):
	stu_map = models.ForeignKey(Stumapping,null=True,on_delete=models.CASCADE)
	date = models.DateTimeField()

class Portal (models.Model):
	starttime = models.DateTimeField()
	endtime = models.DateTimeField()
	subject_id = models.ForeignKey(Subjects,null=True,on_delete=models.CASCADE)

			

	