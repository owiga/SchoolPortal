import os
import pymorphy3
import json
from collections import defaultdict

from django.apps import apps
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import RegistrationForm, LoginForm, AvatarUploadForm, TeacherRegForm
from .models import User, Profile, Friendship, PrivacySettings
from grades.models import Grade


def to_genitive(phrase):
    morph = pymorphy3.MorphAnalyzer()
    return ' '.join(morph.parse(word)[0].inflect({'gent'}).word for word in phrase.split()).capitalize()

# Профиль
# Друзья
# └─Список
# └─Заявки
# └─Отправленные
# Оценки
# Карта Школьника
# Настройки
# └─Профиль
# └─Конфиденциальность
# └─Настройки Сайта

# Раздел - Профиль

def profile(request, username):
    """Профиль пользователя"""
    user = get_object_or_404(User, username=username)

    if request.user != user:
        redirect('/')

    if request.user.is_authenticated:
        pending_requests = Friendship.objects.filter(friend=request.user, status="pending").values_list("user_id",
                                                                                                        flat=True)
        sent_requests = Friendship.objects.filter(user=request.user, status="pending").values_list("friend_id",
                                                                                                   flat=True)
        friends_list = Friendship.objects.filter(user=user, status="accepted").values_list("friend_id", flat=True)
    else:
        pending_requests = None
        sent_requests = None
        friends_list = None

    grades_user = Grade.objects.filter(student_id=user.id)
    gSum, gTotal = 0, 0

    for item in grades_user:
        gSum += item.value
        gTotal += 1

    try:
        middle_score = "%.2f" % (gSum / gTotal)
    except ZeroDivisionError:
        middle_score = 0.00

    if user.is_teacher == 1:
        if user.lesson_name == 'Математика':
            lesson = "Математики"
        elif user.lesson_name == 'ОБЗР':
            lesson = 'ОБЗР'
        else:
            lesson = to_genitive(user.lesson_name)
    else:
        lesson = None

    return render(request, 'accounts/profile.html',
                  {
                        'user': user,
                        'cover': user.cover,
                        "pending_requests": pending_requests,
                        "sent_requests": sent_requests,
                        "friends": friends_list,
                        "middle_score": middle_score,
                        "lesson": lesson
                  })


# Раздел - Друзья

def friends(request, username):
    """Список друзей пользователя"""

    user = get_object_or_404(User, username=username)

    if request.user.is_authenticated:
        sent_requests = Friendship.objects.filter(user=request.user, status="pending").values_list("friend_id", flat=True)
        friends_list = Friendship.objects.filter(user=user, status="accepted").values_list("friend_id", flat=True)
        pending_requests = Friendship.objects.filter(friend=request.user, status="pending").values_list("user_id",
                                                                                                        flat=True)
    else:
        sent_requests = None
        pending_requests = None
        friends_list = Friendship.objects.filter(user=user, status="accepted").values_list("friend_id", flat=True)

    privacy = PrivacySettings.objects.filter(user=user).first()

    return render(request, 'friends/friends.html', {
        'user': user,
        'cover': user.cover,
        "sent_requests": sent_requests,
        'pending_requests': pending_requests,
        "friends": friends_list,
        "privacy": privacy
    })


@login_required
def friend_request(request, username):
    """Заявки в друзья пользователя"""

    user = get_object_or_404(User, username=username)

    pending_requests = Friendship.objects.filter(friend=request.user, status="pending").values_list("user_id",
                                                                                                    flat=True)
    sent_requests = Friendship.objects.filter(user_id=request.user.id, status="pending").values_list("friend_id",
                                                                                                     flat=True)
    friends = Friendship.objects.filter(user_id=request.user.id, status="accepted").values_list("friend_id", flat=True)

    return render(request, 'friends/request_list.html', {'user': user,
                                                         'cover': user.cover,
                                                         "pending_requests": pending_requests,
                                                         "sent_requests": sent_requests,
                                                         "friends": friends,
                                                         })


@login_required
def sended(request, username):
    """Отправленные заявки пользователем"""

    user = get_object_or_404(User, username=username)

    pending_requests = Friendship.objects.filter(friend=request.user, status="pending").values_list("user_id",
                                                                                                    flat=True)
    sent_requests = Friendship.objects.filter(user=request.user, status="pending").values_list("friend_id", flat=True)

    return render(request, 'friends/sended_list.html', {
        'user': user,
        'cover': user.cover,
        "pending_requests": pending_requests,
        "sent_requests": sent_requests,
    })


@require_POST
@login_required
def send_friend_request(request, username, user_id):
    """Отправить заявку в друзья"""

    try:
        friend = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Пользователь не найден"}, status=404)

    if request.user != friend and not Friendship.objects.filter(user=request.user, friend=friend).exists():
        Friendship.objects.create(user=request.user, friend=friend, status="pending")
        return JsonResponse({"status": "success", "message": "Заявка отправлена"}, status=200)

    return JsonResponse({"status": "error", "message": "Ошибка при отправке"}, status=400)


