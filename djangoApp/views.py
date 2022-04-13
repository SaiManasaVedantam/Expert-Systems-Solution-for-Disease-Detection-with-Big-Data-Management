from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import TemplateView,ListView

from djangoApp.models import *


class IndexView(ListView):
    template_name = "index.html"
    def get_queryset(self):
        result = Diseases_Symptoms.objects.all()
        result = result.distinct().order_by()
        return result