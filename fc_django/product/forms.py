from django import forms
from .models import Product, Patient_info, Pt_diagnosis, Diagnosis_0, Diagnosis_1, Diagnosis_2
from fcuser.models import Fcuser, Physician

import simplejson
from django.http import HttpResponse


class RegisterForm(forms.Form):
    name = forms.CharField(
        error_messages={
            'required': '상품명을 입력해주세요'
        },
        max_length=64, label="상품명"
    )
    price = forms.IntegerField(
        error_messages={
            'required': '가격을 입력해주세요'
        }, label="상품가격"
    )
    description = forms.CharField(
        error_messages={
            'required': '상품상세설명을 입력해주세요'
        }, label="상품설명"
    )
    stock = forms.IntegerField(
        error_messages={
            'required': '재고를 입력해주세요'
        }, label="재고"
    )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        description = cleaned_data.get('description')
        stock = cleaned_data.get('stock')

        if not (name and price and description and stock):
            self.add_error('name', '값이 없습니다')
            self.add_error('price', '값이 없습니다')
            self.add_error('description', '값이 없습니다')
            self.add_error('stock', '값이 없습니다')


class DxRegisterForm(forms.Form):
    unitnumb = forms.CharField(
        error_messages={
            'required': '등록번호를 입력해주세요'
        },
        max_length=64, label="등록번호"
    )
    dxcode_0 = forms.ChoiceField(
        error_messages={
            'required': '진단명을 입력해주세요'
        }, label="진단명 대분류", widget=forms.Select
    )
    dxcode_1 = forms.ChoiceField(
        error_messages={
            'required': '진단명을 입력해주세요'
        }, label="진단명 중분류", widget=forms.Select
    )
    dxcode_2 = forms.ChoiceField(
        error_messages={
            'required': '진단명을 입력해주세요'
        }, label="진단명 소분류", widget=forms.Select
    )

    def clean(self):
        cleaned_data = super().clean()
        unitnumb = cleaned_data.get('unitnumb')
        dxcode_0 = cleaned_data.get('dxcode_0')
        dxcode_1 = cleaned_data.get('dxcode_1')
        dxcode_2 = cleaned_data.get('dxcode_2')

        if not (unitnumb and dxcode_0 and dxcode_1 and dxcode_2):
            self.add_error('unitnumb', '값이 없습니다')
            self.add_error('dxcode_0', '값이 없습니다')
            self.add_error('dxcode_1', '값이 없습니다')
            self.add_error('dxcode_2', '값이 없습니다')


