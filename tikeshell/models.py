from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from random import randint
from django.utils import timezone
import datetime 
from StringIO import StringIO
from tikeshell.utils import qrcodeGenerator
from django.http import HttpResponse
today=datetime.datetime.today


# Create your models here.
class Keyword(models.Model):
    word=models.CharField(max_length=100)
    def __str__(self):
        return self.word

class Review(models.Model):
    source=models.CharField(max_length=100)
    text=models.TextField()
    url=models.CharField(max_length=200)
    def __str__(self):
        return self.text[:20]+'...'

class Picture(models.Model): #add the thumb stuff
    image=models.ImageField()#upload_to='photos' ? #thumbfield
    alt_text=models.TextField()
    def __str__(self):
        return self.alt_text

class Account(models.Model):
    user=models.ForeignKey(User)
    full_name=models.CharField(max_length=200)
    phone_number=models.BigIntegerField(blank=True)
    email=models.EmailField(blank=True)
    #profile_pic=models.ImageField() #maybe a field of a picture #or avatar
    #put fav_tags,fav_keywords,fav_events?
    
    def __str__(self):
        return self.full_name


class Category(models.Model):
    category_title=models.CharField(max_length=100)#changed to this dumb name for the sake of a better representation in the admin filters
    description=models.TextField()
    class meta:
        plural='Categories' #not working why?
    def __str__(self):
        return self.category_title

class Venue(models.Model):
    name=models.CharField(max_length=100)
    capacity=models.IntegerField()
    location=models.CharField(max_length=100)
    description=models.TextField()
    hallmap=models.TextField()#still choosing between a big array/matrix or a markup/xml/json
    #imgs='' #many to many rel with Picture?
    def __str__(self):
        return self.name

#efficient here because you can reuse some of the types
class tickettype(models.Model):
    tike_type = models.CharField(max_length=100)
    amount = models.IntegerField()
    def __str__(self):
        return self.tike_type

class Show(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category)
    description = models.TextField()
    imageurl = models.CharField(max_length=200, default="0")#change to ImageField,or folder?
    date = models.DateTimeField(default=today())
    venue = models.ForeignKey(Venue)
    tickets_no = models.IntegerField()
    #i use BigInt because i'm optimistic about our popularity :)
    likes=models.BigIntegerField(default=randint(1000,2000))
    #bought_tickets=models.IntegerField(default=0) #calculate from tickets
    views=models.BigIntegerField(default=randint(2000,3000))#randint(int(self.likes),int(int(self.likes)+1000))) #since views must be greater that likes
    stars=models.IntegerField(default=randint(5,10))#out of 10
    tickettypes=models.ManyToManyField(tickettype)
    reviews=models.ManyToManyField(Review)
    #organizer=models.ForeignKey(SellerAccount) #discuss this with team first #have an account or not? we can name this account SellerAccount
    tags=models.ManyToManyField(Keyword)
    '''
    posters a variant of manytomany rel with pictures
    include or not?
    '''
    def __str__(self):
        return self.title
    

class Admin:
    pass
 #is it one org or many can organize one so maybe put Show to manage this
class SellerAccount(Account):
    hosted_shows=models.ManyToManyField(Show)
    introduction=models.TextField()
    def __str__(self):
        return self.full_name
#again for a good usage of resources we don't save tickets with relations
#we have a dilemna should we use users or just plain entry forms?
#gonna use users for non users we wiil save with not_user set to true
#the above is just lack of time we could have set a new user and 
#deleted him after the transaction

class Ticket(models.Model):
    event_id=models.BigIntegerField() #because names overlap #thinking on making this a foreignKey
    pin=models.CharField(max_length=6)#upgrade at 6*(10**26)th ticket
    phone_number=models.BigIntegerField()
    email=models.EmailField(blank=True)
    full_name=models.CharField(max_length=200)
    tickettype_id=models.BigIntegerField()
    user_id=models.BigIntegerField()#user_id,"-1" when not a user
    payed=models.BooleanField(default=False)
    used=models.BooleanField(default=False)
    is_user=models.BooleanField(default=True)
    date=models.DateTimeField(default=today())
    def __str__(self):
        return self.full_name+": "+self.pin
    #this here produce the qrcode was wrote for security reasons
    #the issue is you can't output directly an httpresponse in a html doc
    #when solved there will be no vurnelabilities on the qrcode generation
    def _save_to_string(self,img):
        obj=StringIO()
        img.save(obj,format='PNG',quality=90)
        obj.seek(0)
        return obj.read()
    def render_qrcode(self):
        text='name: %s event_id: %s pin: %s' % (self.full_name,self.event_id,self.pin) #encrypt in some ways
        qrcode=self._save_to_string(qrcodeGenerator.init(text))
        return HttpResponse(qrcode,content_type='image/png')

class comment(models.Model):
    #idcomment= models.CharField(max_length= 10)
    text= models.CharField(max_length= 500)
    event= models.ForeignKey(Show)
    user = models.ForeignKey(User)
    date = models.DateTimeField()

    def __str__(self):
        return self.text[:20]+'...'

class stats(models.Model):
    None
    #put things as web_views,mem_usage[?],
#classes to represent models in the admin page
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id','user','full_name','phone_number')
    search_fields = ('user__username','full_name','phone_number','email')

class ShowAdmin(admin.ModelAdmin):
    list_display = ('id','title','category','venue','date')
    search_fields = ('id','title','category','tags__word','venue__name','description')
    list_filter=('category__category_title','date')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('user_id','full_name','pin','phone_number','date')
    search_fields = ('full_name','pin','phone_number','email','event_id','tickettype_id')
    list_filter=('event_id','tickettype_id','used','is_user','date')

