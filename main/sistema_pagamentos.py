# main/sistema_pagamentos.py
class SistemaPagamentos:
    def __init__(self):
        # pagamentos: email -> list of Evento
        self.pagamentos = {}

    def processar_pagamento(self, participante, evento):
        eventos_pagos = self.pagamentos.get(participante.email, [])
        if evento.nome in [e.nome for e in eventos_pagos]:
            print(f"{participante.nome} já realizou o pagamento do evento '{evento.nome}'.")
            return
        eventos_pagos.append(evento)
        self.pagamentos[participante.email] = eventos_pagos
        print(f"Pagamento de R${evento.preco} registrado para {participante.nome} no evento '{evento.nome}'.")

    def listar_pagamentos(self, participante=None):
        if participante:
            eventos_pagos = self.pagamentos.get(participante.email, [])
            print(f"\nPagamentos de {participante.nome}:")
            for e in eventos_pagos:
                print(f"- {e.nome} - R${e.preco}")
        else:
            print("\nTodos os pagamentos registrados:")
            for email, eventos in self.pagamentos.items():
                print(f"{email}:")
                for e in eventos:
                    print(f" - {e.nome} - R${e.preco}")

    def get_receita_evento(self, evento):
        """Retorna a receita total arrecadada para um evento (somando pagamentos registrados)."""
        total = 0.0
        for eventos in self.pagamentos.values():
            for e in eventos:
                if e.nome == evento.nome:
                    total += e.preco
        return total
