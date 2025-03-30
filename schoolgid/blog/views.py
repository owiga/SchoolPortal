from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Post, Logo, Like
from .forms import AddPost
from accounts.models import User


def blog_news(request):
    posts = Post.objects.all()
    logo = Logo.objects.all()
    post_creators = []
    if request.user.is_authenticated:
        for post in posts:
            post.is_liked = post.user_liked_post(request.user)
            if post.author:
                post_creators.append((post.id, post.author))
        return render(request, 'blog/blog_news.html', {'posts': posts, 'user': request.user,
                                                       'cover': request.user.cover, 'logo': logo,
                                                       'teachers': post_creators})
    else:
        return render(request, 'blog/blog_news.html',
                      {'posts': posts, 'user': request.user, 'logo': logo, 'teachers': post_creators})


@login_required()
def add_news(request):
    if request.user.is_teacher:
        if request.method == 'POST':

            form = AddPost(request.POST, request.FILES, user=request.user)

            try:
                if form.is_valid():
                    post = form.save(commit=False)
                    author_choice = form.cleaned_data['author']

                    if author_choice == 'anonymous':
                        post.author = None
                    else:
                        post.author = User.objects.get(id=int(author_choice))
                    post.save()
                    return HttpResponseRedirect('/')
                else:
                    print(form.errors)
            except Exception as ex:
                print(ex)

        else:
            form = AddPost(user=request.user)
        return render(request, 'add_news.html', {"cover": request.user.cover, "form": form})
    else:
        return HttpResponseRedirect('/')


def search_users(request):
    query = request.GET.get('q')
    users = User.objects.all()
    query_res = query.lower().capitalize()
    if query:
        users = User.objects.filter(Q(first_name__icontains=query_res) | Q(last_name__icontains=query_res) |
                                    Q(username__icontains=query_res) | Q(first_name__icontains=query) |
                                    Q(last_name__icontains=query) | Q(username__icontains=query))  # Фильтр по логину

    return render(request, 'user_search.html', {'users': users, 'text_query': query})


def school_map(request):
    return render(request, "map.html")


def zvonki(request):
    return render(request, 'zvonki.html')


def contact_school(request):
    if request.user.is_authenticated:
        return render(request, 'contacts.html', {'cover': request.user.cover})
    else:
        return render(request, 'contacts.html', {'cover': None})


@login_required
@csrf_exempt
@require_POST
def like_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        user = request.user

        if post.user_liked_post(user):  # Если пользователь уже лайкнул пост
            # Удаляем лайк
            Like.objects.filter(user=user, post=post).delete()
            liked = False
        else:
            # Добавляем лайк
            Like.objects.create(user=user, post=post)
            liked = True

        # Возвращаем ответ в формате JSON
        return JsonResponse({
            'liked': liked,
            'total_likes': post.total_likes
        })
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
