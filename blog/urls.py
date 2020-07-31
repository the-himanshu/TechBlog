from . import views
from django.urls import path

urlpatterns = [
    path('blog/', views.PostList, name='home'),
    path('', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('blog/makePost/', views.makePost, name='makePost'),
    path('blog/logout/', views.Logout, name='logout'),
    path('blog/profile/', views.Profile, name='profile'),
    path('blog/portfolio/', views.Portfolio, name='portfolio'),
    path('blog/makePost/savePost/', views.savePost, name='savePost'),
    path('blog/<slug:slug>/', views.PostDetail, name='post_detail'),
]