import os

from django.contrib import messages
from django.shortcuts import render

from horas_extras.calcula import calcula_he
from relatorios.processa_relatorios import gera_relatorio_solicitacao, gera_relatorio_erros, \
    gera_relatorio_confirmacao, gera_relatorio_entrada_saida, gera_relatorio_codigo90, \
    gera_relatorio_negativos, gera_relatorio_rejeitar_batidas, gera_relatorio_pagas, gera_relatorio_setores, \
    gera_relatorio_rejeitadas, gera_voltar_negativos


def relatorios(request):
    if request.user.is_authenticated:
        return render(request, "relatorios/relatorios.html")
    else:
        return render(request, "usuarios/login.html")


def gera_relatorio(request):
    if request.user.is_authenticated:
        relatorio = ''
        nome = ''
        response1, response2 = '', ''
        tipo = request.POST.get('tipo')
        matricula = request.POST.get('matricula')
        final = request.POST.get('final')
        data_inicial = request.POST['data_inicial']
        data_final = request.POST['data_final']
        ano, mes = str(data_inicial).split('-')
        ano2, mes2 = str(data_final).split('-')
        usuario = request.user
        if tipo == 'solicitadas_mes':
            relatorio = gera_relatorio_solicitacao(mes, ano, mes2, ano2, matricula)

        if tipo == 'pagas_mes':
            relatorio, conclusao, response1, response2 = calcula_he(ano, mes, usuario, final)
            relatorio['saldo_mes_decimal'] = relatorio['saldo_mes_decimal'].map(lambda x: format(x, '.2f'))
            relatorio['saldo_banco_decimal'] = relatorio['saldo_banco_decimal'].map(lambda x: format(x, '.2f'))
            relatorio['horas_trabalhadas'] = relatorio['horas_trabalhadas'].map(lambda x: format(x, '.2f'))
            relatorio['horas_diurnas'] = relatorio['horas_diurnas'].map(lambda x: format(x, '.2f'))
            relatorio['horas_noturnas'] = relatorio['horas_noturnas'].map(lambda x: format(x, '.2f'))

            relatorio = relatorio.head(1000)
            relatorio = relatorio.to_html(index=True)
            nome = f'Horas extras pagas - {mes}/{ano}'
            messages.info(request, conclusao)

        return render(request, "relatorios.html", context={'relatorio': relatorio,
                                                           'nome': nome, 'mes': mes, 'ano': ano,
                                                           'response1': response1, 'response2': response2})
    else:
        return render(request, "usuarios/login.html")


def escolhe_relatorio(request):
    try:
        if request.user.is_authenticated:
            arquivo, response, df = '', '', ''
            tipo = request.POST.get('tipo')
            tipo3 = request.POST.get('tipo3')
            matricula = request.POST.get('matricula')
            data = request.POST.get('data')
            data2 = request.POST.get('data2')
            ano, mes = str(data).split('-')[0], str(data).split('-')[1]
            if data2 != '' and data2 is not None:
                ano2, mes2 = str(data2).split('-')[0], str(data2).split('-')[1]
            else:
                ano2, mes2 = '', ''

            if tipo == 'solicitacao':
                response, arquivo, df = gera_relatorio_solicitacao(mes, ano, mes2, ano2, matricula)

            if tipo == 'erros2':
                response, arquivo, df = gera_relatorio_erros(mes, ano, mes2, ano2, tipo3, matricula)

            if tipo == 'confirmacao':
                response, arquivo, df = gera_relatorio_confirmacao(mes, ano, mes2, ano2, matricula)

            if tipo == 'erros':
                response, arquivo, df = gera_relatorio_erros(mes, ano, mes2, ano2, tipo3, matricula)

            if tipo == 'entrada_saida':
                response, arquivo, df = gera_relatorio_entrada_saida(mes, ano, mes2, ano2, matricula)

            if tipo == 'cod_90':
                response, arquivo, df = gera_relatorio_codigo90(mes, ano, mes2, ano2, matricula)

            if tipo == 'negativos':
                response, arquivo, df = gera_relatorio_negativos(mes, ano, mes2, ano2, tipo3, matricula)

            if tipo == 'rejeitar_batidas':
                response, arquivo, df = gera_relatorio_rejeitar_batidas(mes, ano, mes2, ano2, matricula)

            if tipo == 'pagas':
                response, arquivo, df = gera_relatorio_pagas(mes, ano, matricula, mes2, ano2)

            if tipo == 'setores':
                response, arquivo, df = gera_relatorio_setores(mes, ano, mes2, ano2)

            if tipo == 'rejeitadas':
                response, arquivo, df = gera_relatorio_rejeitadas(mes, ano, mes2, ano2, matricula)

            if tipo == 'voltar_negativos':
                response, arquivo, df = gera_voltar_negativos(mes, ano)

            if not response:
                messages.error(request, 'Relatório não disponível!')
                render(request, 'relatorios/relatorios.html')
            else:
                df = df.to_html(index=False)

                diretorio = os.getcwd()
                for i in os.listdir(diretorio):
                    if i == arquivo:
                        caminho = os.path.join(diretorio, arquivo)
                        os.remove(caminho)

                arquivo = arquivo.replace('-', '/').replace('.xlsx', '').replace('.txt', '')

            return render(request, "relatorios/relatorios.html",
                          context={'relatorio': df, 'nome': arquivo, 'mes': mes, 'ano': ano, 'mes2': mes2, 'ano2': ano2,
                                   'matricula': matricula, 'tipo': tipo, 'tipo3': tipo3})
    except Exception as e:
        messages.error(request, f'Erro {e}')
        return render(request, "relatorios/relatorios.html")
    else:
        return render(request, "usuarios/login.html")


