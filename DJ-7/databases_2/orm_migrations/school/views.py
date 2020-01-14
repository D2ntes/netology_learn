from django.views.generic import ListView
from django.shortcuts import render

from .models import Student, Teacher


def students_list(request):
    template = 'school/students_list.html'
    ordering = 'group'
    student_list = Student.objects.all().prefetch_related('teacher').order_by(ordering)
    context = {'student_list': student_list}
    return render(request, template, context)