@require_POST
@login_required
def cancel_friend_request(request, username, user_id):
    """Отменить отправленную заявку в друзья"""

    friend = get_object_or_404(User, id=user_id)  # Класс друга, чья заявку отклоняем

    Friendship.objects.filter(user=request.user, friend=friend, status="pending").delete()  # Удаляем

    return JsonResponse({"status": "success", "message": "Заявка отменена"}, status=200)  # Код 200


@login_required
def accept_friend_request(request, username, user_id):
    """Принять заявку в друзья"""

    friend = get_object_or_404(User, id=user_id)

    friendship = Friendship.objects.filter(user=friend, friend=request.user, status="pending").first()

    if friendship:
        friendship.status = "accepted"
        friendship.save()
        Friendship.objects.create(user=request.user, friend=friend, status="accepted")

    return redirect(request.META.get("HTTP_REFERER", '/'))


@login_required
def reject_friend_request(request, username, user_id):
    """Отклонить заявку (удалить её)"""

    friend = get_object_or_404(User, id=user_id)

    Friendship.objects.filter(user=friend, friend=request.user, status="pending").delete()

    return redirect(request.META.get("HTTP_REFERER", '/'))


@require_POST
@login_required
def delete_friend(request, username, user_id):
    """Удалить из друзей"""

    friend = get_object_or_404(User, id=user_id)

    friendship_user = Friendship.objects.filter(user=request.user, friend=friend, status="accepted")
    friendship_friend = Friendship.objects.filter(user=friend, friend=request.user, status="accepted")

    if friendship_friend and friendship_user:
        friendship_friend.delete()
        friendship_user.delete()
        return JsonResponse({"status": "success", "message": "Пользователь удалён из друзей!"}, status=200)

    else:
        return JsonResponse({"status": "error", "message": "Ошибка, вы не друзья!"}, status=400)


# Раздел - Оценки

def grades(request, username):
    """Оценки пользователя"""

    user = get_object_or_404(User, username=username)

    if request.user.is_authenticated:
        pending_requests = Friendship.objects.filter(friend=request.user, status="pending").values_list("user_id",
                                                                                                        flat=True)
        sent_requests = Friendship.objects.filter(user=request.user, status="pending").values_list("friend_id",
                                                                                                   flat=True)
        friends = Friendship.objects.filter(user=request.user, status="accepted").values_list("friend_id", flat=True)
    else:
        pending_requests = None
        sent_requests = None
        friends = None

    grades_user = Grade.objects.filter(student_id=user.id)

    if int(user.classroom[:-1]) > 7:
        grades_of_user = {
            'Математика': [],
            'Русский язык': [],
            'Английский язык': [],
            'ОБЗР': [],
            'История': [],
            'География': [],
            'Физическая культура': [],
            'Физика': [],
            'Химия': [],
            'Биология': [],
            'Обществознание': [],
            'Литература': [],
            'Информатика': []
        }
    elif int(user.classroom[:-1]) == 7:
        grades_of_user = {
            'Математика': [],
            'Русский язык': [],
            'Английский язык': [],
            'ОБЗР': [],
            'История': [],
            'География': [],
            'Физическая культура': [],
            'Физика': [],
            'Биология': [],
            'Обществознание': [],
            'Литература': [],
            'Информатика': [],
            'Музыка': [],
            'Труды': [],
            'ИЗО': []
        }
    elif 4 < int(user.classroom[:-1]) < 7:
        grades_of_user = {
            'Математика': [],
            'Русский язык': [],
            'Английский язык': [],
            'ОБЗР': [],
            'История': [],
            'География': [],
            'Физическая культура': [],
            'Биология': [],
            'Обществознание': [],
            'Литература': [],
            'Музыка': [],
            'Труды': [],
            'ИЗО': []
        }
    else:
        grades_of_user = {
            'Математика': [],
            'Русский язык': [],
            'Английский язык': [],
            'Физическая культура': [],
            'Окружающий мир': [],
            'Литература': [],
            'Музыка': [],
            'Труды': [],
            'ИЗО': []
        }

    for grade in grades_user:
        grades_of_user[grade.lesson].append((grade.value, grade.date))
    middle_grades_score = dict()
    for key, value in list(grades_of_user.items()):
        try:
            tempSum = 0
            if len(value) != 0:
                for grade__, time in value:
                    tempSum += grade__
                middle_grades_score[key] = "%.2f" % (tempSum / len(value))
            else:
                middle_grades_score[key] = 0
        except ZeroDivisionError:
            continue

    privacy = PrivacySettings.objects.filter(user=user).first()

    return render(request, 'accounts/grades.html', {'user': user,
                                                    'cover': user.cover,
                                                    "pending_requests": pending_requests,
                                                    "sent_requests": sent_requests,
                                                    "friends": friends,
                                                    "grades_us": sorted(grades_of_user.items()),
                                                    "middle_score": sorted(middle_grades_score.items()),
                                                    "privacy": privacy})

