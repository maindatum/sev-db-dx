from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm, LoginForm
from .models import Fcuser
from product.models import Diagnosis_0, Diagnosis_1, Diagnosis_2
import pandas as pd
import os

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
            email=form.data.get('email'),
            password=make_password(form.data.get('password')),
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


def DbImport(request):
    tb_dxcoding_0 = pd.read_csv(os.path.join(BASE_DIR, "dxcoding_0ex.csv"), encoding="cp949")
    tb_dxcoding_1 = pd.read_csv(os.path.join(BASE_DIR, "dxcoding_1ex.csv"), encoding="cp949")
    tb_dxcoding_2 = pd.read_csv(os.path.join(BASE_DIR, "dxcoding_2ex.csv"), encoding="cp949")
    print(tb_dxcoding_0.columns)
    for dxcode in tb_dxcoding_0.itertuples():
        if not Diagnosis_0.objects.filter(dxcode_0=dxcode.dxcode_0):
            Diagnosis_0.objects.create(dxcode_0=dxcode.dxcode_0, dxname_0=dxcode.dxname_0)
    for dxcode in tb_dxcoding_1.itertuples():
        if not Diagnosis_1.objects.filter(dxcode_1=dxcode.dxcode_1):
            Diagnosis_1.objects.create(dxcode_0=Diagnosis_0.objects.get(dxcode_0=dxcode.dxcode_0),
                                       dxcode_1=dxcode.dxcode_1, dxname_1=dxcode.dxname_1)
    for dxcode in tb_dxcoding_2.itertuples():
        if not Diagnosis_2.objects.filter(dxcode_2=dxcode.dxcode_2):
            Diagnosis_2.objects.create(dxcode_1=Diagnosis_1.objects.get(dxcode_1=dxcode.dxcode_1),
                                       dxcode_2=dxcode.dxcode_2, dxname_2=dxcode.dxname_2)

    print(len(tb_dxcoding_0))
    print('dbimport!!')
    return redirect('/')
