from asgiref.sync import sync_to_async
from category.models import CategoryExpenses
from report.models import ReportExpenses

# Функция для получения категорий из базы
@sync_to_async
def get_categories():
    return [str(cat) for cat in CategoryExpenses.objects.all()]

@sync_to_async
def get_response():
    return [str(expense) for expense in ReportExpenses.objects.all()]

@sync_to_async
def save_expenses(category_name, amount, body):
    try:
        category = CategoryExpenses.objects.get(name=category_name)  # Ищем категорию в базе
        expense = ReportExpenses(category=category, how_much=amount, body=body)
        expense.save()  # Сохраняем в базе
        return True
    except CategoryExpenses.DoesNotExist:
        return False