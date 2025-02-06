from asgiref.sync import sync_to_async
from category.models import Category
from report_daily.models import ReportDailyR

# Функция для получения категорий из базы
@sync_to_async
def get_categories():
    return [str(cat) for cat in Category.objects.all()]

@sync_to_async
def get_response():
    return [str(consumption) for consumption in ReportDailyR.objects.all()]

@sync_to_async(thread_sensitive=True)
def save_expense(category, amount, body):
    print(f"Категория: {category}, Сумма: {amount}, Описание: {body}")  # Здесь можно добавить логику сохранения в БД


@sync_to_async
def save_expense(category_name, amount, body):
    try:
        category = Category.objects.get(name=category_name)  # Ищем категорию в базе
        expense = ReportDailyR(category=category, how_much=amount, body=body)
        expense.save()  # Сохраняем в базе
        return True
    except Category.DoesNotExist:
        return False