class DxForm(forms.ModelForm):
    class Meta:
        model = Pt_diagnosis
        fields = ('unitnumb', 'dxcode_0', 'dxcode_1', 'dxcode_2', 'dxcode_3', 'regist_user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dxcode_0'].queryset = Diagnosis_0.objects.all()
        self.fields['dxcode_1'].queryset = Diagnosis_1.objects.none()
        self.fields['dxcode_2'].queryset = Diagnosis_2.objects.none()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class PtForm(forms.ModelForm):
    class Meta:
        model = Pt_diagnosis
        fields = ('dx_date', 'dxcode_0', 'dxcode_1', 'dxcode_2', 'dxcode_3', 'need_confirm', 'compl_confirm', 'dr_name',
                  'regist_user')

    # class Meta:
    #     model = Pt_diagnosis
    #     fields = (
    #         'unitnumb', 'dx_date', 'dxcode_0', 'dxcode_1', 'dxcode_2', 'dxcode_3', 'need_confirm', 'compl_confirm',
    #         'dr_name', 'regist_user')
    #     widgets = {
    #         'unitnumb': forms.TextInput(),
    #         'dx_date': forms.SelectDateWidget(),
    #         'dxcode_0': forms.Select()
    #     }
    #     labels = {
    #         'unitnumb' : '올랄라'
    #     }
    # unitnumb = forms.CharField(
    #     label='등록번호',
    #     error_messages={
    #         'required': '등록번호를 입력해주세요'
    #     }
    # )
    dx_date = forms.DateField(
        error_messages={
            'required': '진단일을 입력해주세요'
        },
        label='진단일',
        widget=forms.DateInput
    )

    dxcode_0 = forms.ModelChoiceField(
        queryset=Diagnosis_0.objects.all(),
        widget=forms.Select,
        error_messages={
            'required': '대분류를 입력해주세요'
        },
        label='대분류',
    )

    dxcode_1 = forms.ModelChoiceField(
        error_messages={
            'required': '중분류를 입력해주세요'
        },
        label='중분류',
        widget=forms.Select,
        queryset=Diagnosis_2.objects.none()
    )

    dxcode_2 = forms.ModelChoiceField(
        error_messages={
            'required': '소분류를 입력해주세요'
        },
        label='소분류',
        widget=forms.Select,
        queryset=Diagnosis_2.objects.none()
    )
    need_confirm = forms.BooleanField(
        label='컨펌필요여부',
        required=False,
        initial=False,
    )
    compl_confirm = forms.BooleanField(
        label='컨펌완료',
        required=False,
        initial=False,
    )
    dr_name = forms.ModelChoiceField(
        queryset=Physician.objects.all(),
        label='의사성명'
    )
    regist_user = forms.ModelChoiceField(
        queryset=Fcuser.objects.all(),
        label='등록자'
    )

    def clean(self):
        cleaned_data = super().clean()
        unitnumb = cleaned_data.get('unitnumb')
        dx_date = cleaned_data.get('dx_date')
        dxcode_0 = cleaned_data.get('dxcode_0')
        dxcode_1 = cleaned_data.get('dxcode_1')
        dxcode_2 = cleaned_data.get('dxcode_2')
        dxcode_3 = cleaned_data.get('dxcode_3')
        need_confirm = cleaned_data.get('need_confirm')
        compl_confirm = cleaned_data.get('compl_confirm')
        dr_name = cleaned_data.get('dr_name')
        regist_user = cleaned_data.get('regist_user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dxcode_1'].queryset = Diagnosis_1.objects.none()
        self.fields['dxcode_2'].queryset = Diagnosis_2.objects.none()

        if 'dxcode_0' in self.data:
            try:
                dxcode_0_id = int(self.data.get('dxcode_0'))
                self.fields['dxcode_1'].queryset = Diagnosis_1.objects.filter(dxcode_0_id=dxcode_0_id).order_by(
                    'dxname_1')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['dxcode_1'].queryset = self.instance.diagnosis_0.dxcode_1_set.order_by('dxname_1')

        if 'dxcode_1' in self.data:
            try:
                dxcode_1_id = int(self.data.get('dxcode_1'))
                self.fields['dxcode_2'].queryset = Diagnosis_2.objects.filter(dxcode_1_id=dxcode_1_id).order_by(
                    'dxname_2')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['dxcode_2'].queryset = self.instance.diagnosis_1.dxcode_2_set.order_by('dxname_2')

    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'
    #
    #     # def get_diagnosis_1(self, request, **kwargs):
    #     #     diagnosis_1 = Diagnosis_1.objects.get(id=kwargs['dxcode_0'])
    #     #     diagnosis_1_list = list(diagnosis_1.dxcode_1.values('id', 'name'))
    #     #     print(diagnosis_1_list)
    #     #     return HttpResponse(simplejson.dumps(diagnosis_1_list), content_type='application/json')
    #


class PtRegisterForm(forms.Form):
    unitnumb = forms.CharField(
        max_length=12,
        label='등록번호')
    ptname = forms.CharField(
        max_length=48,
        label='환자성명')
    birthdate = forms.DateField(
        label='생년월일')

# class PtForm2(forms.ModelForm):
#     class Meta:
#         model = Pt_diagnosis
#         fields = ('unitnumb', 'dxcode_0', 'dxcode_1', 'dxcode_2', 'dxcode_3')
#
#     def __init__(self, request, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.request = request
#         self.fields['dxcode_1'].queryset = Diagnosis_1.objects.none()
#         self.fields['dxcode_2'].queryset = Diagnosis_2.objects.none()
#
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'
#
#         if 'dxcode_0' in self.data:
#             try:
#                 dxcode_0_id = int(self.data.get('dxcode_0'))
#                 self.fields['dxcode_1'].queryset = Diagnosis_1.objects.filter(dxcode_0_id=dxcode_0_id).order_by(
#                     'dxname_1')
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to empty City queryset
#         elif self.instance.pk:
#             self.fields['dxcode_1'].queryset = self.instance.diagnosis_0.dxcode_1_set.order_by('dxname_1')
#
#         if 'dxcode_1' in self.data:
#             try:
#                 dxcode_1_id = int(self.data.get('dxcode_1'))
#                 self.fields['dxcode_2'].queryset = Diagnosis_2.objects.filter(dxcode_1_id=dxcode_1_id).order_by(
#                     'dxname_2')
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to empty City queryset
#         elif self.instance.pk:
#             self.fields['dxcode_2'].queryset = self.instance.diagnosis_1.dxcode_2_set.order_by('dxname_2')
#
#     def clean(self):
#         cleaned_data = super().clean()
#         unitnumb = cleaned_data.get('unitnumb')
#         dxcode_0 = cleaned_data.get('dxcode_0')
#         dxcode_1 = cleaned_data.get('dxcode_1')
#         dxcode_2 = cleaned_data.get('dxcode_2')
#         dxcode_3 = cleaned_data.get('dxcode_3')
#         fcuser = self.request.session.get('user')
#
#         # if not (quantity and product):
#         #     self.add_error('quantity', '값이 없습니다')
#         #     self.add_error('product', '값이 없습니다')
