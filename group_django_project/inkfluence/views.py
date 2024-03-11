from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm

from .models import *


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_author = request.POST.get('is_author')

        if User.objects.filter(username=username).exists():
            context = {'error': 'Username already exists. Choose another one.'}
            return render(request, 'signup.html', context)
        else:
            user = User.objects.create_user(username=username, password=password)
            role = 'author' if is_author else 'reader'
            profile = Profile.objects.create(user=user, role=role)
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f'username={username}    password={password}')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context = {'error': 'Invalid username or password.'}
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page

@login_required
def home_view(request):
    title = 'And So It Begins...'
    author = 'Jane Doe'
    summary_text = 'Lorem ipsum dolor sit amet consectetur. Arcu donec in facilisis pulvinar elit vitae. In justo vitae vitae\
              in massa lorem orci pellentesque. Suspendisse amet donec vel est porttitor purus. Tincidunt praesent risus\
              a feugiat facilisi. Senectus nulla penatibus arcu rhoncus viverra id eleifend sapien etiam. Ac quis\
              lacinia lacus quam.'
    genre = 'Fantasy'

    context = {'title': title,
               'summary_text': summary_text,
               'author': author,
               'genre': genre}
    return render(request, 'homePage.html', context)

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
    print(request.user.profile.role)
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