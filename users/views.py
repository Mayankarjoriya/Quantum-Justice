from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import get_user_model, login
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from lawyer.models import LawCategory

User = get_user_model()


def search_lawyer(request):
    categories = LawCategory.objects.all()
    selected = request.GET.getlist('categories')

    if selected:
        lawyers = User.objects.filter(role='lawyer', categories__in=selected).distint()
    else:
        lawyers = User.objects.filter(role='lawyer')

    if not lawyers.exists():
        return HttpResponse("NO LAWYER FOUND TRY AGAIN!")

    Data = []
    for lawyer in lawyers:
        Data.append({
            "username": lawyer.username,
            "email": lawyer.email,
            "categories": [cat.name for cat in lawyer.categories.all()]
        })


    return render(request, 'users/Client-page.html', {
        'categories':categories,
        'lawyer': lawyers,

    })

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        user= self.request.user
        if user.role == 'client':
            return '/client-page'
        elif user.role == 'lawyer':
            return '/lawyer-page'
        else:
            return '/'

def home(request):
    return render(request, 'users/index.html')

@login_required
def client_page(request):
    categories = LawCategory.objects.all()
    lawyers = None
    selected = request.GET.getlist('categories')


    if request.GET.getlist('categories'):
        
        lawyers = User.objects.filter(role='lawyer',categories__in=selected).distinct()


    return render(request, 'users/Client-page.html', {
        'categories': categories,
        'lawyers': lawyers,
        "selected_categories": selected,
    })
    


@login_required
def lawyer_page(request):

    return render(request, 'users/Lawyer-Page.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request, user)

            if user.role == 'client':
                HttpResponse(f'You are register as {user.role}')
                return redirect('/client-page')
            elif user.role == 'lawyer':
                HttpResponse(f'You are register as {user.role}')
                return redirect('/lawyer-page')
            else:
                return HttpResponse(f"Error: {user.role} is invalid")
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
