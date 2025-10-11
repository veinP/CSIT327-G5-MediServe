from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm
from .models import Account


# 🏠 Redirect root to login
def home_redirect(request):
    return redirect('login')


# ==========================
# SIGNUP VIEW
# ==========================
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
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


# ==========================
# LOGIN VIEW
# ==========================
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        email = request.POST.get('username')  # Django default username field name
        password = request.POST.get('password')

        # Check if email exists
        user_exists = Account.objects.filter(email=email).exists()

        if not user_exists:
            messages.error(request, 'No account found with this email. Please sign up first.')
        else:
            # Authenticate user
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on role
                if user.is_staff or user.is_superuser:
                    return redirect('admin_menu')
                else:
                    return redirect('main_menu')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# ==========================
# LOGOUT VIEW
# ==========================
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')


# ==========================
# MENU & PROFILE VIEWS
# ==========================
@login_required
def admin_menu_view(request):
    return render(request, 'admin_menu.html')


@login_required
def main_menu_view(request):
    return render(request, 'main_menu.html')


@login_required
def profile_view(request):
    return render(request, 'profile_view.html', {'user': request.user})

@login_required
def settings_page(request):
    return render(request, 'settings.html')

@login_required
def feedback_page(request):
    return render(request, 'feedback.html')