def imprime(request):
    if request.user.is_authenticated:
        arquivo, response = '', ''
        mes = request.POST.get('mes')
        ano = request.POST.get('ano')
        mes2 = request.POST.get('mes2')
        ano2 = request.POST.get('ano2')
        tipo2 = request.POST.get('tipo2')
        matricula = request.POST.get('matricula')
        tipo3 = request.POST.get('tipo3')

        if tipo2 == 'solicitacao':
            response, arquivo, df = gera_relatorio_solicitacao(mes, ano, mes2, ano2, matricula)

        if tipo2 == 'erros2':
            response, arquivo, df = gera_relatorio_erros(mes, ano, mes2, ano2, 'solicitacao', matricula)

        if tipo2 == 'confirmacao':
            response, arquivo, df = gera_relatorio_confirmacao(mes, ano, mes2, ano2, matricula)

        if tipo2 == 'erros':
            response, arquivo, df = gera_relatorio_erros(mes, ano, mes2, ano2, 'confirmacao', matricula)

        if tipo2 == 'entrada_saida':
            response, arquivo, df = gera_relatorio_entrada_saida(mes, ano, mes2, ano2, matricula)

        if tipo2 == 'cod_90':
            response, arquivo, df = gera_relatorio_codigo90(mes, ano, mes2, ano2, matricula)

        if tipo2 == 'negativos':

            if tipo3 == '':
                response, arquivo, df = gera_relatorio_negativos(mes, ano, mes2, ano2, 'confirmacao', matricula)
            else:
                response, arquivo, df = gera_relatorio_negativos(mes, ano, mes2, ano2, tipo3, matricula)

        if tipo2 == 'negativos2':
            response, arquivo, df = gera_relatorio_negativos(mes, ano, mes2, ano2, 'solicitacao', matricula)

        if tipo2 == 'rejeitar_batidas':
            response, arquivo, df = gera_relatorio_rejeitar_batidas(mes, ano, mes2, ano2, matricula)

        if tipo2 == 'rejeitadas':
            response, arquivo, df = gera_relatorio_rejeitadas(mes, ano, mes2, ano2, matricula)

        if tipo2 == 'pagas':
            response, arquivo, df = gera_relatorio_pagas(mes, ano, matricula, mes2, ano2)

        if tipo2 == 'setores':
            response, arquivo, df = gera_relatorio_setores(mes, ano, mes2, ano2)

        if tipo2 == 'voltar_negativos':
            response, arquivo, df = gera_voltar_negativos(mes, ano)

        diretorio = os.getcwd()
        for i in os.listdir(diretorio):
            if i == arquivo:
                caminho = os.path.join(diretorio, arquivo)
                os.remove(caminho)

        if response == '':
            pagina = request.POST.get('pagina')
            if pagina == 'processar':
                relatorio = request.POST.get('relatorio')
                nome = request.POST.get('nome')
                tipo = request.POST.get('tipo')
                messages.error(request, 'Relatório não disponível!')
                return render(request, "horas_extras/processar.html",
                              context={'relatorio': relatorio, 'nome': nome, 'mes': mes,
                                       'ano': ano, 'tipo': tipo, 'matricula': matricula})
            if pagina == 'reprocessar':
                relatorio = request.POST.get('relatorio')
                nome = request.POST.get('nome')
                tipo = request.POST.get('tipo')
                messages.error(request, 'Relatório não disponível!')
                return render(request, "horas_extras/reprocessar.html",
                              context={'relatorio': relatorio, 'nome': nome, 'mes': mes,
                                       'ano': ano, 'tipo': tipo, 'matricula': matricula})
            else:
                render(request, 'relatorios/relatorios.html')
        else:
            return response
    else:
        return render(request, "usuarios/login.html")
