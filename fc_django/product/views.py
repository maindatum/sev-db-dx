from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormView
from .models import Product, Pt_diagnosis, Diagnosis_0, Diagnosis_1, Diagnosis_2
from fcuser.models import Fcuser
from .forms import RegisterForm, DxRegisterForm, PtForm, DxForm
from order.forms import RegisterForm as OrderForm
from django.utils.decorators import method_decorator
from fcuser.decorator import login_required, admin_required
from django.core.paginator import Paginator

import simplejson
from django.http import HttpResponse


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

def dxlistview(request):
    ptdxs = Pt_diagnosis.objects.all()

    ptdxlist = []
    # print(ptdxs)
    for ptdx in ptdxs:
        ptdxtrans_dict = {}
        print(ptdx.dxcode_0)
        ptdxtrans_dict['unitnumb'] = ptdx.unitnumb
        ptdxtrans_dict['dxname0'] = Diagnosis_0.objects.get(dxcode_0=ptdx.dxcode_0).dxname_0
        ptdxtrans_dict['dxname1'] = Diagnosis_1.objects.get(dxcode_1=ptdx.dxcode_1).dxname_1
        ptdxtrans_dict['dxname2'] = Diagnosis_2.objects.get(dxcode_2=ptdx.dxcode_2).dxname_2
        ptdxtrans_dict['dxname3'] = ptdx.dxcode_3
        ptdxlist.append(ptdxtrans_dict)
    print(ptdxtrans_dict)
    paginator = Paginator(ptdxlist, 7)
    page = request.GET.get('page')
    ptdx_paged = paginator.get_page(page)
    return render(request, "dxlist.html", {'result1': ptdx_paged})


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
class PtCreate(CreateView):
    model = Pt_diagnosis
    form_class = PtForm
    template_name = "regist_dx.html"
    success_url = '/regist_dx'

    def form_valid(self, form):
        # print(self.request.session.get('user'))
        # print(Fcuser.objects.get(email=self.request.session.get('user')))
        # print(Fcuser.objects.get(email=self.request.session.get('user')))
        print(form.data.get('dxcode_0'))
        ptdiagnosis = Pt_diagnosis(
            unitnumb=form.data.get('unitnumb'),
            dxcode_0=Diagnosis_0.objects.get(pk=form.data.get('dxcode_0')),
            dxcode_1=Diagnosis_1.objects.get(pk=form.data.get('dxcode_1')),
            dxcode_2=Diagnosis_2.objects.get(pk=form.data.get('dxcode_2')),
            dxcode_3=form.data.get('dxcode_3'),
            regist_user=Fcuser.objects.get(pk=form.data.get('regist_user')),
        )
        ptdiagnosis = form.save(commit=False)
        # regist_user = Fcuser.objects.get(email=self.request.session.get('user'))
        # ptdiagnosis.regist_user = Fcuser.objects.get(email=regist_user)
        ptdiagnosis.save()
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request': self.request
        })
        return kw


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
            unitnumb=form.data.get('unitnumb'),
            dxcode_0=Diagnosis_0.objects.get(pk=form.data.get('dxcode_0')),
            dxcode_1=Diagnosis_1.objects.get(pk=form.data.get('dxcode_1')),
            dxcode_2=Diagnosis_2.objects.get(pk=form.data.get('dxcode_2')),
            dxcode_3=form.data.get('dxcode_3'),
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
    print(dx_0_pk, dx_1_pk, dx_2_pk)
    if dx_0_pk:
        ptdxs = Pt_diagnosis.objects.filter(dxcode_0=dx_0_pk)

    ptdxlist = []
    # print(ptdxs)
    for ptdx in ptdxs:
        ptdxtrans_dict = {}
        print(ptdx.dxcode_0)
        ptdxtrans_dict['unitnumb'] = ptdx.unitnumb
        ptdxtrans_dict['dxname0'] = Diagnosis_0.objects.get(dxcode_0=ptdx.dxcode_0).dxname_0
        ptdxtrans_dict['dxname1'] = Diagnosis_1.objects.get(dxcode_1=ptdx.dxcode_1).dxname_1
        ptdxtrans_dict['dxname2'] = Diagnosis_2.objects.get(dxcode_2=ptdx.dxcode_2).dxname_2
        ptdxtrans_dict['dxname3'] = ptdx.dxcode_3
        ptdxlist.append(ptdxtrans_dict)

    print(ptdxs)
    paginator = Paginator(ptdxlist, 7)
    page = request.GET.get('page')
    ptdx_paged = paginator.get_page(page)
    return render(request, 'dx_query_tbl.html', {'results': ptdx_paged})
