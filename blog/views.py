from django.shortcuts import render,HttpResponse,redirect
from blog.models import Post,BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    #for latest blog show first
    allPosts = allPosts.order_by('-timeStamp')
    context = {'allPosts':allPosts}
    return render(request,'blog/blogHome.html',context)

def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    #whenever user comes to the post view will increase by one
    post.views=post.views+1 
    post.save()

    if post is None:
        return HttpResponse('<h2>404 Page Not Found!</h2>')
    comments = BlogComment.objects.filter(post=post, parent=None)
    comments= comments.order_by('-timeStamp')
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replies = replies.order_by('-timeStamp')

    #creating reply dictionary (saparating each comment's replies)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'post':post, 'comments':comments, 'replies':replies, 'replyDict':replyDict}
    return render(request,'blog/blogPost.html',context)

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')  #parentComment serial no 

        #if it is comment then parentSno == "" else reply and it will have id of its parent comment
        if parentSno == "":
            blogComment = BlogComment(comment = comment, user=user, post = post)
            blogComment.save()
            messages.success(request, 'Your Comment has been posted successfully!')
        else :
            parentComment = BlogComment.objects.get(sno = parentSno)
            blogComment = BlogComment(comment = comment, user=user, post = post, parent=parentComment)
            blogComment.save()
            messages.success(request, 'Your Reply has been posted successfully!')
            
        return redirect(f"/blog/{post.slug}")
    else:
        return HttpResponse('<h2>404 Page Not Found!</h2>')
    

