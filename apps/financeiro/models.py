from django.db import models

class ContaBancaria(models.Model):
    TIPO_CONTA_CHOICES = (
        ('corrente', 'Conta Corrente'),
        ('poupanca', 'Conta Poupança'),
    )
    titular = models.CharField(max_length=100)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_conta = models.CharField(max_length=10, choices=TIPO_CONTA_CHOICES)

    def __str__(self):
        return self.titular
    
    class Meta:
        db_table = 'conta_bancaria'
        verbose_name = 'Conta Bancária'
        verbose_name_plural = 'Contas Bancárias'


class Transacao(models.Model):
    conta_origem = models.ForeignKey(ContaBancaria, related_name='transacoes_origem', on_delete=models.CASCADE)
    conta_destino = models.ForeignKey(ContaBancaria, related_name='transacoes_destino', on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.valor

    class Meta:
        db_table: 'transacao'
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'


class Extrato(models.Model):
    conta = models.ForeignKey(ContaBancaria, on_delete=models.CASCADE)
    data = models.DateTimeField()
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.conta.titular
    
    class Meta:
        db_table = 'extrato'
        verbose_name = 'Extrato'
        verbose_name_plural = 'Extratos'