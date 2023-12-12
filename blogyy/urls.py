
from . import views
from django.urls import path
urlpatterns = [
    path("home/",views.Homepage.as_view(), name='home'),
    path('post/<int:pk>/',views.Blogpost, name='blogpost'),
    path("about/",views.About, name='about'),
    path("category/",views.Category.as_view(), name='category'),
    path("contact/",views.contact, name='contact'),
    path("signup/",views.Signup.as_view(), name='signup'),
    path("signin/",views.signin.as_view(), name='signin'),
    path('logout/',views.logout_view,name='logout'),
    path('create/',views.post_create,name='create_blog'),
    path('comment/<int:pk>/', views.post_comments, name='post_comment'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('dislike/<int:pk>/', views.dislike_post, name='dislike_post'),
    path('update/<int:pk>/',views.update_blog,name='update_blog'),
    path('delete_blog/<int:pk>', views.delete_blog, name='delete_blog'),
    # path('post/<int:pk>/comment/', post_comment_view, name='post_comment'),


]