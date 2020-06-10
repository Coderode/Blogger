from django.shortcuts import render,HttpResponse,redirect
from blog.models import Post,BlogComment
from django.contrib import messages

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts':allPosts}
    return render(request,'blog/blogHome.html',context)

def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post)
    comments= comments.order_by('-timeStamp')
    context = {'post':post, 'comments':comments}
    return render(request,'blog/blogPost.html',context)

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)

        blogComment = BlogComment(comment = comment, user=user, post = post)
        blogComment.save()
        messages.success(request, 'Your comment has been posted successfully!')
            # messages.error(request,'Please login/signup first to post a comment or reply!')

    return redirect(f"/blog/{post.slug}")

