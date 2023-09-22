
from apps.financeiro.models import ContaBancaria, Extrato, Transacao
from rest_framework import serializers

class SaldoContaBancariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaBancaria
        fields = ['saldo']


class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        fields = '__all__'
        read_only_fields = ['conta_origem', 'conta_destino']


class ExtratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extrato
        fields = ['descricao']
        read_only_fields = ['conta']

    def to_representation(self, instance):
        data_formatada = instance.data.strftime("%d/%m/%Y")
        return {
            'data': data_formatada,
            'descricao': instance.descricao,
        }


