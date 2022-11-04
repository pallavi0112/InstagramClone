from django.urls import path
from . import views
urlpatterns = [
    path('', views.Home , name="home"),
    path('signup/', views.SignUp , name="signup"),
    path('login/', views.Login , name="login"),
    path('logout/', views.LogOut , name="logout"),
    path('profile/',views.profile , name="profile"),
    path('profile/<int:id>',views.profile , name="profile"),
    path('search/',views.Search ,name="search"),
    path('follow/', views.Follow , name="follow"),
    path('post', views.UploadPosts , name="post"),
    path('like/<int:id>', views.Like , name="like" ),
    path('Uploadreels/', views.UploadReels, name="Uploadreels" ),
    path('reels/', views.reel , name="reels" ),
    path('uploadstory/' , views.UploadStory , name="uploadstory"),
    path('delete/', views.Delete , name="delete"),

]