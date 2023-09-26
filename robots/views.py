import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import RobotForm


@csrf_exempt
def create_robot(request):
    """Обработка записи, которая отражает информацию о
    произведенном на заводе роботе."""
    if request.method == 'POST':
        data = json.loads(request.body)
        form = RobotForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {'message': 'Робот успешно создан!'}, status=201)
        else:
            return JsonResponse({'error': 'Неверные данные!'}, status=400)
    else:
        return JsonResponse({'error': 'Метод не разрешен!'}, status=405)
