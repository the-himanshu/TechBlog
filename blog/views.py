from django.contrib.auth.models import User
from .models import Post
from django.views import generic, View
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .forms import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from braces.views import LoginRequiredMixin



class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html', { 'form': UserCreationForm() })

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #return HttpResponse('post chala')
            return redirect('login')

        #return HttpResponse('template')
        return render(request, 'register.html', { 'form': form })

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', { 'form':  AuthenticationForm })

    # really low level
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )

            if user is None:
                return render(
                    request,
                    'login.html',
                    { 'form': form, 'invalid_creds': True }
                )

            try:
                form.confirm_login_allowed(user)
            except ValidationError:
                return render(
                    request,
                    'login.html',
                    { 'form': form, 'invalid_creds': True }
                )
            login(request, user)

            return redirect ('home')

def PostList(request):
    object_list = Post.objects.filter(status=1).order_by('-created_on')
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    return render(request,
                  'index.html',
                  {'page': page,
                   'posts': post_list})
 
def PostDetail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

def makePost(request) :
    return render(request, 'makePost.html')

from django.utils.text import slugify

def savePost(request) :
    if request.method=="POST" :
        pub = request.POST.get('name','')
        title = request.POST.get('title','')
        cont = request.POST.get('cont','')
        x = request.user
        user = User.objects.get(username=x.username)
        from datetime import datetime
        z = datetime.today().strftime('%Y-%m-%d')
        x = title.lower()
        x = x.split()
        j = ''
        for i in x :
            j = j + i + '-'
        x = x[0: len(x)-1]
        s = slugify(title, allow_unicode=True)
        post = Post(author=user, title=title, created_on=z, content=cont, publisher=pub, slug=s)
        post.save()
    return redirect('home')

def Logout(request) :
    logout(request)
    return redirect('login')

def Portfolio(request) :
    return HttpResponse('portfolio')

def Profile(request) :
    user = request.user
    x = user.id
    object_list = Post.objects.filter(author=x)
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    return render(request,
                  'profile.html',
                  {'page': page,
                   'posts': post_list})
    #return HttpResponse('profile')