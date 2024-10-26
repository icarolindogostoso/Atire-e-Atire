import pygame
import sys

pygame.init()

def atirando (contador_de_tiro,barulho_colisao,direcao,listaprojeteis,jogadorrect):
    if contador_de_tiro == 0:
        barulho_colisao.play()
        contador_de_tiro = 3
    if direcao == 'esquerda':
        listaprojeteis.append((jogadorrect.x,jogadorrect.y + 18, -15, jogadorrect.x))
    if direcao == 'direita':
        listaprojeteis.append((jogadorrect.x + 25, jogadorrect.y + 18, 15, jogadorrect.x))
    contador_de_tiro -= 1
    return contador_de_tiro, listaprojeteis

def projetil_andando (listaprojeteis):
    novos_projeteis = [] # editar lista para modificar a posicao do projetil, fazer com que o projetil ande
    for posx, posy, velx, x_ini in listaprojeteis:
        nova_posx = posx + velx
        if x_ini - 200 <= nova_posx <= x_ini + 220:
            novos_projeteis.append((nova_posx, posy, velx, x_ini))
    return novos_projeteis

def projetil_sumindo (i,listaprojeteis):
    projeteis_temp = []
    for posx, posy, velx, x_ini in listaprojeteis:
        retangulo_projetil = pygame.Rect(posx, posy, 25, 6)
        if not retangulo_projetil.colliderect(i):
            projeteis_temp.append((posx, posy, velx, x_ini))
    return projeteis_temp

def pulando (jogadorrect,velocidade_pulo,gravidade,colisoes,contador):
    jogadorrect.y += velocidade_pulo
    if velocidade_pulo < 0: # movimentacao do personagem 2 para cima
        velocidade_pulo += gravidade
        for i in colisoes: # colisao do personagem 2 com o teto
            if jogadorrect.colliderect(i):
                jogadorrect.top = i.bottom
                velocidade_pulo = 0
    if velocidade_pulo >= 0: # movimentacao do personagem 2 para baixo
        for i in colisoes: # colisao do personagem 2 com o chao
            if jogadorrect.colliderect(i):
                jogadorrect.bottom = i.top
                velocidade_pulo = 0
                contador = 0
        else:
            velocidade_pulo += gravidade
    if jogadorrect.bottom >= 480: # fazer o personagem ao sair da tela para baixo, ir para cima
        jogadorrect.bottom = 5
        velocidade_pulo = 0
        contador = 10
    if jogadorrect.bottom <= 0: # fazer o personagem ao sair da tela para cima, ir para baixo
        jogadorrect.bottom = 475
    return jogadorrect, velocidade_pulo, contador

def personagem_tomando_dano (jogadorrect,retangulo_projetil,direcao,vidajogador,atingiu,jogador):
    if jogadorrect.colliderect(retangulo_projetil) and direcao == 'direita':
        jogador = pygame.image.load("heavytomandodano.bmp")
        jogador.set_colorkey((255,0,255))
        vidajogador -= 1
        atingiu = True
    if jogadorrect.colliderect(retangulo_projetil) and direcao == 'esquerda':
        jogador = pygame.image.load("heavytomandodanoinvertido.bmp")
        jogador.set_colorkey((255,0,255))
        vidajogador -= 1
        atingiu = True
    return vidajogador,atingiu,jogador

def colisao_tiro (posx,posy,atingiu,vidajogador,jogador,jogadorrect,direcao,contadorimortalidade,barulho_dor,jogador_jogado):
    retangulo_projetil = pygame.Rect(posx,posy,25,8)
    if atingiu == False:
        vidajogador,atingiu,jogador = personagem_tomando_dano(jogadorrect,retangulo_projetil,direcao,vidajogador,atingiu,jogador)
        if not jogadorrect.colliderect(retangulo_projetil) and direcao == 'direita':
            jogador = escolher_lado(direcao,jogador_jogado,jogador)
        if not jogadorrect.colliderect(retangulo_projetil) and direcao == 'esquerda':
            jogador = escolher_lado(direcao,jogador_jogado,jogador)
    if atingiu == True:
        contadorimortalidade,atingiu = frame_imortalidade(contadorimortalidade,barulho_dor,atingiu)
    return vidajogador,atingiu,jogador,contadorimortalidade

