from __future__ import unicode_literals

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.db import models

# Create your models here.
class UserManager(models.Manager):
	def validate_user(request, postData):
		errors = {}


		# validate Name
		if len(postData['name']) < 2 or not postData['name'].isalpha():
			if len(postData['name']) < 2:
				errors['name_length'] = "Name must be at least two characters."
			if not postData['name'].isalpha():
				errors['name_alpha'] = "Name can only contain letters."

	

		# validate email
		try:
			validate_email(postData['email'])
		except ValidationError:
			errors['email'] = "This is not a valid email."
		else:

			if User.objects.filter(email=postData['email']):
				errors['email'] = "This user already exists."


		# validate password
		if len(postData['password']) < 8:
			if len(postData['password']) < 8:
				errors['password_length'] = "Password must be at least 8 characters."

		# check if passwords match
		if postData['password'] != postData['confirm_pw']:
			errors['confirm_pw'] = "Passwords must match"


		return errors

class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = UserManager()

class AuthorManager(models.Manager):
	def validate_author(request, postData):
		errors = {}
		return errors

class Author(models.Model):
	author = models.CharField(max_length=255)

	objects = AuthorManager()


class BookManager(models.Manager):
	def validate_book(request, postData):
		errors = {}
		return errors

class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.ForeignKey(Author, related_name="books")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = BookManager()

class ReviewManager(models.Manager):
	def validate_review(request, postData):
		errors = {}
		return errors

class Review(models.Model):
	rating = models.IntegerField()
	review = models.TextField()
	reviewer = models.ForeignKey(User, related_name="reviews")
	book = models.ForeignKey(Book, related_name="reviews")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = ReviewManager()






