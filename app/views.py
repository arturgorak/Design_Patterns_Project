from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from datetime import datetime
from django.views.generic import View
from .forms import *
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .decorators import *
from django.contrib.auth import update_session_auth_hash

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect


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


@login_required
def logoutPage(request):
    logout(request)
    return redirect('/')


@login_required
def home(request):

    context = {
        # "no_of_students": students,
        # "no_of_staff": staff,
        # "no_of_courses": courses,
        # "no_of_1st_class_students": no_of_1st_class_students,
        # "no_of_students_to_repeat": no_of_students_to_repeat,
        # "no_of_carry_over_students": no_of_carry_over_students,
    }

    return render(request, 'home.html', context)


@login_required
def student_list(request):
    if request.user.is_student:
        students = Student.objects.filter(students_class=request.user.student.students_class)\
            .filter(year=request.user.student.year)
    else:
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


@login_required
@director_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.user.delete()
    student.delete()
    messages.success(request, "Successfully deleted")
    return redirect('student_list')


@login_required
@director_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentAddForm(request.POST, instance=student)
        print(form.errors)
        if form.is_valid():
            student.user.password1 = form.cleaned_data.get("password1")
            student.user.password2 = form.cleaned_data.get("password2")
            student.year = form.cleaned_data.get("year")
            student.user.first_name = form.cleaned_data.get("firstname")
            student.user.username = form.cleaned_data.get("username")
            student.user.last_name = form.cleaned_data.get("lastname")
            student.students_class = form.cleaned_data.get("branch")
            student.user.email = form.cleaned_data.get("email")
            student.user.address = form.cleaned_data.get("address")
            student.user.phone = form.cleaned_data.get("phone")
            student.user.save()
            messages.success(request, "Successfully Updated")
            return redirect('student_list')
    else:

        form = StudentAddForm(instance=student, initial={
            'username': student.user.username,
            'lastname': student.user.last_name,
            'firstname': student.user.first_name,
            'email': student.user.email,
            'year': student.year,
            'branch': student.students_class,
            'password': student.user.password,
            'password2': student.user.password2,
            'password1':student.user.password1,
            'address': student.user.address,
            'phone': student.user.phone,
        })
    return render(request, 'students/edit_student2.html', {'form': form})


def teachers_subject(teacher):

    subjects = Subject.objects.all()
    sub_array = []
    for y in subjects:
        if teacher == y.teacher:
            sub_array.append(y)
    return sub_array


