from django.shortcuts import render,HttpResponse
from home.models import Contact
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'home/home.html')
    # return HttpResponse("this is home")

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

