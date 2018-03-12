from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def index(request):
	return render(request, 'book_reviews/index.html')

def register(request):
	return redirect('/')

def login(request):
	return redirect('/')