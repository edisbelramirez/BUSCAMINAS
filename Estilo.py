class Estilo():
    def __init__(self,canvas,frame):
        self.f= frame
        self.c = canvas

        self.f.pack(side="top",anchor='center',fill='both',expand=True )
        self.f.config(bg='black',bd=5,relief="ridge")
    
    def configurar_lienzo(self,bg="black",width=50,height=50):

        self.c.config(width= width,height=height,bg=bg)