from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns =[

    path('home',views.index,name='index'),
    path('admin',views.adm,name='adm'),
    path('face',views.face,name='face'),
    path('outh',views.outh,name='outh'),
    path('store',views.store,name='store'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('',views.register,name='register'),
    path('info',views.info,name='info')

]


urlpatterns  += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)