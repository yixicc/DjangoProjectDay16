"""
URL configuration for DjangoProjectDay16 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from app01 import views
urlpatterns = [

    # 部门管理
    #    path('admin/', admin.site.urls),
    path('depart/list/',views.depart_List),
    path('depart/add/',views.depart_add),
    path('depart/<int:nid>/update/',views.depart_update),
    path('depart/delete/',views.depart_delete),

    # 员工管理
    path('user/list/', views.user_List),
    path('user/add/', views.user_add),
    path('user/add/form', views.user_add_form),
    path('user/add/modelform', views.user_add_modelform),
    path('user/<int:nid>/update/', views.user_update),
    path('user/<int:nid>/edit/', views.user_edit),
    path('user/delete/', views.user_delete),

    # 靓号管理
    path('prettynum/list/', views.prettynum_list),
    path('prettynum/add/', views.prettynum_add),
    path('prettynum/<int:nid>/edit/', views.prettynum_edit),
    path('prettynum/delete/', views.prettynum_delete),

]
