from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormView
from .models import Product, Patient_info, Pt_diagnosis, Diagnosis_0, Diagnosis_1, Diagnosis_2, Book
from fcuser.models import Fcuser
from .forms import RegisterForm, DxRegisterForm, PtForm, DxForm, PtRegisterForm, PtUpdateForm, BookForm, PtDx2Form, \
    PtDx3Form
from order.forms import RegisterForm as OrderForm
from django.utils.decorators import method_decorator
from fcuser.decorator import login_required, admin_required
from django.core.paginator import Paginator
import pandas as pd
import os
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
import simplejson
import datetime
from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.


class ProductList(ListView):
    model = Product
    template_name = "product.html"
    context_object_name = "product_list"


@method_decorator(admin_required, name='dispatch')
class ProductCreate(FormView):
    form_class = RegisterForm
    template_name = "register_product.html"
    success_url = '/product/'

    def form_valid(self, form):
        product = Product(
            name=form.data.get('name'),
            price=form.data.get('price'),
            description=form.data.get('description'),
            stock=form.data.get('stock')
        )
        product.save()
        return super().form_valid(form)


class ProductDetail(DetailView):
    template_name = "product_detail.html"
    queryset = Product.objects.all()
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm(self.request)
        return context


@method_decorator(admin_required, name='dispatch')
class DxCreate(FormView):
    form_class = DxRegisterForm
    template_name = "dx_register_product.html"
    success_url = '/dx_product/'

    def form_valid(self, form):
        ptdiagnosis = Pt_diagnosis(
            unitnumb=form.data.get('unitnumb'),
            dxcode_0=form.data.get('dxcode_0'),
            dxcode_1=form.data.get('dxcode_1'),
            dxcode_2=form.data.get('dxcode_2')
        )
        ptdiagnosis.save()
        return super().form_valid(form)


def DxRegister(request):
    if request.method == "GET":
        return render(request, 'dxuserregist.html')
    elif request.method == "POST":
        unitnumb = request.POST.get('unitnumb', None)
        dxcode_0 = request.POST.get('dxcode_0', None)
        dxcode_1 = request.POST.get('dxcode_1', None)
        dxcode_2 = request.POST.get('dxcode_2', None)

        res_data = {}

        if not (unitnumb and dxcode_0 and dxcode_1 and dxcode_2):
            res_data['error'] = "모든 값을 입력해야 합니다"
        else:
            ptdiagnosis = Pt_diagnosis(
                unitnumb=unitnumb,
                dxcode_0=dxcode_0,
                dxcode_1=dxcode_1,
                dxcode_2=dxcode_2
            )

            ptdiagnosis.save()

        return render(request, 'dxuserregist.html', res_data)
    pass


# class NewDxCreate(CreateView):
#     model = Pt_diagnosis
#     form_class = DxForm
#     template_name = "regist_dx.html"
#     success_url = '/'
#
#     #Get information from related object in generic list view
#     def form_valid(self, form):
#         dx = Pt_diagnosis(
#             unitnumb=form.data.get('unitnumb'),
#             dxcode_0=Diagnosis_0.objects.get(dxcode_0=form.data.get('dxcode_0')),
#             dxcode_1=Diagnosis_1.objects.get(dxname_1=form.data.get('dxcode_1')),
#             dxcode_2=Diagnosis_2.objects.get(dxname_2=form.data.get('dxcode_2')),
#             dxcode_3=form.data.get('dxcode_3'),
#             regist_user=form.data.get('regist_user'),
#         )
#         # dx = form.save(commit=False)
#         dx.save()
#         return super().form_valid(form)

