<<<<<<< HEAD
import tkinter as tk


def vent_juego():
    prin_menu.destroy()
    juego = tk.Tk()
    juego.title("Juego")
    juego.minsize(height=700, width=1200)


    vent_juego.mainloop()



=======
import json
import tkinter as tk
import juego_pygame
from JsonHndlr import jsonhandler
from array import  array
#importar la "clase" juego
tipoJuego=0#variable global que se usa como flags
puntajes =["puntaje1","puntaje2","puntaje3"]
nombres=["n1","n2","n3"]
nombre ="randomName"
puntaje=0
#archivador.agregar_persona("tuma",580)#aca se llama para guardar el score al json
>>>>>>> Danie-rama
def ven_info():
    infor = tk.Toplevel()
    infor.title("Información")
    infor.minsize(height=600, width=1200)

<<<<<<< HEAD
=======
    info_proyec = tk.PhotoImage(file="Fondo_info.png")
    lbl_fondo_inf = tk.Label(infor, image=info_proyec)
    lbl_fondo_inf.pack()

>>>>>>> Danie-rama
    btn_cerrarinfo = tk.Button(infor, command=infor.destroy, font=("Arial", 20), fg="black",
                               text="Volver")
    btn_cerrarinfo.place(x=1050, y=500)


    infor.mainloop()


<<<<<<< HEAD
=======
def guardar_usuario():#funcion para almacenar el nombre de usuario.
    global nombre
    nombre =nom_juga.get()
    print(nombre)

def iniciarJuego():#funcion para crear una instancia de juego_pygame,llama al metodo ejecutar
    global tipoJuego
    global nombre
    global puntaje
    if tipoJuego == 1:
        juego = juego_pygame.Juego(800, 720)
        juego.ejecutar()
        archivador = jsonhandler()
        archivador.agregar_persona(nombre, puntaje)

def cambiarJuego():
    global  tipoJuego
    if tipoJuego ==0:
        tipoJuego=1
        print("el juego cambio a 1")
    else:
        tipoJuego=0
        print("el juego cambio a 0")
>>>>>>> Danie-rama

def rankings():
    rank = tk.Tk()
    rank.title("Tabla de puntaciones")
    rank.minsize(height=600, width=1200)

    btn_cerrarranked = tk.Button(rank, command=rank.destroy, font=("Arial", 20), fg="black",
                                 text="Volver")
    btn_cerrarranked.place(x=1050, y=500)

<<<<<<< HEAD
    titu_rankds = tk.Label(rank, text="Tabla de clasificacion:", bg="gray", fg="white", font=("Arial", 30))
    titu_rankds.place(x=430, y=50)


    rank.mainloop()



prin_menu = tk.Tk()
prin_menu.title("Inicio")

pacman = tk.PhotoImage(file="fondprin.png")
lbl_fondo = tk.Label(prin_menu, image=pacman)
lbl_fondo.pack()




btn_juego = tk.Button(prin_menu, text="PLAY", command=vent_juego, font=("Arial", 30), fg="black")
btn_juego.place(x=430, y=300)


btn_info = tk.Button(prin_menu, text="INFO", command=ven_info, font=("Arial", 30), fg="black")
btn_info.place(x=220, y=300)


btn_rankings = tk.Button(prin_menu, text="RANKING", command=rankings, font=("Arial", 30), fg="black")
btn_rankings.place(x=670, y=300)

=======
    btn_actuali = tk.Button(rank, font=("Arial", 20), fg="black",
                                 text="Actualizar")
    btn_actuali.place(x=500, y=500)

    titu_rankds = tk.Label(rank, text="Tabla de clasificacion:", bg="gray", fg="white", font=("Arial", 20))
    titu_rankds.place(x=430, y=50)
    usua1 = tk.Label(rank, bg="gray", fg="white", font=("Arial", 20), text="")
    usua1.place(x=430, y=100)
    puntaje1 = tk.Label(rank, bg="gray", fg="white", font=("Arial", 20), text="")
    puntaje1.place(x=520, y=100)

    usua2 = tk.Label(rank, bg="gray", fg="white", font=("Arial", 20), text="")
    usua2.place(x=430, y=140)
    puntaje2 = tk.Label(rank, bg="gray", fg="white", font=("Arial", 20), text="")
    puntaje2.place(x=520, y=140)

    usua3 = tk.Label(rank, bg="gray", fg="white", font=("Arial", 20), text="")
    usua3.place(x=430, y=180)
    puntaje3 = tk.Label(rank, bg="gray", fg="white", font=("Arial", 20), text="")
    puntaje3.place(x=520, y=180)
    global puntajes
    global nombres
    try:
        with open('scores.json', 'r') as f:
            diccionario = json.load(f)
    except FileNotFoundError:
        pass
    puntaje = diccionario.get("puntajes", [])  # agarra el tag puntajes
    # obtiene el diccionario
    # self.diccionario["puntajes"] = sorted(self.diccionario["puntajes"], key=lambda x: (x["edad"], x["valor"]))
    for i, person in enumerate(puntaje):  # dentro de puntajes agarra los elementos y los almacena
        nombres[i] = person["nombre"]  # en la variable persona
        puntajes[i] = person["score"]
    # Cambia directamente el texto del Label
    usua1.config(text=nombres[0])
    puntaje1.config(text=puntajes[0])
    usua2.config(text=nombres[1])
    puntaje2.config(text=puntajes[1])
    usua3.config(text=nombres[2])
    puntaje3.config(text=puntajes[2])
    rank.mainloop()


prin_menu = tk.Tk()
prin_menu.title("Inicio")
pacman = tk.PhotoImage(file="fondprin.png")
lbl_fondo = tk.Label(prin_menu, image=pacman)
lbl_fondo.pack()
nom_juga = tk.Entry(prin_menu)#es la zona para escibir el nombre de jugador
nom_juga.place(x=530, y=200)
#aca esta la solucion , el problema es que inicia el juego directamente
btn_juego = tk.Button(prin_menu,command= iniciarJuego, text="PLAY", font=("Arial", 20), fg="black")
btn_juego.place(x=530, y=500)

btn_gua_usu = tk.Button(prin_menu, text="Guardar jugador", font=("Arial", 20), fg="black", command=guardar_usuario)
btn_gua_usu.place(x=430, y=300)
btn_info = tk.Button(prin_menu, text="INFO", command=ven_info, font=("Arial", 20), fg="black")
btn_info.place(x=420, y=500)
btn_info = tk.Button(prin_menu, text="CargarJuego", command=cambiarJuego, font=("Arial", 20), fg="black")
btn_info.place(x=120, y=500)

btn_rankings = tk.Button(prin_menu, text="RANKING", command=rankings, font=("Arial", 20), fg="black")
btn_rankings.place(x=670, y=500)

#esto son pruebas
>>>>>>> Danie-rama
prin_menu.mainloop()