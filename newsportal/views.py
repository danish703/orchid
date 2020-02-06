from django.shortcuts import render,HttpResponse,redirect
from blog.models import Blog
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.forms import BlogForm

def about(request):
    return render(request,'about.html')


def views_more(request,id):
    data = Blog.objects.get(pk=id)
    context = {
        'blog':data
    }
    return render(request,'views_more.html',context)

#SELECT * FROM `blog`
def home(request):
    data =  Blog.objects.all() #SELECT * FROM `blog`
    context = {
        'blog':data
    }
    return render(request,'home.html',context)

def siginin(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        u = request.POST['username']
        p = request.POST['pass1']
        user = authenticate(username=u,password=p)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.add_message(request,messages.ERROR,"password does not match")
            return redirect('signin')

def signup(request):
    if request.method=='GET':
        return render(request,'signup.html')
    else:
        u = request.POST['username']
        e = request.POST.get('email')
        p1 = request.POST['pass1']
        p2 = request.POST['pass2']

        if p1==p2:
            u = User(username=u,email=e)
            u.set_password(p1)
            u.save()
            messages.add_message(request,messages.SUCCESS,"signup successfull")
            return redirect('signin')
        else:
            messages.add_message(request,messages.ERROR,"password does not match")
            return redirect('signup')


def signout(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def dashboard(request):
    data = Blog.objects.all()[::-1]
    context = {
        'blog':data
    }
    return render(request,'dashboard.html',context)

def create_post(request):
    form = BlogForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        form.save()
        messages.add_message(request,messages.SUCCESS,"Created successfully")
        return redirect('dashboard')
    context = {
        'form':form
    }
    return render(request,'create_post.html',context)


def editpost(request,id):
    data = Blog.objects.get(pk=id)
    form = BlogForm(request.POST or None,request.FILES or None,instance=data)
    if form.is_valid():
        form.save()
        messages.add_message(request,messages.SUCCESS,"update successfully")
        return redirect('dashboard')
    context = {
        'form':form
    }
    return render(request,'edit_post.html',context)

def deletepost(request,id):
    b = Blog.objects.get(pk=id)
    b.delete()
    messages.add_message(request,messages.SUCCESS,"successfully deleted")
    return redirect('dashboard')