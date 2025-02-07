from asgiref.sync import sync_to_async
from category.models import CategoryExpenses
from report.models import ReportExpenses, ReportIncomes
from datetime import datetime, timedelta

# Функция для получения категорий из базы
@sync_to_async
def get_categories():
    return [str(cat) for cat in CategoryExpenses.objects.all()]

@sync_to_async
def get_report(operation: str, period: str):
    now = datetime.now()

    # Определяем начальную дату для фильтрации
    if period == "день":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "неделя":
        start_date = now - timedelta(days=7)
    elif period == "месяц":
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        return []  # Если период некорректный, возвращаем пустой список

    # Выбираем правильную модель
    model = ReportIncomes if operation == "доходы" else ReportExpenses
    return [str(expense) for expense in model.objects.filter(created_at__gte=start_date)]

@sync_to_async
def save_expenses(category_name, amount, body):
    try:
        category = CategoryExpenses.objects.get(name=category_name)  # Ищем категорию в базе
        expense = ReportExpenses(category=category, amount=amount, body=body)
        expense.save()  # Сохраняем в базе
        return True
    except CategoryExpenses.DoesNotExist:
        return False