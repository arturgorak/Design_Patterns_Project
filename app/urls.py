from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from .views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('', loginPage, name='login'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
    path('student_list/', student_list, name='student_list'),
    path('student_add/', StudentAddView.as_view(), name='student_add'),
    path('student_delete/<int:pk>/', delete_student, name="delete_student"),
    path('student_edit/<int:pk>/', edit_student, name="edit_student"),
    path('teacher_list/', teacher_list, name='teacher_list'),
    path('teacher_add/', TeacherAddView.as_view(), name='teacher_add'),
    path('teacher_delete/<int:pk>/', delete_teacher, name="delete_teacher"),
    path('teacher_edit/<int:pk>/', edit_teacher, name="edit_teacher"),
    path('profile/', profile, name='profile'),
    path("edit_profile", profile_update, name="edit_profile"),
    path("change_password", change_password, name="change_password"),
    path('add_grade/', create_grade, name="add_grade"),
    path('edit_grade/', edit_grades, name="edit_grades"),
    path("grades_list", GradeListView.as_view(), name="grades_list"),
    path("subject_add", SubjectAddView.as_view(), name="subject_add"),
    path("subject_list", subject_list, name="subject_list"),
    path("subject_delete/<int:pk>/", delete_subject, name="subject_delete"),
    path("subject_edit/<int:pk>/", edit_subject, name="subject_edit"),
    path('session_add', session_add, name="session_add"),
    path('session_list', session_list, name="session_list"),
    path("session_edit/<int:pk>/", session_edit, name="session_edit"),
    path("session_delete/<int:pk>/", delete_session, name="session_delete"),

]
