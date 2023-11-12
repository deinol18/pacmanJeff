import threading
import pygame
import random
import time

ANCHO_VENTANA = 800
ALTO_VENTANA = 720

objetos_negros = [(0, 0, 800, 50), (0, 670, 800, 50), (0, 0, 50, 720), (750, 0, 50, 720)]

puntos = 0

nivel_actual = 1

cantF = 0

bola = None

segundos = 0

#-------------------------------- Contador del tiempo   -----------------------------------
def incrementar_tiempo():
    global segundos, puntos
    interval = 10
    while True:
        if segundos % interval == 0 and segundos > 0:
            puntos += 5
        time.sleep(1)
        segundos += 1


thread = threading.Thread(target=incrementar_tiempo)
pygame.init()
matriz = [[0] * 40 for i in range(36)]

#------------------------------ Clase con las funciones del pacman  ------------------------------
class Bola:
    def __init__(self, ventana, x, y, radio, velocidad):
        self.ventana = ventana
        self.x = ANCHO_VENTANA // 2
        self.y = ALTO_VENTANA // 2
        self.radio = radio
        self.velocidad = velocidad
        self.gameover = False
        self.comiendo = False

    def subir_nivel(self):  #   Funcion para subir nivel
        global fantasmas, nivel_actual, fantasmas_iniciales, pastillas, pastillas_iniciales, frutas, fantasmas_iniciales
        if len(fantasmas) == 0:
            nivel_actual += 1
            self.comiendo = False
            fantasmas = fantasmas_iniciales
            pastillas = pastillas_iniciales
            #   Agregar fantasmas, frutas y pastillas
            for i in range(nivel_actual * 2):
                fantasmas.append(
                    Fantasma(x=random.randint(110, 245), y=random.randint(110, 245), velocidad=0.1 * nivel_actual,
                             ANCHO_VENTANA=ANCHO_VENTANA, ALTO_VENTANA=ALTO_VENTANA, color=(random.randint(0, 255),
                                                                                            random.randint(0, 255),
                                                                                   random.randint(0, 255))), )
            for i in range(nivel_actual+1):
                pastillas.append(
                    Pastilla(x=random.randint(100, 750), y=random.randint(100, 610), radio=8, )
                )

                frutas.append(
                    Fruta(x=random.randint(100, 750), y=random.randint(100, 600), radio=12, )
                )

    def mover(self, teclas, objetos_negros):    #   Funcion del movimiento del del pacman
        global pastillas, fantasmas, puntos, alimentos, nivel_actual, frutas, cantF
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

        for objeto in objetos_negros:   #   Colision con las paredes
            if self.colisiona_con_objeto(x_siguiente, y_siguiente, objeto):
                return

        fantasmas_muertos = []

        for i, fantasma in enumerate(fantasmas):    # Colisión con los fantasmas
            if not bola.comiendo:
                if self.colisiona_con_objeto(x_siguiente, y_siguiente, (fantasma.x, fantasma.y, 10, 10,)):
                    self.gameover = True

            else:
                if self.colisiona_con_objeto(x_siguiente, y_siguiente, (fantasma.x, fantasma.y, 10, 10,)):
                    fantasmas_muertos.append(i)
                    cantF += 1
                    print(cantF)
                    puntos += 10

        fantasmas_vivos = []

        for i, fantasma in enumerate(fantasmas):
            if not i in fantasmas_muertos:
                fantasmas_vivos.append(fantasma)

        fantasmas = fantasmas_vivos

        pastillas_aborrar = []

        for i, pastilla in enumerate(pastillas):    #   Colisión con las pastillas
            if self.colisiona_con_objeto(x_siguiente, y_siguiente, (pastilla.x, pastilla.y, 20, 20,)):
                pastillas_aborrar.append(i)
                self.comiendo = True

        pastillas_sobro = []

        for i, pastilla in enumerate(pastillas):
            if not i in pastillas_aborrar:
                pastillas_sobro.append(pastilla)

        pastillas = pastillas_sobro


        ali_aborrar = []

        for i, alimento in enumerate(alimentos):    #   Colisión con los alimentos
            if self.colisiona_con_objeto(x_siguiente, y_siguiente, (alimento[0], alimento[1], 7, 7,)):
                puntos += 1
                ali_aborrar.append(i)

        alimentos_sobro = []

        for i, alimento in enumerate(alimentos):
            if not i in ali_aborrar:
                alimentos_sobro.append(alimento)

        alimentos = alimentos_sobro


        frutas_aborrar = []

        for i, fruta in enumerate(frutas):  #   Colisión con las frutas
            if self.colisiona_con_objeto(x_siguiente, y_siguiente, (fruta.x, fruta.y, 20, 20,)):
                puntos += 20
                frutas_aborrar.append(i)

        frutas_sobro = []

        for i, fruta in enumerate(frutas):
            if not i in frutas_aborrar:
                frutas_sobro.append(fruta)

        frutas = frutas_sobro

        self.x = x_siguiente
        self.y = y_siguiente
        self.subir_nivel()


    def colisiona_con_objeto(self, x, y, objeto):   #   Colisión con los objetos
        return (
                x + self.radio > objeto[0] and
                x - self.radio < objeto[0] + objeto[2] and
                y + self.radio > objeto[1] and
                y - self.radio < objeto[1] + objeto[3])

    def dibujar(self):  #   Dibujar el pacman
        pygame.draw.circle(self.ventana, (255, 255, 0), (int(self.x), int(self.y)), self.radio)


