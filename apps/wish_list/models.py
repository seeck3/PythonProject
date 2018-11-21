# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt

class UserManager(models.Manager):
    def register_validation(self, form_data):

        errors = []

        name = form_data['fullname']
        username = form_data['username']
        password = form_data['password']
        con_pw = form_data['confirm']
        date = form_data['date']

        if not name:
            errors.append("Name is required.")
        elif len(name) < 3:
            errors.append("Name must be at least 3 characters.")
        elif not name.isalpha():
            errors.append("Name cannot contain numbers.")

        if not username:
            errors.append("Username is required.")
        elif len(username) < 3:
            errors.append("Username must be at least 3 characters.")
        else:
            users = User.objects.filter(username = username)
            if users:
                errors.append("Username already exists. Please Log in.")

        if not password:
            errors.append("Password is required.")
        elif len(password) < 8:
            errors.append('Password must be at least 8 characters')
        if not con_pw:
            errors.append("Confirm password is required.")
        if password != con_pw:
            errors.append("Passwords must match.")

        if not date:
            errors.append("Please, enter Date.")

        if not errors:
            hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = User.objects.create(name=name, username=username, password=hash_pw)
            return (True, user)
        else:
            return (False, errors)

    def login_validation(self, form_data):
        errors = []

        username = form_data['username']
        password = form_data['password']

        if not username:
            errors.append('Username is required')
        else:
            users = User.objects.filter(username = username)
            if not users:
                errors.append('Username does not exist. Please register.')
            else:
                user = users[0]
                if not bcrypt.checkpw(password.encode(), user.password.encode()):
                    errors.append("Password does not match. Please check again.")
        if not password:
            errors.append('Password is required.')

        if not errors:
            user = User.objects.get(username = username)
            return (True, user)
        else:
            return (False, errors)


class ItemManager(models.Manager):
    def item_validation(self, form_data, id):

        errors = []

        items = form_data['item']
        # this_user = User.objects.filter(id=user_id)

        if not items:
            errors.append('Please, enter your wish item.')
        elif len(items) < 3:
            errors.append('Item must be at least 3 characters.')
        else:
            checkitem = Items.objects.filter(item = items)
            if checkitem:
                errors.append("Item already exists.")
       

        if not errors:
            item = Items.objects.create(item=items, uploaded_by_id = id)
            return (True, item)
        else:
            return (False, errors)




# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()



class Items(models.Model):
    item = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name="uploadeditem")

    objects = ItemManager()

class Wish(models.Model):
    wishitem = models.ForeignKey(Items, related_name="wishes")
    wanter = models.ForeignKey(User, related_name="wisher")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)