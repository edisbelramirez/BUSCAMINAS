from tkinter import Canvas,Frame
from Ventana.ventana import Ventana
from Ventana.juego import Juego
from MaquinaEstados.enumEstados import EnumEstadosJuego
from utiles import MaquinaEstadosBuscaminas
   
class VentanaBuscaminas(Ventana):
    def __init__(self,ancho,alto,titulo,me,juego,enumEstados):
        super().__init__(ancho,alto,titulo,me,juego,enumEstados)
        self.frame = Frame() # Empaqueta el frame en Estilo
        self.lienzo = Canvas(self.frame)
        self.lienzo.pack()

        self.me = me(enumEstados().ESTADO_JUEGO,enumEstados,self.lienzo,self.frame)
        self.juego = juego(self,self.me)

        self.animate(self.juego)        
        self.main()
       
        
class Buscaminas():
    def __init__(self) -> None:
        self.ventana = VentanaBuscaminas(850,450,"Buscaminas",MaquinaEstadosBuscaminas,Juego,EnumEstadosJuego)
    
b = Buscaminas()
