

from django.urls import path
from .views import agendamento_detail ,agendamento_list

urlpatterns = [
    path('agendamentos/<int:id>',agendamento_detail, name='agendamento_detail'),
    path('agendamentos/',agendamento_list, name='agendamento_list')
]
