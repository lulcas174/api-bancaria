from django.contrib import admin

from apps.financeiro.models import ContaBancaria, Extrato

# Register your models here.
admin.site.register(ContaBancaria)
admin.site.register(Extrato)
