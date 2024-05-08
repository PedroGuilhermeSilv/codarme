from agenda.models import Agendamento
from .serializers import AgendamentoSerializer, PrestadorSerializer
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from django.http import JsonResponse
from datetime import datetime
from .utils import get_horarios_disponiveis


class IsOwnerOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        username = request.query_params.get("username", None)
        return request.user.username == username


class IsPrestador(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.prestador


class AgendamentoDetail(RetrieveUpdateDestroyAPIView):  # api/agendamentos/<int:pk>
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsPrestador]

    def perform_destroy(self, instance):
        instance.cancelado = True
        instance.save()


class AgendamentoList(ListCreateAPIView):  # api/agendamentos/?username=<username>
    serializer_class = AgendamentoSerializer
    permission_classes = [IsOwnerOrCreateOnly]

    def get_queryset(self):
        username = self.request.query_params.get("username", None)
        return Agendamento.objects.filter(prestador__username=username)


class PrestadorList(ListAPIView):
    serializer_class = PrestadorSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]


@api_view(http_method_names=["GET"])
def get_horarios(request):
    data = request.query_params.get("data")
    data = datetime.fromisoformat(data).date() if data else datetime.now().date()

    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
    return JsonResponse(horarios_disponiveis, safe=False)
