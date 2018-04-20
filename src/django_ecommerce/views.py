from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ContactForm, LoginForm, RegisterForm


def home_page(request):
    print(request.session.get('first_name', 'Unknown'))  # Getter
    context = {
        "title": "Home page",
        "content": "Welcome to the home page.",
    }
    if request.user.is_authenticated:
        context["premium_content"] = "YEAHHHHH"
    return render(request, 'home_page.html', context)


def about_page(request):
    context = {
        "title": "About page",
        "content": "Welcome to the about page.",
    }
    return render(request, 'home_page.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact page",
        "content": "Welcome to the contact page.",
        "form": contact_form,
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    return render(request, 'contact/view.html', context)
