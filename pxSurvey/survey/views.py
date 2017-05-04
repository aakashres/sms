from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.shortcuts import render, redirect
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import random
import string

from .models import *
from .forms import *

from fobi.models import *


class AdminLogInView(View):
    def get(self, request):
        form = LogInForm()
        context = {
            'form': form,
        }
        return render(request, 'survey/adminLogIn.html', context)

    def post(self, request):
        form = LogInForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                messages.success(request, "Logged In Successfully")
                login(request, user)
                return redirect('survey:dashboard')
        messages.warning(request, "Log In Failure")
        context = {
            'form': form,
        }
        return render(request, 'survey/adminLogIn.html', context)


class AdminLogOutView(View):

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            logout(request)
        messages.success(request, "Logged Out Successfully")
        return redirect('survey:adminLogIn')


class DashboardView(TemplateView):
    template_name = 'survey/dashboard.html'


class StaffCreateView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'survey/staffCreate.html'
    form_class = StaffForm
    success_url = reverse_lazy("survey:dashboard")
    success_message = "Staff Successfully Added"

    def post(self, request, *args, **kwargs):
        form = StaffForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation)
                                for n in range(18)])
            user.set_password(password)
            user.save()
            grp = Group.objects.get(name='Staff')
            grp.user_set.add(user)
        return HttpResponseRedirect(self.success_url)


class StaffEmailChangeView(SuccessMessageMixin, FormView):
    template_name = 'survey/staffEmailChange.html'
    form_class = EmailForm
    success_url = reverse_lazy("survey:staffList")
    success_message = "Email Successfully Changed"

    def dispatch(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=kwargs['pk'])
        return super(StaffEmailChangeView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form, **kwargs):
        email = form.cleaned_data.get('email')
        self.user.email = email
        self.user.save()
        return super(StaffEmailChangeView, self).form_valid(form, **kwargs)


class StaffToggleGroupView(View):
    def get(self, request, **kwargs):
        pk = kwargs['pk']
        user = User.objects.get(pk=pk)
        if user.groups.all().first().name == 'Staff':
            grp = Group.objects.get(name='Staff')
            grp.user_set.remove(user)
            grp = Group.objects.get(name='Admin')
            grp.user_set.add(user)
        else:
            grp = Group.objects.get(name='Admin')
            grp.user_set.remove(user)
            grp = Group.objects.get(name='Staff')
            grp.user_set.add(user)
        return redirect(reverse_lazy("survey:staffList"))


class StaffListView(ListView):
    model = User
    template_name = 'survey/staffList.html'
    context_object_name = 'staffs'


class FormEntryListView(ListView):
    model = FormEntry
    template_name = 'survey/formList.html'
    context_object_name = 'formEntries'
