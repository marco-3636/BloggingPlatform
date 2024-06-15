from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Blog, Post, Comment
# Create your views here.



# Create your views here.
def home(request):


    context = {
      'title': 'Home',
      'blogs': Blog.objects.all,
      'posts': Post.objects.all
     }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html', {'title': 'About'})


def blogs(request):
    query = request.GET.get('name')
    print(query)
    if query:
        blogs = Blog.objects.filter(blog_title__contains=query)
    else:
        blogs = Blog.objects.all()
    context = {'blogs': blogs, 'title': 'Blogs'}
    return render(request, 'blogs.html', context)


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog_posts = Post.objects.filter(post_blog=blog)
    blog_author = get_object_or_404(User, id=blog.blog_author_id)
    if blog_author == request.user:
        author = request.user
    else:
        author = None

    context = {
        'blog': blog,
        'user': author,
        'posts': blog_posts
    }
    return render(request, 'blog_detail.html', context)


@login_required
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('blog_title')
        try:
            blog = Blog.objects.get(blog_title=title)
        except Blog.DoesNotExist:
            blog = None
        if blog is None:
            blog = Blog(blog_title=title, blog_author=request.user)
            blog.save()
            return redirect('/user/')
        else:
            message = "Blog title already in use."
            return render(request, 'create_blog.html', {'error_message': message, 'title': 'Create Blog'})
    return render(request, 'create_blog.html', {'title': 'Create Blog'})


@login_required
def delete_blog(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        blog = None
        return redirect('blog_manager_blogs')
    try:
        blog_author = User.objects.get(id=blog.blog_author_id)
    except User.DoesNotExist:
        blog_author = None
    if blog_author != request.user:
        redirect('blog_manager_blog', blog_id=blog_id)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_manager_user_detail')
    context = {
        'blog': blog,
        'title': 'Delete Blog'
    }
    return render(request, 'delete_blog.html', context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/user/')
        else:
            message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': message, 'title': 'Login'})
    else:
        return render(request, 'login.html', {'title': 'Login'})


@login_required
def logout_page(request):
    logout(request)
    return redirect('/')


def register_page(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserCreationForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        if form.is_valid():
            form.save()
            user = authenticate(request, username=username, password=password, email=email)
            login(request, user)
            return redirect('/user/')
        else:
            message = "Username already in use or invalid password."
            return render(request, 'register.html', {'error_message': message, 'title': 'Register'})
    return render(request, 'register.html', {'title': 'Register'})


@login_required
def user_page(request):
    user = request.user
    blogs = Blog.objects.filter(blog_author_id=user)

    context = {
        'user': user,
        'blogs': blogs,
        'title': 'User Page'
    }
    return render(request, 'user.html', context)


@login_required
def create_post(request, blog_id):
    if request.method == 'POST':
        title = request.POST.get('post_title')
        content = request.POST.get('post_content')
        blog = Blog.objects.get(id=blog_id)
        author = User.objects.get(id=blog.blog_author_id)
        if author == request.user:
            try:
                existing_post = Post.objects.filter(post_blog=blog).get(post_title=title)
                message = "Post with the same title already in this blog."
                return render(request, 'create_post.html', {'error_message': message, 'title': 'Create Post'})
            except Post.DoesNotExist:
                post = Post(post_title=title, post_content=content, post_author=author, post_blog=blog)
                post.save()
                return redirect('blog_manager_blog', blog_id=blog_id)

    return render(request, 'create_post.html', {'title': 'Create Post'})


def post_detail(request, blog_id, post_id):
    try:
        post = Post.objects.filter(post_blog_id=blog_id).get(id=post_id)
    except Post.DoesNotExist:
        return redirect('blog_manager_blog', blog_id=blog_id)
    post_author = get_object_or_404(User, id=post.post_author_id)
    if post_author == request.user:
        author = request.user
    else:
        author = None
    post_comments = Comment.objects.filter(comment_post=post)
    context = {
        'post': post,
        'user': author,
        'comments': post_comments,
        'title': post.post_title
    }
    return render(request, 'post_detail.html', context)


@login_required
def delete_post(request, blog_id, post_id):
    try:
        post = Post.objects.filter(post_blog_id=blog_id).get(id=post_id)
    except Post.DoesNotExist:
        return redirect('blog_manager_blog', blog_id=blog_id)
    try:
        post_author = User.objects.get(id=post.post_author_id)
    except User.DoesNotExist:
        post_author = None
    if post_author != request.user:
        return redirect('blog_manager_post', blog_id=blog_id, post_id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog_manager_blog', blog_id=blog_id)  # Redirect to the blogs page after successful deletion
    context = {
        'post': post,
        'title': 'Delete Post'
    }
    return render(request, 'delete_post.html', context)


@login_required
def edit_post(request, blog_id, post_id):
    try:
        post = Post.objects.filter(post_blog_id=blog_id).get(id=post_id)
    except Post.DoesNotExist:
        return redirect('blog_manager_blog', blog_id=blog_id)
    try:
        post_author = User.objects.get(id=post.post_author_id)
    except User.DoesNotExist:
        post_author = None
    if post_author != request.user:
        return redirect('blog_manager_post', blog_id=blog_id, post_id=post_id)
    if request.method == 'POST':
        new_title = request.POST.get('new_post_title')
        try:
            existing_post = Post.objects.filter(post_blog_id=blog_id).get(post_title=new_title)
        except Post.DoesNotExist:
            existing_post = post
        if existing_post != post:
            message = "Post with the same title already in this blog."
            return render(request, 'edit_post.html', {'error_message': message, 'title': 'Edit Post'})
        new_content = request.POST.get('new_post_content')
        post.post_title = new_title
        post.post_content = new_content
        post.save()
        return redirect('blog_manager_post', blog_id=blog_id, post_id=post_id)
    context = {
        'post': post,
        'title': 'Edit Post'
    }
    return render(request, 'edit_post.html', context)


@login_required
def create_comment(request, blog_id, post_id):
    post = Post.objects.get(id=post_id)
    context = {
        'post': post,
        'title': 'Create Comment'
    }
    if request.method == 'POST':
        content = request.POST.get('comment_content')
        comment = Comment(comment_content=content, comment_author=request.user, comment_post=post)
        comment.save()
        return redirect('blog_manager_post', blog_id=blog_id, post_id=post_id)
    return render(request, 'create_comment.html', context)


@login_required
def delete_comment(request, blog_id, post_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    author = User.objects.get(id=comment.comment_author_id)
    if author == request.user:
        comment.delete()
    return redirect('blog_manager_post', blog_id=blog_id, post_id=post_id)
    
