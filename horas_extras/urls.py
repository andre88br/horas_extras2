from django.urls import path

from . import views

urlpatterns = [
    path("upload", views.solicitacao_confirmacao_upload, name="upload"),
    path("processar", views.processar, name="processar"),
    path("importacoes", views.importacoes, name="importacoes"),
    path("confirmacao/<int:file_id>", views.confirmacao, name="confirmacao"),
    path("solicitacao/<int:file_id>", views.solicitacao, name="solicitacao"),
    path("frequencias/<int:file_id>", views.frequencias, name="frequencias"),
    path("deleta_mes/<int:file_id>", views.deleta_mes, name="deleta_mes"),
    path("deleta_mes_frequencia", views.deleta_mes_frequencia, name="deleta_mes_frequencia"),
    path("salvar_alteracao_frequencia", views.salvar_alteracao_frequencia, name="salvar_frequencia"),
    path("salvar_confirmacao", views.salvar_alteracao_confirmacao, name="salvar_confirmacao"),
    path("salvar_alteracao_solicitacao", views.salvar_alteracao_solicitacao, name="salvar_solicitacao"),
    path("frequencia", views.frequencia, name="frequencia"),
    path("salvar_alteracao_banco", views.salvar_alteracao_banco, name="salvar_banco_total"),
    path("salvar_banco_mes", views.salvar_alteracao_saldo_mes, name="salvar_banco_mes"),
    path("banco_total/<int:file_id>", views.banco_total, name="banco_total"),
    path("banco_mes/<int:file_id>", views.banco_mes, name="banco_mes"),
    path("deleta_banco_mes", views.deleta_banco_mes, name="deleta_banco_mes"),
    path("deleta_banco_total_mes", views.deleta_banco_total_mes, name="deleta_banco_total_mes"),
    path("banco_de_horas", views.bancos, name="banco_de_horas"),
    path("inserir_bases", views.inserir_bases, name="inserir_bases"),
    path("reprocessar", views.reprocessar, name="reprocessar"),
    path("salva_solicitacao_reprocessar", views.salva_solicitacao_reprocessar, name="salva_solicitacao_reprocessar"),
    path("salva_confirmacao_reprocessar", views.salva_confirmacao_reprocessar, name="salva_confirmacao_reprocessar"),
    path("salvar_banco_total_reprocessar", views.salvar_banco_total_reprocessar, name="salvar_banco_total_reprocessar"),
    path("salvar_banco_mes_reprocessar", views.salvar_banco_mes_reprocessar, name="salvar_banco_mes_reprocessar"),
    path("salvar_frequencia_reprocessar", views.salvar_frequencia_reprocessar, name="salvar_frequencia_reprocessar"),
]
