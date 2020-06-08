from django.shortcuts import render,HttpResponse
from home.models import Contact
from django.contrib import messages
from blog.models import Post
import datetime


# Create your views here.
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
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() < 1:
        messages.error(request,'No search results found. Please refine your query!')
    params = {'allPosts':allPosts,'query':query}
    return render(request,'home/search.html',params)