# def dxlistview(request):
#     ptdxs = Pt_diagnosis.objects.all()
#     ptdxtrans_dict = {}
#     ptdxlist = []
#     print(ptdxs)
#     for ptdx in ptdxs:
#         ptdxtrans_dict = {}
#         print(ptdx.dxcode_0)
#         print(ptdx.dxcode_1)
#         print('ptdx.code2', ptdx.dxcode_2)
#         ptdxtrans_dict['unitnumb'] = ptdx.unitnumb.unitnumb
#         ptdxtrans_dict['ptname'] = ptdx.unitnumb.ptname
#         ptdxtrans_dict['dxname0'] = ptdx.dxcode_0
#         ptdxtrans_dict['dxname1'] = ptdx.dxcode_1
#         ptdxtrans_dict['dxname2'] = ptdx.dxcode_2
#         ptdxtrans_dict['dxname3'] = ptdx.dxcode_3
#         ptdxlist.append(ptdxtrans_dict)
#     print(ptdxtrans_dict)
#     paginator = Paginator(ptdxlist, 7)
#     page = request.GET.get('page')
#     ptdx_paged = paginator.get_page(page)
#     print(ptdx_paged)
#     return render(request, "dxlist.html", {'result1': ptdx_paged})

def dxlistview(request):
    ptdxs = Pt_diagnosis.objects.all()
    paginator = Paginator(ptdxs, 7)
    page = request.GET.get('page')
    ptdxs_paged = paginator.get_page(page)
    return render(request, "dxlist.html", {'ptdxs': ptdxs_paged})


def dxlistquery(request):
    dx0 = Diagnosis_0.objects.all()
    dx0_list = []
    for dx in dx0:
        dx0_dict = {}
        dx0_dict['dx_0_pk'] = dx.pk
        dx0_dict['dxcode_0'] = dx.dxcode_0
        dx0_dict['dxname_0'] = dx.dxname_0
        dx0_list.append(dx0_dict)
    print(dx0_list)
    return render(request, "dxlistquery.html", {'result1': dx0_list})


class DxLV(ListView):
    model = Pt_diagnosis
    context_object_name = 'pt_dxs'
    template_name = "dxlist.html"

    def get_context_data(self, **kwargs):
        # xxx will be available in the template as the related objects
        context = super(DxLV, self).get_context_data(**kwargs)
        # context['dxcode_1'] = Diagnosis_1.objects.filter(dxcode_0=self.)
        return context


# @method_decorator(login_required, name='dispatch')
class PtCreate(FormView):
    model = Pt_diagnosis
    form_class = PtForm
    template_name = "regist_dx.html"
    # template_name = "dxupdate.html"
    success_url = '/regist_dx'

    # def form_valid(self, form):
    #     unitnumb = str(form.data.get('unitnumb'))
    #     print(unitnumb)

    def form_valid(self, form):
        print(self.request.session.get('user'))
        # print(Fcuser.objects.get(email=self.request.session.get('user')))
        # print(Fcuser.objects.get(email=self.request.session.get('user')))
        print(form.data.get('dxcode_0'))
        unitnumb_pk = int(form.data.get('unitnumb'))
        print('unirnumb_pk', unitnumb_pk)
        birthdate = Patient_info.objects.get(pk=unitnumb_pk).birthdate
        print(birthdate)
        dx_date = datetime.datetime.strptime(form.data.get('dx_date'), '%Y-%m-%d').date()
        print(type(dx_date))
        print(type(birthdate))
        td = dx_date - birthdate
        dx_age = float(td.days / 365.25)
        print(dx_age)
        print(dx_age)
        print(type(dx_age))
        print('ptinfo object', Patient_info.objects.get(pk=unitnumb_pk))
        need_confirm = form.data.get('need_confirm')
        compl_confirm = form.data.get('comp_confirm')
        if form.data.get('need_confirm') == 'on':
            need_confirm = True
        else:
            need_confirm = False

        if form.data.get('compl_confirm') == 'on':
            compl_confirm = True
        else:
            compl_confirm = False

        ptdiagnosis = Pt_diagnosis(
            unitnumb=Patient_info.objects.get(pk=unitnumb_pk),
            dx_date=dx_date,
            dxcode_0=Diagnosis_0.objects.get(pk=form.data.get('dxcode_0')),
            dxcode_1=Diagnosis_1.objects.get(pk=form.data.get('dxcode_1')),
            dxcode_2=Diagnosis_2.objects.get(pk=form.data.get('dxcode_2')),
            dxcode_3=form.data.get('dxcode_3'),
            regist_user=Fcuser.objects.get(pk=form.data.get('regist_user')),
            dr_name=form.data.get('dr_name'),
        )
        print('the age', ptdiagnosis.dx_age)
        # ptdiagnosis = form.save(commit=False)
        ptdiagnosis.dx_age = dx_age
        ptdiagnosis.need_confirm = need_confirm
        ptdiagnosis.compl_confirm = compl_confirm
        print('ptdx.unitnumb is', ptdiagnosis.unitnumb)
        print('ptdx.dxage is', ptdiagnosis.dx_age)
        # regist_user = Fcuser.objects.get(email=self.request.session.get('user'))
        # ptdiagnosis.regist_user = Fcuser.objects.get(email=regist_user)
        ptdiagnosis.save()
        return super().form_valid(form)

    # def get_form_kwargs(self, **kwargs):
    #     kw = super().get_form_kwargs(**kwargs)
    #     kw.update({
    #         'request': self.request
    #     })
    #     return kw


