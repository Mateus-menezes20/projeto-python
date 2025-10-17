# main/sistema_relatorios.py
class SistemaRelatorios:
    def gerar_relatorio_eventos(self, sistema_eventos, sistema_pagamentos=None):
        print("\n==================== RELATÓRIO DE EVENTOS ====================")
        for evento in sistema_eventos.eventos:
            print(f"\nEvento: {evento.nome}")
            print(f"Data: {evento.data}")
            print(f"Local: {evento.local}")
            print(f"Categoria: {evento.categoria}")
            print(f"Preço: R${evento.preco}")
            print(f"Capacidade máxima: {evento.capacidade_maxima}")
            print(f"Total de inscritos: {len(evento.inscritos)}")
            if evento.inscritos:
                inscritos_nomes = ', '.join([p.nome for p in evento.inscritos])
                print(f"Inscritos: {inscritos_nomes}")
            else:
                print("Inscritos: Nenhum")

            print(f"Total de presenças: {len(evento.presenca)}")
            if evento.presenca:
                presenca_nomes = ', '.join([p.nome for p in evento.presenca])
                print(f"Presenças: {presenca_nomes}")
            else:
                print("Presenças: Nenhuma")
            print(f"Vagas disponíveis: {evento.vagas_disponiveis()}")
            if sistema_pagamentos:
                receita = sistema_pagamentos.get_receita_evento(evento)
                print(f"Receita arrecadada: R${receita}")
            print("--------------------------------------------------------------")
        print("====================== FIM DO RELATÓRIO ======================\n")
