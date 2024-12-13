from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder
from kivy.clock import Clock
import trimesh
import subprocess
import sys

def calcula_volume_pulmao(altura, peso):
        return (((0.0472*(altura))+(0.000009*peso))-5.92)*1000
    
def calcula_densidade(volume, peso, vol_pulmao):
	volume = volume/1000
	return peso/(volume - vol_pulmao) 
    
def calcula_perc_gordura(densidade, etnia):
    gordura = 0
    
    if(etnia == "preto"):gordura = (437 / densidade) - 393
    elif(etnia == "pardo"):gordura = (437 / densidade) - 392
    elif(etnia == "amarelo"):gordura = (503 / densidade) - 462
    else:gordura = (495 / densidade) - 450
            
    return (gordura)

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
        screen.ids.perc_gordura.text = ""

        etnia = screen.ids.etnia_input.text
        idade = int(screen.ids.idade_input.text)
        peso = float(screen.ids.peso_input.text)
        altura = float(screen.ids.altura_input.text)
        sexo = ""
        if screen.ids.male_checkbox.active:
            sexo = "M"
            print("Male")
        else:
            sexo = "F"
            print("Female")
        volume_malha = float(screen.ids.volume_malha_input.text)

        print("Etnia:", etnia)
        print("Idade:", idade)
        print("Peso:", peso)
        #print("Sexo:", sexo)
        print("Volume da Malha:", volume_malha)
        
        volume_pulmao = calcula_volume_pulmao(altura, peso)
        print("vol. pulmão:", volume_pulmao)

        densidade = calcula_densidade(volume_malha, peso,volume_pulmao)
        print("densidade:", densidade)
        perc_gordura = calcula_perc_gordura(densidade, etnia)
        print("perc_gordura:", perc_gordura)
        screen.ids.perc_gordura.text = f"{perc_gordura:.2f}%"

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
