"""fc_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from fcuser.views import index, logout, RegisterView, LoginView, DrCreateView
from product.views import ProductList, ProductCreate, ProductDetail, \
    DxCreate, load_dx1, load_dx3, PtCreate, query_tbl, DxLV, \
    dxlistview, dxlistquery, DbImport, Pt_Dx_Detail, ptcheck, RegisterView, \
    DxUpdateView, book_list, book_create, book_update, save_book_form, book_delete, \
    dx2, dx2_update, dx2_create, dx2_delete, dx2_search, dx2_anysearch
from order.views import OrderCreate, OrderList
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', logout),
    path('product/', ProductList.as_view()),
    path('product/create/', ProductCreate.as_view()),
    path('dx_product/', DxCreate.as_view()),
    path('product/<int:pk>/', ProductDetail.as_view()),
    path('order/create/', OrderCreate.as_view()),
    path('order', OrderList.as_view()),
    path('ptdx/<int:pk>', Pt_Dx_Detail.as_view()),
    path('regist_dx/', PtCreate.as_view(), name='regist_dx'),
    path('dxlist/', dxlistview),
    path('dxlistquery/', dxlistquery),
    path('ptcheck/', ptcheck),
    path('ptregist/', RegisterView.as_view()),
    path('db_import/', DbImport),
    # path('dxcode_0/<int:dxcode_0_id>/', get_diagnosis_1),
    # path('dxcode_1/<int:dxcode_1_id>/', get_diagnosis_2),
    path('ajax/load-cities/', load_dx1, name='ajax_load_dxs'),
    # path('ajax/load-cities2/', load_dx2, name='ajax_load_dxs2'),
    path('dxlistquery/loaddx', load_dx3),
    path('dxlistquery/tblquery', query_tbl),
    path('dr_create/', DrCreateView.as_view()),
    path('dr_register/', TemplateView.as_view(template_name='drregister.html'), name='dr_registration_home'),
    path('dx_update/<int:pk>', DxUpdateView.as_view()),
    path('books/', book_list, name='book_list'),
    path('dx2/', dx2, name='dx2'),
    path('dx2/create/', dx2_create, name='dx2_create'),
    path('dx2/<int:pk>/update/', dx2_update, name='dx2_update'),
    path('dx2/<int:pk>/delete/', dx2_delete, name='dx2_delete'),
    path('books/create/', book_create, name="book_create"),
    path('dx2/search/', dx2_search, name="dx2_search"),
    path('dx2/search/any/', dx2_anysearch ,name="dx2_anysearch"),
    path('books/<int:pk>/update/', book_update, name="book_update"),
    path('books/<int:pk>/delete/', book_delete, name="book_delete"),
]
