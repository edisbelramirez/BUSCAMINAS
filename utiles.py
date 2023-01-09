from MaquinaEstados.maquinaEstados import MaquinaEstados
from estadoJuegoBuscaminas import EstadoJuegoBuscaminas

class MaquinaEstadosBuscaminas(MaquinaEstados):
    def __init__(self,estadoInicial,enumEstados,lienzo,frame):
        self.frame = frame
        super().__init__(estadoInicial,enumEstados,lienzo)
    
    def cambiarEstado(self, nuevoEstado,lienzo):
        if nuevoEstado == self.enumEstadosJuego.ESTADO_JUEGO:
            self.estadoActual = EstadoJuegoBuscaminas(lienzo,self.frame)

class Colors:
    color_set_numbers = ["#c8c7c7","#6ea1ad","#167b94","#ac2f2f"]