@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    subject_list = []

    for x in teachers:
        subject_list.append(teachers_subject(x))

    context = {
        'teachers': teachers,
        'subjects': subject_list

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


@login_required
@director_required()
def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.user.delete()
    teacher.delete()
    messages.success(request, "Successfully deleted")
    return redirect('teacher_list')


@login_required
@director_required()
def edit_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    #teacher = Teacher.objects.get(pk=pk)
    if request.method == "POST":
        form = TeacherAddForm(request.POST, instance=teacher)
        if not form.is_valid():
            print(form.errors)
        if form.is_valid():
            teacher.user.password1 = form.cleaned_data.get("password1")
            teacher.user.password2 = form.cleaned_data.get("password2")
            teacher.user.first_name = form.cleaned_data.get("firstname")
            teacher.user.username = form.cleaned_data.get("username")
            teacher.user.last_name = form.cleaned_data.get("lastname")
            teacher.user.email = form.cleaned_data.get("email")
            teacher.user.address = form.cleaned_data.get("address")
            teacher.user.phone = form.cleaned_data.get("phone")
            teacher.user.save()
            #teacher.save()
            messages.success(request, "Successfully Updated")
            return redirect('teacher_list')
    else:
        form = TeacherAddForm(instance=teacher)
    return render(request, 'teachers/edit_teacher2.html', {'form': form})


@login_required
def profile(request):
    if request.user.is_teacher:
        subjects = teachers_subject(request.user.teacher)
        teacher_class = Class.objects.filter(supervising_teacher=request.user.teacher)
        class_count = len(teacher_class)
        context = {
            'subjects': subjects,
            'class': teacher_class,
            'count': class_count
        }

        return render(request, 'profile/profile.html', context)
    elif request.user.is_student:
        student = Student.objects.get(user__pk=request.user.id)
        subjects = Subject.objects.filter(branch=request.user.student.students_class)\
            .filter(year=request.user.student.year)
        students_class = Class.objects.filter(branch=request.user.student.students_class)\
            .filter(year=request.user.student.year)
        context = {
            'student': student,
            'subjects': subjects,
            'class': students_class
        }
        return render(request, 'profile/profile.html', context)
    else:
        staff = User.objects.filter(is_teacher=True)
        return render(request, 'profile/profile.html', {"staff": staff})


@login_required
def profile_update(request):
    user = request.user.id
    user = User.objects.get(pk=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.phone = form.cleaned_data.get('phone')
            user.address = form.cleaned_data.get('address')
            user.save()
            messages.success(request, 'Your profile was successfully edited.')
            return redirect("/profile/")
    else:
        form = ProfileForm(instance=user, initial={
            'firstname': user.first_name,
            'lastname': user.last_name,
            'email': user.email,
            'phone': user.phone,

        })

    return render(request, 'profile/profile_update.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile/change_password.html', {
        'form': form
    })


def students_with_teacher_learns(teacher_tmp):
    students = Student.objects.all()
    subject_tmp = teachers_subject(teacher_tmp)
    sub_array = []
    for x in students:

        for y in subject_tmp:
            if x.year == y.year and x.students_class == y.branch:
                sub_array.append(x)
                break
    return sub_array


@login_required
@teacher_required()
def create_grade(request):
    students = sorted(students_with_teacher_learns(request.user.teacher), key=lambda x: x.user.last_name, reverse=False)
    if request.method == "POST":
        # second page
        if "finish" in request.POST:
            form = GradeAddForm(request.user, request.POST,
                                initial={
                                    'date': datetime.now
                                })
            if form.is_valid():
                subjects = form.cleaned_data["subject"]
                students = request.POST["students"]
                grades = []
                for student in students.split(","):
                    stu = Student.objects.get(pk=student)
                    if stu.students_class:
                        for subject in subjects:
                            check = Grade.objects.filter(
                                subject=subject,
                                student=stu,
                                teacher=request.user.teacher,

                            ).first()
                            if not check:
                                grades.append(
                                    Grade(

                                        subject=subject,
                                        student=stu,
                                        teacher=request.user.teacher,


                                    )
                                )

                Grade.objects.bulk_create(grades)
                messages.success(request, "Successfully Updated")
                return redirect("edit_grades")

        # after choosing students
        id_list = request.POST.getlist("students")
        if id_list:
            form = GradeAddForm(request.user)
            studentlist = ",".join(id_list)
            context = {"students": studentlist, "form": form, "count": len(id_list)}

            return render(request, "grades/create_grade_page2.html", context,)
        else:
            messages.warning(request, "You didnt select any student.")

    context = {
        "students": students,
        "teacher": request.user.teacher,
    }

    return render(request, "grades/create_grade.html", context)


@login_required
@teacher_required()
def edit_grades(request):

    if request.method == "POST":
        form = EditGrades(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Grades successfully updated")
            return redirect("edit_grades")
    else:

        if request.user.is_director or request.user.is_superuser:
            grades = Grade.objects.all()
        else:
            grades = Grade.objects.filter(student__grade__teacher=request.user.teacher)
        form = EditGrades(queryset=grades)

    return render(request, "grades/edit_grades.html", {"formset": form})


class GradeListView(View):
    def get(self, request, *args, **kwargs):
        grades = Grade.objects.all()

        if request.user.is_director or request.user.is_superuser:
            grades = Grade.objects.all()
        elif request.user.is_teacher:
            grades = Grade.objects.filter(teacher=request.user.teacher)
        elif request.user.is_student:
            grades = Grade.objects.filter(student=request.user.student)

        bulk = {}

        for grade in grades:
            test_total = 0
            exam_total = 0
            subjects = []
            for subject in grades:
                if subject.student == grade.student:
                    subjects.append(subject)

            bulk[grade.student.id] = {
                "student": grade.student,
                "subjects": subjects,
                "test_total": test_total,
                "exam_total": exam_total,
                "total_total": test_total + exam_total,
            }

        context = {"results": bulk}
        return render(request, "grades/grades_list.html", context)