from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
	if request.session.get('id') != None:
		return redirect('/books')

	return render(request, 'book_reviews/index.html')

def register(request):
	errors = User.objects.validate_user(request.POST)

	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error)
		return redirect('/')
	else:
		name = request.POST['name']
		alias = request.POST['alias']
		email = request.POST['email']
		password = request.POST['password']
		hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

		User.objects.create(name=name, alias=alias, email=email, password=hashed_pw)

		u = User.objects.get(email=email)
		request.session['id'] = u.id

		return redirect('/books')

def login(request):

	email = request.POST['email']
	password = request.POST['password']

	user = User.objects.filter(email=email)
	if len(user) > 0:
		# if user exists, check password
		isPassword = bcrypt.checkpw(password.encode(), user[0].password.encode())
		if isPassword:
			request.session['id'] = user[0].id
			return redirect('/books')
		else:
			messages.error(request, "Incorrect username/password combination.")
			return redirect('/')
	else:
		message.error(request, "User does not exist.")
		return redirect('/')

	return redirect('/')

def logout(request):
	request.session.clear()
	return redirect('/')

def books(request):
	if request.session.get('id') == None:
		return redirect('/')

	context = {
			'user': User.objects.get(id=request.session['id']),
			'books': Book.objects.all(),
			'recent_reviews': Review.objects.all().order_by('-created_at')[:3],
			}

	return render(request, 'book_reviews/books.html', context)

def add_book(request):

	context = {
			'authors': Author.objects.all()
	}

	return render(request, 'book_reviews/add_book.html', context)

def save_book(request):
	errors = Book.objects.validate_book(request.POST)

	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error)
		return redirect('/books/add')
	else:
		title = request.POST['title']
		if request.POST['add_author'] == "":
			author = Author.objects.get(id=request.POST['author_dropdown'])
		else:
			errors = Author.objects.validate_author(request.POST)
			author = Author.objects.create(author=request.POST['add_author'])
		review_input = request.POST['review']
		rating = request.POST['rating']

		book = Book.objects.create(title=title, author=author)
		Review.objects.create(rating=rating, review=review_input, reviewer=User.objects.get(id=request.session['id']), book=book)

		return redirect("/books/{}".format(book.id))
	

def show_book(request, id):
	book = Book.objects.get(id=id)
	reviews = Review.objects.filter(book=book).order_by('-created_at')
	context = {
			'book': book,
			'reviews': reviews
	}

	return render(request, 'book_reviews/show_book.html', context)

def add_review(request, id):
	errors = Review.objects.validate_review(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error)
		return redirect('/books/add')
	else:
		review_text = request.POST['review']
		rating = request.POST['rating']
		book = Book.objects.get(id=id)
		user = User.objects.get(id=request.session['id'])

		Review.objects.create(rating=rating, review=review_text, reviewer=user, book=book)
		messages.success(request, "Added review")

		return redirect('/books/{}'.format(id))

def show_user(request, id):
	user = User.objects.get(id=id)
	review_count = Review.objects.filter(reviewer=user).count()
	reviewed_books = Review.objects.filter(reviewer=user).values_list('book__id', 'book__title').distinct()
	
	context = {
			'user': user,
			'review_count': review_count,
			'reviewed_books':  reviewed_books
	}

	return render(request, 'book_reviews/show_user.html', context)

def delete_review(request, book_id, review_id):
	review = Review.objects.get(id=review_id)
	review.delete()
	messages.success(request, "Deleted Review")
	return redirect('/books/{}'.format(book_id))







