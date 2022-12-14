import sys
sys.path.insert(0, ".\src")
import unittest as u
import classes as c
from pygame.math import Vector2
from datetime import date
import re

def setUpModule():
    print("Iniciando rodada de testes")

def tearDownModule():
    print("Finalizando rodada de testes")
    
class TesteClasses(u.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Realizando testes do módulo classes")
    @classmethod
    def tearDownClass(cls):
        print("Terminando testes do módulo classes")
        
    def setUp(self):
        print("Executando SetUpMethod")
    
    def tearDown(self):
        print("Executando TearDownMethod")
    
    def test_case_trem_mover_trem_false(self):
        print("Executando Caso de Teste: Mover trem sem novo vagão")
        trem = c.Trem()
        trem.mover_trem()
        self.assertEqual(trem.corpo, [Vector2(6,2), Vector2(5,2), Vector2(4,2)])
    
    def test_case_trem_mover_trem_true(self):
        print("Executando Caso de Teste: Mover trem com novo vagão")
        trem = c.Trem()
        trem.novo_vagao = True
        trem.mover_trem()
        self.assertEqual(trem.corpo, [Vector2(6,2), Vector2(5,2), Vector2(4,2), Vector2(3,2)])
        print("O vagão novo foi adicionado")
        self.assertFalse(trem.novo_vagao)
        print("O tamanho do trem foi fixado")
    
    def test_case_recorde_escrever(self):
        recorde = c.Recorde("Individuo")
        recorde.escrever(1000, 2)
        recorde.arquivo.seek(0,0)
        linhas = recorde.arquivo.readlines()
        nome, data, pontuacao, tempo = re.split("\|", linhas[-1])
        self.assertEqual(f"{nome}|{data}|{pontuacao}|{tempo}", f"Individuo|{date.today()}|1000|2\n")



if __name__ == "__main__":
    u.main(verbosity=2)
