import requests
import json


class jsonhandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(jsonhandler, cls).__new__(cls)
            cls._instance.cargar_json()
        return cls._instance

    def cargar_json(self):
        try:
            with open('scores.json', 'r') as f:
                self.diccionario = json.load(f)
        except FileNotFoundError:
            self.diccionario = {"puntajes": []}

    def guardar_json(self):
        with open('scores.json', 'w') as f:
            json.dump(self.diccionario, f, indent=2)

    def agregar_persona(self, nombre, puntaje):
        nueva_persona = {"nombre": nombre, "score": puntaje}
        puntajes = self.diccionario.get("puntajes", [])
        for i, person in enumerate(puntajes):
            if person["score"] <= nueva_persona["score"]:
                puntajes[i] = nueva_persona
                break
        else:
            puntajes.append(nueva_persona)
        self.diccionario["puntajes"] = sorted(puntajes, key=lambda x: x["score"], reverse=True)
        self.guardar_json()