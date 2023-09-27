import datetime as dt
import io

from django.http import HttpResponse
from django.views.generic import View
from openpyxl import Workbook

from .models import Robot


class ExcelReportView(View):
    """Скачивание по прямой ссылке excel-файла со сводкой по
    суммарным показателям производства роботов за последнюю неделю."""
    def get(self, request):
        end_date = dt.datetime.now()
        start_date = end_date - dt.timedelta(days=7)
        # Получение данных о роботах за последнюю неделю
        robots = Robot.objects.filter(
            created__range=(start_date, end_date)
        )

        # Словарь для хранения данных о количестве версий для каждой модели
        model_version_counts = {}

        for robot in robots:
            model = robot.model
            version = robot.version

            # Инициализация счетчика версий для данной модели, если его еще нет
            if model not in model_version_counts:
                model_version_counts[model] = {}

            # Увеличение счетчика для данной версии данной модели
            if version in model_version_counts[model]:
                model_version_counts[model][version] += 1
            else:
                model_version_counts[model][version] = 1

        # Создание нового документа excel
        workbook = Workbook()

        for model, version_counts in model_version_counts.items():
            # Создание отдельного листа для каждой модели
            model_sheet = workbook.create_sheet(title=model)
            model_sheet.append(['Модель', 'Версия', 'Количество за неделю'])

            for version, count in version_counts.items():
                model_sheet.append([model, version, count])

        # Если есть роботы за последнюю неделю, то удаляем лист по умолчанию
        if robots:
            workbook.remove(workbook.active)
        else:
            workbook.active.append(
                ['Даннные о роботах за неделю отсутствуют.']
            )

        # Создание excel-файла в буфере
        excel_buffer = io.BytesIO()
        workbook.save(excel_buffer)
        excel_buffer.seek(0)

        # Создание прямой ссылки для скачивания excel-файла
        response = HttpResponse(excel_buffer.read())
        response['Content-Type'] = ('application/vnd.openxmlformats-'
                                    'officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = ('attachment; '
                                           'filename=robots_week.xlsx')
        return response
