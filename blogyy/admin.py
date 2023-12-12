from django.contrib import admin
from .models import Post
from .models import Category
from .models import Contact
from.models import Tag,PostComments

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Contact)

admin.site.register(Tag)
admin.site.register(PostComments)