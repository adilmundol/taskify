from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homefn),
    path('main/', mainfn),
    path('login/', loginfn),
    path('logout/',logoutfn),
    path('register/',regfn),
    path('adminpanel/', adminpanel),
    path('add/',addfn),
    path('addtask/',addfn1),
    path('profile/',profilefn),
    path('view/<int:sid>/', views.viewfn, name='viewfn'),
    path('deleteproject/<int:p_id>',deleteproject),
    path('editproject/<int:s_id>',editproject),
    path('deletetask/<int:p_id>',deletetask),
    path('edittask/<int:s_id>',edittask),
    path('statusupdate/<int:s_id>',statusupdate),




]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)