@login_required()
def add_grades(request, username):
    if request.user.is_teacher == 1 and request.user.username == username:
        users = User.objects.all().filter(classroom="10Т")
        classes = {'А': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                   'Б': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                   'В': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                   'Г': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'],
                   'Д': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                   'К': ['5', '6', '7', '8', '9'],
                   'Т': ['7', '8', '9', '10', '11']}
        return render(request, 'accounts/add-grades.html', {'cover': request.user.cover,
                                                            'classes': classes,
                                                            'users': users,
                                                            'username': request.user.username,
                                                            'n': range(1, 32)
                                                            })
    else:
        return HttpResponseRedirect('/')

@login_required()
def filter_users(request, username):
    if request.user.is_teacher == 1:
        classroom = request.GET.get('classroom', '')
        users = User.objects.filter(classroom=classroom).values("id", "first_name", "last_name")
        grade3 = Grade.objects.filter(student__classroom=classroom, lesson=request.user.lesson_name).values("student_id", "date",
                                                                                              "lesson", "value")
        grades_dict = {}
        for grade in grade3:
            key = f"{grade['student_id']}.{grade['date'].day}"
            grades_dict[key] = grade["value"]
        if classroom:
            users = users.filter(classroom=classroom)

        user_data = list(users.values('id', 'first_name', 'last_name', 'classroom'))
        return JsonResponse({'users': user_data, "grades": grades_dict})
    else:
        return HttpResponseRedirect("/")

# Раздел - Карта
@login_required
def school_card(request, username):
    """Школьная карта пользователя"""

    user = get_object_or_404(User, username=username)
    if user != request.user:
        return redirect(f'{user.username}/main')
    SchoolCard = apps.get_model('school_card', 'SchoolCard')
    card = SchoolCard.objects.filter(user=request.user).first()
    splited = str(card.balance).split('.')
    rubl = splited[0]
    copeyka = splited[1]
    number = card.card_number[4:8]
    return render(request, 'accounts/school_card.html', {'user': user,
                                                                            'cover': user.cover,
                                                                            'balance1': rubl,
                                                                            'balance2': copeyka,
                                                                            'number': number})


# Раздел - Настройки

@login_required()
def setting_profile(request, username):
    """Вкладка настроек профиля пользователя"""

    user = get_object_or_404(User, username=username)

    if user != request.user:
        return redirect(f'{user.username}/main')

    if request.method == 'POST':
        form_avatar = AvatarUploadForm(request.POST, request.FILES, instance=request.user.profile)

        if form_avatar.is_valid():  # Меняем аватарку профиля.
            os.remove(f"media/{request.user.cover}")
            user.cover = form_avatar.cleaned_data.get('avatar')
            request.user.cover = user.cover
            user.save()
            return redirect(f'/profile/{request.user.username}/main')  # Перенаправление на страницу профиля
    else:
        form_avatar = AvatarUploadForm(instance=request.user.profile)
    return render(request, 'settings/profile.html', {'user': user, 'cover': user.cover, 'form': form_avatar})


@login_required()
def confidentiality(request, username):
    """Вкладка конфиденциальности"""
    user = get_object_or_404(User, username=username)
    if user != request.user:
        return HttpResponseRedirect('/')
    else:
        privacy_user = PrivacySettings.objects.filter(user=user).first()
        return render(request, 'settings/confidentiality.html', {'user': user,
                                                                 'cover': user.cover,
                                                                 'privacy_user': privacy_user})


@login_required()
def site_settings(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'settings/site-settings.html', {'user': user, 'cover': user.cover})

@csrf_exempt
@login_required()
def update_privacy(request):
    if request.method == "POST":
        try:
            privacy, created = PrivacySettings.objects.get_or_create(user=request.user)
            data = json.loads(request.body)
            show_grades = int(data.get("show_grades", privacy.show_grades))
            show_friends = int(data.get("show_friends", privacy.show_friends))
            privacy.show_grades = show_grades
            privacy.show_friends = show_friends
            privacy.save()

            return JsonResponse({"success": True, "message": f"Настройки обновлены!"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Неверный запрос"})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)

                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.classroom = form.cleaned_data.get('number') + form.cleaned_data.get('classroom')
                user.email = form.cleaned_data.get('email')
                user.lesson_name = None
                user.save()

                login(request, user)

                return HttpResponseRedirect('/')
            except IntegrityError:
                form.add_error(None, form.errors)
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')  # Перенаправление после успешного входа
            else:
                form.add_error("username", "Неверное имя пользователя или пароль")

    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def teacher_register(request):
    if request.method == 'POST':
        form = TeacherRegForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return HttpResponseRedirect('/blog')
            except IntegrityError:
                form.add_error(None, form.errors)
    else:
        form = TeacherRegForm()
    return render(request, 'accounts/teacher_register.html', {'form': form})

@login_required
def custom_logout(request):
    logout(request)  # Выполняем выход пользователя
    response = redirect('/')
    return response
