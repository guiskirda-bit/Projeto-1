import random
import datetime

# ================= MENU =================

def menu():
    arquivo = "log.txt"

    while True:
        print("\n=== MONITOR LOGPY ===")
        print("1 - Gerar logs")
        print("2 - Analisar logs")
        print("3 - Gerar e analisar")
        print("4 - Sair")

        op = input("Escolha: ")

        if op == "1":
            try:
                q = int(input("Quantidade: "))
                gerar_arquivo_logs(arquivo, q)
            except:
                print("Valor inválido")

        elif op == "2":
            analisar_arquivo_logs(arquivo)

        elif op == "3":
            try:
                q = int(input("Quantidade: "))
                gerar_arquivo_logs(arquivo, q)
                analisar_arquivo_logs(arquivo)
            except:
                print("Valor inválido")

        elif op == "4":
            print("Encerrando...")
            break
        else:
            print("Opção inválida")


# ================= GERAÇÃO =================

def gerar_arquivo_logs(nome_arquivo, quantidade):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        for i in range(quantidade):
            linha = montar_linha_log(i)
            f.write(linha + "\n")

    print("Logs criados com sucesso!")


def montar_linha_log(i):
    data = gerar_data(i)
    ip = gerar_ip(i)
    metodo = gerar_metodo()
    recurso = gerar_recurso()
    status = gerar_status(recurso)
    tempo = gerar_tempo(i)
    tamanho = gerar_tamanho()
    protocolo = gerar_protocolo()
    agente = gerar_user_agent()
    referer = gerar_referer()

    return f"[{data}] {ip} - {metodo} - {status} - {recurso} - {tempo}ms - {tamanho}B - {protocolo} - {agente} - {referer}"


def gerar_data(i):
    base = datetime.datetime(2026, 3, 23, 10, 0, 0)
    return (base + datetime.timedelta(seconds=i * random.randint(5, 15))).strftime("%d/%m/%Y %H:%M:%S")


def gerar_ip(i):
    if 5 <= i <= 20:
        return "200.1.1.1"  # suspeito
    return f"192.168.0.{random.randint(1, 10)}"


def gerar_metodo():
    r = random.randint(1, 3)
    if r == 1:
        return "GET"
    elif r == 2:
        return "POST"
    else:
        return "PUT"


def gerar_recurso():
    r = random.randint(1, 6)
    if r == 1:
        return "/home"
    elif r == 2:
        return "/login"
    elif r == 3:
        return "/admin"
    elif r == 4:
        return "/config"
    elif r == 5:
        return "/api"
    else:
        return "/produto"


def gerar_status(recurso):
    r = random.randint(1, 10)

    if recurso == "/login" and r <= 4:
        return 403
    elif recurso == "/admin" and r <= 3:
        return 403
    elif r == 1:
        return 500
    elif r <= 3:
        return 404
    else:
        return 200


def gerar_tempo(i):
    if 20 <= i <= 30:
        return 200 + i * 50  # degradação
    return random.randint(100, 1200)


def gerar_tamanho():
    return random.randint(200, 2000)


def gerar_protocolo():
    return "HTTP/1.1"


def gerar_user_agent():
    r = random.randint(1, 5)
    if r == 5:
        return "Bot"
    return "Chrome"


def gerar_referer():
    return "/home"


# ================= ANÁLISE =================

