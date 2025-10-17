# main/sistema_eventos.py
from datetime import datetime
import json
from typing import List, Dict

# -------------------------
# Classe base Evento
# -------------------------
class Evento:
    def __init__(self, nome: str, local: str, capacidade_maxima: int, categoria: str, preco: float):
        if capacidade_maxima <= 0:
            raise ValueError("capacidade_maxima deve ser um número positivo.")
        self.__nome = nome
        self.__data = None  # datetime.date
        self.__local = local
        self.__capacidade_maxima = int(capacidade_maxima)
        self.__categoria = categoria
        self.__preco = float(preco)
        self.__inscritos: List['Participante'] = []
        self.__presenca: List['Participante'] = []

    def __str__(self):
        return f"{self.__nome}"

    def __repr__(self):
        return self.__str__()

    # --- properties ---
    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        self.__nome = valor

    @property
    def data(self):
        return self.__data

    @property
    def local(self):
        return self.__local

    @local.setter
    def local(self, valor):
        self.__local = valor

    @property
    def capacidade_maxima(self):
        return self.__capacidade_maxima

    @capacidade_maxima.setter
    def capacidade_maxima(self, valor):
        if valor <= 0:
            raise ValueError("capacidade_maxima deve ser um número positivo.")
        self.__capacidade_maxima = int(valor)

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, valor):
        self.__categoria = valor

    @property
    def preco(self):
        return self.__preco

    @preco.setter
    def preco(self, valor):
        self.__preco = float(valor)

    @property
    def inscritos(self):
        return self.__inscritos

    @property
    def presenca(self):
        return self.__presenca

    # --- métodos ---
    def adicionar_data(self, data_str: str):
        """Recebe string dd/mm/YYYY; valida data (não pode ser passada)."""
        data_evento = datetime.strptime(data_str, "%d/%m/%Y").date()
        data_atual = datetime.now().date()
        if data_atual <= data_evento:
            self.__data = data_evento
        else:
            raise ValueError("A data do evento não pode ser anterior à data atual.")

    def adicionar_presenca(self, pessoa: 'Participante'):
        """Marca presença se inscrito e não duplicar presença."""
        if pessoa in self.__inscritos and pessoa not in self.__presenca:
            self.__presenca.append(pessoa)

    def vagas_disponiveis(self) -> int:
        return self.__capacidade_maxima - len(self.__inscritos)

    # serialização
    def to_dict(self) -> Dict:
        base = {
            "tipo": self.__class__.__name__,
            "nome": self.__nome,
            "data": self.__data.strftime("%d/%m/%Y") if self.__data else None,
            "local": self.__local,
            "capacidade_maxima": self.__capacidade_maxima,
            "categoria": self.__categoria,
            "preco": self.__preco,
            "inscritos": [p.email for p in self.__inscritos],
            "presenca": [p.email for p in self.__presenca],
        }
        return base

    @staticmethod
    def from_dict(data: Dict) -> 'Evento':
        tipo = data.get("tipo", "Evento")
        # constrói de acordo com o tipo
        if tipo == "Workshop":
            ev = Workshop(
                data.get("nome"),
                data.get("local"),
                int(data.get("capacidade_maxima")),
                data.get("categoria"),
                float(data.get("preco")),
                data.get("material_necessario", "")
            )
        elif tipo == "Palestra":
            ev = Palestra(
                data.get("nome"),
                data.get("local"),
                int(data.get("capacidade_maxima")),
                data.get("categoria"),
                float(data.get("preco")),
                data.get("palestrante", "")
            )
        else:
            ev = Evento(
                data.get("nome"),
                data.get("local"),
                int(data.get("capacidade_maxima")),
                data.get("categoria"),
                float(data.get("preco")),
            )
        if data.get("data"):
            try:
                ev.adicionar_data(data.get("data"))
            except ValueError:
                # ignore invalid saved date
                ev._Evento__data = None
        # inscritos/presenca serão reconectados pelo SistemaEventos ao carregar participantes
        return ev


