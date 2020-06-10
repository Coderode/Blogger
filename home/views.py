from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
import datetime


# Create your views here.

#HTML pages
def home(request):
    newPosts = Post.objects.order_by('-timeStamp')[:5]
    context = {'newPosts':newPosts}
    return render(request,'home/home.html',context)

def contact(request):
    if request.method=="POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        contact = Contact(name=name,email=email,phone=phone,content=content)
        if(len(name)<3 or len(email)<4 or len(content)<10 or len(phone)<10):
            messages.error(request,'Please fill your details correctly :-(')
            messages.error(request,'name length > 3 , email length>4 , content length > 10, phone >= 10')
        else:
            contact.save()
            messages.success(request, 'Your messages has been successfully sent :-)')
    return render(request,'home/contact.html')

def about(request):
    return render(request,'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
        allPosts = allPosts.union(allPostsAuthor)
    if allPosts.count() == 0:
        messages.error(request,'No search results found. Please refine your query!')
    params = {'allPosts':allPosts,'query':query}
    return render(request,'home/search.html',params)

#authentication APIs
def handleSignup(request):
    if request.method == 'POST':
        #get the post parameter
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        #checks for user inputs
        # username length and alphanumeric
        errors = []
        if len(username) > 10 or len(username) < 3 or not username.isalnum(): 
            errors.append('Username length should be between 3 and 10 and it should be alphanumeric!')
        if len(password1) < 5 or len(password1) > 30:
            errors.append('Password length should be between 4 and 30!')
        if len(fname) <3:
            errors.append('Please enter a valid name!')
        if password1 != password2:
            errors.append('Passwords should Match!')

        #if any error occures redirect to home
        if len(errors) > 0 :
            for error in errors:
                messages.error(request,error)
            return redirect('home')

        #else create the user
        #create the user
        try:
            myuser = User.objects.create_user(username,email,password1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request,'Your Kolaborate Account has been successfully created! Now can login Now :-)')
        except:
            messages.error(request,'Username already exist please enter another unique username!')
        return redirect('home')
    else:
        return HttpResponse('<h2>404 - Page Not Found</h2>')

def handleLogin(request):
    if request.method == 'POST':
        #get the post parameters
        username = request.POST['loginusername']
        password = request.POST['loginpassword']

        user = authenticate(username= username, password= password)
        if user is not None:
            login(request,user)
            messages.success(request, 'Welcome '+username+', You are successfully logged In!')
            return redirect('home')
        else:
            messages.error(request,'Invalid credentials, Please try again!')
            return redirect('home')
    else:
        return HttpResponse('<h2>404 - Page Not Found</h2>')

def handleLogout(request):
    logout(request)
    messages.success(request, 'You are successfully logged out!')
    return redirect('home')