from django.urls import path

from apps.financeiro.views import consultar_saldo, consultar_extrato_mes, transferencia_conta_corrente, resgate_poupanca

urlpatterns = [
    path('consultar-saldo/<int:id_conta>/', consultar_saldo, name='consultar-saldo'),
    path('consultar-extrato-mes/<int:id_conta>/', consultar_extrato_mes, name='consultar-extrato-mes'),
    path('transferencia-investimento/<int:id_conta_corrente>/<int:id_conta_poupanca>', transferencia_conta_corrente, name='transferencia-contas'),
    path('transferencia-resgate/<int:id_conta_corrente>/<int:id_conta_poupanca>', resgate_poupanca, name='resgate-poupanca')
]