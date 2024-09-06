"""
Отклчил celery. Не хватало оперативной памяти на реальном сервере или произошла утечка памяти
"""
# import os
# from celery import Celery

# # задать стандартный модуль настроек Django
# # для программы 'celery'.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pshop.settings')
# app = Celery('pshop')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()
