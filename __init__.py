import json

from mycroft import MycroftSkill, intent_file_handler

ficheroJSON = "/home/serggom/scraping/datos.json"


class AsignaturasCampus(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('campus.asignaturas.intent')
    def handle_campus_asignaturas(self, message):
        # Lectura de la informacion del fichero JSON
        with open(ficheroJSON) as ficheroAsignaturas:
            data = json.load(ficheroAsignaturas)
            self.speak(
                "En el curso actual estás matriculado en las siguientes asignaturas:")

            for subject in data['asignaturas']:
                self.speak(subject['nombre'])


def create_skill():
    return AsignaturasCampus()
