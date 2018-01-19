from django.shortcuts import render
from tikeshell.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from pprint import pprint as pp
import time
from StringIO import StringIO
from tikeshell.utils import qrcodeGenerator
#utility functions
SHARED_VALS={'qr_code_info':'place_holder'}#not needed
def sort(_list):
    _list.sort()
    return(_list)

def highest_vals_calc(vals,lookup=3):
    vals.sort(reverse=True)
    return vals[:lookup]

def save_to_string(img):
    obj=StringIO()
    img.save(obj,format='PNG',quality=90)
    obj.seek(0)
    return obj.read()

def get_similar_events(event,choices=3):
    '''
    get event that have at least one tag in common
    choose 3{?} of which have the most common tags
    i have used iterators as oftenly possible as i can 
    to reduce the time it takes per loop but still it loops alot
    i have introduced a timer that will stop the main big loop after 0.5 sec max
    so it won't ever cause serious trouble, use less memmory too than before
    '''
    tags=event.tags
    same_tag={}
    begin_time=time.time()
    for tag in tags.iterator():
        if time.time()-begin_time>0.5: #no matter what size spend only 0.5 sec here, dumb i know :(
            break
        #maybe by using select_related[?] we can go still faster[?]
        for event_ in tag.show_set.all().exclude(id=event.id):
            same_tag.setdefault(event_.id,0)
            same_tag[event_.id]+=1

    query=Q()
    highest_vals=highest_vals_calc(same_tag.values(),choices)
    for key,val in same_tag.iteritems(): #use iterator cause it's faster that items list
        if val in highest_vals:
            query |= Q(id=key)

    return Show.objects.filter(query)
#security vurnelability here ,if you where to generate random pins and requests their qrcodes...
#{don't consider} this is part of our api, so we request an api_token, plus we get someone to blame on error :)
#will look into a more serious security for this func
#this ain't a fix at all because if we put a token everyone can see ours when we call it
#for lack of a better security idea i will pass all of the text to this func,no way can they hack this
#anyway feel free to improve on this, and don;t make something that write qrcode on the filesys
#this func was made entirely so we generate qrcodes without the need of any temp filesys
#last try is to make this as an object of the Ticket models class and call it on the ticket simply
#this will not show any vurnelabilities
#tried it but we can't output directly a httpresponse in html
def render_qrcode(request,text): #this is considered a helper function not really a view func
    '''
    #this here is just for the idea of the previous and projected work that had security vurnelabilities
    if not api_token: #verify the token
        return HttpResponse('<h2>Not Allowed</h2>',content_type='text/html') #replace with a 404
    try:
        ticket=Ticket.objects.get(pin=ticket_pin)
    except:
        return HttpResponse('<h2>None</h2>',content_type='text/html') #replace with a 404
    event_name=Show.objects.get(id=ticket.event_id)
    text='name: %s event: %s pin: %s' % (ticket.full_name,event_name,ticket.pin)'''
    qrcode=save_to_string(qrcodeGenerator.init(text)) #render and save it in mem
    response=HttpResponse(qrcode,content_type='image/png') 
    return response
#next is the function that renders the hallmap
def render_hallmap(event):
    color_keys={}
    None
# Create your views here.

def home(request):
    return render(request,'html/index.html',{})
def event(request):
    return render(request,'html/event.html',{})
def category(request,id):
    #get events in that category
    #order by likes or such things
    return render(request,'html/category.html',{})

def search(request,q):
    event_query=Q(Q(title__contains=q)|Q(description__contains=q))
    org_query=Q(Q(full_name__contains=q)|Q(introduction__contains=q))
    for word in q.split(' '):
        event_query |= Q(Q(title__contains=word)|Q(description__contains=word))
        org_query |=Q(Q(full_name__contains=word)|Q(introduction__contains=word))
    event_results=Show.objects.filter(event_query)#maybe put tags and reviews too
    organizers_results=SellerAccount.objects.filter(org_query)
    #mix queuries and sort them 
    print event_results,'\n',organizers_results
    return render(request,'html/search.html',locals())

def createacc(request):

	return render(request,'html/createacc.html')
def view_event(request,event_id):
    event=Show.objects.get(id=event_id)
    organizer=SellerAccount.objects.get(hosted_shows=event)
    ticket_types=event.tickettypes.iterator()
    tickets_sold=Ticket.objects.filter(event_id=event.id).count()
    #new default should be 6 event as in view_ticket
    similar_events=get_similar_events(event,3)
    return render(request,'html/view_event.html',locals())
#@login_required 
def cart(request): #cart at dashboard
    return render(request,'html/cart.html') 
def support(request):
    return render(request,'html/support.html')
#@login_required 
def requestbuy(request):
    #output tickets not yet payed for json
    #get an input of tickets choose
    #for all of those tickets apply buy_ticket()

    #buy_ticket() will make a new entry and send a msg
    return render(request,'html/checkout.html')
#@login_required
def dashboard(request,user):
    #derive it from django.auth
    basket=Ticket.objects.filter(user_id=user,payed=False)
    my_tickets=Ticket.objects.filter(user_id=user,payed=True)
    #similar_events=get_similar_events(event,6) #PUBLICITY_EVENTS
    return render(request,'html/dashboard.html',locals())

def view_ticket(request,event_id):
    event=Show.objects.get(id=event_id)
    ticket_types=event.tickettypes.iterator()
    reviews=event.reviews.iterator()
    similar_events=get_similar_events(event,6)
    print event.venue.name
    #some hallmap processing here!
    #handle post events
    #when ticket specs selected and number 
    #create a new entry for all and mark them as not yet paid for
    return render(request,'html/view_ticket.html',locals())
def ticket(request,ticket_pin):
    #ticket_pin='A1B2E3'
    ticket=Ticket.objects.get(pin=ticket_pin)
    event=Show.objects.get(id=ticket.event_id)
    tickets_avail=event.tickets_no-Ticket.objects.filter(event_id=event.id).count()
    tickets_sameName=Ticket.objects.filter(full_name=ticket.full_name).count()
    tickets_sameName_used=Ticket.objects.filter(full_name=ticket.full_name,used=True).count()
    qr_code_info='name: %s event: %s pin: %s' % (ticket.full_name,event.title,ticket.pin) #put some kind of encryption here
    return render(request,'html/ticket.html',locals())
def sitemap(request):
	return render(request,'html/sitemap.html')
def music(request):
	return render(request,'html/serve.html')



