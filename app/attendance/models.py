from django.db import models

class Department(models.Model):

    name = models.CharField(max_length=20)

    password = models.CharField(max_length=30)

    phone_no = models.IntegerField()

    email =  models.EmailField()

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    phone_no = models.IntegerField()
    email = models.EmailField()
    pic_location = models.FileField()

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    phone_no = models.IntegerField()
    email = models.EmailField()
    pic_location = models.FileField()

    def __str__(self):
        return self.name

class Class(models.Model):
    s = models.ForeignKey(Student,on_delete=models.PROTECT)
    t = models.ForeignKey(Teacher,on_delete=models.PROTECT)
    date = models.DateField()

class Offers(models.Model):
    d = models.ForeignKey(Department,on_delete=models.PROTECT)
    c = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return self.d.name + " offers " + self.c.name

class Teaches(models.Model):
    t = models.ForeignKey(Teacher,on_delete=models.PROTECT)
    c = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return self.t.name + " teaches " + self.c.name

class Enroll(models.Model):
    s = models.ForeignKey(Student,on_delete=models.PROTECT)
    c = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return self.s.name + " enrolls in " + self.c.name









