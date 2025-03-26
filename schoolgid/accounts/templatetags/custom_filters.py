from django import template
from ..models import User

register = template.Library()

@register.filter
def get_user_by_id(user_id):
    return User.objects.filter(id=user_id).first()  # Получаем пользователя или None