# -------------------------
# Subclasses: Workshop e Palestra
# -------------------------
class Workshop(Evento):
    def __init__(self, nome, local, capacidade_maxima, categoria, preco, material_necessario: str):
        super().__init__(nome, local, capacidade_maxima, categoria, preco)
        self.__material_necessario = material_necessario

    @property
    def material_necessario(self):
        return self.__material_necessario

    @material_necessario.setter
    def material_necessario(self, valor):
        self.__material_necessario = valor

    def detalhes(self):
        return f"Workshop: {self.nome} - Material necessário: {self.__material_necessario}"


class Palestra(Evento):
    def __init__(self, nome, local, capacidade_maxima, categoria, preco, palestrante: str):
        super().__init__(nome, local, capacidade_maxima, categoria, preco)
        self.__palestrante = palestrante

    @property
    def palestrante(self):
        return self.__palestrante

    @palestrante.setter
    def palestrante(self, valor):
        self.__palestrante = valor

    def detalhes(self):
        return f"Palestra: {self.nome} - Palestrante: {self.__palestrante}"


# -------------------------
# Participante
# -------------------------
class Participante:
    def __init__(self, nome: str, email: str):
        self.__nome = nome
        self.__email = email
        self.__evento_inscrito: List[Evento] = []

    def __str__(self):
        return f"{self.__nome}"

    def __repr__(self):
        return self.__str__()

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        self.__nome = valor

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        self.__email = valor

    @property
    def evento_inscrito(self):
        return self.__evento_inscrito

    def add_evento(self, evento: Evento):
        if evento.vagas_disponiveis() <= 0:
            raise ValueError(f"Erro! O evento '{evento.nome}' está lotado.")
        for inscrito in evento.inscritos:
            if inscrito.email == self.__email:
                raise ValueError(f"Email '{self.__email}' já registrado no evento '{evento.nome}'.")
        self.__evento_inscrito.append(evento)
        evento.inscritos.append(self)

    def cancelar_inscricao(self, evento: Evento):
        if evento in self.__evento_inscrito:
            self.__evento_inscrito.remove(evento)
        if self in evento.inscritos:
            evento.inscritos.remove(self)


# -------------------------
# SistemaEventos (gerenciamento)
# -------------------------
class SistemaEventos:
    def __init__(self):
        self.__eventos: List[Evento] = []
        self.__participantes: Dict[str, Participante] = {}  # email -> Participante

    @property
    def eventos(self) -> List[Evento]:
        return self.__eventos

    def adicionar_evento(self, evento: Evento):
        self.__eventos.append(evento)

    def cadastrar_participante(self, participante: Participante):
        if participante.email in self.__participantes:
            raise ValueError("Participante já cadastrado no sistema.")
        self.__participantes[participante.email] = participante

    def get_participante(self, email: str) -> Participante:
        return self.__participantes.get(email)

    def eventos_por_categoria(self, categoria: str) -> List[Evento]:
        return [e for e in self.__eventos if e.categoria.lower() == categoria.lower()]

    def eventos_por_data(self, data_str: str) -> List[Evento]:
        data_evento = datetime.strptime(data_str, "%d/%m/%Y").date()
        return [e for e in self.__eventos if e.data == data_evento]

    def listar_eventos_com_vagas(self) -> List[Evento]:
        return [e for e in self.__eventos if e.vagas_disponiveis() > 0]

    # Persistência simples em JSON:
    def save_to_json(self, filepath: str):
        data = {
            "eventos": [e.to_dict() for e in self.__eventos],
            # participantes serão gravados apenas emails -> names for simple restore
            "participantes": {email: {"nome": p.nome, "eventos": [ev.nome for ev in p.evento_inscrito]} for email, p in self.__participantes.items()}
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_from_json(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        # recriar eventos (sem inscritos ainda)
        nome_para_evento = {}
        self.__eventos = []
        for evdata in data.get("eventos", []):
            ev = Evento.from_dict(evdata)
            self.__eventos.append(ev)
            nome_para_evento[ev.nome] = ev
        # recriar participantes e reinscrever
        self.__participantes = {}
        for email, pdata in data.get("participantes", {}).items():
            p = Participante(pdata["nome"], email)
            self.__participantes[email] = p
            for evnome in pdata.get("eventos", []):
                evobj = nome_para_evento.get(evnome)
                if evobj:
                    try:
                        p.add_evento(evobj)
                    except Exception:
                        # se por algum motivo não conseguir reinscrever (capacidade), ignora
                        pass
