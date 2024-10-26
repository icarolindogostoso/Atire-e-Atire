import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Cronômetro")

# Configurações do cronômetro
FPS = 60
clock = pygame.time.Clock()
tempo_inicio = pygame.time.get_ticks()  # Marca o tempo inicial
tempo_maximo = 10000  # Tempo máximo em milissegundos (10 segundos)

# Fonte para desenhar o texto
fonte = pygame.font.Font(None, 74)

def desenhar_cronometro(tela, segundos):
    texto = fonte.render(f"Tempo: {segundos:.2f}", True, (255, 255, 255))
    tela.blit(texto, (250, 250))

# Loop principal do jogo
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Calcula o tempo decorrido
    tempo_atual = pygame.time.get_ticks()
    tempo_decorrido = tempo_atual - tempo_inicio

    # Calcula o tempo restante, reinicia se necessário
    if tempo_decorrido > tempo_maximo:
        tempo_inicio = pygame.time.get_ticks()  # Reinicia o cronômetro
        tempo_decorrido = 0

    # Converte o tempo decorrido para segundos
    segundos = tempo_decorrido / 1000.0

    # Preenche a tela com uma cor de fundo
    tela.fill((0, 0, 0))

    # Desenha o cronômetro na tela
    desenhar_cronometro(tela, segundos)

    # Atualiza a tela
    pygame.display.flip()

    # Controla a taxa de quadros
    clock.tick(FPS)