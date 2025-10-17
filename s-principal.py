import sys
import os
from datetime import datetime

# =========================
# Adiciona a pasta "main" no caminho do Python
# =========================
main_path = os.path.join(os.path.dirname(__file__), "main")
if main_path not in sys.path:
    sys.path.insert(0, main_path)

# =========================
# Importando módulos
# =========================
try:
    from sistema_eventos import Evento, Workshop, Palestra, Participante, SistemaEventos
    from sistema_login import SistemaLogin
    from sistema_pagamentos import SistemaPagamentos
    from sistema_relatorios import SistemaRelatorios
except ModuleNotFoundError as e:
    print("Erro de importação:", e)
    print("Verifique se todos os arquivos estão dentro da pasta 'main'.")
    sys.exit(1)

# =========================
# Função principal
# =========================
def main():
    print("=== Sistema de Gerenciamento de Eventos ===")

    # Inicialização dos sistemas
    sistema_eventos = SistemaEventos()
    sistema_login = SistemaLogin()
    sistema_pagamentos = SistemaPagamentos()
    sistema_relatorios = SistemaRelatorios()

    # =========================
    # Criando eventos
    # =========================
    evento1 = Workshop("Oficina de Artes", "Rua Bartolomeu", 50, "Artes", 20, "Tinta e pincel")
    evento1.adicionar_data("19/11/2025")

    evento2 = Palestra("Artes Cênicas Modernas", "Rua Eucalipto", 60, "Artes", 50, "Prof. João Silva")
    evento2.adicionar_data("20/11/2025")

    sistema_eventos.adicionar_evento(evento1)
    sistema_eventos.adicionar_evento(evento2)

    # =========================
    # Cadastro e login
    # =========================
    sistema_login.cadastrar("andrew19@gmail.com", "senha123")
    login_ok = sistema_login.autenticar("andrew19@gmail.com", "senha123")

    if not login_ok:
        print("Erro no login! Encerrando sistema.")
        return

    participante1 = Participante("Andrew", "andrew19@gmail.com")
    sistema_eventos.cadastrar_participante(participante1)

    # =========================
    # Inscrição e pagamento
    # =========================
    try:
        participante1.add_evento(evento1)
        sistema_pagamentos.processar_pagamento(participante1, evento1)
        print(f"\n {participante1.nome} inscrito com sucesso no evento '{evento1.nome}'.")
    except ValueError as e:
        print("Erro na inscrição:", e)

    # =========================
    # Check-in (presença)
    # =========================
    evento1.adicionar_presenca(participante1)

    # =========================
    # Listar eventos
    # =========================
    print("\nLista de eventos disponíveis:")
    for e in sistema_eventos.eventos:
        data_formatada = e.data.strftime("%d/%m/%Y") if e.data else "Data não definida"
        vagas_disponiveis = e.vagas_disponiveis()
        print(f" - {e.nome} ({e.categoria}) em {data_formatada} - R${e.preco:.2f} | Vagas: {vagas_disponiveis}")

    # =========================
    # Buscar por categoria
    # =========================
    print("\nEventos na categoria 'Artes':")
    for e in sistema_eventos.eventos_por_categoria("Artes"):
        print(f"  • {e.nome}")

    # =========================
    # Listar eventos com vagas disponíveis
    # =========================
    print("\nEventos com vagas disponíveis:")
    for e in sistema_eventos.listar_eventos_com_vagas():
        print(f"  • {e.nome} ({e.vagas_disponiveis()} vagas)")

    # =========================
    # Relatórios
    # =========================
    sistema_relatorios.gerar_relatorio_eventos(sistema_eventos)

    # =========================
    # Persistência de dados
    # =========================
    arquivo_dados = os.path.join(os.path.dirname(__file__), "dados_eventos.json")
    sistema_eventos.save_to_json(arquivo_dados)
    print(f"\n Dados salvos em: {arquivo_dados}")

    # =========================
    # Receita total do evento (exemplo)
    # =========================
    receita = len(evento1.inscritos) * evento1.preco
    print(f"\n Receita total do evento '{evento1.nome}': R${receita:.2f}")

# =========================
# Execução principal
# =========================
if __name__ == "__main__":
    main()
