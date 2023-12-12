from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView ,ListView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CommentForm, PostBlogForm, UserRegistrationForm,UserSigninForm
from .models import Post, PostComments, Contact, Category


# Create your views here.
class Homepage(ListView):
    cs = Post.objects.all()
    model = Post
    template_name='home.html'
def Blogpost(request,pk):
    form = CommentForm()
    post_comment = PostComments.objects.filter(Post_id=pk)
    try:
       cv = Post.objects.get(id=pk)
    except Post.DOESNOTEXIST:
        return HttpResponse('POST NOT FOUND')
    return render(request,'blogpost.html',{'post': cv, 'form': form, 'post_comment': post_comment})
def About(request):
    return render(request,'about.html')
# def Contactpage(request):
#     return render(request,'contact.html')
class Category(ListView):
    cs = Category.objects.all()
    model = Category
    template_name = 'category.html'

def contact(request):
    if request.method == 'POST':
        name = request.POST['username']
        email = request.POST['email']
        msg = request.POST['message']

        contact = Contact(name=name, email=email, message=msg)
        contact.save()
        return HttpResponse('Thanks for your response')
        # Contact.objects.create(name=name, email=email, message=msg)

    else:
        form= UserRegistrationForm()
        return render(request,'contact.html',context={'form':form})

class Signup(TemplateView):
    extra_context = {'form': UserRegistrationForm()}
    template_name = 'signup.html'


    def post(self,request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            if request.POST['password'] != request.POST['confirm_password']:
                return render(request,'signup.html',context={'form':form,'error':'Password and confirm password does not match'})

            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request,'signup.html',context={'form':form,'error':'Username already exists'})
            except:
                pass

            try:
                user = User.objects.get(email=request.POST['email'])
                return render(request,'signup.html',context={'form':form,'error':'Email already exists'})
            except:
                pass

            user = User.objects.create_user(username=request.POST['username'],email=request.POST['email'],password=request.POST['password'])
            user.save()

            return render(request,'signup.html',context={'form':form})
        else:
            return render(request,'signup.html',context={'form':form})


class signin(TemplateView):
    extra_context = {'form': UserSigninForm()}
    template_name = 'login.html'

    def post(self, request):
        form = UserSigninForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            try:
                user = authenticate(username=request.POST['username'], password=request.POST['password'])

                if user is not None:
                    login(request, user)

                    return render(request, 'home.html')
                else:
                    return render(request, 'login.html', context={'form': form, 'error': 'Invalid username or password'})
            except:
                pass

            return render(request, 'login.html', context={'form': form})
        else:
            return render(request, 'login.html', context={'form': form})

def logout_view(request):
    logout(request)
    return redirect ('home')


def post_create(request):
    if request.method == 'POST':
        form = PostBlogForm(request.POST,request.FILES)

        print(request.POST['title'])
        title = request.POST['title']
        description = request.POST['description']
        author = request.user
        category = request.POST['category']
        tags = request.POST['tags']
        status = request.POST['status']
        date = request.POST['date']
        user = request.user.username
        post = Post.objects.create(title=title, desc=description, author=author, Category_id=category,status=status,user=user,created_at=date)

        post.save()
        return HttpResponse('Successfull')
            # return redirect('home')
        # else:
        #     return render(request, 'create_blog.html', {'form': form})
    else:
        return render(request, 'create_blog.html', {'form': PostBlogForm()})
def update_blog(request,pk):
    postt = Post.objects.get(pk=pk)
    form = PostBlogForm(initial={'title':postt.title,'description':postt.desc,'image':postt.image,})

    if request.method=='POST':
        form = PostBlogForm(request.POST,request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            title = form.cleaned_data['title']
            desc = form.cleaned_data['description']
            active = form.cleaned_data['active']
            image = form.cleaned_data['image']
            Category: object = form.cleaned_data['category']
            user = request.user

            Post.title = title
            Post.desc = desc
            Post.active = active
            Post.image = image
            Post.Category = Category
            Post.user = user
            Post.save()
            return HttpResponse('Blog update successfully')
        else:
            return render(request,'create_blog.html',{'form':form,'error':'Invalid data'})

    return render(request,'update_blog.html',{'form':form})

def delete_blog(request,pk):
    postt = Post.objects.get(pk=pk)
    Post.delete()
    return HttpResponse('Blog deleted successfully')

def post_comments(request,pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            comment = form.cleaned_data['comment']
            post = Post.objects.get(id=pk)
            PostComments.objects.create(comment=comment,author=request.user,Post=post)
            return redirect('blogpost',pk=pk)

def like_post(request, pk):
    if request.user.is_authenticated:
        post = Post.objects.get(id=pk)
        if request.user in post.like_by.all():
        # post.like_by.remove(request.user)
          pass
        else:
         post.like_by.add(request.user)
        return redirect('home')
    else:
         return HttpResponse("you must be logged")

def dislike_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.user in post.like_by.all():
        post.like_by.remove(request.user)
    else:
        pass
    return redirect('home')

def search_query(request):

    if request.method == 'GET':

        q = request.GET.get('q')
        if q:
           postt = Post.objects.filter(desc__icontains=q)

        else:
            postt = Post.objects.all()

    return render(request, 'home.html', context={'post_list': postt})