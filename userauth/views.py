from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, get_user_model,logout
from django.contrib import messages
from userauth.forms import UserRegisterFrom

User = get_user_model()

def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = UserRegisterFrom(request.POST)
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax') == 'true'
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            msg = f'Hey {user.username}, your account was created successfully!'
            messages.success(request, msg)
            
            if is_ajax:
                return JsonResponse({'status': 'success', 'message': msg})
            return redirect('core:home')
        
        if is_ajax:
            error_list = [error for errors in form.errors.values() for error in errors]
            return JsonResponse({'status': 'error', 'errors': error_list}, status=400)
    else:
        form = UserRegisterFrom()
        
    return render(request, 'userauths/sign-up.html', {'form': form})

def loginView(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You Allready Logdin...')
        return redirect('core:home')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax') == 'true'

        user_obj = User.objects.filter(email=email).first() or User.objects.filter(username=email).first()
        user = authenticate(request, email=user_obj.email, password=password) if user_obj else None

        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)

            msg = f'Welcome back, {user.username.title()}!'
            messages.success(request, msg)

            next_url = request.GET.get('next') or request.POST.get('next')
            if is_ajax:
                return JsonResponse({'status': 'success', 'message': msg, 'next': next_url or '/'})
            if next_url:
                return redirect(next_url)
            return redirect('core:home')
        else:
            msg = 'Invalid username/email or password. Please try again.'
            messages.warning(request, msg)

            if is_ajax:
                return JsonResponse({'status': 'error', 'errors': [msg]}, status=400)

            return render(request, 'userauths/sign-in.html', {'email': email})

    return render(request, 'userauths/sign-in.html')

def logoutView(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('userauth:login')

