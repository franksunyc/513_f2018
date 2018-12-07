from django.db import models

# Create your models here.
#class Zhuce(models.Model):
   # user=models.CharField(Max_length=20)
   # pwd=models.CharField(Max_length=32)

class Post(models.Model):
    # 标题
    name = models.CharField(max_length=20 ,default=None)
    img_url = models.ImageField(upload_to='img',default=None)
    address = models.CharField(max_length=45,default=None)
    author = models.CharField(max_length=45,default=None)
    categories = models.CharField(max_length=45,default=None)


    # 其他属性

    def __str__(self):
        return self.name


