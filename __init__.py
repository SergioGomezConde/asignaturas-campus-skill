from mycroft import MycroftSkill, intent_file_handler


class AsignaturasCampus(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('campus.asignaturas.intent')
    def handle_campus_asignaturas(self, message):
        self.speak_dialog('campus.asignaturas')


def create_skill():
    return AsignaturasCampus()