class Fantasma: #   Clase con las funciones de los fantasmas
    def __init__(self, x, y, velocidad, ANCHO_VENTANA, ALTO_VENTANA, color):
        self.x, self.y = x, y
        self.velocidad = velocidad
        self.direccion_x, self.direccion_y = random.choice([-1, 1]), random.choice([-1, 1])
        self.ANCHO_VENTANA, self.ALTO_VENTANA = ANCHO_VENTANA, ALTO_VENTANA
        self.color = color

    def colisiona_con_objeto(self, x, y, objeto):   #   Colisión con las paredes
        return (
                x + 20 > objeto[0] and
                x - 20 < objeto[0] + objeto[2] and
                y + 20 > objeto[1] and
                y - 20 < objeto[1] + objeto[3])

    def mover_continuamente(self):  #   Función de movimiento

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

#   Lista con los fantasmas iniciales
fantasmas = [
    Fantasma(x=100, y=100, velocidad=0.1, ANCHO_VENTANA=ANCHO_VENTANA, ALTO_VENTANA=ALTO_VENTANA, color=(255, 20, 147)),
    # Rosa
    Fantasma(x=200, y=200, velocidad=0.1, ANCHO_VENTANA=ANCHO_VENTANA, ALTO_VENTANA=ALTO_VENTANA, color=(255, 69, 0)),
    # Naranja
    Fantasma(x=300, y=300, velocidad=0.1, ANCHO_VENTANA=ANCHO_VENTANA, ALTO_VENTANA=ALTO_VENTANA, color=(0, 255, 255)),
    # Cian
    Fantasma(x=400, y=400, velocidad=0.2, ANCHO_VENTANA=ANCHO_VENTANA, ALTO_VENTANA=ALTO_VENTANA, color=(255, 0, 0))]
    # Rojo


fantasmas_iniciales = fantasmas


class Item: #   Clases con los atributos de los items

    def __init__(self, x, y, radio):
        self.x = x
        self.y = y
        self.radio = radio


class Fruta(Item):

    def __init__(self, x, y, radio):
        Item.__init__(self, x, y, radio)


class Alimento(Item):

    def __init__(self, x, y, radio):
        Item.__init__(self, x, y, radio)


class Pastilla(Item):

    def __init__(self, x, y, radio):
        Item.__init__(self, x, y, radio)


def generar_alimentos(cantidad):    #   Generación de los alimentos random
    return [(random.randint(30, 700), random.randint(30, 700),) for _ in range(cantidad)]


alimentos = generar_alimentos(150)

pastillas = [Pastilla(80, 543, radio=8), Pastilla(x=600, y=100, radio=8)]   #   Generación de las pastillas
pastillas_iniciales = pastillas

frutas = [Pastilla(x=450, y=360, radio=12), Pastilla(340, 300, radio=12), Pastilla(70, 383, radio=12)]  #   Generación de las pastillas
frutas_iniciales = frutas


