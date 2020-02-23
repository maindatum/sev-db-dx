from django import forms
from . import widgets
from .models import Order
from product.models import Product
from fcuser.models import Fcuser
from django.db import transaction


class RegisterForm(forms.Form):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    quantity = forms.IntegerField(
        error_messages={
            'required': '수량을 입력해주세요'
        },
        label = "수량"
    )
    product = forms.IntegerField(
        error_messages={
            'required': '상품설명을 입력해주세요'
        }, label="상품설명", widget=forms.HiddenInput
    )

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')
        fcuser = self.request.session.get('user')

        if not (quantity and product):
            self.add_error('quantity', '값이 없습니다')
            self.add_error('product', '값이 없습니다')

class CustomWidgetForm(forms.Form):

    working = forms.BooleanField(
        # required must be false, otherwise you will get error when the toggle is off
        # at least in chrome
        required=False,
        widget=widgets.ToggleWidget(
            options={
                'on': 'Yep',
                'off': 'Nope'
            }
        )
    )

    countries = [
        ('id', 'Indonesia'),
        ('sar', 'Saudi Arabia'),
        ('usa', 'United Stated')
    ]

    country = forms.ChoiceField(
        choices=countries,
        widget=widgets.Select2Widget
    )

    hobbies = [
        ('fishing', 'Fishing'),
        ('writing', 'Writing'),
        ('coding', 'Coding')
    ]

    hobby = forms.MultipleChoiceField(
        choices=hobbies,
        widget=widgets.Select2MultipleWidget(
            options={
                'placeholder': 'Your placeholder',
                'multiple': True,
                'maximum-selection-length': 1
            }
        )
    )





