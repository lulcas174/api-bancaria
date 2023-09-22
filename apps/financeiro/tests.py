from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import ContaBancaria

class ConsultarSaldoTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.conta = ContaBancaria.objects.create(
            titular="João",
            saldo=1000.00,
            tipo_conta="corrente"
        )
        self.url = reverse('consultar_saldo', args=[self.conta.id])

    def test_consultar_saldo_sucesso(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['saldo'], "1000.00")
        self.assertEqual(response.data['titular'], "João")

    def test_consultar_saldo_conta_nao_encontrada(self):
        url_conta_invalida = reverse('consultar_saldo', args=[999])
        response = self.client.get(url_conta_invalida)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Conta não encontrada.")


class ResgatePoupancaTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.conta_corrente = ContaBancaria.objects.create(
            titular="João",
            saldo=1000.00,
            tipo_conta="corrente"
        )
        self.conta_poupanca = ContaBancaria.objects.create(
            titular="João",
            saldo=500.00,
            tipo_conta="poupanca"
        )
        self.url = reverse('resgate_poupanca', args=[self.conta_corrente.id, self.conta_poupanca.id])
        self.data = {
            'valor': 300.00,
            'descricao': 'Resgate de poupança'
        }

    def test_resgate_poupanca_sucesso(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['saldo_atual_resgate'], "700.00")

    def test_resgate_poupanca_conta_corrente_nao_encontrada(self):
        url_conta_invalida = reverse('resgate_poupanca', args=[999, self.conta_poupanca.id])
        response = self.client.post(url_conta_invalida, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Conta corrente não encontrada.")