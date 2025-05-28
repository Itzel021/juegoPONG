import pygame
import time
import sys
import random 

# Inicializa pygame
pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (154, 3, 30)
PINK = (181, 23, 158)
YELLOW = (255, 213, 0)
ORANGE = (255, 103, 0)
SKYBLUE = (0, 245, 212)
GREEN = (170, 204, 0)
BLUE = (0, 48, 73)

# Jugador y computadora
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 25
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
POINTS_TO_WIN = 10

# Cargar música y efectos de sonido
pygame.mixer.music.load('fondo1.mp3')
collision_sound = pygame.mixer.Sound('collision.wav')
win_sound = pygame.mixer.Sound('win.ogg')
lose_sound = pygame.mixer.Sound('lose.ogg')

# Clases
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, up=True, speed=PADDLE_SPEED):
        if up:
            self.rect.y -= speed  # Usar el parámetro de velocidad
        else:
            self.rect.y += speed  # Usar el parámetro de velocidad

        # Limitar el movimiento para no salir de la pantalla
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Rebote en los bordes superior e inferior
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

        # Rebote en las paletas
        if self.rect.colliderect(player.rect) or self.rect.colliderect(opponent.rect):
            self.speed_x *= -1
        # Variación en el rebote
            self.speed_y += random.uniform(-2, 2)  # Añadir un rebote menos predecible
            collision_sound.play()

    def draw(self):
        pygame.draw.ellipse(screen, YELLOW, self.rect)

# Función para mostrar texto
def draw_text(text, font, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))

# Pantalla de inicio
def show_menu():
    font = pygame.font.Font(None, 50)
    options = ['Jugador 1 vs CPU', 'Jugador 1 vs Jugador 2']
    selected_option = 0

    # Cargar la imagen de fondo del menú
    menu_background = pygame.image.load('fondoMenu.jpg')
    menu_background = pygame.transform.scale(menu_background, (300, 250))
    menu_background_rect = menu_background.get_rect()
    menu_background_rect.center = (SCREEN_WIDTH // 2, 150) 

    while True:
        screen.fill(BLUE)  # Asegúrate de limpiar la pantalla antes de dibujar
        # Dibujar la imagen de fondo
        screen.blit(menu_background, menu_background_rect.topleft)

        for i, option in enumerate(options):
            color = YELLOW if i == selected_option else WHITE
            draw_text(option, font, color, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + i * 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                if event.key == pygame.K_RETURN:
                    return 'player_vs_computer' if selected_option == 0 else 'player_vs_player'


# Función principal del juego
def pong_game(mode):
    pygame.mixer.music.play(-1)  # Reproduce la música de fondo en bucle
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)
    fontMessage = pygame.font.Font(None, 80)

    player_score = 0
    opponent_score = 0
    start_time = time.time()

    global player, opponent, ball
    player = Paddle(SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2 - 50)
    opponent = Paddle(10, SCREEN_HEIGHT // 2 - 50)
    ball = Ball(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10)

    # Establecer los nombres dependiendo del modo de juego
    if mode == 'player_vs_computer':
        player_name = "Jugador 1"
        opponent_name = "CPU"
    else:
        player_name = "Jugador 1"
        opponent_name = "Jugador 2"

    game_running = True
    while game_running:
        screen.fill(WHITE)
        # Calcular tiempo transcurrido en minutos y segundos
        elapsed_time = int(time.time() - start_time)
        minutes, seconds = divmod(elapsed_time, 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move(up=True)
        if keys[pygame.K_DOWN]:
            player.move(up=False)

        # Movimiento del oponente (computadora)
        if mode == 'player_vs_computer':
            if random.random() > 0.1:  
                if opponent.rect.centery < ball.rect.centery:
                    opponent.move(up=False, speed=7)
                if opponent.rect.centery > ball.rect.centery:
                    opponent.move(up=True, speed=7)
            else:
                if opponent.rect.centery < ball.rect.centery:
                    opponent.move(up=True, speed=2)  
                if opponent.rect.centery > ball.rect.centery:
                    opponent.move(up=False, speed=2)

        else:  # Jugador 2
            if keys[pygame.K_w]:
                opponent.move(up=True)
            if keys[pygame.K_s]:
                opponent.move(up=False)

        # Mover la pelota
        ball.move()

        # Puntos
        if ball.rect.left <= 0:
            player_score += 1
            ball.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball.speed_x *= -1
        if ball.rect.right >= SCREEN_WIDTH:
            opponent_score += 1
            ball.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball.speed_x *= -1

        # Dibujar objetos
        player.draw()
        opponent.draw()
        ball.draw()

        # Mostrar puntajes y tiempo formateado (minutos:segundos)
        draw_text(f'{player_name}: {player_score}', font, BLACK, SCREEN_WIDTH // 2 + 50, 20)
        draw_text(f'{opponent_name}: {opponent_score}', font, BLACK, SCREEN_WIDTH // 2 - 200, 20)
        draw_text(f'Tiempo: {minutes:02}:{seconds:02}', font, GREEN, SCREEN_WIDTH // 2 - font.size(f'Tiempo: {minutes:02}:{seconds:02}')[0] // 2, 60)

        # Verificar si alguien ganó
        if player_score == POINTS_TO_WIN:
            pygame.mixer.music.stop()
            win_sound.play()
            draw_text(f"¡{player_name} gana!", fontMessage, GREEN, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 50)
            pygame.display.flip()
            pygame.time.wait(3000)
            game_running = False  # Detener el ciclo del juego
        elif opponent_score == POINTS_TO_WIN:
            pygame.mixer.music.stop()
            lose_sound.play()
            draw_text(f"¡Perdiste!", fontMessage, RED, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 50)
            pygame.display.flip()
            pygame.time.wait(3000)
            game_running = False  # Detener el ciclo del juego

        pygame.display.flip()
        clock.tick(60)

# Main loop
def main():
    while True:
        mode = show_menu()
        pong_game(mode)

if __name__ == "__main__":
    main()
