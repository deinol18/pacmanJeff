import tkinter as tk


def vent_juego():
    prin_menu.destroy()
    juego = tk.Tk()
    juego.title("Juego")
    juego.minsize(height=700, width=1200)


    vent_juego.mainloop()



def ven_info():
    infor = tk.Toplevel()
    infor.title("Información")
    infor.minsize(height=600, width=1200)

    btn_cerrarinfo = tk.Button(infor, command=infor.destroy, font=("Arial", 20), fg="black",
                               text="Volver")
    btn_cerrarinfo.place(x=1050, y=500)


    infor.mainloop()



def rankings():
    rank = tk.Tk()
    rank.title("Tabla de puntaciones")
    rank.minsize(height=600, width=1200)

    btn_cerrarranked = tk.Button(rank, command=rank.destroy, font=("Arial", 20), fg="black",
                                 text="Volver")
    btn_cerrarranked.place(x=1050, y=500)

    titu_rankds = tk.Label(rank, text="Tabla de clasificacion:", bg="gray", fg="white", font=("Arial", 20))
    titu_rankds.place(x=430, y=50)


    rank.mainloop()



prin_menu = tk.Tk()
prin_menu.title("Inicio")

pacman = tk.PhotoImage(file="fondprin.png")
lbl_fondo = tk.Label(prin_menu, image=pacman)
lbl_fondo.pack()




btn_juego = tk.Button(prin_menu, text="PLAY", command=vent_juego, font=("Arial", 20), fg="black")
btn_juego.place(x=530, y=500)


btn_info = tk.Button(prin_menu, text="INFO", command=ven_info, font=("Arial", 20), fg="black")
btn_info.place(x=420, y=500)


btn_rankings = tk.Button(prin_menu, text="RANKING", command=rankings, font=("Arial", 20), fg="black")
btn_rankings.place(x=670, y=500)

prin_menu.mainloop()