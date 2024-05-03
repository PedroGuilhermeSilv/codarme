from django.urls import path
from .views import AgendamentoDetail, AgendamentoList, PrestadorList, get_horarios

urlpatterns = [
    path(
        "agendamentos/<int:pk>", AgendamentoDetail.as_view(), name="agendamento_detail"
    ),
    path("agendamentos/", AgendamentoList.as_view(), name="agendamento_list"),
    path("prestadores/", PrestadorList.as_view(), name="prestador_list"),
    path("horarios/", get_horarios, name="get_horarios"),
]
