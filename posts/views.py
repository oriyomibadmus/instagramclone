from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from posts.models import Stream, Post, Tag, Likes #PostFileContent
from posts.forms import NewPostForm
#from stories.models import Story, StoryStream

#from comment.models import Comment
#from comment.forms import CommentForm


from django.contrib.auth.decorators import login_required

from django.urls import reverse
from userauth.models import Profile

# the home page view
@login_required
def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    #stories = StoryStream.objects.filter(user=user)
    
    group_ids = [post.post_id for post in posts]  # Creating a list to store all the post_id of each post in the stream object
    
    post_items = Post.objects.filter(id__in=group_ids).order_by('-posted')

    context = {
        'post_items': post_items,
        #'stories': stories,
    }

    return render(request, 'posts/index.html', context)



# View for the create new post form
@login_required
def NewPost(request):
	user = request.user
	tags_objs = []
	files_objs = []

	if request.method == 'POST':
		form = NewPostForm(request.POST, request.FILES)
		if form.is_valid():
			picture = form.cleaned_data.get('picture')
			caption = form.cleaned_data.get('caption')
			tags_form = form.cleaned_data.get('tags')

			tags_list = list(tags_form.split(','))

			for tag in tags_list:
				t, created = Tag.objects.get_or_create(title=tag)
				tags_objs.append(t)

			

			p, created = Post.objects.get_or_create(picture=picture, caption=caption, user=user)
			p.tags.set(tags_objs)
			p.save()
			return redirect('posts:index')
	else:
		form = NewPostForm()

	context = {
		'form':form,
	}

	return render(request, 'posts/newpost.html', context)

# Post Detail View
def PostDetails(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    profile = None
    favorited = False
    liked = False
    likeObj = Likes.objects.filter(user=user, post=post)
    
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=user)
        if profile.favorites.filter(id=post_id).exists():
            favorited = True
        if likeObj.exists():
            liked = True
    
    context = {
        'post': post,
        'favorited': favorited,
        'liked': liked,
        'profile': profile,
    }
    
    return render(request, 'posts/postdetail.html', context)


# Tag Views
def Tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    context = {
        'posts': posts,
        'tag': tag,
    }

    return render(request, 'posts/tag.html', context)

@login_required
def like(request, post_id):
	user = request.user
	post = Post.objects.get(id=post_id)
	current_likes = post.likes
	liked = Likes.objects.filter(user=user, post=post).count()

	if not liked:
		like = Likes.objects.create(user=user, post=post)
		#like.save()
		current_likes = current_likes + 1

	else:
		Likes.objects.filter(user=user, post=post).delete()
		current_likes = current_likes - 1

	post.likes = current_likes
	post.save()

	return HttpResponseRedirect(reverse('posts:postdetails', args=[post_id]))

@login_required
def favorite(request, post_id):

	user = request.user
	post = Post.objects.get(id=post_id)
	profile = Profile.objects.get(user=user)

	if profile.favorites.filter(id=post_id).exists():
		profile.favorites.remove(post)

	else:
		profile.favorites.add(post)

	return HttpResponseRedirect(reverse('posts:postdetails', args=[post_id]))





"""
def PostDetails(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	user = request.user
	profile = Profile.objects.get(user=user)
	favorited = False

	#comment
	comments = Comment.objects.filter(post=post).order_by('date')
	
	if request.user.is_authenticated:
		profile = Profile.objects.get(user=user)
		#For the color of the favorite button

		if profile.favorites.filter(id=post_id).exists():
			favorited = True
	#Comments Form
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.user = user
			comment.save()
			return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
	else:
		form = CommentForm()


	template = loader.get_template('post_detail.html')

	context = {
		'post':post,
		'favorited':favorited,
		'profile':profile,
		'form':form,
		'comments':comments,
	}

	return HttpResponse(template.render(context, request))


def tags(request, tag_slug):
	tag = get_object_or_404(Tag, slug=tag_slug)
	posts = Post.objects.filter(tags=tag).order_by('-posted')

	template = loader.get_template('tag.html')

	context = {
		'posts':posts,
		'tag':tag,
	}

	return HttpResponse(template.render(context, request))


@login_required
def like(request, post_id):
	user = request.user
	post = Post.objects.get(id=post_id)
	current_likes = post.likes
	liked = Likes.objects.filter(user=user, post=post).count()

	if not liked:
		like = Likes.objects.create(user=user, post=post)
		#like.save()
		current_likes = current_likes + 1

	else:
		Likes.objects.filter(user=user, post=post).delete()
		current_likes = current_likes - 1

	post.likes = current_likes
	post.save()

	return HttpResponseRedirect(reverse('postdetails', args=[post_id]))


@login_required
def favorite(request, post_id):

	user = request.user
	post = Post.objects.get(id=post_id)
	profile = Profile.objects.get(user=user)

	if profile.favorites.filter(id=post_id).exists():
		profile.favorites.remove(post)

	else:
		profile.favorites.add(post)

	return HttpResponseRedirect(reverse('postdetails', args=[post_id]))

"""