def analisar_arquivo_logs(nome_arquivo):
    try:
        total = sucesso = erro = erro500 = 0
        soma_tempo = maior = 0
        menor = 99999

        rapido = normal = lento = 0

        s200 = s403 = s404 = s500 = 0

        recurso_mais = ""
        recurso_cont = 0
        recurso_atual = ""
        cont_recurso = 0

        ip_mais = ""
        ip_mais_cont = 0

        ip_erro = ""
        ip_erro_cont = 0

        brute = 0
        seq_login = 0
        ultimo_brute = ""

        admin_err = 0

        degradacao = 0
        seq_tempo = 0
        tempo_ant = 0

        falha = 0
        seq_500 = 0

        bot = 0
        rep_ip = 0
        ip_ant = ""

        rotas = 0
        rotas_err = 0

        with open(nome_arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                total += 1

                # EXTRAÇÃO MANUAL
                campo = ""
                parte = 0

                ip = ""
                status = ""
                recurso = ""
                tempo = ""

                for c in linha:
                    if c == "-":
                        parte += 1
                        if parte == 1:
                            ip = campo.strip()
                        elif parte == 3:
                            status = campo.strip()
                        elif parte == 4:
                            recurso = campo.strip()
                        campo = ""
                    elif c == "m" and parte == 4:
                        tempo = campo.strip()
                        break
                    else:
                        campo += c

                try:
                    status = int(status)
                    tempo = int(tempo)
                except:
                    continue

                # CONTAGENS
                if status == 200:
                    sucesso += 1
                    s200 += 1
                else:
                    erro += 1

                if status == 403:
                    s403 += 1
                elif status == 404:
                    s404 += 1
                elif status == 500:
                    s500 += 1
                    erro500 += 1

                soma_tempo += tempo

                if tempo > maior:
                    maior = tempo
                if tempo < menor:
                    menor = tempo

                # TEMPO
                if tempo < 200:
                    rapido += 1
                elif tempo < 800:
                    normal += 1
                else:
                    lento += 1

                # RECURSO MAIS ACESSADO (sequencial simples)
                if recurso == recurso_atual:
                    cont_recurso += 1
                else:
                    if cont_recurso > recurso_cont:
                        recurso_cont = cont_recurso
                        recurso_mais = recurso_atual
                    recurso_atual = recurso
                    cont_recurso = 1

                # FORÇA BRUTA
                if recurso == "/login" and status == 403:
                    seq_login += 1
                    if seq_login >= 3:
                        brute += 1
                        ultimo_brute = ip
                else:
                    seq_login = 0

                # ADMIN
                if recurso == "/admin" and status != 200:
                    admin_err += 1

                # ROTAS SENSÍVEIS
                if recurso == "/admin" or recurso == "/config":
                    rotas += 1
                    if status != 200:
                        rotas_err += 1

                # DEGRADAÇÃO
                if tempo > tempo_ant:
                    seq_tempo += 1
                    if seq_tempo >= 3:
                        degradacao += 1
                else:
                    seq_tempo = 0
                tempo_ant = tempo

                # ERRO 500
                if status == 500:
                    seq_500 += 1
                    if seq_500 >= 3:
                        falha += 1
                else:
                    seq_500 = 0

                # BOT
                if ip == ip_ant:
                    rep_ip += 1
                    if rep_ip >= 5:
                        bot += 1
                else:
                    rep_ip = 1
                ip_ant = ip

        media = soma_tempo / total
        disponibilidade = (sucesso / total) * 100
        taxa_erro = (erro / total) * 100

        estado = "SAUDÁVEL"
        if falha > 0 or disponibilidade < 70:
            estado = "CRÍTICO"
        elif disponibilidade < 85:
            estado = "INSTÁVEL"
        elif disponibilidade < 95 or bot > 0:
            estado = "ATENÇÃO"

        print("\n===== RELATÓRIO =====")
        print("Total:", total)
        print("Sucesso:", sucesso)
        print("Erros:", erro)
        print("Erro 500:", erro500)

        print("Disponibilidade:", disponibilidade)
        print("Taxa erro:", taxa_erro)

        print("Tempo médio:", media)
        print("Maior:", maior)
        print("Menor:", menor)

        print("Rápido:", rapido)
        print("Normal:", normal)
        print("Lento:", lento)

        print("200:", s200)
        print("403:", s403)
        print("404:", s404)
        print("500:", s500)

        print("Recurso mais acessado:", recurso_mais)

        print("Força bruta:", brute)
        print("Último brute:", ultimo_brute)

        print("Admin indevido:", admin_err)

        print("Degradação:", degradacao)
        print("Falha crítica:", falha)

        print("Bots:", bot)

        print("Rotas sensíveis:", rotas)
        print("Erros rotas:", rotas_err)

        print("Estado final:", estado)

    except FileNotFoundError:
        print("Arquivo não encontrado")


menu()
