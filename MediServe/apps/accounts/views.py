from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm
from .models import Account
from supabase import create_client
import os

# Supabase connection
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-supabase-url.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-supabase-service-role-key")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def home_redirect(request):
    return redirect('login')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html', {'form': form})

        # if email already exists
        if Account.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'signup.html', {'form': form})

        # If form is valid, save the user
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Signup successful! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        email = request.POST.get('username')
        password = request.POST.get('password')

        user_exists = Account.objects.filter(email=email).exists()

        if not user_exists:
            messages.error(request, 'No account found with this email. Please sign up first.')
        else:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)

                if user.is_staff or user.is_superuser:
                    return redirect('admin_menu')
                else:
                    return redirect('main_menu')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')


@login_required
def admin_menu_view(request):
    return render(request, 'admin_menu.html')


@login_required
def main_menu_view(request):
    """Main menu view that includes the most recent announcement."""
    latest_announcement = None
    try:
        response = supabase.table("tblannouncements").select("*").order("date_posted", desc=True).limit(1).execute()
        if response.data:
            latest_announcement = response.data[0]
    except Exception as e:
        print("Error fetching announcement:", e)

    return render(request, 'main_menu.html', {
        'latest_announcement': latest_announcement
    })


@login_required
def profile_view(request):
    return render(request, 'profile_view.html', {'user': request.user})


@login_required
def settings_page(request):
    return render(request, 'settings.html')


@login_required
def feedback_page(request):
    return render(request, 'feedback.html')

