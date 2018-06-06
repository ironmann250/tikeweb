from django.shortcuts import render
from tikeshell.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from pprint import pprint as pp
import time,json,string,random
from django.contrib.auth import authenticate,login
from StringIO import StringIO
from tikeshell.utils import qrcodeGenerator
#utility functions
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

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    generate a 6 character pi that is unique in db/ticket
    """
    pin=''.join(random.choice(chars) for _ in range(size))
    if Ticket.objects.filter(pin=pin).count() !=0:
        id_generator()
    else:
        return pin

def randomize_users(init,size=6, chars=string.ascii_uppercase + string.digits):
    id_=''.join(random.choice(chars) for _ in range(size))
    if User.objects.filter(username=init+id_).count() !=0:
        randomize_users(init)
    else:
        return init+id_
def loginpg(request):
    print request.POST.keys()
    if 'email' not in request.POST.keys():
        return render(request,'html/login.html',locals())
    email=request.POST['email']
    pwd=request.POST['password']
    if True:
        uname=Account.objects.get(email=email).user.username
        user=authenticate(request,username=uname,password=pwd)
        if user:
            login(request,user)
            return HttpResponseRedirect("/dashboard/"+str(user.id))
        else:
            err_msg='incorrect password'
            return render(request,'html/login.html',locals())
    if False:# Exception as x:
        print x
        err_msg='incorrect login info'+str(x)
        return render(request,'html/login.html',locals())
    print user
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
# Create your views here vyhvkfghvmvm
def home(request):
    return render(request,'html/index.html',{})
def event(request): 
    return render(request,'html/event.html',{})
def category(request,id):
    #get events in that category
    #order by likes or such things
    return render(request,'html/category.html',{})

def search(request):
    q=request.GET['q']
    event_query=Q(Q(title__contains=q)|Q(description__contains=q))
    org_query=Q(Q(full_name__contains=q)|Q(introduction__contains=q))
    for word in q.split(' '):
        event_query |= Q(Q(title__contains=word)|Q(description__contains=word))
        org_query |=Q(Q(full_name__contains=word)|Q(introduction__contains=word))
    event_results=Show.objects.filter(event_query)#maybe put tags and reviews too
    organizers_results=SellerAccount.objects.filter(org_query)
    #mix queuries and sort them 
    print q,'\n',event_results,'\n',organizers_results
    return render(request,'html/search.html',locals())

def subscribe(request):
    #error checking/validation
    print request.POST.keys()
    if 'fname' in request.POST.keys():
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        phone=request.POST['phone']
        pwd=request.POST['pwd']
        for tag in ['fname','lname','email','phone','pwd','repeater']:
            if tag not in request.POST.keys():
                err_msg="Fill all fields!"
                return render(request,'html/createacc.html',locals())
        if Account.objects.filter(email=email).count() !=0:
            err_msg='Email already Registered'
            return render(request,'html/createacc.html',locals())
        if Account.objects.filter(phone_number=phone).count() !=0:
            err_msg='Phone number already Registered'
            return render(request,'html/createacc.html',locals())
        if request.POST['pwd']!=request.POST['repeater']:
            err_msg='Passwords do not match'
            return render(request,'html/createacc.html',locals())
        user = User.objects.create_user(username=randomize_users(fname+lname),
            email=email,
            password=pwd)
        newaccount=Account.objects.create(user=user,full_name=fname+' '+lname,phone_number=phone,email=email)
        newaccount.save()
        return HttpResponseRedirect("/dashboard/"+str(user.id))
    else:
        return render(request,'html/createacc.html')
def view_event(request,event_id):
    event=Show.objects.get(id=event_id)
    organizer=SellerAccount.objects.get(hosted_shows=event)
    ticket_types=event.tickettypes.iterator()
    tickets_sold=Ticket.objects.filter(event_id=event.id).count()
    #new default should be 6 event as in view_ticket
    similar_events=get_similar_events(event,3)
    return render(request,'html/view_event.html',locals())
@login_required 
def cart(request): #cart at dashboard
    return render(request,'html/cart.html') 
def support(request):
    return render(request,'html/support.html')
#@login_required 
@login_required 
def requestbuy(request):
    #output tickets not yet payed for json
    #get an input of tickets choose
    #for all of those tickets apply buy_ticket()

    #buy_ticket() will make a new entry and send a msg
    #__^ in version 2 ,multiple ticket per cart
    #get user data
    #request.user...
    user = request.user
    account=Account.objects.get(user=user)
    ticket_type=request.POST['types']
    amount=request.POST['num_tickets']
    event_id=request.POST['transaction_id']
    price=tickettype.objects.get(id=ticket_type).amount
    type_=tickettype.objects.get(id=ticket_type).tike_type
    event=Show.objects.get(id=event_id)
    tot_price=float(price)*int(amount)
    last_price=(tot_price*11)/10 #tot_price+10%
    pin_=id_generator()
    print ticket_type,amount,event_id
    newticket= Ticket.objects.create(event_id=event_id,pin=pin_,full_name=account.full_name,tickettype_id=ticket_type,phone_number=account.phone_number,user_id=user.id)
    newticket.save()
    return render(request,'html/checkout.html',locals())

def pytsys(request):
    redirect_url=request.GET['redirect-url']
    return render(request,'html/pytsys.html',locals())

def validate(request):
    pin_=request.GET['pin']
    ticket=Ticket.objects.get(pin=pin_)
    ticket.payed=True
    ticket.save()
    #add sms stuff
    if ticket.user_id>0:
         return HttpResponseRedirect("/dashboard/"+str(ticket.user_id))
    else:
         return HttpResponseRedirect("/")

@login_required
def dashboard(request,user):
    #derive it from django.auth
    user = request.user
    basket=Ticket.objects.filter(user_id=user.id,payed=False)
    my_tickets=Ticket.objects.filter(user_id=user.id,payed=True)
    #similar_events=get_similar_events(event,6) #PUBLICITY_EVENTS
    return render(request,'html/dashboard.html',locals())

@login_required 
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
def api_update_shows(request):#put a field of a password
    '''
    add info in db/shows, checks first if info is already in
    returns item.id if update and 0 if not
    '''
    '''
    TODO: make this functional
    i have skipped this because updating the db from onsite's data
    requires handling many uncertainities will work on this on v2
    '''
    fields={'id':'','title':'','category':'','desc':'','image':'','date':'','venue_info':'','num':'','tickettypes_info':'','organizer_info':''}
    for key in request.GET.keys():
        if key in fields.keys() and request.GET[key] not in ['']:
            fields[key]=request.GET[key]
    return JsonResponse({'info':'TODO'})

def pin_lookup(request):
    fields={'event':'','full_name':'','phone_number':''
    ,'tickettype':'','used':'','date':'','info':'0'}
    try:
        ticket=Ticket.objects.get(request.GET[pin].upper())
        vnt_nm=Show.objects.get(ticket.event_id).title
        tickettype_=tickettype.objects.get(ticket.tickettype_id).tike_type
        fields={'event':vnt_nm,'full_name':ticket.full_name,
        'phone_number':ticket.phone_number,'tickettype':tickettype_,
        'used':ticket.used,'date':ticket.date,'info':'1'}
        return JsonResponse(json.dumps(fields))
    except Exception as e:
        print e
        return JsonResponse(json.dumps(fields)) 

def sitemap(request):
	return render(request,'html/sitemap.html')
def music(request):
	return render(request,'html/serve.html')



