from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
	return render(request, 'book_reviews/index.html')

def register(request):
	errors = User.objects.validate_user(request.POST)

	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error)
		return redirect('/')


	return redirect('/')

def login(request):
	return redirect('/')