import pygame
import random
import math

ANCHO_VENTANA = 800
ALTO_VENTANA = 720

objetos_negros = [(0, 0, 800, 50), (0, 670, 800, 50), (0, 0, 50, 720), (750, 0, 50, 720)]



bola = None


pygame.init()
matriz = [[0] * 40 for _ in range(36)]

class Bola:
    def __init__(self, ventana, x, y, radio, velocidad):
        self.ventana = ventana
        self.x = ANCHO_VENTANA // 2
        self.y = ALTO_VENTANA // 2
        self.radio = radio
        self.velocidad = velocidad
        self.gameover = False
        self.comiendo = False

    def mover(self, teclas, objetos_negros):
        global pastillas, fantasmas
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

        fantasmas_muertos = []

        for i , fantasma in enumerate(fantasmas):
            if not bola.comiendo:
                if self.colisiona_con_objeto(x_siguiente, y_siguiente, (fantasma.x, fantasma.y, 10, 10,)):
                    self.gameover = True
            else:
                if self.colisiona_con_objeto(x_siguiente, y_siguiente, (fantasma.x, fantasma.y, 10, 10,)):
                    fantasmas_muertos.append(i)

        fantasmas_vivos = []

        for i , fantasma in enumerate(fantasmas):
            if not i in fantasmas_muertos:
                fantasmas_vivos.append(fantasma)

        fantasmas = fantasmas_vivos

        pastillas_aborrar = []

        for i , pastilla in enumerate(pastillas):
            if self.colisiona_con_objeto(x_siguiente, y_siguiente, (pastilla.x, pastilla.y, 20, 20,)):
                self.comiendo = True
                pastillas_aborrar.append(i)

        pastillas_sobro = []

        for i , pastilla in enumerate(pastillas):
            if not i in pastillas_aborrar:
                pastillas_sobro.append(pastilla)

        pastillas = pastillas_sobro

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


    def colisiona_con_objeto(self, x, y, objeto):
        return (
            x + 20 > objeto[0] and
            x - 20 < objeto[0] + objeto[2] and
            y + 20 > objeto[1] and
            y - 20 < objeto[1] + objeto[3])

    def mover_continuamente(self):

        x_siguiente = self.x + self.direccion_x * self.velocidad
        y_siguiente = self.y + self.direccion_y * self.velocidad
        for objeto in objetos_negros:
            if self.colisiona_con_objeto(x_siguiente, y_siguiente, objeto):
                self.direccion_x, self.direccion_y = random.choice([-1, 1]), random.choice([-1, 1])
                return
            
        self.x = x_siguiente
        self.y = y_siguiente

        if self.x < 0 or self.x > self.ANCHO_VENTANA:
            self.direccion_x = -self.direccion_x
        if self.y < 0 or self.y > self.ALTO_VENTANA:
            self.direccion_y = -self.direccion_y

fantasmas = [
    Fantasma(x=100, y=100, velocidad=0.1, ANCHO_VENTANA=ANCHO_VENTANA, ALTO_VENTANA=ALTO_VENTANA, color=(255, 20, 147)),    # Rosa
    Fantasma(x=200, y=200, velocidad=0.1, ANCHO_VENTANA=ANCHO_VENTANA, ALTO_VENTANA=ALTO_VENTANA, color=(255, 69, 0)),      # Naranja
    Fantasma(x=300, y=300, velocidad=0.1, ANCHO_VENTANA=ANCHO_VENTANA, ALTO_VENTANA=ALTO_VENTANA, color=(0, 255, 255)),     # Cian
    Fantasma(x=400, y=400, velocidad=0.2, ANCHO_VENTANA=ANCHO_VENTANA, ALTO_VENTANA=ALTO_VENTANA, color=(255, 0, 0))]       # Rojo


class Item:
    
    def __init__(self, x, y, radio):
        self.x = x
        self.y = y
        self.radio = radio


class Fruta(Item):

    def __init__(self, x, y, radio):
        Item.__init__(self,x,y, radio)

