from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm

from .models import Profile

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            profile = Profile.objects.create(user=user, role=role)
            profile.save()
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of the view you want to redirect to
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'homePage.html')
        else:
            # Return an 'invalid login' error message
            form = AuthenticationForm()
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page

@login_required
def home_view(request):
    return render(request, 'homePage.html')

@login_required
def search_view(request):
    return render(request, 'searchPage.html')

@login_required
def submit_view(request):
    return render(request, 'storySubmission.html')

@login_required
def profile_view(request):
    profile = request.user.profile
    if profile.role == 'reader':
        return render(request, 'profileAuthor.html', {'profile': profile})
    else:
        return render(request, 'profileReader.html', {'profile': profile})

@login_required
def story_submission_view(request):
    # verify the role is author
    if request.user.profile.role != 'author':
        return JsonResponse({'message': 'the user role is not author'}, status=400)
    # create story object
    return JsonResponse({'message': 'submit story successfully'}, status=201)

@login_required
def story_view(request):
    # find the story
    return render(request, 'storyPage.html')

@login_required
def comment_view(request):
    # find the story
    return JsonResponse({'message': 'comment story successfully'}, status=201)