from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .forms import *
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.contrib import messages


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        context = {}
        return render(request, 'registration/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('/')


def home(request):
    """
    Shows our dashboard containing number of students, courses, lecturers, repating students,
    carry over students and 1st class students in an interactive graph

    """

    context = {
        # "no_of_students": students,
        # "no_of_staff": staff,
        # "no_of_courses": courses,
        # "no_of_1st_class_students": no_of_1st_class_students,
        # "no_of_students_to_repeat": no_of_students_to_repeat,
        # "no_of_carry_over_students": no_of_carry_over_students,
    }

    return render(request, 'home.html', context)


def student_list(request):
    students = Student.objects.all()
    context = {
        'students': students,

    }
    return render(request, 'students/student_list.html', context)


class StudentAddView(CreateView):
    model = User
    form_class = StudentAddForm
    template_name = 'students/add_student.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('student_list')


def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('student_list')


def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentAddForm(request.POST, instance=student)

        if form.is_valid():
            student.save()
            messages.success(request, "Successfully Updated")
            return redirect('student_list')
    else:

        form = StudentAddForm(instance=student)
    return render(request, 'students/edit_student.html', {'form': form})


def teacher_list(request):
    teachers = Teacher.objects.all()
    context = {
        'teachers': teachers,

    }
    return render(request, 'teachers/teacher_list.html', context)


class TeacherAddView(CreateView):
    model = User
    form_class = TeacherAddForm
    template_name = 'teachers/add_teacher.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('teacher_list')


def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.delete()
    return redirect('teacher_list')

def edit_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == "POST":
        form = StudentAddForm(request.POST, instance=teacher)

        if form.is_valid():
            teacher.save()
            messages.success(request, "Successfully Updated")
            return redirect('teacher_list')
    else:

        form = TeacherAddForm(instance=teacher)
    return render(request, 'teachers/edit_teacher.html', {'form': form})