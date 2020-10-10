from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Profile

# Create your views here.


class ProfileDetailView(generic.DetailView):
    model = User
    template_name = "userprofile/userprofile.html"
    slug_field = 'username'
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        return context
