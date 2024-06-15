from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog_manager_home'),
    path('about/', views.about, name='blog_manager_about'),
    path('blogs/', views.blogs, name='blog_manager_blogs'),
    path('blogs/?', views.blogs, name='blog_manager_blogs_search'),
    path('blogs/<int:blog_id>', views.blog_detail, name='blog_manager_blog'),
    path('blogs/<int:blog_id>/delete_blog', views.delete_blog, name='blog_manager_blog_delete'),
    path('blogs/<int:blog_id>/create_post/', views.create_post, name='blog_manager_post_create'),
    path('blogs/<int:blog_id>/<int:post_id>', views.post_detail, name='blog_manager_post'),
    path('blogs/<int:blog_id>/<int:post_id>/edit', views.edit_post, name='blog_manager_post_edit'),
    path('blogs/<int:blog_id>/<int:post_id>/delete_post', views.delete_post, name='blog_manager_post_delete'),
    path('blogs/<int:blog_id>/<int:post_id>/create_comment', views.create_comment, name='blog_manager_comment_create'),
    path('blogs/<int:blog_id>/<int:post_id>/delete_comment/<int:comment_id>', views.delete_comment,  name='blog_manager_comment_delete'),
    path('create_blog/', views.create_blog, name='blog_manager_blog_create'),
    path('register/', views.register_page, name='blog_manager_user_register'),
    path('login/', views.login_page, name='blog_manager_user_login'),
    path('logout/', views.logout_page, name='blog_manager_user_logout'),
    path('user/', views.user_page, name='blog_manager_user_detail'),
]