from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from .validators import ASCIIUsernameValidator


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_director = models.BooleanField(default=False)
    phone = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    username_validator = ASCIIUsernameValidator()

    def get_full_name(self):
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = self.last_name + " " + self.first_name
        return full_name


class Session(models.Model):  # academic year
    session = models.CharField(max_length=200, unique=True)
    is_current_session = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.session


FIRST = "First"
SECOND = "Second"

SEMESTER = (
    (FIRST, "First"),
    (SECOND, "Second"),
)


YEAR = (
    ("1", 1),
    ("2", 2),
    ("3", 3),
)

a = "a"
b = "b"
c = "c"
d = "d"

BRANCH = (
    (a, "a"),
    (b, "b"),
    (c, "c"),
    (d, "d"),
)

SUBJECTS = (
    ("biology", "biology"),
    ("civics", "civics"),
    ("chemistry", "chemistry"),
    ("English", "English"),
    ("geography", "geography"),
    ("German", "German"),
    ("mathematics", "mathematics"),
    ("physical education", "physical education"),
    ("physics", "physics"),
    ("Polish", "Polish"),
    ("Spanish", "Spanish")
)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Class(models.Model):
    year = models.CharField(choices=YEAR, max_length=1, blank=True)
    branch = models.CharField(choices=BRANCH, max_length=1, blank=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True)
    supervising_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Classes'


DAY = (
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday")
)

NUMBER = (
    ("0", 0),
    ("1", 1),
    ("2", 2),
    ("3", 3),
    ("4", 4),
    ("5", 5),
    ("6", 6),
    ("7", 7),
    ("8", 8),
    ("9", 9),
)


class Subject(models.Model):
    subjectName = models.CharField(choices=SUBJECTS, max_length=200)
    subjectCode = models.CharField(max_length=200, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    classroom = models.IntegerField(unique=False, null=True)
    description = models.TextField(max_length=200, blank=True)
    day = models.CharField(choices=DAY, max_length=200)
    number = models.CharField(choices=NUMBER, max_length=200)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True)
    semester = models.CharField(choices=SEMESTER, max_length=200)
    branch = models.CharField(choices=BRANCH, max_length=1, blank=True, null=True)
    year = models.CharField(choices=YEAR, max_length=1, blank=True, null=True)

    def __str__(self):
        return self.subjectCode + " (" + self.subjectName + ")"

    def get_absolute_url(self):
        return reverse('subject_list', kwargs={'pk': self.pk})


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=20, unique=True)
    students_class = models.CharField(choices=BRANCH, max_length=1, blank=True, null=True)
    year = models.CharField(choices=YEAR, max_length=1, blank=True, null=True)

    def __str__(self):
        return self.id_number

    def get_absolute_url(self):
        return reverse('profile')


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance


class Director(models.Model, Singleton):
    user = models.OneToOneField(Teacher, on_delete=models.CASCADE)


PASS = "PASS"
FAIL = "FAIL"

COMMENT = (
    (PASS, "PASS"),
    (FAIL, "FAIL"),
)

GRADE = (
    ("1", 1),
    ("2", 2),
    ("3", 3),
    ("4", 4),
    ("5", 5),
    ("6", 6),
)

WEIGHT = (
    ("1", 1),
    ("2", 2),
    ("3", 3),
)


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    date = models.DateField(blank=True, null=True)
    grade = models.CharField(choices=GRADE, max_length=1, blank=True)
    weight = models.CharField(choices=WEIGHT, max_length=1, blank=True)
    comment = models.CharField(max_length=200, blank=True)

