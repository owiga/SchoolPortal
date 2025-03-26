from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Post, Logo, Like
from accounts.models import User


def blog_news(request):
    posts = Post.objects.all()
    logo = Logo.objects.all()
    if request.user.is_authenticated:
        for post in posts:
            post.is_liked = post.user_liked_post(request.user)
        return render(request, 'blog/blog_news.html', {'posts': posts, 'user': request.user,
                                                       'cover': request.user.cover, 'logo': logo})
    else:
        return render(request, 'blog/blog_news.html',
                      {'posts': posts, 'user': request.user, 'logo': logo})

def search_users(request):
    query = request.GET.get('q')
    users = User.objects.all()
    query_res = query.lower().capitalize()
    if query:
        users = User.objects.filter(Q(first_name__icontains=query_res)  | Q(last_name__icontains=query_res) |
                                    Q(username__icontains=query_res) | Q(first_name__icontains=query)  |
                                    Q(last_name__icontains=query) | Q(username__icontains=query)) # Фильтр по логину

    return render(request, 'user_search.html', {'users': users})

def zvonki(request):
    return render(request, 'zvonki.html')

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