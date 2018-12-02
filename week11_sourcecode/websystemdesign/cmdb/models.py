from django.db import models

# Create your models here.
#class Zhuce(models.Model):
   # user=models.CharField(Max_length=20)
   # pwd=models.CharField(Max_length=32)

class Post(models.Model):
    # 标题
    name = models.CharField(max_length=20)
    img_url = models.ImageField(upload_to='img')
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    zipcode = models.ImageField(max_length=10)
    author = models.CharField(max_length=45)
    categories = models.CharField(max_length=45)


    # 其他属性

    def __str__(self):
        return self.name