def frame_imortalidade (contadorimortalidade,barulho_dor,atingiu):
    if contadorimortalidade == 20:
        barulho_dor.play()
        atingiu = False
        contadorimortalidade = 0
    contadorimortalidade += 1
    return contadorimortalidade,atingiu

def coracoes (posicoes_x,coracao,y):
    coracoes_rects = []
    estados_coracoes = []
    for x in posicoes_x:
        coracao_rect = coracao.get_rect()
        coracao_rect.y = y
        coracao_rect.x = x
        coracoes_rects.append(coracao_rect)
        estados_coracoes.append(False)
    return coracoes_rects,estados_coracoes

def apagar_coracao (vidajogador,estados_coracoes,barulho_morte,tela,coracao,coracoes_rects):
    if vidajogador >= -20:
        if vidajogador == -20:
            estados_coracoes[0] = True
        if estados_coracoes[0] == True:
            barulho_morte.play()
            estados_coracoes[0] = False
            vidajogador = -21
        tela.blit(coracao,coracoes_rects[0])
    if vidajogador >= -10:
        if vidajogador == -10:
            estados_coracoes[1] = True
        if estados_coracoes[1] == True:
            barulho_morte.play()
            estados_coracoes[1] = False
            vidajogador = -11
        tela.blit(coracao,coracoes_rects[1])
    if vidajogador >= 0:
        if vidajogador == 0:
            estados_coracoes[2] = True
        if estados_coracoes[2] == True:
            barulho_morte.play()
            estados_coracoes[2] = False
            vidajogador = -1
        tela.blit(coracao,coracoes_rects[2])
    return vidajogador,estados_coracoes

