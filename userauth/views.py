from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password

from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.core.paginator import Paginator

from userauth.models import User, Profile
from userauth.forms import UserRegistrationForm
from posts.models import Post, Follow

# Create your views here.
def RegisterView(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered')
            return redirect('userauth:login')
        else:
            messages.warning(request, 'Confirm all fields are filled correctly')
            return redirect('userauth:register')
    else:
       form = UserRegistrationForm()
    
    context = {
        'form': form
    }
    return render(request, 'userauth/register.html', context)

def LoginView(request):
    if request.method =='POST':
        email = request.POST.get('email')  #You can also set it up to login with username instead
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            print(user)
            if user is not None and check_password(password, user.password):
                authenticated_user = authenticate(request, email=email, password=password)
                print(authenticated_user)
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    messages.success(request, 'You have been logged in successfully')
                    return redirect("posts:index")
                else:
                    messages.warning(request, "email or password is incorrect, try again")
                    return redirect("userauth:login")
            else:
                messages.warning(request, "User does not exist!")
                return redirect("userauth:login")
        except User.DoesNotExist:
            messages.warning(request, "User does not exist!")
            return redirect("userauth:login")


    return render(request, 'userauth/login.html')

def LogoutView(request):
    logout(request)
    messages.success(request, 'You have successfully been logged out')
    return redirect('userauth:login')

@login_required
def ProfileView(request):
    return render(request, 'userauth/profile.html')


def UserProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    
    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favorites.all()

    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts': posts_paginator,
        'profile': profile,
        'following_count': following_count,
        'followers_count': followers_count,
        'posts_count': posts_count,
        'follow_status': follow_status,
        'url_name': url_name,
    }

    return render(request, 'userauth/profile.html', context)


"""


from django.urls import resolve

# Create your views here.
def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	url_name = resolve(request.path).url_name
	
	if url_name == 'profile':
		posts = Post.objects.filter(user=user).order_by('-posted')

	else:
		posts = profile.favorites.all()

	#Profile info box
	posts_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()

	#follow status
	follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

	#Pagination
	paginator = Paginator(posts, 8)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile.html')

	context = {
		'posts': posts_paginator,
		'profile':profile,
		'following_count':following_count,
		'followers_count':followers_count,
		'posts_count':posts_count,
		'follow_status':follow_status,
		'url_name':url_name,
	}

	return HttpResponse(template.render(context, request))

def UserProfileFavorites(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	
	posts = profile.favorites.all()

	#Profile info box
	posts_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()

	#Pagination
	paginator = Paginator(posts, 8)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile_favorite.html')

	context = {
		'posts': posts_paginator,
		'profile':profile,
		'following_count':following_count,
		'followers_count':followers_count,
		'posts_count':posts_count,
	}

	return HttpResponse(template.render(context, request))

"""