class Alimento(Item):

    def __init__(self, x, y, radio):
        Item.__init__(self,x,y, radio)

class Pastilla(Item):

    def __init__(self, x, y, radio):
        Item.__init__(self,x,y, radio)

alimentos = []

pastillas = [Pastilla(x=400, y=300, radio=10), Pastilla(300, 600, radio=10), Pastilla(80, 543, radio=10)]

frutas = [Pastilla(x=450, y=360, radio=15), Pastilla(340, 300, radio=10), Pastilla(70, 383, radio=10)]

class Juego:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.ventana = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("PAC-MAN")
        self.tecla_m_presionada = False

    def imprimir_matriz(self):
        for fila in range(36):
            for columna in range(40):
                if matriz[fila][columna] == 0:
                    print(" ", end= " ")
                else:
                    print(matriz[fila][columna], end=" ")
            print()

    def act_mat(self):
        global fantasmas, matriz, alimentos, pastillas, frutas, objetos_negros

        for fila in range(36):
            for columna in range(40):
                matriz[fila][columna] = 0

        x_matriz = (int(bola.y) // 20)
        y_matriz = (int(bola.x) // 20)
        matriz[x_matriz][y_matriz] = 8
        

        for ghost in fantasmas:
            x_matriz = (int(ghost.y) // 20)
            y_matriz = (int(ghost.x) // 20)
            matriz[x_matriz][y_matriz] = 9
        for ali in alimentos:
            x_matriz = int(ali.y // 20)
            y_matriz = int(ali.x // 20)
            matriz[x_matriz][y_matriz] = 1
        for pelota in pastillas:
            x_matriz = int(pelota.y // 20)
            y_matriz = int(pelota.x // 20)
            matriz[x_matriz][y_matriz] = 2
        for cereza in frutas:
            x_matriz = int(cereza.y // 20)
            y_matriz = int(cereza.x // 20)
            matriz[x_matriz][y_matriz] = 3
        for bloque in objetos_negros:
            x_matriz = int(bloque[1] // 20)
            y_matriz = int(bloque[0] // 20)
            matriz[x_matriz][y_matriz] = 0

       

    def ejecutar(self):
        
        global objetos_negros, bola, pastillas, frutas

        bola = Bola(self.ventana, 20, self.alto - 40, 20, 0.2)

        pausa = False

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            teclas = pygame.key.get_pressed()

            if teclas[pygame.K_m] and not self.tecla_m_presionada:
                if not pausa:
                    self.imprimir_matriz()
                print(f"Posición de la bola: ({int(bola.x/20)}, {int(bola.y/20)})")
                self.tecla_m_presionada = True
                pausa = not pausa
            elif not teclas[pygame.K_m]:
                self.tecla_m_presionada = False
            

            if not pausa:
                if not bola.gameover:
                    bola.mover(teclas, objetos_negros)

                if bola.gameover:
                    pausa = True
                else:


                    self.ventana.fill((0, 0, 128))


                    # Dibujar objetos negros
                    for objeto in objetos_negros:
                        pygame.draw.rect(self.ventana, (0, 0, 0), objeto)

                    bola.dibujar()

                    for fantasma in fantasmas:
                        fantasma.mover_continuamente()

                    for fantasma in fantasmas:
                        pygame.draw.polygon(self.ventana, fantasma.color, [(fantasma.x, fantasma.y - 20), (fantasma.x - 20, fantasma.y + 20), (fantasma.x + 20, fantasma.y + 20)])

                    for pastilla in pastillas:
                        pygame.draw.circle(self.ventana, (255, 255, 255), (int(pastilla.x), int(pastilla.y)), pastilla.radio)

                    for fruta in frutas:
                        pygame.draw.circle(self.ventana, (20, 123, 200), (int(fruta.x), int(fruta.y)), fruta.radio)

                    self.act_mat()

            pygame.display.update()

            

if __name__ == "__main__":
    juego = Juego(800, 720)
    juego.ejecutar()