from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
def mycustomvalidator(value):
    if len(value)>5:
        return True
    else:
        raise ValidationError("must have more then 5 characters")

def val2(value):
    if '@' in value:
        raise ValidationError("tilte can to have @ character")
    else:
        return True

class Cateogry(models.Model):
    title = models.CharField(max_length=100,unique=True,validators=[mycustomvalidator,val2])

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='blog/',null=True,blank=True)
    publish_date = models.DateField(auto_now=True)
    category = models.ForeignKey(Cateogry,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "blog"
