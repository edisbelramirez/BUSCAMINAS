from tkinter import Tk, Canvas, Frame
import tkinter

a = Tk()
a.config()

f = Frame()


c= Canvas(f)
c.pack()
c.config(bg="blue",width=560,height=600,bd=5,relief='flat')

f.pack(side="top",anchor='center',fill='both',expand=True )
f.config(bg='black',bd=5,relief="ridge")

a.mainloop()
