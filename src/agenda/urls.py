from django.urls import path
from .views import AgendamentoDetail, AgendamentoList

urlpatterns = [
    path("agendamentos/<int:id>", AgendamentoDetail.as_view(), name="agendamento_detail"),
    path("agendamentos/", AgendamentoList.as_view(), name="agendamento_list"),
]
