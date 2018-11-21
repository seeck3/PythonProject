# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    
    return render(request, 'pages/index.html')

def registered(request):

    return render(request, 'pages/registered.html')

def user_process(request):

    action = request.POST['action']

    if action == "register":

        result = User.objects.register_validation(request.POST)

        if result[0]:

            request.session['id'] = result[1].id
            request.session['name'] = result[1].name

            return redirect("/registered")

        else:
            error_list = result[1]
            for error in error_list:
                messages.add_message(request, messages.ERROR, error)

            return redirect('/')
    
    if action == "login":

        result = User.objects.login_validation(request.POST)

        if result[0]:

            request.session['name'] = result[1].name
            request.session['id'] = result[1].id
            print result[1].id
            print result[1].name
            print request.session['id']
            return redirect("/dashboard")

        else:
            error_list = result[1]
            for error in error_list:
                messages.add_message(request, messages.ERROR, error)

            return redirect('/')

def dashboard(request):

    if 'id' not in request.session:
        return redirect("/")
    else:
        print request.session['id']

        context = {
            
            'mywish' : Items.objects.filter(uploaded_by_id = request.session['id'])|Items.objects.filter(wishes__wanter_id= request.session['id']),
            'otherwish' : Items.objects.exclude(uploaded_by_id = request.session['id']) & Items.objects.exclude(wishes__wanter_id= request.session['id'])
        }
        return render(request, "pages/dashboard.html", context)

def add_item(request):
    if 'id' not in request.session:
        return redirect("/")
    print request.session['id']
    return render(request, "pages/create_items.html")

def adding(request):
  
    action = request.POST['action']
    

    if action == "adding":
        
        result = Items.objects.item_validation(request.POST, request.session['id'])
        

        if result[0]:

            return redirect("/dashboard")

        else:
            error_list = result[1]
            
            for error in error_list:
                messages.add_message(request, messages.ERROR, error)

            return redirect('/add_item')

def wish_items(request, item_id):
    if 'id' not in request.session:
        return redirect("/")

    context = {
        'wishinfo' : Items.objects.get(id = item_id),
        'wishpeople' : Items.objects.get(id = item_id).wishes.all()
    }

    return render (request, "pages/show_items.html", context)

def wish(request, item_id):
    
    if 'id' not in request.session:
        return redirect("/")
    elif Wish.objects.filter(wanter_id = request.session['id'], wishitem_id = item_id):
        return redirect("/dashboard")
    else:
        Wish.objects.create(wanter_id = request.session['id'], wishitem_id = item_id)
    
    return redirect("/dashboard")

def destroy(request, id):
    Wish.objects.get(wanter_id = request.session['id']).delete()
    return redirect('/dashboard')

def remove(request, id):
    
    Items.objects.get(id = id).delete()

    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect("/")