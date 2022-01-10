from django.contrib.auth import login, logout, authenticate
from datetime import datetime
from django.views.generic import View
from .forms import *
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from .decorators import *
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
    }

    return render(request, 'home.html', context)


@login_required
def student_list(request):
    if request.user.is_student:
        students = Student.objects.filter(students_class=request.user.student.students_class) \
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
    subjects = Subject.objects.filter(teacher=teacher)
    classes = Class.objects.filter(supervising_teacher=teacher)
    grades = Grade.objects.filter(teacher=teacher)

    for subject in subjects:
        subject.delete()

    for grade in grades:
        grade.delete()

    for clas in classes:
        clas.delete()

    teacher.user.delete()
    teacher.delete()
    messages.success(request, "Successfully deleted")
    return redirect('teacher_list')


@login_required
@director_required()
def edit_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == "POST":
        form = TeacherAddForm(request.POST, instance=teacher)
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
            messages.success(request, "Successfully Updated")
            return redirect('teacher_list')
    else:
        form = TeacherAddForm(instance=teacher, initial={
            'username': teacher.user.username,
            'lastname': teacher.user.last_name,
            'firstname': teacher.user.first_name,
            'email': teacher.user.email,
            'address': teacher.user.address,
            'phone': teacher.user.phone,
        })
    return render(request, 'teachers/edit_teacher2.html', {'form': form})


class Person:
    def subjects(self): pass

    def subjects_monday(self): pass

    def subjects_tuesday(self): pass

    def subjects_wednesday(self): pass

    def subjects_thursday(self): pass

    def subjects_friday(self): pass

    def supervising(self): pass

    def full_name(self): pass

    def is_from_school(self): pass


# The Adapter
class Adapter(Person):
    __person = None

    def __init__(self, persona):
        self.__person = persona

    def subjects(self):
        if self.__person.is_teacher:
            return Subject.objects.filter(teacher=self.__person.teacher)
        elif self.__person.is_student:
            return Subject.objects.filter(branch=self.__person.student.students_class).filter(
                year=self.__person.student.year)
        else:
            return User.objects.filter(is_teacher=True)

    def subjects_monday(self):
        return self.subjects().filter(day="Monday").order_by("number")

    def subjects_tuesday(self):
        return self.subjects().filter(day="Tuesday").order_by("number")

    def subjects_wednesday(self):
        return self.subjects().filter(day="Wednesday").order_by("number")

    def subjects_thursday(self):
        return self.subjects().filter(day="Thursday").order_by("number")

    def subjects_friday(self):
        return self.subjects().filter(day="Friday").order_by("number")

    def supervising(self):
        if self.__person.is_student:
            return Class.objects.filter(branch=self.__person.student.students_class).filter(
                year=self.__person.student.year)
        else:
            return Class.objects.filter(supervising_teacher=self.__person.teacher)

    def full_name(self):
        full_name = self.__person.username
        if self.__person.first_name and self.__person.last_name:
            full_name = self.__person.first_name + " " + self.__person.last_name
        return full_name

    def is_from_school(self):
        return self.__person.is_teacher or self.__person.is_student


@login_required
def profile(request):
    person = Adapter(request.user)
    return render(request, 'profile/profile2.html', {'person': person})


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
    students = sorted(students_with_teacher_learns(request.user.teacher), key=lambda x: x.students_class, reverse=False)
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

            return render(request, "grades/create_grade_page2.html", context, )
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

        if request.user.is_superuser:
            grades = Grade.objects.all()
        else:
            grades = Grade.objects.filter(teacher=request.user.teacher)
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
            subjects = []
            for subject in grades:
                if subject.student == grade.student:
                    subjects.append(subject)

            bulk[grade.student.id] = {
                "student": grade.student,
                "subjects": subjects,
            }

        context = {"results": bulk}
        return render(request, "grades/grades_list.html", context)


class SubjectAddView(CreateView):
    model = Subject
    form_class = SubjectAddForm
    template_name = 'subjects/subject_add.html'

    def form_valid(self, form):
        form.save()
        return redirect('subject_list')


@login_required
def subject_list(request):
    subjects = sorted(Subject.objects.all(), key=lambda x: x.teacher.user.last_name, reverse=False)
    context = {
        'subjects': subjects,

    }
    return render(request, 'subjects/subject_list.html', context)


@login_required
@director_required
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()
    messages.success(request, "Successfully deleted")
    return redirect('subject_list')


@login_required
@director_required
def edit_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        form = SubjectAddForm(request.POST, instance=subject)
        if form.is_valid():
            subject.subjectCode = form.cleaned_data.get("subjectCode")
            subject.subjectName = form.cleaned_data.get("subjectName")
            subject.teacher = form.cleaned_data.get("teacher")
            subject.description = form.cleaned_data.get("description")
            subject.session = form.cleaned_data.get("session")
            subject.semester = form.cleaned_data.get("semester")
            subject.year = form.cleaned_data.get("year")
            subject.branch = form.cleaned_data.get("branch")
            subject.day = form.cleaned_data.get("day")
            subject.number = form.cleaned_data.get("number")
            subject.classroom = form.cleaned_data.get("classroom")
            subject.save()
            messages.success(request, "Successfully Updated")
            return redirect('subject_list')
    else:

        form = SubjectAddForm(instance=subject, initial={
            'subjectCode': subject.subjectCode,
            'subjectName': subject.subjectName,
            'teacher': subject.teacher,
            'description': subject.description,
            'session': subject.session,
            'semester': subject.semester,
            'year': subject.year,
            'branch': subject.branch,
            'day': subject.day,
            'number': subject.number,
            'classroom': subject.classroom

        })
    return render(request, 'subjects/subject_edit.html', {'form': form})


@login_required
@director_required
def session_add(request):
    if request.method == 'POST':
        form = SessionAddForm(request.POST)
        if form.is_valid():
            form.save()
            # comment
            new_session = Session.objects.filter(session=form.cleaned_data.get("session")).first()
            obs = ConcreteObserver(new_session)
            new_session.register(obs)
            new_session.count_observers()
            new_session.notify()
            # -----------------------------------------
            messages.success(request, 'Session added successfully ! ')
        return redirect("session_list")
    else:
        form = SessionAddForm()
    return render(request, 'sessions/session_add.html', {'form': form})


@login_required
@director_required
def session_list(request):
    sessions = Session.objects.all().order_by('-session')
    return render(request, 'sessions/session_list.html', {"sessions": sessions, })


@login_required
@director_required
def session_edit(request, pk):
    session = Session.objects.get(pk=pk)
    if request.method == 'POST':
        form = SessionAddForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            # comment -------------------------
            edited_session = Session.objects.filter(session=form.cleaned_data.get("session")).first()
            edited_session.count_observers()
            edited_session.notify()
            # -------------------------------------
            messages.success(request, 'Session updated successfully ! ')
        return redirect('session_list')
    else:
        form = SessionAddForm(instance=session, initial={
            'is_current_session': session.is_current_session,
            'session': session.session,
        })

    return render(request, 'sessions/session_edit.html', {'form': form})


@login_required
@director_required
def delete_session(request, pk):
    session = get_object_or_404(Session, pk=pk)
    session.delete()
    messages.success(request, "Successfully deleted")
    return redirect('session_list')
