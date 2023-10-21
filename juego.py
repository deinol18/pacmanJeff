import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Colores
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pac-Man Game")

# Clase Juego
class Juego:
    def __init__(self):
        self.pacman = Pacman(400, 300)
        self.fantasmas = [Fantasma(100, 100, ROJO), Fantasma(700, 100, AZUL)]
        self.puntuacion = 0

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def actualizar(self):
        self.pacman.actualizar()
        for fantasma in self.fantasmas:
            fantasma.actualizar()
            if self.pacman.colision(fantasma):
                self.puntuacion -= 10
                fantasma.reiniciar()

    def dibujar(self):
        pantalla.fill(NEGRO)
        self.pacman.dibujar()
        for fantasma in self.fantasmas:
            fantasma.dibujar()
        pygame.display.flip()

    def ejecutar(self):
        reloj = pygame.time.Clock()

        while True:
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            reloj.tick(30)

# Clase Pacman
class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radio = 20
        self.angulo_boca = 0
        self.velocidad = 5

    def actualizar(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidad
        if teclas[pygame.K_UP]:
            self.y -= self.velocidad
        if teclas[pygame.K_DOWN]:
            self.y += self.velocidad
        self.angulo_boca += 5
        if self.angulo_boca > 45:
            self.angulo_boca = 0

    def dibujar(self):
        pygame.draw.circle(pantalla, AMARILLO, (self.x, self.y), self.radio)
        boca_rect = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)
        pygame.draw.arc(pantalla, NEGRO, boca_rect, pygame.math.radians(0), pygame.math.radians(self.angulo_boca), 0)

    def colision(self, fantasma):
        distancia = pygame.math.sqrt((fantasma.x - self.x) ** 2 + (fantasma.y - self.y) ** 2)
        return distancia < self.radio + fantasma.radio

# Clase Fantasma
class Fantasma:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radio = 20
        self.color = color
        self.velocidad = random.randint(1, 3)

    def actualizar(self):
        self.x += random.randint(-self.velocidad, self.velocidad)
        self.y += random.randint(-self.velocidad, self.velocidad)

        # Asegurarse de que el fantasma no se salga de la pantalla
        self.x = max(self.radio, min(ANCHO - self.radio, self.x))
        self.y = max(self.radio, min(ALTO - self.radio, self.y))

    def dibujar(self):
        pygame.draw.circle(pantalla, self.color, (self.x, self.y), self.radio)

    def reiniciar(self):
        self.x = random.randint(50, ANCHO - 50)
        self.y = random.randint(50, ALTO - 50)

if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()