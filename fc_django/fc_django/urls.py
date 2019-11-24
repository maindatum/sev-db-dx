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
from django.urls import path
from fcuser.views import index, logout, RegisterView, LoginView, DbImport
from product.views import ProductList, ProductCreate, ProductDetail, DxCreate, load_dx1, load_dx3, PtCreate, query_tbl, DxLV, dxlistview, dxlistquery
from order.views import OrderCreate, OrderList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', logout),
    path('product/', ProductList.as_view()),
    path('product/create/', ProductCreate.as_view()),
    path('dx_product/', DxCreate.as_view()),
    path('product/<int:pk>/',ProductDetail.as_view()),
    path('order/create/', OrderCreate.as_view()),
    path('order', OrderList.as_view()),
    path('regist_dx/', PtCreate.as_view()),
    path('dxlist/', dxlistview),
    path('dxlistquery/', dxlistquery),
    path('dx/db_import/', DbImport),
    # path('dxcode_0/<int:dxcode_0_id>/', get_diagnosis_1),
    # path('dxcode_1/<int:dxcode_1_id>/', get_diagnosis_2),
    path('ajax/load-cities/', load_dx1, name='ajax_load_dxs'),
    # path('ajax/load-cities2/', load_dx2, name='ajax_load_dxs2'),
    path('dxlistquery/loaddx', load_dx3),
    path('dxlistquery/tblquery', query_tbl)
]