class Juego:    #   Clases con los métodos del juego
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.ventana = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("PAC-MAN")
        self.tecla_m_presionada = False

    def imprimir_matriz(self):  #   Imprimir la matriz inicialmente
        for fila in range(36):
            for columna in range(40):
                print(matriz[fila][columna], end="")
            print()

    def act_mat(self):  #   Actualización de la matriz
        global fantasmas, matriz, alimentos, pastillas, frutas, objetos_negros

        for fila in range(36):
            for columna in range(40):
                if fila < 3 or fila > 32 or columna < 3 or columna > 36:
                    matriz[fila][columna] = 0
                else:
                    matriz[fila][columna] = " "

        x_matriz = (int(bola.y) // 20)
        y_matriz = (int(bola.x) // 20)
        matriz[x_matriz][y_matriz] = 8

        for ghost in fantasmas: #   Actualización de la matriz con los fantasmas
            x_matriz = (int(ghost.y) // 20)
            y_matriz = (int(ghost.x) // 20)
            matriz[x_matriz][y_matriz] = 9
        for ali in alimentos:   #   Actualización de la matriz con los alimentos
            x_matriz = int(ali[1] // 20)
            y_matriz = int(ali[0] // 20)
            matriz[x_matriz][y_matriz] = 1
        for pelota in pastillas:    #   Actualización de la matriz con las pastillas
            x_matriz = int(pelota.y // 20)
            y_matriz = int(pelota.x // 20)
            matriz[x_matriz][y_matriz] = 2
        for cereza in frutas:   #   Actualización de la matriz con las frutas
            x_matriz = int(cereza.y // 20)
            y_matriz = int(cereza.x // 20)
            matriz[x_matriz][y_matriz] = 3
        for bloque in objetos_negros:   #   Actualización de la matriz con las paredes
            x_matriz = int(bloque[1] // 20)
            y_matriz = int(bloque[0] // 20)
            matriz[x_matriz][y_matriz] = 0

    def ejecutar(self): #   Función para ejecutar el juego

        global objetos_negros, bola, pastillas, frutas

        bola = Bola(self.ventana, 20, self.alto - 40, 20, 1)

        pausa = False

        thread.start()

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            teclas = pygame.key.get_pressed()

            if teclas[pygame.K_m] and not self.tecla_m_presionada:  # Presionar M para printear la matriz y la posición actual del pacman
                if not pausa:
                    self.imprimir_matriz()
                print(f"Posición de la bola: ({int(bola.x / 20)}, {int(bola.y / 20)})")
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

                    for alimento in alimentos:
                        pygame.draw.circle(self.ventana, (255, 255, 255), alimento, 2)

                    # Dibujar objetos negros
                    for objeto in objetos_negros:
                        pygame.draw.rect(self.ventana, (0, 0, 0), objeto)

                    font = pygame.font.SysFont(None, 48)
                    textimage = font.render(f"Puntos: {puntos}", True, (255, 255, 255,))
                    self.ventana.blit(textimage, (50, 10,))

                    font = pygame.font.SysFont(None, 48)
                    textimage = font.render(f"Nivel: {nivel_actual}", True, (255, 255, 255,))
                    self.ventana.blit(textimage, (250, 10,))

                    font = pygame.font.SysFont(None, 48)
                    textimage = font.render(f"Tiempo: {segundos}", True, (255, 255, 255,))
                    self.ventana.blit(textimage, (400, 10,))

                    bola.dibujar()

                    for fantasma in fantasmas:
                        fantasma.mover_continuamente()

                    #   Texto mostrado en pantalla
                    for fantasma in fantasmas:
                        pygame.draw.polygon(self.ventana, fantasma.color,
                                            [(fantasma.x, fantasma.y - 20), (fantasma.x - 20, fantasma.y + 20),
                                             (fantasma.x + 20, fantasma.y + 20)])

                    for pastilla in pastillas:
                        pygame.draw.circle(self.ventana, (255, 255, 255), (int(pastilla.x), int(pastilla.y)),
                                           pastilla.radio)

                    for fruta in frutas:
                        pygame.draw.circle(self.ventana, (172, 0, 0), (int(fruta.x), int(fruta.y)), fruta.radio)

                    self.act_mat()

            pygame.display.update()


if __name__ == "__main__":
    juego = Juego(800, 720)
    juego.ejecutar()