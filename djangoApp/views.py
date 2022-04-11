from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import TemplateView,ListView

from djangoApp.models import Symptoms


class IndexView(ListView):
    template_name = "index.html"
    def get_queryset(self):
        result=Symptoms.objects.all()
        return result


        