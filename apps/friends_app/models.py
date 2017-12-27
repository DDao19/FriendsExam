# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[ .a-zA-Z0-9\s]+$')

# Create your models here.
class UserManager(models.Manager):
    def validate_registration(self, form_data):
        errors = []
        user_dob = datetime.strptime(form_data['dob'], "%Y-%m-%d")
        current_date = datetime.now()

        if len(form_data['name']) < 3:
            errors.append("Name is required.")
        if len(form_data['alias']) < 2:
            errors.append("Alias must be at least 2 characters.")
        #check if name and alias is valid
        if not re.match(NAME_REGEX, form_data['name']):
            errors.append('Invalid Name.')
        if not re.match(NAME_REGEX, form_data['alias']):
            errors.append('Invalid Alias.')
        if len(form_data['email']) == 0:
            errors.append("Email is required.")
        #check if valid email
        if not re.match(EMAIL_REGEX, form_data['email']):
            errors.append("Invalid email.")
        if len(User.objects.filter(email=form_data['email'])) > 0:
            errors.append("Email already in use.")
        if len(form_data['password']) == 0:
            errors.append("Password is required.")
        if form_data['password'] != form_data['confirm_password']:
            errors.append("Password must match.")
        if len(form_data['dob']) == 0:
            errors.append('Must include date of birth')
        if user_dob > current_date:
            errors.append("DOB cannot be current date")

        return errors

    def validate_login(self, form_data):
        errors = []
        if len(form_data['email']) == 0:
            errors.append("Enter your email.")
        if len(form_data['password']) == 0:
            errors.append("Enter your password.")
        if len(self.filter(email=form_data['email'])) > 0:
            user = self.filter(email=form_data['email'])[0]
            if not bcrypt.checkpw(form_data['password'].encode(), user.password.encode()):
                errors.append('Email or Password is incorrect.')
        else:
            errors.append('Email or Password is incorrect.')

        if errors:
            return errors
        return user


    def create_user(self, form_data):
        hashedpw = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt(6))
        return User.objects.create(
            name = form_data['name'],
            alias = form_data['alias'],
            email = form_data['email'],
            password = hashedpw,
            date_of_birth = form_data['dob']
        )



class User(models.Model):
    name = models.CharField(max_length=40)
    alias = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    date_of_birth = models.DateField()
    favorites = models.ManyToManyField("Friend", related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return "{}, {}, {}, {}".format(self.name, self.alias, self.email, self.date_of_birth)


class Friend(models.Model):
    friendster = models.ForeignKey(User, related_name="friends")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}, {}".format(self.author, self.content)
