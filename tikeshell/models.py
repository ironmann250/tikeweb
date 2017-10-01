from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class showtype(models.Model):
    idshowtype = models.CharField(max_length= 10, primary_key= True)
    showtype = models.CharField(max_length= 20)
    
    def __str__(self):
        return self.showtype


class Show(models.Model):
    idshow = models.CharField(max_length=10,primary_key=True)
    title = models.CharField(max_length=100)
    showtype = models.ForeignKey(showtype)
    Description = models.TextField()
    imageurl = models.CharField(max_length=200, default="0")
    date = models.DateTimeField()
    venue = models.CharField(max_length=100, default="0")
    tickets_no = models.IntegerField()

    def __str__(self):
        return self.title


class Admin:
    pass


class profile(models.Model):
    seller = models.ForeignKey(User)
    iduser = models.CharField(primary_key=True, max_length = 40)
    event = models.ForeignKey(Show, default="0")


''' @receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
	'''


class Admin:
    pass


class tickettype(models.Model):
    tike_types = models.CharField(max_length=30)
    event = models.ForeignKey(Show)
    amount = models.IntegerField()
    idticktype = models.CharField(primary_key=True,max_length =30)

    def __str__(self):
        return self.tike_type


class Admin:
    pass

class comment(models.Model):
    idcomment= models.CharField(max_length= 10)
    text= models.CharField(max_length= 500)
    event= models.ForeignKey(Show)
    user = models.ForeignKey(User)
    date = models.DateTimeField()

    def __str__(self):
        return self.text