# def get_diagnosis_1(request, dxcode_0_id):
#     diagnosis_0 = Diagnosis_0.objects.get(pk=dxcode_0_id)
#     diagnosis_1 = Diagnosis_1.objects.filter(dxcode_0=diagnosis_0)
#     return render(request, 'dropdownlist_dx1.html', {'diagnosis_1': diagnosis_1})
#
# def get_diagnosis_2(request, dxcode_1_id):
#     diagnosis_1 = Diagnosis_1.objects.get(pk=dxcode_1_id)
#     diagnosis_2 = Diagnosis_2.objects.filter(dxcode_1=diagnosis_1)
#     return render(request, 'dropdownlist_dx2.html', {'diagnosis_2': diagnosis_2})
# print(diagnosis_1)
# diagnosis_1_dict = {}
# for diagnosis in diagnosis_1:
#     print (diagnosis.dxname_1)
#     diagnosis_1_dict["dxcode_1"] = diagnosis.dxcode_1
#     diagnosis_1_dict["dxname_1"] = diagnosis.dxname_1
# print(diagnosis_1_dict)
# return HttpResponse(simplejson.dumps(diagnosis_1_dict), content_type='application/json')


class RegistDx(CreateView):
    model = Pt_diagnosis
    form_class = PtForm
    template_name = "regist_dx.html"
    success_url = '/dx'

    def form_valid(self, form):
        print(self.request.session.get('user'))
        print(Fcuser.objects.get(email=self.request.session.get('user')))
        print(Fcuser.objects.get(email=self.request.session.get('user')))
        ptdiagnosis = Pt_diagnosis(
            unitnumb=form.data.get('id_unitnumb'),
            dx_date=form.data.get('id_dx_date'),
            dxcode_0=Diagnosis_0.objects.get(pk=form.data.get('id_dxcode_0')),
            dxcode_1=Diagnosis_1.objects.get(pk=form.data.get('id_dxcode_1')),
            dxcode_2=Diagnosis_2.objects.get(pk=form.data.get('id_dxcode_2')),
            dxcode_3=form.data.get('dxcode_3'),
            dr_name=form.data.get('id_dr_name'),
            regist_user=form.data.get(''),
        )
        ptdiagnosis = form.save(commit=False)
        regist_user = Fcuser.objects.get(email=self.request.session.get('user'))
        ptdiagnosis.regist_user = Fcuser.objects.get(email=regist_user)
        ptdiagnosis.save()
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request': self.request
        })
        return kw


class Pt_Dx_Detail(DetailView):
    template_name = 'pt_dx_detail.html'
    queryset = Pt_diagnosis.objects.all()
    context_object_name = 'ptdx'


#
def load_dx1(request):
    print("333")
    dxcode_0_id = request.GET.get('dxcode_0')
    dxcode_1_id = request.GET.get('dxcode_1')
    print(dxcode_0_id, dxcode_1_id)
    dxcode_1 = Diagnosis_1.objects.filter(dxcode_0_id=dxcode_0_id).order_by('dxname_1')
    dxcode_2 = Diagnosis_2.objects.filter(dxcode_1_id=dxcode_1_id).order_by('dxname_2')
    return render(request, 'dropdownlist_dx1.html', {'dxcode_1': dxcode_1, 'dxcode_2': dxcode_2})


