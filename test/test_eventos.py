# tests/test_eventos.py
import sys
import os
import unittest
import tempfile
import json

# garante import de 'main'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "main"))

from sistema_eventos import Evento, Workshop, Palestra, Participante, SistemaEventos
from sistema_pagamentos import SistemaPagamentos
from sistema_relatorios import SistemaRelatorios
from datetime import datetime

class TestSistemaEventos(unittest.TestCase):

    def test_capacidade_positiva(self):
        with self.assertRaises(ValueError):
            Evento("E1", "Local", 0, "cat", 10)  # capacidade 0 inválida

    def test_data_nao_passada(self):
        e = Evento("E2", "Local", 10, "cat", 5)
        future = (datetime.now().date().replace(year=datetime.now().year + 1)).strftime("%d/%m/%Y")
        e.adicionar_data(future)
        self.assertIsNotNone(e.data)

        with self.assertRaises(ValueError):
            e.adicionar_data("01/01/2000")  # data passada

    def test_inscricao_e_vagas(self):
        e = Evento("E3", "Local", 2, "cat", 0)
        p1 = Participante("A", "a@example.com")
        p2 = Participante("B", "b@example.com")
        p1.add_evento(e)
        p2.add_evento(e)
        self.assertEqual(e.vagas_disponiveis(), 0)
        with self.assertRaises(ValueError):
            p3 = Participante("C", "a@example.com")  # mesmo email não pode inscrever no mesmo evento
            p3.add_evento(e)

    def test_prevenir_duplicidade_email(self):
        e = Evento("E4", "Local", 3, "cat", 0)
        p = Participante("X", "x@example.com")
        p.add_evento(e)
        with self.assertRaises(ValueError):
            p2 = Participante("X2", "x@example.com")
            p2.add_evento(e)

    def test_cancelar_inscricao(self):
        e = Evento("E5", "Local", 5, "cat", 0)
        p = Participante("P", "p@example.com")
        p.add_evento(e)
        p.cancelar_inscricao(e)
        self.assertNotIn(p, e.inscritos)

    def test_checkin_presenca(self):
        e = Evento("E6", "Local", 5, "cat", 0)
        p = Participante("Q", "q@example.com")
        p.add_evento(e)
        e.adicionar_presenca(p)
        self.assertIn(p, e.presenca)

    def test_persistencia_json(self):
        se = SistemaEventos()
        e1 = Workshop("W1", "L", 5, "tech", 10, "caderno")
        e2 = Palestra("P1", "L2", 10, "tech", 0, "Dr. Who")
        se.adicionar_evento(e1)
        se.adicionar_evento(e2)
        p = Participante("U", "u@example.com")
        se.cadastrar_participante(p)
        p.add_evento(e1)
        # salvar
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        se.save_to_json(path)
        # carregar em novo sistema
        se2 = SistemaEventos()
        se2.load_from_json(path)
        # as events carregados devem existir
        nomes = [ev.nome for ev in se2.eventos]
        self.assertIn("W1", nomes)
        os.remove(path)

    def test_receita_evento(self):
        se = SistemaEventos()
        e = Evento("E7", "L", 10, "cat", 50)
        se.adicionar_evento(e)
        p1 = Participante("A", "a1@example.com")
        p2 = Participante("B", "b1@example.com")
        # inscrever
        p1.add_evento(e)
        p2.add_evento(e)
        sp = SistemaPagamentos()
        sp.processar_pagamento(p1, e)
        sp.processar_pagamento(p2, e)
        self.assertEqual(sp.get_receita_evento(e), 100)

    def test_listar_eventos_com_vagas(self):
        se = SistemaEventos()
        e1 = Evento("E8", "L", 2, "cat", 10)
        e2 = Evento("E9", "L", 1, "cat", 10)
        se.adicionar_evento(e1)
        se.adicionar_evento(e2)
        p = Participante("Z", "z@example.com")
        p.add_evento(e2)  # lota e2
        vagas = se.listar_eventos_com_vagas()
        nomes = [ev.nome for ev in vagas]
        self.assertIn("E8", nomes)
        self.assertNotIn("E9", nomes)

    def test_polimorfismo_detalhes(self):
        w = Workshop("W2", "L", 5, "tech", 15, "lapis")
        p = Palestra("P2", "L", 5, "talk", 0, "Prof X")
        self.assertIn("Material", w.detalhes())
        self.assertIn("Palestrante", p.detalhes())

    def test_cadastrar_participante_no_sistema(self):
        se = SistemaEventos()
        p = Participante("Nome", "nom@example.com")
        se.cadastrar_participante(p)
        self.assertIsNotNone(se.get_participante("nom@example.com"))

if __name__ == "__main__":
    unittest.main()
