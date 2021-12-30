
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
    path('add_grade/', create_grade, name="add_grade"),
    path('edit_grade/', edit_grades, name="edit_grades"),
    path("grades_list", GradeListView.as_view(), name="grades_list"),

]