# def load_dx2(request):
#     dxcode_1_id = request.GET.get('dxcode_1')
#     print(dxcode_1_id)
#     dxcode_2 = Diagnosis_2.objects.filter(dxcode_1_id=dxcode_1_id).order_by('dxname_2')
#     return render(request, 'dropdownlist_dx2.html', {'dxcode_2': dxcode_2})

def load_dx3(request, *args, **kwargs):
    print("333")
    dx_0_pk = request.GET.get('dx_0_pk')
    print(dx_0_pk)
    # dx_0 = Diagnosis_0.objects.filter(pk=dx_0_pk)
    print("hi")
    # dxcode_1_id = request.GET.get('dxcode_1')
    # print(dxcode_0_id, dxcode_1_id)
    dx_1 = Diagnosis_1.objects.filter(dxcode_0=dx_0_pk).order_by('dxname_1')
    print("hihihi")
    print(dx_1)

    dx_1_pk = request.GET.get('dx_1_pk')
    print("hihihihihi")
    print(dx_1_pk)
    dx_2 = Diagnosis_2.objects.filter(dxcode_1=dx_1_pk).order_by('dxname_2')
    print('almost')
    print(dx_2)
    # dxcode_2 = Diagnosis_2.objects.filter(dxcode_1=dx_2.pk).order_by('dxname_2')
    # # print(dx_0[0].id, dx_1[0].id)

    return render(request, 'dropdownlist_dx3.html', {'dx_1': dx_1, 'dx_2': dx_2})


def query_tbl(request, *args, **kwargs):
    dx_0_pk = request.GET.get('dx_0_pk')
    dx_1_pk = request.GET.get('dx_1_pk')
    dx_2_pk = request.GET.get('dx_2_pk')
    print('query', dx_0_pk, dx_1_pk, dx_2_pk)
    if dx_0_pk:
        ptdxs = Pt_diagnosis.objects.filter(dxcode_0_id=dx_0_pk)
    print(ptdxs)

    ptdxlist = []
    # print(ptdxs)
    for ptdx in ptdxs:
        ptdxtrans_dict = {}
        print(ptdx.dxcode_0)
        ptdxtrans_dict['unitnumb'] = ptdx.unitnumb.unitnumb
        ptdxtrans_dict['ptname'] = ptdx.unitnumb.ptname
        ptdxtrans_dict['birthdate'] = ptdx.unitnumb.birthdate
        ptdxtrans_dict['dx_date'] = ptdx.dx_date
        ptdxtrans_dict['dx_age'] = ptdx.dx_age
        ptdxtrans_dict['dxname0'] = ptdx.dxcode_0
        ptdxtrans_dict['dxname1'] = ptdx.dxcode_1
        ptdxtrans_dict['dxname2'] = ptdx.dxcode_2
        ptdxtrans_dict['dxname3'] = ptdx.dxcode_3
        ptdxlist.append(ptdxtrans_dict)

    print(ptdxs)
    paginator = Paginator(ptdxlist, 7)
    page = request.GET.get('page')
    ptdx_paged = paginator.get_page(page)
    return render(request, 'dx_query_tbl.html', {'results': ptdx_paged})


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


def ptcheck(request, *args, **kwargs):
    unitnumb = request.GET.get('unitnumb')
    result_count = Patient_info.objects.filter(unitnumb=str(unitnumb)).count()
    flag = 0
    response_dict = {}
    if result_count < 1:
        response_dict['flag'] = 0
        response_dict['unitnumb_pk'] = None
        print(simplejson.dumps(response_dict))
        return HttpResponse(simplejson.dumps(response_dict), content_type="application/json")
    elif result_count > 1:
        response_dict['flag'] = 2
        response_dict['unitnumb_pk'] = None
        print(simplejson.dumps(response_dict))
        return HttpResponse(simplejson.dumps(response_dict), content_type="application/json")
    else:
        response_dict['flag'] = 1
        unitnumb_pk = Patient_info.objects.get(unitnumb=str(unitnumb)).pk
        response_dict['unitnumb_pk'] = unitnumb_pk
        print(response_dict)
        return HttpResponse(simplejson.dumps(response_dict), content_type="application/json")


