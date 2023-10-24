import pygame

class Bola:
    def __init__(self, ventana, x, y, radio, velocidad):
        self.ventana = ventana
        self.x = ANCHO_VENTANA // 2
        self.y = ALTO_VENTANA // 2
        self.radio = radio
        self.velocidad = velocidad

    def mover(self, teclas):
        if teclas[pygame.K_UP]:
            self.y -= self.velocidad
        if teclas[pygame.K_DOWN]:
            self.y += self.velocidad
        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidad

        if self.x + self.radio >= ANCHO_VENTANA:
            self.x = ANCHO_VENTANA - self.radio
        if self.x - self.radio <= 0:
            self.x = self.radio
        if self.y + self.radio >= ALTO_VENTANA:
            self.y = ALTO_VENTANA - self.radio
        if self.y - self.radio <= 0:
            self.y = self.radio

    def dibujar(self):
        pygame.draw.circle(self.ventana, (255, 255, 0), (int(self.x), int(self.y)), self.radio)

class Juego:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.ventana = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Mueve la bola")

    def dibujar_borde(self):
        pygame.draw.rect(self.ventana, (0, 0, 0), (0, 0, self.ancho, self.alto), 100)

    def ejecutar(self):
        bola = Bola(self.ventana, 20, self.alto - 20, 20, 0.4)

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            teclas = pygame.key.get_pressed()

            bola.mover(teclas)

            self.ventana.fill((0, 0, 128))

            self.dibujar_borde()
            bola.dibujar()

            pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    ANCHO_VENTANA = 800
    ALTO_VENTANA = 720

    juego = Juego(ANCHO_VENTANA, ALTO_VENTANA)
    juego.ejecutar()