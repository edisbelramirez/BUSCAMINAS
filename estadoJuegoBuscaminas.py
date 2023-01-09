from MaquinaEstados.interfazEstadosJuego import InterfazEstadosJuego
from Elementos.elementos import Tablero,Casilla,Punto
from Estilo import Estilo

class EstadoJuegoBuscaminas(InterfazEstadosJuego):
    def __init__(self,lienzo,frame):
        self.pixelInicialCanvas = 1 # Los px del canvas comienza en 1
        self.estilo = Estilo(lienzo,frame)

        self.tablero = None
        self.lienzo = lienzo
        self.cambiosRecientes = False
        self.DERROTA = False
        self.VICTORIA = False
        self.iniciar_tablero()
       
    def iniciar_tablero(self):
        #Configura el ancho el alto y las minas del tablero
        self.tablero = Tablero(10,20,8)

        self.estilo.configurar_lienzo("black",self.tablero.ancho*self.tablero.pixelesCuadro,
        self.tablero.alto*self.tablero.pixelesCuadro)

        relleno = "#bbb4b4"
        for i in range(0,self.tablero.alto):
            for x in range(0,self.tablero.ancho):
      
                xInicial = x * self.tablero.pixelesCuadro + self.pixelInicialCanvas
                yInicial = i * self.tablero.pixelesCuadro + self.pixelInicialCanvas
                xFinal = x * self.tablero.pixelesCuadro + self.tablero.pixelesCuadro
                yFinal = i * self.tablero.pixelesCuadro + self.tablero.pixelesCuadro

                refCuadro = self.lienzo.create_rectangle(xInicial,yInicial,xFinal,yFinal,fill=relleno,outline='#000')
                self.lienzo.tag_bind(refCuadro,'<ButtonPress-1>',self.eventoClick)
                self.lienzo.tag_bind(refCuadro,"<ButtonPress-3>",self.clickMarcarCuadro) # presionar click derecho
                cuadro = Casilla(self.tablero.pixelesCuadro,0,Punto(x,i),refCuadro)
                self.tablero.cuadros.append(cuadro)
        
        self.tablero.repartirMinas()
        self.__numerarCasillas()
        
    def eventoClick(self,evento):
        # Se ejecuta en cada click sobre un cuadro
        refLienzo = evento.widget.find_withtag('current')[0]
        if any(x.refCanvas == refLienzo for x in self.tablero.cuadros):
                
            cuadro_a_voltear = self.obtenerCuadro(refLienzo)
    
            if not cuadro_a_voltear.tieneMina():
                self.__voltear_adyacentes(cuadro_a_voltear)
                self.tablero.voltear_cuadro(cuadro_a_voltear)
            else:
                print("Tiene mina")  
                self.DERROTA = True

            self.cambiosRecientes = True   
            [self.lienzo.tag_unbind(cuadro.refCanvas,"<ButtonPress-1>") for cuadro in self.tablero.cuadros if cuadro.BOCA_ARRIBA]
            [self.lienzo.tag_unbind(cuadro.refCanvas,"<ButtonPress-3>") for cuadro in self.tablero.cuadros if cuadro.BOCA_ARRIBA]

    def clickMarcarCuadro(self,evento):
        refLienzo = evento.widget.find_withtag('current')[0]
        
        if any(x.refCanvas == refLienzo for x in self.tablero.cuadros):
            cuadro = self.obtenerCuadro(refLienzo)
    
            if cuadro.MARCADO and not cuadro.BOCA_ARRIBA and not cuadro.tieneMina():
                cuadro.desmarcar()
            else:
                cuadro.marcar()  
            
            self.cambiosRecientes = True

            c = self.tablero.totalMinas
            print("  Minas:",str(c))
          
            for i in self.tablero.cuadrosMinas:
                    if i.MARCADO:
                        c -= 1
                    else:
                        pass
               
            print("Minas restantes: ",str(c))
            if c == 0:
                self.VICTORIA = True

    def obtenerCuadro(self,reflienzo):
        if any(x.refCanvas == reflienzo for x in self.tablero.cuadros):
            for i in range(len(self.tablero.cuadros)):
                if self.tablero.cuadros[i].refCanvas == reflienzo:
                    return self.tablero.cuadros[i]
    
    def obtenerCuadroPorCoordenada(self,coordPoint:Punto) -> Casilla:
        if type(coordPoint) == Punto:
         
            for c in self.tablero.cuadros:
                if c.position.x == coordPoint.x and c.position.y == coordPoint.y:        
                    return c 

    def __voltear_adyacentes(self,celdaInicial):
        adyacentes = self.tablero.adyacente(celdaInicial.position.x,celdaInicial.position.y,self.tablero.ancho,self.tablero.alto)
        adyacentes = [x for x in adyacentes]

        while len(adyacentes) > 0:
            for cuadro in adyacentes :
                celda = self.obtenerCuadroPorCoordenada(Punto(cuadro[0],cuadro[1]))
                if celda.BOCA_ARRIBA == False:
                    if celda.content == celdaInicial.content and not celda.tieneMina():
                        if celda != celdaInicial:
                         
                            if celda.MARCADO: # cuadro marcado sin minas a voltear se desmarca
                                celda.desmarcar()
                            
                            self.tablero.voltear_cuadro(celda)
                        adyacentes.remove(cuadro)
                    
                        aux = self.tablero.adyacente(celda.position.x,celda.position.y,self.tablero.ancho,self.tablero.alto)
                        for i in aux:
                            adyacentes.append(i)
                    else:
                        adyacentes.remove(cuadro)
                else:
                    adyacentes.remove(cuadro)  
    
    def __numerarCasillas(self):
      
        for i in self.tablero.cuadrosMinas:
            adyacentes = self.tablero.adyacente(i.position.x,i.position.y,self.tablero.ancho,self.tablero.alto)
            for a in adyacentes:
                celda = self.obtenerCuadroPorCoordenada(Punto(a[0],a[1]))
                if not celda.tieneMina():
                    celda.content += 1
                    
        del adyacentes       

    def actualizar(self):
        
        if self.DERROTA:
           print("Perdiste")
        
        elif self.VICTORIA:
            print("Ganaste")

        if self.DERROTA or self.VICTORIA:
            self.tablero.voltear_minas() 
            if not self.cambiosRecientes:
                exit() # Salir del juego
        
    def dibujar(self):
        medioCuadro = int(self.tablero.pixelesCuadro / 2)
        mina = "#141212"
        color_nmro = "#bbb4b4"
        margen_marcado = 10
        relleno = "#bbb4b4"
        color_set_numbers = ["#c8c7c7","#6ea1ad","#167b94","#ac2f2f"]
        
        if self.cambiosRecientes: #Por rendimiento
            for cuadro in self.tablero.cuadros:
                
                if cuadro.MARCADO and not cuadro.BOCA_ARRIBA and cuadro.refMarcado == None:
                    startX = cuadro.position.x * self.tablero.pixelesCuadro + 1 # inicio del cuadrado X 
                    endX = startX + self.tablero.pixelesCuadro - 1
                    startY = cuadro.position.y * self.tablero.pixelesCuadro + 1 
                    endY = startY + self.tablero.pixelesCuadro - 1

                    triangleId = self.lienzo.create_polygon([(startX+margen_marcado,endY-margen_marcado),
                    (int((startX+endX)/2),int((startY+endY)/2) - margen_marcado), #punto medio menos el margen
                    (endX-margen_marcado,endY-margen_marcado)],
                    fill='red')

                    cuadro.refMarcado = triangleId
                   
                elif cuadro.MARCADO and cuadro.refMarcado != None:
                    # Si esta marcado boca abajo y una bandera dibujada
                    pass
                else:
                    if  cuadro.tieneMina() == False and cuadro.refMarcado != None:
                        #print(cuadro.refMarcado)
                        try:
                            self.lienzo.delete(cuadro.refMarcado)
                            cuadro.refMarcado = None
                        except:
                            pass
                
                if cuadro.BOCA_ARRIBA and not cuadro.tieneMina():
                        try:
                            color_nmro = color_set_numbers[cuadro.content]
                        except IndexError:
                            pass

                        if cuadro.content == 0:
                            relleno = color_nmro
                    
                        self.lienzo.create_text(cuadro.position.x * self.tablero.pixelesCuadro + medioCuadro,
                        cuadro.position.y * self.tablero.pixelesCuadro + medioCuadro,
                        text=str(cuadro.content),fill=color_nmro,font="Arial 18 bold")
            
                elif cuadro.tieneMina() and cuadro.BOCA_ARRIBA:
                    relleno = mina

                self.lienzo.itemconfig(cuadro.refCanvas,fill=relleno)
                relleno = "#bbb4b4"
                
            self.cambiosRecientes = False
    
