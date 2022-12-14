import pygame, sys
from classes import Botao, Partida, SubMenu
from googletrans import Translator
import time
import httpcore
import re

# Inicia o módulo PyGame.
pygame.init()


# Quantidade de células no mapa.
cn = 25
# Tamanho das células.
cs = 32

# Define as dimensões da tela do jogo.
screen = pygame.display.set_mode((cn * cs,cn * cs)) 
pygame.display.set_caption("Metrô")


# Imagem de fundo do menu principal.
estacao_com_metro = pygame.image.load("imagens/estação_menu.jpg")
# Imagem de fundo do menu Jogar, Opção e Créditos.
estacao_sem_metro = pygame.image.load("imagens/estação_sem_metro.jpeg")
retang_fundo = pygame.image.load("imagens/retang_fundo.png")

class Menu:
    """ Classe responsável por gerar e gerir o menu principal, o de créditos, o de opções e o de jogar. Os objetos dessa classe são a 
        base para o funcionamento do jogo.
    """
    def __init__(self, screen=pygame.display.set_mode((cn * cs,cn * cs)) , estacao_com_metro=pygame.image.load("imagens/estação_menu.jpg"), estacao_sem_metro=pygame.image.load("imagens/estação_sem_metro.jpeg"), retang_fundo=pygame.image.load("imagens/retang_fundo.png"),cn=25, cs=32):
        """ Construtor da classe.

        Args:
            self: palavra-chave que acessa os atributos e métodos da classe Menu.
            screen (pygame.Surface): janela do programa.
            estacao_com_metro: imagem de fundo do menu principal.
            estacao_sem_metro: imagem de fundo para os menus de jogar, opções e créditos.
            retang_fundo: imagem semitransparente.
            cn (int): Número de células da janela do programa.
            cs (int): Tamanho das células.
        """ 
        self.screen = screen
        self.imagem_menu_principal = estacao_com_metro
        self.imagem_submenus = estacao_sem_metro
        self.retang_fundo = retang_fundo
        self.cn = cn
        self.cs = cs
        # Cria os objetos da classe SubMenu
        self.fontes = [pygame.font.Font(None, 120), pygame.font.Font(None, 30)]
        self.submenu = SubMenu(cn, cs, screen, self.fontes, "Jogador")
        self.tradutor = Translator()
        self.idiomas = ["Português", "Inglês", "Francês", "Latim", "Alemão", "Esperanto", "Javanes", "Espanhol"]
        self.fundo = pygame.image.load("imagens/retang_fundo.png")


    def fonte(self, tamanho): 
        """ Reponsável por carregar a fonte "caverson".
        :return pygame.font.Font("imagens/caverson.otf", tamanho): fonte de letra com tamanho definido.
        Args:
            tamanho (int): tamanho da escrita.
        """ 
        return pygame.font.Font("imagens/caverson.otf", tamanho)


    def jogar(self):
        """ Função reponsável pelo submenu "Jogar", ou seja, a interface do cadastro, da seleção de fases e das intruções.

        Args:
            self: palavra-chave que acessa os atributos e métodos da classe Menu.
        """
        jogar_textos = self.traduzir_lingua("jogar_textos")
        txt_1, txt_2, fa, fa_1, fa_2, fa_3, fa_4, fa_5, volta = re.split("\.", jogar_textos)
        while True:
            # Cria a superfície da imagem de fundo.
            fundo_rect = pygame.Rect(0, 0, self.cs * self.cn, self.cs * self.cn)         # (Xo, Yo, X, Y)
            # Ajusta as dimensões da imagem de fundo.
            imagem_fundo = pygame.transform.scale(self.imagem_submenus, (self.cs * self.cn, self.cs * self.cn))
            # SCREEN.blit(nome_imagem, (x_pos, y_pos))
            self.screen.blit(imagem_fundo, fundo_rect)

            # Cria a superfície das instruções.
            intrucoes_rect = pygame.Rect(380, 330, 750, 650)     # (Xo, Yo, X, Y)
            # Ajusta as dimensões do retangulo_cinza.
            fundo_intrucoes = pygame.transform.scale(self.retang_fundo, (370, 320))      # (deltaX, deltaY)
            # Ajusta as dimensões da imagem de fundo.
            imagem_intrucoes = pygame.transform.scale(pygame.image.load("imagens/" + self.submenu.idioma + ".png"), (370, 320))
            # SCREEN.blit(nome_imagem, (x_pos, y_pos))
            self.screen.blit(fundo_intrucoes, intrucoes_rect)       # Aplica fundo cinza.
            self.screen.blit(imagem_intrucoes, intrucoes_rect)      # Aplica imagem das instruções.

            # Cria a superfície do quadrado cinza.
            fundo_cinza_rect = pygame.Rect(100, 220, 700, 320)                           # (Xo, Yo, X, Y)
            # Ajusta as dimensões do retangulo_cinza.
            imagem_cinza = pygame.transform.scale(self.retang_fundo, (600, 100))
            # SCREEN.blit(nome_imagem, (x_pos, y_pos))
            self.screen.blit(imagem_cinza, fundo_cinza_rect)

            # Obtem a posição (x,y) do cursor do mouse.
            jogar_mouse_pos = pygame.mouse.get_pos()

            # Título da tela de jogar.
            jogar_titulo = self.fonte(80).render(fa, True, "#e48b39")
            jogar_rect = jogar_titulo.get_rect(center = (400, 120))
            self.screen.blit(jogar_titulo, jogar_rect)

            # Texto da tela de jogar.
            texto_1 = self.fonte(25).render(txt_1+"                        ", True, "#d7fcd4")
            texto_2 = self.fonte(25).render(txt_2, True, "#d7fcd4")
            y_coord = 250
            for texto in [texto_1, texto_2]:
                texto_rect = texto.get_rect(center = (400, y_coord))
                self.screen.blit(texto, texto_rect)
                y_coord += 40

            # BOTÕES
            # Cria o botão da fase 1.
            fase_1 = Botao(imagem = pygame.image.load("imagens/retang_fundo_fases.png"), pos = (200, 370), texto_cont = fa_1, 
                           fonte = self.fonte(22), cor_base = "#d7fcd4", cor_com_mause = "#5b9388")
            # Cria o botão da fase 2.
            fase_2 = Botao(imagem = pygame.image.load("imagens/retang_fundo_fases.png"), pos = (200, 430), texto_cont = fa_2, 
                           fonte = self.fonte(22), cor_base = "#d7fcd4", cor_com_mause = "#5b9388")
            # Cria o botão da fase 3.
            fase_3 = Botao(imagem = pygame.image.load("imagens/retang_fundo_fases.png"), pos = (200, 490), texto_cont = fa_3, 
                           fonte = self.fonte(22), cor_base = "#d7fcd4", cor_com_mause = "#5b9388")
            # Cria o botão da fase 4.
            fase_4 = Botao(imagem = pygame.image.load("imagens/retang_fundo_fases.png"), pos = (200, 550), texto_cont = fa_4, 
                           fonte = self.fonte(22), cor_base = "#d7fcd4", cor_com_mause = "#5b9388")
            # Cria o botão da fase 5.
            fase_5 = Botao(imagem = pygame.image.load("imagens/retang_fundo_fases.png"), pos = (200, 610), texto_cont = fa_5, 
                           fonte = self.fonte(22), cor_base = "#d7fcd4", cor_com_mause = "#5b9388")
            # Cria o botão de voltar.
            jogar_voltar = Botao(imagem = None, pos = (400, 700), texto_cont = volta, 
                                 fonte = self.fonte(50), cor_base = "Black", cor_com_mause = "#568e81")

            # Acionar as funções de atualização e mudança de cor para os botões criados.
            for botao in [fase_1, fase_2, fase_3, fase_4, fase_5, jogar_voltar]:
                botao.mudar_cor(jogar_mouse_pos)
                botao.atualizar(self.screen)

            # pygame.event.get() obtém os eventos que ocorrem.
            for evento in pygame.event.get():
                # Finaliza o programa se o botão X (canto superior direito) for clicado.
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # É checado se o botão esquerdo do mouse clicou sobre algum botão, nesse caso, ele é redirecionado para a referida página.
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if fase_1.checar_clique(jogar_mouse_pos):
                        # Cria os objetos da classe Partida.
                        self.partida = Partida(cn, cs, screen, pygame.font.Font(None, 30), 1, self.submenu.nome, self.submenu.idioma)    # Fase = 1
                        self.submenu.musica.stop()
                        self.partida.inicia_partida()
                        self.submenu.musica.play(-1)

                    if fase_2.checar_clique(jogar_mouse_pos):
                        # Cria os objetos da classe Partida.
                        self.partida = Partida(cn, cs, screen, pygame.font.Font(None, 30), 2, self.submenu.nome, self.submenu.idioma)    # Fase = 2
                        self.submenu.musica.stop()
                        self.partida.inicia_partida()
                        self.submenu.musica.play(-1)

                    if fase_3.checar_clique(jogar_mouse_pos):
                        # Cria os objetos da classe Partida.
                        self.partida = Partida(cn, cs, screen, pygame.font.Font(None, 30), 3, self.submenu.nome, self.submenu.idioma)    # Fase = 3
                        self.submenu.musica.stop()
                        self.partida.inicia_partida()
                        self.submenu.musica.play(-1)

                    if fase_4.checar_clique(jogar_mouse_pos):
                        # Cria os objetos da classe Partida.
                        self.partida = Partida(cn, cs, screen, pygame.font.Font(None, 30), 4, self.submenu.nome, self.submenu.idioma)    # Fase = 4
                        self.submenu.musica.stop()
                        self.partida.inicia_partida()
                        self.submenu.musica.play(-1)

                    if fase_5.checar_clique(jogar_mouse_pos):
                       # Cria os objetos da classe Partida.
                        self.partida = Partida(cn, cs, screen, pygame.font.Font(None, 30), 5, self.submenu.nome, self.submenu.idioma)    # Fase = 5
                        self.submenu.musica.stop()
                        self.partida.inicia_partida()
                        self.submenu.musica.play(-1)

                    if jogar_voltar.checar_clique(jogar_mouse_pos):
                        self.menu_principal()

                        # Espaço para nome do jogador:
                    # Se selecionar o retânculo do nome, começa a escrever o nome do jogador.
                    if self.submenu.cadastro_rect.collidepoint(evento.pos):
                        self.submenu.selecionado = True
                    else:
                        self.submenu.selecionado = False
                
                # Se uma tecla for clicada:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_BACKSPACE and self.submenu.selecionado == True:
                        self.submenu.nome = self.submenu.nome[:-1]
                    elif len(self.submenu.nome) < 20 and self.submenu.selecionado == True:
                        if evento.key != pygame.K_RETURN and evento.key != pygame.K_KP_ENTER:
                            self.submenu.nome += evento.unicode
            self.submenu.desenhar_elementos()  

            # Faz com que a superfície de exibição apareça no monitor do usuário.
            pygame.display.update()
        
    def opcoes(self):
        """ Função reponsável pelo submenu "Opções", ou seja, a interface de controle do volume e do idioma do jogo.

        Args:
            self: palavra-chave que acessa os atributos e métodos da classe Menu.
        """
        # Texto da interface opções.
        opcoes_textos = self.traduzir_lingua("opcoes_textos")
        # Idioma do menu Opções.
        idioma = self.atualizar_idiomas()
        
        idioma[0].selecionado = True
        
        # Volume 0.
        vol_menu_0 = Botao(imagem = pygame.transform.scale(self.fundo, (self.cs, self.cs)), pos = (270, 600), 
                           texto_cont = "0", fonte = self.fonte(25), cor_base = "#d7fcd4", cor_com_mause = "#5b9388")
        # Volume 1.
        vol_menu_1 = Botao(imagem = pygame.transform.scale(self.fundo, (self.cs, self.cs)), pos = (320, 600), 
                           texto_cont = "1", fonte = self.fonte(25), cor_base = "#d7fcd4", cor_com_mause = "#5b9388")
        # Volume 2.
        vol_menu_2 = Botao(imagem = pygame.transform.scale(self.fundo, (self.cs, self.cs)), pos = (370, 600), 
                           texto_cont = "2", fonte = self.fonte(25), cor_base = "#d7fcd4", cor_com_mause = "#5b9388")
        # Volume 3.
        vol_menu_3 = Botao(imagem = pygame.transform.scale(self.fundo, (self.cs, self.cs)), pos = (420, 600), 
                           texto_cont = "3", fonte = self.fonte(25), cor_base = "#d7fcd4", cor_com_mause = "#5b9388")
        # Volume 4.
        vol_menu_4 = Botao(imagem = pygame.transform.scale(self.fundo, (self.cs, self.cs)), pos = (470, 600), 
                           texto_cont = "4", fonte = self.fonte(25), cor_base = "#d7fcd4", cor_com_mause = "#5b9388")
        # Volume 5.
        vol_menu_5 = Botao(imagem = pygame.transform.scale(self.fundo, (self.cs, self.cs)), pos = (520, 600), 
                           texto_cont = "5", fonte = self.fonte(25), cor_base = "#d7fcd4", cor_com_mause = "#5b9388")
        
        vol_menu_5.selecionado = True
        
        condicao = True
        while condicao:
            # Cria a superfície da imagem de fundo.
            fundo_rect = pygame.Rect(0, 0, self.cs * self.cn, self.cs * self.cn)
            # Ajusta as dimensões da imagem de fundo.
            imagem_fundo = pygame.transform.scale(self.imagem_submenus, (self.cs * self.cn, self.cs * self.cn))
            # SCREEN.blit(nome_imagem, (x_pos, y_pos))
            self.screen.blit(imagem_fundo, fundo_rect)
            
            op_t, op_tx, back, vol = re.split("\.", opcoes_textos)
            
            # Renderiza o título.
            opcoes_titulo = self.fonte(80).render(op_t, True, "#e48b39")
            # Superfície do título.
            opcoes_rect_t = opcoes_titulo.get_rect(center=(400, 120))
            # Renderiza o texto.
            opcoes_texto = self.fonte(45).render(op_tx, True, "Black")
            # Superfície do texto.
            opcoes_rect_tx = opcoes_texto.get_rect(center=(400, 210))

            # Obtem a posição (x,y) do cursor do mouse.
            opcoes_menu_pos = pygame.mouse.get_pos()

            # Adicionar à tela de opções.
            self.screen.blit(opcoes_titulo, opcoes_rect_t)
            self.screen.blit(opcoes_texto, opcoes_rect_tx)
            
            # BOTÕES DE IDIOMA.            
            # Idioma português.
            idioma[0].mudar_cor(opcoes_menu_pos)            # Muda de cor se o mouse estiver em cima.
            idioma[0].atualizar(self.screen)                # Adiciona à tela.

            # Idioma inglês.
            idioma[1].mudar_cor(opcoes_menu_pos)
            idioma[1].atualizar(self.screen)

            # Idioma francês.
            idioma[2].mudar_cor(opcoes_menu_pos)
            idioma[2].atualizar(self.screen)

            # Idioma latim.
            idioma[3].mudar_cor(opcoes_menu_pos)
            idioma[3].atualizar(self.screen)

            # Idioma alemão.
            idioma[4].mudar_cor(opcoes_menu_pos)
            idioma[4].atualizar(self.screen)

            # Idioma esperanto.
            idioma[5].mudar_cor(opcoes_menu_pos)
            idioma[5].atualizar(self.screen)

            # Idioma javanes.
            idioma[6].mudar_cor(opcoes_menu_pos)
            idioma[6].atualizar(self.screen)
            
            # Idioma espanhol.
            idioma[7].mudar_cor(opcoes_menu_pos)
            idioma[7].atualizar(self.screen)

            # Cria os botões para mudar o volume da música do menu.
            vol_menu_texto = self.fonte(45).render(vol, True, "Black")

            # Superfície para o botão.
            opcoes_vol_rect = vol_menu_texto.get_rect(center=(400, 550))

            # Adicionar o botão à tela de jogo.
            self.screen.blit(vol_menu_texto, opcoes_vol_rect)

            # Volume 0
            vol_menu_0.mudar_cor(opcoes_menu_pos)       # Mudar de cor para posição do mause
            vol_menu_0.atualizar(self.screen)           # Aplicar na tela o botão

            # Volume 1
            vol_menu_1.mudar_cor(opcoes_menu_pos)
            vol_menu_1.atualizar(self.screen)

            # Volume 2
            vol_menu_2.mudar_cor(opcoes_menu_pos)
            vol_menu_2.atualizar(self.screen)

            # Volume 3
            vol_menu_3.mudar_cor(opcoes_menu_pos)
            vol_menu_3.atualizar(self.screen)

            # Volume 4
            vol_menu_4.mudar_cor(opcoes_menu_pos)
            vol_menu_4.atualizar(self.screen)

            # Volume 5
            vol_menu_5.mudar_cor(opcoes_menu_pos)
            vol_menu_5.atualizar(self.screen)

            # Cria o botão de voltar.
            back = self.tradutor.translate("Back", dest=self.submenu.idioma).text
            opcoes_voltar = Botao(imagem = None, pos = (400, 700), texto_cont = back, 
                                 fonte = self.fonte(50), cor_base = "Black", cor_com_mause = "#568e81")

            # Aciona changecolor para alterar a cor quando o mouse está sobre o botão.
            opcoes_voltar.mudar_cor(opcoes_menu_pos)
            # Adiciona o texto e a imagem à tela.
            opcoes_voltar.atualizar(self.screen)

            # pygame.event.get() obtém os eventos que ocorrem.
            for evento in pygame.event.get():
                # Finaliza o programa se o botão X (canto superior direito) for clicado.
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Se o botão esquerdo do mouse for clicado sobre o botão "Voltar", é acionado a função "menu_principal" e voltamos ao menu.
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if opcoes_voltar.checar_clique(opcoes_menu_pos):
                        condicao = False
                        self.menu_principal()

                        # Checagem de clique para:
                    # Tradução menu opções para português.  
                    elif idioma[0].checar_clique(opcoes_menu_pos):
                        self.submenu.idioma = "pt"
                        idioma = self.atualizar_idiomas()
                        opcoes_textos = self.traduzir_lingua("opcoes_textos")
                        idioma[0].selecionado = True
                    
                    # Tradução menu opções para inglês.
                    elif idioma[1].checar_clique(opcoes_menu_pos):
                        self.submenu.idioma = "en"
                        idioma = self.atualizar_idiomas()
                        opcoes_textos = self.traduzir_lingua("opcoes_textos")
                        idioma[1].selecionado = True

                    # Tradução menu opções para francês.
                    elif idioma[2].checar_clique(opcoes_menu_pos):
                        self.submenu.idioma = "fr"
                        idioma = self.atualizar_idiomas()
                        opcoes_textos = self.traduzir_lingua("opcoes_textos")
                        idioma[2].selecionado = True
                    
                    # Tradução menu opções para latim.
                    elif idioma[3].checar_clique(opcoes_menu_pos):
                        self.submenu.idioma = "la"
                        idioma = self.atualizar_idiomas()
                        opcoes_textos = self.traduzir_lingua("opcoes_textos")
                        idioma[3].selecionado = True

                    # Tradução menu opções para javanes.
                    elif idioma[6].checar_clique(opcoes_menu_pos):
                        self.submenu.idioma = "jw"
                        idioma = self.atualizar_idiomas()
                        opcoes_textos = self.traduzir_lingua("opcoes_textos")
                        idioma[6].selecionado = True

                    # Tradução menu opções para esperanto.
                    elif idioma[5].checar_clique(opcoes_menu_pos):
                        self.submenu.idioma = "eo"
                        idioma = self.atualizar_idiomas()
                        opcoes_textos = self.traduzir_lingua("opcoes_textos")
                        idioma[5].selecionado = True

                    # Tradução menu opções para alemão.
                    elif idioma[4].checar_clique(opcoes_menu_pos):
                        self.submenu.idioma = "de"
                        idioma = self.atualizar_idiomas()
                        opcoes_textos = self.traduzir_lingua("opcoes_textos")
                        idioma[4].selecionado = True

                    # Tradução menu opções para espanhol.
                    elif idioma[7].checar_clique(opcoes_menu_pos):
                        self.submenu.idioma = "es"
                        idioma = self.atualizar_idiomas()
                        opcoes_textos = self.traduzir_lingua("opcoes_textos")
                        idioma[7].selecionado = True

                    # Volume 0.0
                    elif vol_menu_0.checar_clique(opcoes_menu_pos):
                        self.submenu.musica.set_volume(0.0)
                        vol_menu_0.selecionado = True
                        vol_menu_1.selecionado = False
                        vol_menu_2.selecionado = False
                        vol_menu_3.selecionado = False
                        vol_menu_4.selecionado = False
                        vol_menu_5.selecionado = False

                    # Volume 0.2
                    elif vol_menu_1.checar_clique(opcoes_menu_pos):
                        self.submenu.musica.set_volume(0.2)
                        vol_menu_0.selecionado = False
                        vol_menu_1.selecionado = True
                        vol_menu_2.selecionado = False
                        vol_menu_3.selecionado = False
                        vol_menu_4.selecionado = False
                        vol_menu_5.selecionado = False

                    # Volume 0.4
                    elif vol_menu_2.checar_clique(opcoes_menu_pos):
                        self.submenu.musica.set_volume(0.4)
                        vol_menu_0.selecionado = False
                        vol_menu_1.selecionado = False
                        vol_menu_2.selecionado = True
                        vol_menu_3.selecionado = False
                        vol_menu_4.selecionado = False
                        vol_menu_5.selecionado = False

                    # Volume 0.6
                    elif vol_menu_3.checar_clique(opcoes_menu_pos):
                        self.submenu.musica.set_volume(0.6)
                        vol_menu_0.selecionado = False
                        vol_menu_1.selecionado = False
                        vol_menu_2.selecionado = False
                        vol_menu_3.selecionado = True
                        vol_menu_4.selecionado = False
                        vol_menu_5.selecionado = False

                    # Volume 0.8
                    elif vol_menu_4.checar_clique(opcoes_menu_pos):
                        self.submenu.musica.set_volume(0.8)
                        vol_menu_0.selecionado = False
                        vol_menu_1.selecionado = False
                        vol_menu_2.selecionado = False
                        vol_menu_3.selecionado = False
                        vol_menu_4.selecionado = True
                        vol_menu_5.selecionado = False

                    # Volume 1.0
                    elif vol_menu_5.checar_clique(opcoes_menu_pos):
                        self.submenu.musica.set_volume(1.0)
                        vol_menu_0.selecionado = False
                        vol_menu_1.selecionado = False
                        vol_menu_2.selecionado = False
                        vol_menu_3.selecionado = False
                        vol_menu_4.selecionado = False
                        vol_menu_5.selecionado = True

            # Faz com que a superfície de exibição apareça no monitor do usuário.
            pygame.display.update()

    def creditos(self):
        """ Função reponsável pelo submenu "Créditos", ou seja, a interface de crédito para os criadores do jogo.

        Args:
            self: palavra-chave que acessa os atributos e métodos da classe Menu.
        """
        # Textos do menu Créditos preparados para tradução:
        creditos_textos = self.traduzir_lingua("creditos_textos")
        ct, t_2, t_3, t_4, t_5, t_6, t_7, volta = re.split("\.", creditos_textos)

        while True:
            # Cria a superfície da imagem de fundo.
            fundo_rect = pygame.Rect(0, 0, self.cs * self.cn, self.cs * self.cn)
            # Ajusta as dimensões da imagem de fundo.
            imagem_fundo = pygame.transform.scale(self.imagem_submenus, (self.cs * self.cn, self.cs * self.cn))
            # SCREEN.blit(nome_imagem, (x_pos, y_pos))
            self.screen.blit(imagem_fundo, fundo_rect)

            # Cria a superfície do quadrado cinza.
            fundo_rect2 = pygame.Rect(100, 200, 700, 650)   # (Xo, Yo, X, Y)
            # Ajusta as dimensões do retangulo_cinza.
            imagem_fundo2 = pygame.transform.scale(self.retang_fundo, (600, 450))
            # SCREEN.blit(nome_imagem, (x_pos, y_pos))
            self.screen.blit(imagem_fundo2, fundo_rect2)

            # Obtem a posição (x,y) do cursor do mouse.
            opcoes_menu_pos = pygame.mouse.get_pos()

            # Texto da tela de créditos.
            credito_titulo = self.fonte(80).render(ct, True, "#e48b39")
            # Superfície do texto.
            credito_rect = credito_titulo.get_rect(center=(400, 120))
            # Adicionar à tela de créditos.
            self.screen.blit(credito_titulo, credito_rect)

            # Título da tela de créditos.
            texto_1 = self.fonte(20).render("Metrô", True, "#e48b39")
            texto_rect = texto_1.get_rect(center = (285, 250))
            self.screen.blit(texto_1, texto_rect)

            # Texto da tela de créditos.
            texto_2 = self.fonte(20).render("             "+t_2, True, "#d7fcd4")
            texto_3 = self.fonte(23).render(t_3, True, "Black")
            texto_4 = self.fonte(23).render(t_4, True, "Black")
            texto_5 = self.fonte(23).render(t_5, True, "Black")
            texto_6 = self.fonte(23).render(t_6, True, "Black")
            texto_7 = self.fonte(20).render(t_7, True, "#d7fcd4")
            texto_8 = self.fonte(20).render("2022", True, "#d7fcd4")

            # Adiciona texto à tela de creditos.
            y_coord = 250
            for texto in [texto_2, texto_3, texto_4, texto_5, texto_6, texto_7, texto_8]:

                texto_rect = texto.get_rect(center = (400, y_coord))
                self.screen.blit(texto, texto_rect)
                y_coord += 60

            # Cria o botão de voltar.
            creditos_voltar = Botao(imagem = None, pos = (400, 700), texto_cont = volta, 
                                 fonte = self.fonte(50), cor_base = "Black", cor_com_mause = "#568e81")
                                 
            # Aciona changecolor para alterar a cor quando o mouse está sobre o botão.
            creditos_voltar.mudar_cor(opcoes_menu_pos)
            # Adiciona o texto e a imagem à tela.
            creditos_voltar.atualizar(self.screen)

            # pygame.event.get() obtém os eventos que ocorrem.
            for evento in pygame.event.get():
                # Finaliza o programa se o botão X (canto superior direito) for clicado.
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Se o botão esquerdo do mouse for clicado sobre o botão "Voltar", é acionado a função "menu_principal" e voltamos ao menu.
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if creditos_voltar.checar_clique(opcoes_menu_pos):
                        self.menu_principal()

            # Faz com que a superfície de exibição apareça no monitor do usuário.
            pygame.display.update()


    def menu_principal(self):
        """ Responsável por gerar o menu principal do jogo, acionando as funções "jogar", "opcoes", "creditos" e a classe "Botao" para 
        criar os botões.

        Args:
            self: palavra-chave que acessa os atributos e métodos da classe Menu.
        """
        # Texto dos botões do menu principal preparados para tradução.
        inicio_textos = self.traduzir_lingua("inicio_textos")
        j, o, c, s = re.split("\.", inicio_textos)

        # O loop ocorre enquanto não for clicado no botão "SAIR".
        while True:
            # Cria a superfície da imagem de fundo.
            fundo_rect = pygame.Rect(0, 0, self.cs * self.cn, self.cs * self.cn)
            # Ajusta as dimensões da imagem de fundo.
            imagem_fundo = pygame.transform.scale(self.imagem_menu_principal, (self.cs * self.cn, self.cs * self.cn))

            # SCREEN.blit(nome_imagem, (x_pos, y_pos))
            self.screen.blit(imagem_fundo, fundo_rect)
            
            # Obtem a posição do cursor do mouse.
            menu_mouse_pos = pygame.mouse.get_pos()

            # Título principal do menu.
            menu_text = self.fonte(100).render("Metrô", True, "#e48b39")
            # Cria um objeto rect para colocar o texto.
            menu_rect = menu_text.get_rect(center = (400, 120))

            # Adicionar na tela o título.
            self.screen.blit(menu_text, menu_rect)

            # Criar os botões do menu acionando a classe Botao:
            # Botão de jogar.
            botao_jogar = Botao(imagem = pygame.image.load("imagens/retang_fundo.png"), pos = (400, 300), 
                                texto_cont = j, fonte = self.fonte(75), cor_base = "#d7fcd4", cor_com_mause = "#5b9388")
            # Botão de opções.
            botao_opcoes = Botao(imagem = pygame.image.load("imagens/retang_fundo.png"), pos=(400, 430), 
                                texto_cont = o, fonte = self.fonte(75), cor_base = "#d7fcd4", cor_com_mause = "#5b9388")
            # Botão de créditos.
            botao_creditos = Botao(imagem = pygame.image.load("imagens/retang_fundo.png"), pos=(400, 560), 
                                texto_cont = c, fonte = self.fonte(75), cor_base = "#d7fcd4", cor_com_mause = "#5b9388")
            # Botão de sair.
            botao_sair = Botao(imagem = pygame.image.load("imagens/retang_fundo.png"), pos = (400, 690), 
                                texto_cont = s, fonte = self.fonte(75), cor_base = "#d7fcd4", cor_com_mause = "#5b9388")

            # Acionar as funções de atualização e mudança de cor para os botões criados.
            for botao in [botao_jogar, botao_opcoes, botao_creditos, botao_sair]:
                botao.mudar_cor(menu_mouse_pos)
                botao.atualizar(self.screen)
            
            # pygame.event.get() obtem os eventos que ocorrem.
            for evento in pygame.event.get():
                # Finaliza o programa se o botão X (canto superior direito) for clicado.
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Se o botão esquerdo do mouse for clicado sobre o botão
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    # Jogar, é acionado a função "jogar".
                    if botao_jogar.checar_clique(menu_mouse_pos):
                        self.jogar()
                    # Opções, é acionado a função "opções".
                    if botao_opcoes.checar_clique(menu_mouse_pos):
                        self.opcoes()
                    if botao_creditos.checar_clique(menu_mouse_pos):
                        self.creditos()
                    # Sair, o programa é finalizado.
                    if botao_sair.checar_clique(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()
            
            # Faz com que a superfície de exibição apareça no monitor do usuário.
            pygame.display.update()
    
    def atualizar_idiomas(self):
        """ Traduz a lista de idiomas que tem suporte no jogo para a nova língua selecionada pelo usuário.

        :return novo_idioma: lista dos idiomas traduzidos para a língua selecionada.

        Args:
            self: palavra-chave que acessa os atributos e métodos da classe Menu.
        """
        subidioma = self.submenu.idioma
        novo_idioma = []
        for i in range(8):
            novo_idioma.append(self.traduzir_lingua("idioma", self.idiomas[i], 270+30*i, subidioma))
        return novo_idioma
    
    def traduzir_lingua(self, texto, lingua=None, posicao=None, subidioma=None):
        """ Responsável traduzir o conteúdo dos botões, dos títulos e dos textos gerais de cada um dos menus.

        Args:
            self: palavra-chave que acessa os atributos e métodos da classe Menu.
            texto: se refere ao tipo de conteúdo a ser traduzido, por exemplo: idioma, inicio_textos e opcoes_textos.
            lingua: lingua para a qual os textos serão traduzidos.
            posicao: um número que representa a posição vertical do texto.
            subidioma: sigla do idioma para o qual o texto será traduzido.
        """
        if texto == "idioma":
            try:
                lingua = self.tradutor.translate(lingua, dest=subidioma).text
                idioma = Botao(imagem = pygame.transform.scale(self.fundo, (150, self.cs)), pos = (400, posicao), 
                                    texto_cont = lingua, fonte = self.fonte(25), cor_base = "#d7fcd4", cor_com_mause = "#5b9388")
                return idioma
            except TypeError:
                self.traduzir_lingua(lingua, posicao, subidioma)
            except httpcore._exceptions.ReadTimeout:
                self.traduzir_lingua(lingua, posicao, subidioma)
            except AttributeError:
                self.traduzir_lingua(lingua, posicao, subidioma)
        elif texto == "inicio_textos":
            try:
                return self.tradutor.translate("JOGAR. OPÇÕES. CRÉDITOS. SAIR", dest=self.submenu.idioma).text
            except TypeError or AttributeError or httpcore._exceptions.ReadTimeout:
                self.traduzir_lingua("inicio_textos")
        elif texto == "opcoes_textos":
            try:
                return self.tradutor.translate("Opções. Idioma do jogo. Voltar. Volume do menu", dest=self.submenu.idioma).text
            except TypeError or AttributeError or httpcore._exceptions.ReadTimeout:
                self.traduzir_lingua("opcoes_textos")
        elif texto == "creditos_textos":
            try:
                return self.tradutor.translate("Créditos. foi desenvolvido por. Ricael Daniel Vieira da Silva. Rodrigo Cavalcante Kalil. Rodrigo Dhery Silva Prieto. Thiago Franke Melchiors. Alunos do segundo semestre de Ciência de Dados da FGV EMAp. Voltar", dest=self.submenu.idioma).text
            except TypeError or AttributeError or httpcore._exceptions.ReadTimeout:
                self.traduzir_lingua("creditos_textos")
        elif texto == "jogar_textos":
            try:
                return self.tradutor.translate("Que bom te conhecer, maquinista. Escolha uma fase:. Fases. FASE 1: Inglaterra. FASE 2: Brasil. FASE 3: Estados Unidos. FASE 4: China. FASE 5: França. Voltar", dest=self.submenu.idioma).text
            except TypeError or AttributeError or httpcore._exceptions.ReadTimeout:
                self.traduzir_lingua("jogar_textos")


# Inicia o código.
# Se o código for rodado a partir do "main" será acionada a função "menu_principal()", que dá início ao jogo.
if __name__ == "__main__":
    menu = Menu(screen, estacao_com_metro, estacao_sem_metro, retang_fundo, cn, cs)
    menu.menu_principal()