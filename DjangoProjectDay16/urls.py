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

from django.urls import path

from app01.views import depart, user, prettynum, admin

urlpatterns = [

    # 部门管理
    #    path('admin/', admin.site.urls),
    path('depart/list/',depart.depart_List),
    path('depart/add/',depart.depart_add),
    path('depart/<int:nid>/update/',depart.depart_update),
    path('depart/delete/',depart.depart_delete),

    # 员工管理
    path('user/list/', user.user_List),
    path('user/add/', user.user_add),
    path('user/add/form', user.user_add_form),
    path('user/add/modelform', user.user_add_modelform),
    path('user/<int:nid>/update/', user.user_update),
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/delete/', user.user_delete),

    # 靓号管理
    path('prettynum/list/', prettynum.prettynum_list),
    path('prettynum/add/', prettynum.prettynum_add),
    path('prettynum/<int:nid>/edit/', prettynum.prettynum_edit),
    path('prettynum/delete/', prettynum.prettynum_delete),

    # 管理员管理
    path('admin/list/', admin.admin_List),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),

]
