import pygame

ANCHO_VENTANA = 800
ALTO_VENTANA = 720

pygame.init()

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

        # Verificar colisión con los bordes de la ventana
        if x_siguiente - self.radio < 0:
            x_siguiente = self.radio
        if x_siguiente + self.radio > ANCHO_VENTANA:
            x_siguiente = ANCHO_VENTANA - self.radio
        if y_siguiente - self.radio < 0:
            y_siguiente = self.radio
        if y_siguiente + self.radio > ALTO_VENTANA:
            y_siguiente = ALTO_VENTANA - self.radio

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
            y - self.radio < objeto[1] + objeto[3]
        )

    def dibujar(self):
        pygame.draw.circle(self.ventana, (255, 255, 0), (int(self.x), int(self.y)), self.radio)

class Juego:
    def __init(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.ventana = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Mueve la bola")

    def dibujar_borde(self):
        pygame.draw.rect(self.ventana, (0, 0, 0), (0, 0, self.ancho, self.alto), 100)

    def ejecutar(self):
        objetos_negros = [(200, 200, 50, 50), (400, 300, 60, 60)]  # Ejemplo de objetos negros

        bola = Bola(self.ventana, 20, self.alto - 20, 20, 0.4)

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            teclas = pygame.key.get_pressed()

            bola.mover(teclas, objetos_negros)

            self.ventana.fill((0, 0, 128))

            self.dibujar_borde()

            # Dibujar objetos negros
            for objeto in objetos_negros:
                pygame.draw.rect(self.ventana, (0, 0, 0), objeto)

            bola.dibujar()

            pygame.display.update()

if __name__ == "__main__":
    juego = Juego(ANCHO_VENTANA, ALTO_VENTANA)
    juego.ejecutar()