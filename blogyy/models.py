from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Category(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
       return self.name+' '+str(self.id)

class Tag(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
     return self.name

class Post(models.Model):

    title=models.CharField(max_length=100)
    desc=models.TextField()
    image = models.ImageField(upload_to='image/',null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    Category=models.ForeignKey(Category,on_delete=models.CASCADE)
    File=models.FileField(upload_to='blog/file',default='')
    active = models.BooleanField(default=True)
    user = models.CharField(max_length=100,null=True,blank=True)
    status=models.CharField(max_length=1,choices=(('d','Draft'),('p',';Published')),default='d')
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    like_by = models.ManyToManyField(User,related_name='liked_by',blank=True)
    def __str__(self):
         return self.title




class Contact(models.Model):
        name = models.CharField(max_length=200)
        email = models.EmailField(max_length=200)
        message = models.TextField()

        def _str_(self):
            return self.name
class PostComments(models.Model):
    Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment