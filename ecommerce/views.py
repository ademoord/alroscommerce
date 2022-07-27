#
#   file 	: ecommerce/views.py
#	author	: andromeda
#   desc 	: Model parsing and variable retrieval for each eCommerce URL controller
#
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ContactForm, LoginForm, RegisterForm

def home_page(request):
    if not request.user.is_authenticated() :
        print(request.session.get("first_name", "Unknown"))
    context = {
        "title": "Home",
        "content": "Welcome to ALROSCommerce!"
    }
    return render(request, "home_page.html", context)


def about_page(request):
	context = {
		"title": "About",
# 		"content": "This is about page!"
	}
	return render(request, "about_page.html", context)

def contact_page(request):
	contact_form = ContactForm(request.POST or None)
	context = {
		"title": "Contact",
# 		"content": "This is contact page!",
		"form": contact_form,
	}
	if contact_form.is_valid():
		print(contact_form.cleaned_data)
	return render(request, "contact/view.html", context)

def login_page(request):
	form = LoginForm(request.POST or None)
	context = {
		"title": "Login",
		"form": form
	}
	print("User logged in:")
	# print(request.user.is_authenticated())
	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(request, username=username, password=password)
		# print(request.user.is_authenticated())
		if user is not None:
			# print(request.user.is_authenticated())
			login(request, user)
			# context['form'] = LoginForm()
			return redirect("/")
		# else:
			print("Error")

	return render(request, "auth/login.html", context)

User = get_user_model()
def register_page(request):
	form = RegisterForm(request.POST or None)
	context = {
		"title": "Register",
		"form": form
	}
	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		new_user = User.objects.create_user(username, email, password)
		print(new_user)

	return render(request, "auth/register.html", context)


