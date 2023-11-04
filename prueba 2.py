import pygame
import random

ANCHO_VENTANA = 800
ALTO_VENTANA = 720

pygame.init()
matriz = [[0] * 36 for _ in range(40)]

class Bola:
    def __init__(self, ventana, x, y, radio, velocidad):
        self.ventana = ventana
        self.x = ANCHO_VENTANA // 2
        self.y = ALTO_VENTANA // 2
        self.radio = radio
        self.velocidad = velocidad


    def mover(self, teclas, objetos_negros):
        x_siguiente = self.x
        y_siguiente = self.y

        if teclas[pygame.K_UP]:
            y_siguiente -= self.velocidad
        if teclas[pygame.K_DOWN]:
            y_siguiente += self.velocidad
        if teclas[pygame.K_LEFT]:
            x_siguiente -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            x_siguiente += self.velocidad

        for objeto in objetos_negros:
            if self.colisiona_con_objeto(x_siguiente, y_siguiente, objeto):
                return

        self.x = x_siguiente
        self.y = y_siguiente


    def colisiona_con_objeto(self, x, y, objeto):
        return (
            x + self.radio > objeto[0] and
            x - self.radio < objeto[0] + objeto[2] and
            y + self.radio > objeto[1] and
            y - self.radio < objeto[1] + objeto[3])

    def dibujar(self):
        pygame.draw.circle(self.ventana, (255, 255, 0), (int(self.x), int(self.y)), self.radio)

class Fantasma:
    def __init__(self, x, y, velocidad, ANCHO_VENTANA, ALTO_VENTANA, color):
        self.x, self.y = x, y
        self.velocidad = velocidad
        self.direccion_x, self.direccion_y = random.choice([-1, 1]), random.choice([-1, 1])
        self.ANCHO_VENTANA, self.ALTO_VENTANA = ANCHO_VENTANA, ALTO_VENTANA
        self.color = color
        

    def mover_continuamente(self):
        self.x += self.direccion_x * self.velocidad
        self.y += self.direccion_y * self.velocidad

        if self.x < 0 or self.x > self.ANCHO_VENTANA:
            self.direccion_x = -self.direccion_x
        if self.y < 0 or self.y > self.ALTO_VENTANA:
            self.direccion_y = -self.direccion_y

fantasmas = [
    Fantasma(x=100, y=100, velocidad=0.1, ANCHO_VENTANA=ANCHO_VENTANA, ALTO_VENTANA=ALTO_VENTANA, color=(255, 20, 147)),  # Rosa
    Fantasma(x=200, y=200, velocidad=0.1, ANCHO_VENTANA=ANCHO_VENTANA, ALTO_VENTANA=ALTO_VENTANA, color=(255, 69, 0)),  # Naranja
    Fantasma(x=300, y=300, velocidad=0.1, ANCHO_VENTANA=ANCHO_VENTANA, ALTO_VENTANA=ALTO_VENTANA, color=(0, 255, 255)),  # Cian
    Fantasma(x=400, y=400, velocidad=0.2, ANCHO_VENTANA=ANCHO_VENTANA, ALTO_VENTANA=ALTO_VENTANA, color=(255, 0, 0))]  # Rojo

class Juego:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.ventana = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Mueve la bola")
        self.imprimir_una_vez = True  # Variable para imprimir una sola vez
        self.tecla_m_presionada = False  # Variable para rastrear el estado de la tecla M

    def imprimir_matriz(self):
        # Aquí debes definir la lógica para imprimir la matriz
        # Por ejemplo, puedes iterar sobre la matriz y mostrar sus valores en la consola
        if self.imprimir_una_vez:
            for fila in range(40):
                for columna in range(36):
                    print(matriz[fila][columna], end=" ")
                print()
            self.imprimir_una_vez = False  # Restablecer la variable


    def ejecutar(self):
        objetos_negros = [(0, 0, 800, 50), (0, 670, 800, 50), (0, 0, 50, 720), (750, 0, 50, 720)]

        bola = Bola(self.ventana, 20, self.alto - 20, 20, 0.2)

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            teclas = pygame.key.get_pressed()

            if teclas[pygame.K_m] and not self.tecla_m_presionada:
                self.imprimir_matriz()
                print(f"Posición de la bola: ({int(bola.x/20)}, {int(bola.y/20)})")
                self.tecla_m_presionada = True
            elif not teclas[pygame.K_m]:
                self.tecla_m_presionada = False

            bola.mover(teclas, objetos_negros)

            self.ventana.fill((0, 0, 128))

            # Dibujar objetos negros
            for objeto in objetos_negros:
                pygame.draw.rect(self.ventana, (0, 0, 0), objeto)

            bola.dibujar()

            for fantasma in fantasmas:
                fantasma.mover_continuamente()

            for fantasma in fantasmas:
                pygame.draw.polygon(self.ventana, fantasma.color, [(fantasma.x, fantasma.y - 20), (fantasma.x - 20, fantasma.y + 20), (fantasma.x + 20, fantasma.y + 20)])

            pygame.display.update()

if __name__ == "__main__":
    juego = Juego(800, 720)
    juego.ejecutar()