class RegisterView(FormView):
    template_name = "ptregister.html"
    form_class = PtRegisterForm
    success_url = "/"

    def form_valid(self, form):
        ptinfo = Patient_info(
            unitnumb=str(form.data.get('unitnumb')),
            ptname=form.data.get('ptname'),
            birthdate=form.data.get('birthdate'),
        )
        ptinfo.save()

        return super().form_valid(form)


class DxUpdateView(UpdateView):
    model = Pt_diagnosis
    form_class = PtUpdateForm
    template_name = "dxupdate.html"
    success_url = '/regist_dx'
    #
    # context_object_name = "ptdx"
    # fields = "__all__"
    # template_name = "dxupdate.html"
    # success_url = "/"


def book_list(request):
    books = Book.objects.all().order_by('-id')
    print(books)
    return render(request, "book_list.html", {'books': books})


def dx2(request):
    ptinfos_merge_dict2 = get_merged_table()
    # ptdxs = Pt_diagnosis.objects.select_related('unitnumb_set').order_by('-id')
    # ptinfos = Patient_info.objects.get(id=1)
    # ptdxs = Pt_diagnosis.objects.all()
    # ptinfos = Patient_info.objects.all()
    # ptdxtrans_dict = {}
    # ptdxlist = []
    # print(ptdxs)
    # for ptdx in ptdxs:
    #     ptdxtrans_dict = {}
    #     print(ptdx.dxcode_0)
    #     print(ptdx.dxcode_1)
    #     print('ptdx.code2', ptdx.dxcode_2)
    #     ptdxtrans_dict['unitnumb'] = ptdx.unitnumb.unitnumb
    #     ptdxtrans_dict['ptname'] = ptdx.unitnumb.ptname
    #     ptdxtrans_dict['dxname0'] = ptdx.dxcode_0
    #     ptdxtrans_dict['dxname1'] = ptdx.dxcode_1
    #     ptdxtrans_dict['dxname2'] = ptdx.dxcode_2
    #     ptdxtrans_dict['dxname3'] = ptdx.dxcode_3
    #     ptdxlist.append(ptdxtrans_dict)
    #     print(ptdxtrans_dict)
    # print('list',ptdxlist)
    # ptdxlist_df = pd.DataFrame(ptdxlist)
    # print('listdf', ptdxlist_df)
    # ptinfos_df = pd.DataFrame(list(ptinfos.values()))
    # ptdxs_df = pd.DataFrame(list(ptdxs.values()))
    # print(ptinfos_df)
    # print(ptdxs_df)
    # ptinfos_merge = ptinfos_df.merge(ptdxs_df, left_on='id', right_on='unitnumb_id', how='left')
    # ptinfos_merge2 = ptinfos_df.merge(ptdxlist_df, left_on='unitnumb', right_on='unitnumb', how='left')
    # print('m2', ptinfos_merge2)
    # print(ptinfos_merge.columns)
    # ptinfos_merge_dict = ptinfos_merge.set_index('id_x').to_dict('index')
    # ptinfos_merge_dict2 = ptinfos_merge2.set_index('id').to_dict('index')
    # print(ptinfos_merge_dict)
    return render(request, "dx2.html", {'ptdxs': ptinfos_merge_dict2})


def dx2_create(request):
    print('this is dx2_create')
    if request.method == "POST":
        form = PtDx2Form(request.POST)
    else:
        form = PtDx2Form()
    pk = None
    return save_dx2_form(request, form, pk, 'partial_dx2_create.html')


