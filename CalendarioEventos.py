from tkinter import* 
from tkinter import messagebox
from tkcalendar import Calendar

# Ventana principal
ventana = Tk()
ventana.title("Agenda de eventos")
ventana.geometry("600x850")

marco = Frame(ventana)
marco.pack(expand=True)

# Titulo
titulo = Label(marco, text="AGENDA DE EVENTOS", font=(22))
titulo.grid(row=0, column=0, pady=15)

# Calendario
calendario = Calendar(marco, selectmode="day", year=2026, month=10, day=13, locale="es", date_pattern="dd/mm/yyyy")
calendario.grid(row=1, column=0, pady=10)

# Campo para escribir el evento
texto = Label(marco, text="Nombre del evento:")
texto.grid(row=2, column=0, pady=5)

entrada_evento = Entry(marco, width=40)
entrada_evento.grid(row=3, column=0, pady=10)

#Boton para agregar
boton1 = Button(marco, text="Agregar evento")
boton1.grid(row=4, column=0, pady=10)


# Lista donde aparecerán los eventos
text_evento= Label(marco, text="Mis eventos:")
text_evento.grid(row=5, column=0, pady=8)
lista_eventos = Listbox(marco, width=70, height=15)
lista_eventos.grid(row=6, column=0, pady=5)


# Guardar los eventos, cada fecha tiene una lista de eventos
eventos={}

#agregar un evento
def agregar_evento():
    fecha = calendario.get_date()
    nombre = entrada_evento.get().strip()

    if not nombre:
        messagebox.showwarning( "Aviso", "Escribe el nombre del evento.")
        return

    if fecha not in eventos:
        eventos[fecha] = []
    eventos[fecha].append(nombre)
    actualizar_lista()

    entrada_evento.delete(0, END)
    messagebox.showinfo( "Evento agregado", f"Evento guardado para el {fecha}.")

#actualizar la lista segun la fecha seleccionada
def actualizar_lista():
    lista_eventos.delete(0, END)

    fecha = calendario.get_date()

    if fecha in eventos and eventos[fecha]:
        for evento in eventos[fecha]:
            lista_eventos.insert(END, evento)
    else:
        lista_eventos.insert(END, "No hay eventos para esta fecha.")


#eliminar el evento
def eliminar_evento():
    seleccion = lista_eventos.curselection()

    if not seleccion:
        messagebox.showwarning( "Aviso", "Seleccioná un evento para eliminar.")
        return

    fecha = calendario.get_date()
    posicion = seleccion[0]

    # Verificar que haya eventos para esa fecha
    if fecha not in eventos or not eventos[fecha]:
        messagebox.showwarning( "Aviso", "No hay eventos para eliminar.")
        return    

        # Evitar eliminar el mensaje informativo
    if posicion >= len(eventos[fecha]):
        return

    nombre = eventos[fecha][posicion]

    confirmar = messagebox.askyesno( "Confirmar eliminación", f"¿Quieres eliminar el evento '{nombre}'?")
    if confirmar:
        eventos[fecha].pop(posicion)

        # Eliminar la fecha si ya no tiene eventos
        if not eventos[fecha]:
            del eventos[fecha]

        actualizar_lista()

        messagebox.showinfo("Evento eliminado","El evento se eliminó correctamente.")

# Boton para eliminar
boton2 = Button( marco, text="Eliminar evento",command= eliminar_evento)
boton2.grid(row=7, column=0, pady=10)

boton1.config(command=agregar_evento)

#Actualizar la lista al seleccionar otra fecha
def al_seleccionar_fecha(evento):
    actualizar_lista()
    
calendario.bind("<<CalendarSelected>>",  al_seleccionar_fecha)

# Mostrar los eventos iniciales
actualizar_lista()

ventana.mainloop ()