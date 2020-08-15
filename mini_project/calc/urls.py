from django.urls import path
from . import views

urlpatterns=[
    path('',views.signIn,name='signIn'),
    path('postsign',views.postsign,name='postsign'),
    path('signup',views.signUp,name='signup'),
    path('postsignup',views.postsignup,name='postsignup'),
    path('home',views.home,name='home'),
    path('add',views.add,name="add"),
    # path('logout',views.logout,name="log")
]