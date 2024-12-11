from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder
from kivy.clock import Clock
import trimesh
import subprocess


Builder.load_file("tela.kv")

class InputScreen(Screen):
    pass

class MeshScreen(Screen):
    pass

class FormApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(InputScreen(name='inputScreen'))
        sm.add_widget(MeshScreen(name='meshScreen'))

        return sm

    def process_inputs(self):
        screen = self.root.get_screen("inputScreen")

        etnia = screen.ids.etnia_input.text
        idade = screen.ids.idade_input.text
        peso = screen.ids.peso_input.text
        sexo = ""
        if screen.ids.male_checkbox.active:
            sexo = "M"
            print("Male")
        else:
            sexo = "F"
            print("Female")
        volume_malha = screen.ids.volume_malha_input.text

        print("Etnia:", etnia)
        print("Idade:", idade)
        print("Peso:", peso)
        #print("Sexo:", sexo)
        print("Volume da Malha:", volume_malha)

    def on_start(self):
        # Example of attaching a listener to a TextInput field
        screen = self.root
        self.root.get_screen("inputScreen").ids.male_checkbox.active=True

    def checkbox_gender(checkbox, value):
        if value:
            print('The checkbox', checkbox, 'is active')
        else:
            print('The checkbox', checkbox, 'is inactive')
        
    def open_mesh(self):
        file_path = self.root.get_screen("meshScreen").ids.meshPath.text

        mesh = trimesh.load(file_path)
        volume = mesh.volume / 1000.0
        self.mesh_volume = volume
        subprocess.Popen([sys.executable, 'mesh_viewer.py', file_path])


if __name__ == "__main__":
    FormApp().run()
