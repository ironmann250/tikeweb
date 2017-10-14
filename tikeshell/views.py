from django.shortcuts import render
from tikeshell.models import showtype,Show,comment,tickettype
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

def home(request):
    return render(request,'html/index.html',{})
def event(request):
    return render(request,'html/event.html',{})
def category(request):
    return render(request,'html/category.html',{})
def search(request):
    return render(request,'html/search.html')
def createacc(request):
	return render(request,'html/createacc.html')
def view_event(request):
	return render(request,'html/view_event.html')
#@login_required 
def cart(request):
    return render(request,'html/cart.html') 
def support(request):
    return render(request,'html/support.html')
#@login_required 
def requestbuy(request):
    return render(request,'html/checkout.html')
def dashboard(request):
	return render(request,'html/dashboard.html')
def view_ticket(request):
	return render(request,'html/view_ticket.html')
def ticket(request):
    return render(request,'html/ticket.html')
def sitemap(request):
	return render(request,'html/sitemap.html')
def music(request):
	return render(request,'html/serve.html')



