from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
import datetime
from django.views.generic import View
from .forms import *
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .decorators import *


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
    student.delete()
    return redirect('student_list')


@login_required
@director_required
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

    #


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
    teacher.delete()
    return redirect('teacher_list')


@login_required
@director_required()
def edit_teacher(request, pk):
    # teacher = get_object_or_404(Teacher, pk=pk)
    teacher = Teacher.objects.get(pk=pk)
    if request.method == "POST":
        form = TeacherAddForm(request.POST, instance=teacher)

        if not form.is_valid():
            print(form.errors)
        if form.is_valid():
            teacher.user.password1 = form.cleaned_data.get("password1")
            teacher.user.password2 = form.cleaned_data.get("password2")
            teacher.first_name = form.cleaned_data.get("firstname")
            teacher.user.last_name = form.cleaned_data.get("lastname")
            teacher.user.email = form.cleaned_data.get("email")
            teacher.user.address = form.cleaned_data.get("address")
            teacher.user.phone = form.cleaned_data.get("phone")
            teacher.save()
            messages.success(request, "Successfully Updated")
            return redirect('teacher_list')
    else:
        form = TeacherAddForm(instance=teacher)
    return render(request, 'teachers/add_teacher.html', {'form': form})


@login_required
def profile(request):
    if request.user.is_teacher:
        subjects = teachers_subject(request.user.teacher)
        return render(request, 'profile/profile.html', {"subjects": subjects, })
    elif request.user.is_student:
        student = Student.objects.get(user__pk=request.user.id)
        context = {
            'student': student,
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


def students_with_teacher_learns(teacher_tmp):
    students= Student.objects.all()
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
            form = GradeAddForm(request.user, request.POST)
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
                                date=datetime.date.today(),
                            ).first()
                            if not check:
                                grades.append(
                                    Grade(

                                        subject=subject,
                                        student=stu,
                                        teacher=request.user.teacher,
                                        date=datetime.date.today(),

                                    )
                                )

                Grade.objects.bulk_create(grades)

                return redirect("edit_grades")

        # after choosing students
        id_list = request.POST.getlist("students")
        if id_list:
            form = GradeAddForm(request.user)
            studentlist = ",".join(id_list)
            context = {"students": studentlist, "form": form, "count": len(id_list)}

            return render(request, "grades/create_grade_page2.html", context ,)
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