def get_merged_table():
    ptdxs = Pt_diagnosis.objects.all()
    ptinfos = Patient_info.objects.all()
    ptdxtrans_dict = {}
    ptdxlist = []
    print(ptdxs)
    for ptdx in ptdxs:
        ptdxtrans_dict = {}
        ptdxtrans_dict['unitnumb'] = ptdx.unitnumb.unitnumb
        ptdxtrans_dict['ptname'] = ptdx.unitnumb.ptname
        ptdxtrans_dict['dx_date'] = ptdx.dx_date
        ptdxtrans_dict['dx_age'] = ptdx.dx_age
        ptdxtrans_dict['dxname0'] = ptdx.dxcode_0
        ptdxtrans_dict['dxname1'] = ptdx.dxcode_1
        ptdxtrans_dict['dxname2'] = ptdx.dxcode_2
        ptdxtrans_dict['dxname3'] = ptdx.dxcode_3
        ptdxlist.append(ptdxtrans_dict)
    ptdxlist_df = pd.DataFrame(ptdxlist)
    ptinfos_df = pd.DataFrame(list(ptinfos.values()))
    ptdxs_df = pd.DataFrame(list(ptdxs.values()))
    ptinfos_merge = ptinfos_df.merge(ptdxs_df, left_on='id', right_on='unitnumb_id', how='left')
    ptinfos_merge2 = ptinfos_df.merge(ptdxlist_df, left_on='unitnumb', right_on='unitnumb', how='left')
    ptinfos_merge_dict = ptinfos_merge.set_index('id_x').to_dict('index')
    ptinfos_merge_dict2 = ptinfos_merge2.set_index('id').to_dict('index')
    return (ptinfos_merge_dict2)


def save_dx2_form(request, form, pk, template_name):
    print('this is save dx2 form!')
    data = dict()
    print('this request is', request.method)
    if request.method == 'POST':
        if form.is_valid():
            if form.__class__.__name__ == 'PtDx3Form':
                print('this is PtDx3Form, Yes.')
                print('this is form is', form.__class__.__name__)
                print('Form is valid and POST is successful')
                instance=form.save(commit=False)
                birthdate = Patient_info.objects.get(pk=pk).birthdate
                print(birthdate)
                dx_date = datetime.datetime.strptime(form.data.get('dx_date'), '%Y-%m-%d').date()
                print(type(dx_date))
                print(type(birthdate))
                td = dx_date - birthdate
                dx_age = float(td.days / 365.25)
                instance.dx_age = dx_age
                instance.save()

                data['form_is_valid'] = True
                ptdxs = get_merged_table()
                context = {'ptdxs': ptdxs}
                data['html_book_list'] = render_to_string('partial_dx2_list.html', context, request=request)
            else:
                print('this is form is', form.__class__.__name__)
                print('Form is valid and POST is successful')
                form.save()
                data['form_is_valid'] = True
                ptdxs = get_merged_table()
                context = {'ptdxs': ptdxs}
                data['html_book_list'] = render_to_string('partial_dx2_list.html', context, request=request)
        else:
            data['form_is_valid'] = False
            print("Form is not valid...")
            print("this is form", form)
            context = {'form': form, 'pk': pk}
            data['html_form'] = render_to_string(template_name, context, request=request)
    else:
        context = {'form': form, 'pk': pk}
        print("This is Get Method function in save dx2 form")
        print(context)
        print(request)
        data['html_form'] = render_to_string(template_name, context, request=request)

    # print(data)
    return JsonResponse(data)


def dx2_search(request):
    return render(request, 'dx2_search.html')


def dx2_anysearch(request, *args, **kwargs):
    data = dict()
    print("here is function dx2_anysearch")
    keyword = request.GET.get('keyword')
    print('keyword is', keyword)
    ptdxs = get_merged_table()
    print('ptdxs is', ptdxs)
    df_ptdxs = pd.DataFrame(ptdxs)
    df_ptdxs = df_ptdxs.T
    mask = df_ptdxs.applymap(lambda x: str(keyword).lower() in str(x).lower())
    print('mask', mask)
    mask1 = mask.any(axis=1)
    print('anymask', mask1)
    df_ptdxs_masked = df_ptdxs[mask.any(axis=1)]
    print(df_ptdxs)
    print('masked df',df_ptdxs_masked)
    df_ptdxs_masked_dict = df_ptdxs_masked.to_dict('index')
    print('masked dict', df_ptdxs_masked_dict)
    context = {'ptdxs': df_ptdxs_masked_dict}
    data['html_book_list'] = render_to_string('partial_dx2_list.html', context, request=request)
    print('success in dx2_anysearch.')
    return JsonResponse(data)