def temporizador (tempo_inicial,reiniciar_cronometro):
    if reiniciar_cronometro == True:
        tempo_inicial = pygame.time.get_ticks()
        tempo_decorrido_ms = 0
        reiniciar_cronometro = False
    tempo_atual = pygame.time.get_ticks()
    tempo_decorrido_ms = tempo_atual - tempo_inicial
    minutos_passados = (tempo_decorrido_ms // 1000) // 60
    segundos_passados = (tempo_decorrido_ms // 1000) % 60
    return minutos_passados,segundos_passados,reiniciar_cronometro, tempo_inicial

def escolher_lado (direcao,jogador_jogado,jogador):
    if direcao == 'esquerda':
        if jogador_jogado == 'vermelho':
            jogador = pygame.image.load("heavyvermelho1invertido.bmp")
            jogador.set_colorkey((255,0,255))
        if jogador_jogado == 'azul':
            jogador = pygame.image.load("heavyazul1invertido.bmp")
            jogador.set_colorkey((255,0,255))
    if direcao == 'direita':
        if jogador_jogado == 'vermelho':
            jogador = pygame.image.load("heavyvermelho1.bmp")
            jogador.set_colorkey((255,0,255))
        if jogador_jogado == 'azul':
            jogador = pygame.image.load("heavyazul1.bmp")
            jogador.set_colorkey((255,0,255))
    return jogador

def escolha_imagem_fundo (estado):
    if estado == 'jogador2vencedor':
        imagem_fundo = pygame.image.load('teladevitoriaazul.png')
    if estado == 'jogador1vencedor':
        imagem_fundo = pygame.image.load('teladevitoriavermelho.png')
    return imagem_fundo

def vencedor (coracao,estado,tela,minutos_passados,segundos_passados,text_color,vidajogador,barulho_morte,jogador1rect,jogador2rect,vidajogador1,vidajogador2,listaprojeteis1,listaprojeteis2,tempo_atual,reiniciar_cronometro):
    posicoes_x = [550, 587, 624]
    coracoes_rects,estados_coracoes = coracoes(posicoes_x,coracao,90)
    imagem_fundo = escolha_imagem_fundo(estado)
    tela.blit(imagem_fundo,(0,0))
    texto = font.render(f"{minutos_passados:02}:{segundos_passados:02}", True, text_color)
    tela.blit(texto, (50,110))
    text_menu = font.render("Pressione [R] para reiniciar", True, text_color)
    text_menu_rect = text_menu.get_rect()
    text_menu_rect.center = (tela.get_width() // 2, 360)
    tela.blit(text_menu, text_menu_rect)
    vidajogador,estados_coracoes = apagar_coracao(vidajogador,estados_coracoes,barulho_morte,tela,coracao,coracoes_rects)
    if keys[pygame.K_r]:
        estado = 'jogando'
        vidajogador1 = 10
        vidajogador2 = 10
        jogador1rect.y = 430
        jogador1rect.x = 75
        jogador2rect.y = 430
        jogador2rect.x = 740
        listaprojeteis1 = []
        listaprojeteis2 = []
        minutos_passados = 0
        segundos_passados = 0
        tempo_atual = 0
        reiniciar_cronometro = True
    return estado,vidajogador1,vidajogador2,jogador1rect,jogador2rect,listaprojeteis1,listaprojeteis2,minutos_passados,segundos_passados, tempo_atual, reiniciar_cronometro

largura,altura = 840,480
tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption("Atire e ATIRE!")

tempo_inicial = pygame.time.get_ticks()
tempo_atual = 0
minutos_passados = 0
segundos_passados = 0
reiniciar_cronometro = False
clock = pygame.time.Clock()

imagem_fundo = pygame.image.load("seilamacho.png")
gravidade = 0.5
velocidade = 8

barulho_colisao = pygame.mixer.Sound("tiro.wav")
barulho_colisao.set_volume(0.4)

barulho_dor = pygame.mixer.Sound("audiodor.wav")
barulho_dor.set_volume(0.4)

barulho_morte = pygame.mixer.Sound("audiomorte.wav")
barulho_morte.set_volume(0.7)

pygame.mixer.music.set_volume(0.3)
musica_de_mundo = pygame.mixer.music.load('musicatf2.mp3')
pygame.mixer.music.play(-1)

coracao = pygame.image.load("coracao.bmp")
coracao.set_colorkey((255,0,255))

posicoes_x_1 = [70, 140, 210]
coracoes_rects_1,estados_coracoes_1 = coracoes(posicoes_x_1,coracao,20)

posicoes_x_2 = [740, 670, 600]
coracoes_rects_2,estados_coracoes_2 = coracoes(posicoes_x_2,coracao,20)

jogador1 = pygame.image.load("heavyvermelho1.bmp")
jogador1.set_colorkey((255,0,255))
jogador1rect = jogador1.get_rect()
jogador1rect.y = 430
jogador1rect.x = 75
jogador_jogado_1 = 'vermelho'
velocidade_pulo1 = 0
contador1 = 0
direcao1 = 'direita'
listaprojeteis1 = []
atingiu1 = False
contadorimortalidade1 = 0
vidajogador1 = 10
contador_de_tiro1 = 0

jogador2 = pygame.image.load("heavyazul1invertido.bmp")
jogador2.set_colorkey((255,0,255))
jogador2rect = jogador2.get_rect()
jogador2rect.y = 430
jogador2rect.x = 740
jogador_jogado_2 = 'azul'
velocidade_pulo2 = 0
contador2 = 0
direcao2 = 'esquerda'
listaprojeteis2 = []
atingiu2 = False
contadorimortalidade2 = 0
vidajogador2 = 10
contador_de_tiro2 = 0

muro1 = pygame.Rect(0,462,187,18)
muro2 = pygame.Rect(0,0,187,17)
muro3 = pygame.Rect(0,17,50,445)
plataforma1 = pygame.Rect(0,244,104,10)
muro4 = pygame.Rect(267,462,298,18)
muro5 = pygame.Rect(648,462,190,18)
muro6 = pygame.Rect(648,0,190,17)
muro7 = pygame.Rect(782,17,56,445)
plataforma2 = pygame.Rect(733,244,104,10)
muro8 = pygame.Rect(267,0,298,18)
plataforma3 = pygame.Rect(147,360,164,11)
plataforma4 = pygame.Rect(526,360,164,11)
plataforma5 = pygame.Rect(281,244,274,11)
plataforma6 = pygame.Rect(147,113,164,11)
plataforma7 = pygame.Rect(525,113,164,11)
caixa1 = pygame.Rect(422,424,35,38)
caixa2 = pygame.Rect (188,324,35,38)
caixa3 = pygame.Rect(365,208,35,38)

colisoes = [muro1,muro2,muro3,muro4,muro5,muro6,muro7,muro8,plataforma1,plataforma2,plataforma3,plataforma4,plataforma5,plataforma6,plataforma7,caixa1,caixa2,caixa3]

estado = 'menu'
font = pygame.font.Font(None, 64)
text_color = (255, 255, 255)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if estado == 'jogador1vencedor':
        estado,vidajogador1,vidajogador2,jogador1rect,jogador2rect,listaprojeteis1,listaprojeteis2,minutos_passados,segundos_passados,tempo_atual,reiniciar_cronometro = vencedor(coracao,estado,tela,minutos_passados,segundos_passados,text_color,vidajogador1,barulho_morte,jogador1rect,jogador2rect,vidajogador1,vidajogador2,listaprojeteis1,listaprojeteis2,tempo_atual,reiniciar_cronometro)

    if estado == 'jogador2vencedor':
        estado,vidajogador1,vidajogador2,jogador1rect,jogador2rect,listaprojeteis1,listaprojeteis2,minutos_passados,segundos_passados,tempo_atual,reiniciar_cronometro = vencedor(coracao,estado,tela,minutos_passados,segundos_passados,text_color,vidajogador2,barulho_morte,jogador1rect,jogador2rect,vidajogador1,vidajogador2,listaprojeteis1,listaprojeteis2,tempo_atual,reiniciar_cronometro)

    if estado == 'menu': # menu inicial do jogo
        imagem_fundo = pygame.image.load("atireeatireiniciodramatico.png")
        tela.blit(imagem_fundo, (0,0))
        text_menu = font.render("Pressione [Q] para jogar", True, text_color)
        text_menu_rect = text_menu.get_rect()
        text_menu_rect.center = (tela.get_width() // 2, 360)
        tela.blit(text_menu, text_menu_rect)
        if keys[pygame.K_q]:
            estado = "jogando"

    if estado == 'jogando': # jogo iniciado
        imagem_fundo = pygame.image.load("seilamacho.png")
        if keys[pygame.K_a]: # movimentacao jogador 1 para esquerda
            direcao1 = 'esquerda'
            jogador1rect.x -= velocidade
            jogador1 = escolher_lado(direcao1,jogador_jogado_1,jogador1)
            for i in colisoes: # colisao do jogador 1 com as paredes da esquerda
                if jogador1rect.colliderect(i):
                    jogador1rect.left = i.right
        if keys[pygame.K_d]:
            direcao1 = 'direita' # movimentacao jogador 1 para direita
            jogador1rect.x += velocidade
            jogador1 = escolher_lado(direcao1,jogador_jogado_1,jogador1)
            for i in colisoes:
                if jogador1rect.colliderect(i): # colisao do jogador 1 com as paredes da direita
                    jogador1rect.right = i.left
        if contador1 < 8:
            if keys[pygame.K_w]: # pulo do jogador 1
                velocidade_pulo1 = -10
                contador1 += 1

        jogador1rect,velocidade_pulo1,contador1 = pulando(jogador1rect,velocidade_pulo1,gravidade,colisoes,contador1)

        if keys[pygame.K_v] and len(listaprojeteis1) < 5: # apertar para o jogador 1 atirar
            contador_de_tiro1,listaprojeteis1 = atirando(contador_de_tiro1,barulho_colisao,direcao1,listaprojeteis1,jogador1rect)

        listaprojeteis1 = projetil_andando(listaprojeteis1)
        
        if not keys[pygame.K_v]: # fazer o personagem 2  ficar na cor original quando não ter colisão com projeteis do personagem 1
            if direcao2 == 'direita':
                jogador2 = escolher_lado(direcao2,jogador_jogado_2,jogador2)
            if direcao2 == 'esquerda':
                jogador2 = escolher_lado(direcao2,jogador_jogado_2,jogador2)
        
        for posx,posy,velx,x_ini in listaprojeteis1: # colisao do personagem 2 com os projeteis do personagem 1
            vidajogador2,atingiu2,jogador2,contadorimortalidade2 = colisao_tiro(posx,posy,atingiu2,vidajogador2,jogador2,jogador2rect,direcao2,contadorimortalidade2,barulho_dor,jogador_jogado_2)

        for colisao in colisoes: # fazer projetil do personagem 1 sumir quando bater em uma parede ou chegar no limite da sua distancia
            listaprojeteis1 = projetil_sumindo(colisao,listaprojeteis1)

        if keys[pygame.K_LEFT]: # movimentacao do personagem 2 para esquerda
            direcao2 = 'esquerda'
            jogador2rect.x -= velocidade
            jogador2 = escolher_lado(direcao2,jogador_jogado_2,jogador2)
            for i in colisoes: # colisao personagem 2 com as paredes da esquerda
                if jogador2rect.colliderect(i):
                    jogador2rect.left = i.right
        if keys[pygame.K_RIGHT]: # movimentacao personagem 2 para a direita
            direcao2 = 'direita'
            jogador2rect.x += velocidade
            jogador2 = escolher_lado(direcao2,jogador_jogado_2,jogador2)
            for i in colisoes: # colisao personagem 2 com as paredes da direita
                if jogador2rect.colliderect(i):
                    jogador2rect.right = i.left
        if contador2 < 8: # pulo do personagem 2
            if keys[pygame.K_UP]:
                velocidade_pulo2 = -10
                contador2 += 1

        jogador2rect,velocidade_pulo2,contador2 = pulando(jogador2rect,velocidade_pulo2,gravidade,colisoes,contador2)
        
        if keys[pygame.K_p] and len(listaprojeteis2) < 5: # personagem 2 atirando
            contador_de_tiro2,listaprojeteis2 = atirando(contador_de_tiro2,barulho_colisao,direcao2,listaprojeteis2,jogador2rect)
        listaprojeteis2 = projetil_andando(listaprojeteis2)

        for colisao in colisoes:
            listaprojeteis2 = projetil_sumindo(colisao,listaprojeteis2)

        if not keys[pygame.K_p]:
            if direcao1 == 'direita':
                jogador1 = escolher_lado(direcao1,jogador_jogado_1,jogador1)
            if direcao1 == 'esquerda':
                jogador1 = escolher_lado(direcao1,jogador_jogado_1,jogador1)
        
        for posx,posy,velx,x_ini in listaprojeteis2:
            vidajogador1,atingiu1,jogador1,contadorimortalidade1 = colisao_tiro(posx,posy,atingiu1,vidajogador1,jogador1,jogador1rect,direcao1,contadorimortalidade1,barulho_dor,jogador_jogado_1)
        
        minutos_passados, segundos_passados,reiniciar_cronometro, tempo_inicial = temporizador(tempo_inicial,reiniciar_cronometro)
        texto = font.render(f"{minutos_passados:02}:{segundos_passados:02}", True, text_color)

        tela.blit(imagem_fundo, (0,0))
        tela.blit(jogador1, jogador1rect)
        tela.blit(jogador2, jogador2rect)
        tela.blit(texto, (840 // 2 - texto.get_width() // 2, 5))
        if vidajogador1 <= -21:
            estado = 'jogador2vencedor'
        vidajogador1,estados_coracoes_1 = apagar_coracao(vidajogador1,estados_coracoes_1,barulho_morte,tela,coracao,coracoes_rects_1)
        
        if vidajogador2 <= -21:
            estado = 'jogador1vencedor'
        vidajogador2,estados_coracoes_2 = apagar_coracao(vidajogador2,estados_coracoes_2,barulho_morte,tela,coracao,coracoes_rects_2)
        
        for posx, posy, _, _ in listaprojeteis1:
            pygame.draw.rect(tela, (255,255,0), (posx, posy, 25, 6))
        for posx, posy, _, _ in listaprojeteis2:
            pygame.draw.rect(tela,(255,255,0), (posx, posy, 25, 6))
    pygame.display.flip()
    clock.tick(60)