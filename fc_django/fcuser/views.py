from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
from .models import Fcuser, Physician
from product.models import Diagnosis_0, Diagnosis_1, Diagnosis_2
import pandas as pd
import os
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.core.validators import validate_email, ValidationError

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.

def index(request):
    return render(request, 'index.html', {'email': request.session.get('user')})


class RegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = "/"

    def form_valid(self, form):
        fcuser = Fcuser(
            username=form.data.get('username'),
            email=form.data.get('email'),
            password=form.data.get('password'),
            level='user'
        )
        fcuser.save()

        return super().form_valid(form)


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        self.request.session['user'] = form.data.get('email')
        return super().form_valid(form)


def logout(request):
    if 'user' in request.session:
        del (request.session['user'])

    return redirect('/')


class BaseView(View):
    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data': data,
            'message': message,
        }
        print(result)
        return JsonResponse(result, status=status)


class DrCreateView(BaseView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DrCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        print("dr")
        dr_name = request.POST.get('dr_name', '')
        if not dr_name:
            return self.response(message="성명이 없네요", status=400)
        print("dr_name is", dr_name)
        print("email")
        email = request.POST.get('email', '')
        print("email is", email)
        if not email:
            return self.response(message="이메일이 없네요", status=400)
        try:
            validate_email(email)
        except ValidationError:
            return self.response(message="올바른 이메일 형식이 아닙니다", status=400)
        print("comment")
        # comment1 = request.POST.get('comment', '')
        # if not comment1:
        #     return self.response(message="커멘트가 없네요", status=400)

        try:
            physician = Physician(dr_name=dr_name, email=email)
            physician.save()
        except IntegrityError:
            return self.response(message="이미존재하는 아이디입니다", status=400)
        print("dr3")

        return self.response({'physician.id': physician.id})