def dx2_update(request, pk):
    print("this is dx-update function")
    print(pk)
    print(type(pk))
    try:
        ptdx = Pt_diagnosis.objects.get(unitnumb=pk)
    except:
        print("없네요")
        ptdx = None
    #
    # # ptdx = get_object_or_404(Pt_diagnosis, unitnumb=pk)
    # print('postbookgetting')
    print('ptdx is', ptdx)
    if request.method == "POST":
        print("this is if statement post")
        if ptdx:
            print("there is ptdx and doing post")
            form = PtDx3Form(request.POST, instance=ptdx)
        else:
            print("NO PTDX")
            form = PtDx3Form(request.POST)
    else:
        if ptdx:
            print("pk is", pk)
            form = PtDx3Form(instance=ptdx)
        else:
            print("nono ptdx")
            print("pk is", pk)
            form = PtDx3Form(initial={'unitnumb': Patient_info.objects.get(id=pk)})
            return save_dx2_form_initialvalue(request, pk, form, 'partial_book_update.html')
    print("ㅗㅑㅗㅑ")
    return save_dx2_form(request, form, pk, 'partial_book_update.html')


def save_dx2_form_initialvalue(request, pk, form, template_name):
    data = dict()

    ptinfo = Patient_info.objects.get(id=pk)
    ptunitnumb = ptinfo.unitnumb
    print("hererere")
    print(request)
    context = {'form': form, 'pk': pk, 'ptunitnumb': ptunitnumb}
    data['html_form'] = render_to_string(template_name, context, request=request)
    # print(data)
    return JsonResponse(data)


def dx2_delete(request, pk):
    print("this is book-delete function")
    print('this is pk', pk)
    book = get_object_or_404(Book, pk=pk)
    data = dict()
    print('postbookdelete getting')
    print(book)
    if request.method == "POST":
        book.delete()
        data['form_is_valid'] = True
        books = Book.objects.all().order_by('-id')
        data['html_book_list'] = render_to_string('partial_book_list.html', {'books': books})
    else:
        print("this is if statement get")
        context = {'book': book}
        data['html_form'] = render_to_string('partial_book_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


def save_book_form(request, form, template_name):
    data = dict()

    if request.method == 'POST':
        if form.is_valid():
            print('succesful')
            form.save()
            data['form_is_valid'] = True
            books = Book.objects.all().order_by('-id')
            data['html_book_list'] = render_to_string('partial_book_list.html', {
                'books': books
            })
            print('validation', data['form_is_valid'])
        else:
            data['form_is_valid'] = False
            context = {'form': form}
            data['html_form'] = render_to_string(template_name, context, request=request)
    else:
        context = {'form': form}
        data['html_form'] = render_to_string(template_name, context, request=request)
    print('this is data', data)
    return JsonResponse(data)


def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
    else:
        form = BookForm()
    return save_book_form(request, form, 'partial_book_create.html')


def book_update(request, pk):
    print("this is book-update function")
    print(pk)
    print(type(pk))
    book = get_object_or_404(Book, pk=pk)
    print('postbookgetting')
    print(book)
    if book:
        if request.method == "POST":
            print("this is if statement post")
            form = BookForm(request.POST, instance=book)
        else:
            print("this is if statement get")
            form = BookForm(instance=book)
    return save_book_form(request, form, 'partial_book_update.html')


def book_delete(request, pk):
    print("this is book-delete function")
    print('this is pk', pk)
    book = get_object_or_404(Book, pk=pk)
    data = dict()
    print('postbookdelete getting')
    print(book)
    if request.method == "POST":
        book.delete()
        data['form_is_valid'] = True
        books = Book.objects.all().order_by('-id')
        data['html_book_list'] = render_to_string('partial_book_list.html', {'books': books})
    else:
        print("this is if statement get")
        context = {'book': book}
        data['html_form'] = render_to_string('partial_book_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)
