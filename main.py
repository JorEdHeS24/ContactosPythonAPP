from gui.App import AgendaContactos
from database import init_db
import tkinter as tk

if __name__ == "__main__":
    init_db()
    root = tk.Tk()    
    app = AgendaContactos(root)
    app.actualizar_lista_contactos()
    root.mainloop()