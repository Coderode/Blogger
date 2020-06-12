from django.contrib import admin
from blog.models import Post,BlogComment
# Register your models here.

admin.site.register(BlogComment)

#to inject the tinyMCE js file in the admin panel page of the post modal
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ("tinyInject.js",)


#this decorator also register the Post modal and changes the admin of this modal