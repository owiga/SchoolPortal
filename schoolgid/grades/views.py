from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from .models import Grade
from accounts.models import User


months = {
    '1': "Январь",
    '2': "Февраль",
    '3': "Март",
    '4': "Апрель",
    '5': "Май",
    '6': "Июнь",
    '7': "Июль",
    '8': "Август",
    '9': "Сентябрь",
    '10': "Октябрь",
    '11': "Ноябрь",
    '12': "Декабрь",
}


@csrf_exempt
def save_grade(request):
    if request.method == 'POST':
        print(request.content_type, request.body)
        print(json.loads(request.body))
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            lesson_id = data.get('lesson_id')
            day, month = data.get('date').split('.')
            date = f"{datetime.now().year}-{'0'+month if int(month) < 10 else month}-{'0'+day if int(day) < 10 else day}"
            grade_value = data.get('grade')
            teacher_id = data.get('teacher_id')

            # Проверяем, что все данные переданы
            if not (user_id and lesson_id and date):
                return JsonResponse({'success': False, 'error': 'Недостаточно данных'})

            # Получаем пользователя
            user = User.objects.get(id=user_id)
            if not grade_value:
                Grade.objects.filter(student_id=user, lesson=lesson_id, date=date).delete()
                return JsonResponse({'success': True, 'message': 'Оценка сохранена'})
            Grade.objects.filter(student_id=user, lesson=lesson_id, date=date).delete()
            grade, created = Grade.objects.update_or_create(
                student=user,
                lesson=lesson_id,
                date=date,
                defaults={'value': grade_value, 'teacher_id': teacher_id}
            )

            return JsonResponse({'success': True, 'message': 'Оценка сохранена'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Неверный метод запроса'})