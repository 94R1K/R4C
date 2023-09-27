from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from robots.models import Robot
from .models import Customer


@receiver(post_save, sender=Robot)
def notify_customer(sender, instance, **kwargs):
    """Отправка сообщений на почту для тех, кто ждет заказ."""
    if (instance.serial in [order.robot_serial for order in
                            Order.objects.filter(
                                robot_serial=instance.serial
                            )]):
        # Получение всех клиентов, ожидающих данную модель робота
        waiting_customers = Customer.objects.filter(
            order__robot_serial=instance.serial
        )

        if waiting_customers:
            model = instance.model
            version = instance.version

            for customer in waiting_customers:
                subject = 'Робот в наличии'
                message = (
                    f'Добрый день!\n'
                    f'Недавно вы интересовались нашим роботом модели {model}, '
                    f'версии {version}.\n'
                    f'Этот робот теперь в наличии. Если вам подходит этот '
                    f'вариант - пожалуйста, свяжитесь с нами.'
                )
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [customer.email]

                send_mail(subject, message, from_email, recipient_list)
