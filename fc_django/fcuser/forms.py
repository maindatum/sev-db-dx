from django import forms
from django.contrib.auth.hashers import check_password, make_password
from .models import Fcuser, Physician
from .widgets import CounterTextInput, starWidget



class RegisterForm(forms.Form):
    username = forms.CharField(
        label='성명',
        error_messages={
            'required':'성명을 입력해주세요'
        }
    )
    email = forms.EmailField(
        error_messages={
            'required': '이메일을 입력해주세요'
        }
    )
    # password = forms.CharField(
    #     error_messages={
    #         'required': '비밀번호를 입력해주세요'
    #     },
    #     widget=forms.PasswordInput, label='비밀번호'
    # )
    #
    # re_password = forms.CharField(
    #     error_messages={
    #         'required': '비밀번호를 입력해주세요'
    #     },
    #     widget=forms.PasswordInput, label='비밀번호 확인'
    # )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        # password = cleaned_data.get('password')
        # re_password = cleaned_data.get('re_password')

        # if password and re_password:
        #     if password != re_password:
        #         self.add_error('password', '비밀번호가 서로 다릅니다')
        #         self.add_error('re_password', '비밀번호가 서로 다릅니다')


class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': '이메일을 입력해주세요'
        }
    )
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput, label='비밀번호'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                fcuser = Fcuser.objects.get(email=email)
            except Fcuser.DoesNotExist:
                self.add_error('email', '아이디가 없습니다')
                return

            if not check_password(password, fcuser.password):
                self.add_error('password', '비밀번호가 틀립니다')


class StudentForm(forms.ModelForm):
    class Meta:
        model = Physician
        fields = '__all__'
        widgets = {
            'grade': starWidget,
        }

class DrRegisterForm(forms.ModelForm):
    class Meta:
        model = Physician
        fields = ('dr_name','email', 'comment')
