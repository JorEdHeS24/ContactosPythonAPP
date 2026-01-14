import tkinter as tk
from tkinter import messagebox, ttk
import re
from tkinter import filedialog
from repository import ContactoRepository
from pydantic import BaseModel
from dataEntry import baseContact 
from typing import List, Dict, Optional, Any 

class AgendaContactos:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Agenda de Contactos")
        self.root.geometry("660x920")
        self.root.minsize(660, 920)
        self.root.resizable(True, True)
        
        # Configurar el tema y colores.
        self.configurar_estilos()
        
        # Lista para almacenar los contactos (cada contacto es un diccionario).
        self.contactos: List[Dict[str, Any]] = []
        self.contacts: Optional[Any] = None
        self.selected_contact_id: Optional[int] = None
        
        # Crear los elementos de la interfaz.
        self.crear_interfaz()
    
    def configurar_estilos(self) -> None:
        
        # Configurar estilos globales.
        style = ttk.Style()
        
        # Configurar tema.
        style.theme_use('clam')
        
        # Colores principales.
        self.color_fondo = '#ffffff'  # Blanco
        self.color_principal = '#1e88e5'  # Azul principal
        self.color_secundario = '#42a5f5'  # Azul claro
        self.color_acento = '#0d47a1'  # Azul oscuro
        self.color_texto = '#212121'  # Casi negro
        self.color_hover = '#1565c0'  # Azul para hover
        self.color_active = '#64b5f6'  # Azul más claro para active
        
        # Configurar estilos para diferentes widgets.
        style.configure('TFrame', background=self.color_fondo)
        style.configure('TLabel', background=self.color_fondo, foreground=self.color_texto, font=('Segoe UI', 10))
        
        # Estilos de botones con estados.
        style.configure('TButton', 
                       background=self.color_principal, 
                       foreground='white', 
                       font=('Segoe UI', 10),
                       padding=5)
        style.map('TButton',
                 background=[('active', self.color_active),
                           ('hover', self.color_acento)],
                 foreground=[('active', 'white'),
                           ('hover', 'white')])
        
        style.configure('TEntry', 
                       fieldbackground='white', 
                       foreground=self.color_texto, 
                       font=('Segoe UI', 10),
                       borderwidth=1)
        style.configure('TLabelframe', 
                       background=self.color_fondo, 
                       foreground=self.color_principal, 
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=2)
        style.configure('TLabelframe.Label', 
                       background=self.color_fondo, 
                       foreground=self.color_principal, 
                       font=('Segoe UI', 10, 'bold'))
        style.configure('Treeview', 
                       background='white', 
                       foreground=self.color_texto, 
                       fieldbackground='white', 
                       font=('Segoe UI', 10),
                       rowheight=25)
        style.configure('Treeview.Heading', 
                       background=self.color_principal, 
                       foreground='white', 
                       font=('Segoe UI', 10, 'bold'))
        style.map('Treeview.Heading',
                 background=[('active', self.color_hover)])
        
        # Configurar el fondo de la ventana principal.
        self.root.configure(bg=self.color_fondo)
    
    def crear_interfaz(self) -> None:
        
        # Frame principal.
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sección de ingreso de contactos.
        input_frame = ttk.LabelFrame(main_frame, text="Ingreso de Contactos", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        # Campos de entrada.
        ttk.Label(input_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.nombre_entry = ttk.Entry(input_frame, width=30)
        self.nombre_entry.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(input_frame, text="Teléfono:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.telefono_entry = ttk.Entry(input_frame, width=30)
        self.telefono_entry.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(input_frame, text="Email (opcional):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.email_entry = ttk.Entry(input_frame, width=30)
        self.email_entry.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Botón para agregar contacto.
        ttk.Button(input_frame, text="Agregar Contacto", command=self.agregar_contacto).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Después del botón "Agregar Contacto"
        ttk.Button(input_frame, text="Actualizar Contacto", command=self.actualizar_contacto).grid(row=4, column=0, pady=5)
        ttk.Button(input_frame, text="Eliminar Contacto", command=self.eliminar_contacto).grid(row=4, column=1, pady=5)
        
        # Frame para operaciones (ordenamiento y búsqueda).
        operations_frame = ttk.LabelFrame(main_frame, text="Operaciones", padding="10")
        operations_frame.pack()
         
        #Subir contactos.
        upload_text_label = ttk.Label(input_frame, text='Subir contactos')
        upload_text_label.grid(row=0, column=2, sticky=tk.W, pady=2, padx=30)
        
        upload_text_button = ttk.Button(input_frame, text='Subir', command=self.subir_contactos)
        upload_text_button.grid(row=1, column=2, sticky=tk.W, pady=2, padx=30)
        
        # Botones de ordenamiento.
        ttk.Button(operations_frame, text="Ordenar por Nombre", command=lambda: self.ordenar_contactos("name")).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(operations_frame, text="Ordenar por Teléfono", command=lambda: self.ordenar_contactos("telephone")).grid(row=0, column=1, padx=5, pady=5)
        
        # Sección de búsqueda.
        search_frame = ttk.Frame(operations_frame)
        search_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky=tk.W)
        
        ttk.Label(search_frame, text="Buscar por Nombre:").pack(side=tk.LEFT, padx=2)
        self.busqueda_entry = ttk.Entry(search_frame, width=20)
        self.busqueda_entry.pack(side=tk.LEFT, padx=2)
        ttk.Button(search_frame, text="Buscar", command=self.buscar_contacto).pack(side=tk.LEFT, padx=2)
        
        # Botón para estadísticas.
        ttk.Button(operations_frame, text="Mostrar Estadísticas", command=self.mostrar_estadisticas).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Sección para mostrar resultados de búsqueda.
        self.resultados_frame = ttk.LabelFrame(main_frame, text="Resultados de Búsqueda", padding="10")
        self.resultados_frame.pack(fill=tk.X, pady=5)
        
        self.resultado_texto = tk.StringVar()
        self.resultado_texto.set("Aquí se mostrarán los resultados de la búsqueda")
        ttk.Label(self.resultados_frame, textvariable=self.resultado_texto, wraplength=700).pack(fill=tk.X)
        
        # Sección para mostrar estadísticas.
        self.estadisticas_frame = ttk.LabelFrame(main_frame, text="Estadísticas", padding="10")
        self.estadisticas_frame.pack(fill=tk.X, pady=5)
        
        self.total_contactos_var = tk.StringVar(value="Total de contactos: 0")
        self.contactos_email_var = tk.StringVar(value="Contactos con email: 0")
        self.primer_nombre_var = tk.StringVar(value="Primer nombre alfabéticamente: Ninguno")
        
        ttk.Label(self.estadisticas_frame, textvariable=self.total_contactos_var).pack(anchor=tk.W)
        ttk.Label(self.estadisticas_frame, textvariable=self.contactos_email_var).pack(anchor=tk.W)
        ttk.Label(self.estadisticas_frame, textvariable=self.primer_nombre_var).pack(anchor=tk.W)
        
        # Área para visualización de contactos.
        lista_frame = ttk.LabelFrame(main_frame, text="Lista de Contactos", padding="10")
        lista_frame.pack(fill=tk.BOTH, expand=True, pady=5)        
        
        # Frame para el Treeview y su scrollbar.
        tree_frame = ttk.Frame(lista_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para mostrar los contactos en forma de tabla.
        self.contactos_tree = ttk.Treeview(tree_frame, columns=("Nombre", "Teléfono", "Email"), show="headings", height=10)
        self.contactos_tree.heading("Nombre", text="Nombre")
        self.contactos_tree.heading("Teléfono", text="Teléfono")
        self.contactos_tree.heading("Email", text="Email")
        
        self.contactos_tree.column("Nombre", width=200)
        self.contactos_tree.column("Teléfono", width=150)
        self.contactos_tree.column("Email", width=250)
        
        # Scrollbar para la lista de contactos.
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.contactos_tree.yview)
        self.contactos_tree.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar el Treeview y el Scrollbar.
        self.contactos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.contactos_tree.bind('<<TreeviewSelect>>', self.on_contacto_select)
    
    # def validar_formato(self, contact : baseContact):
        
        # # Validaciones básicas.
        # if not nombre:
        #     messagebox.showerror("Error", "El nombre es obligatorio")
        #     return
        
        # if not telefono:
        #     messagebox.showerror("Error", "El teléfono es obligatorio")
        #     return
        
        # # Validar formato de teléfono (solo números).
        # if not re.match(r'^\d+$', telefono):
        #     messagebox.showerror("Error", "El teléfono debe contener solo números")
        #     return
        
        # # Validar formato de email si está presente.
        # if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        #     messagebox.showerror("Error", "Formato de email inválido")
        #     return
    
    def agregar_contacto(self) -> None:
                        
        try: 
            name = self.nombre_entry.get().strip()
            telephone = self.telefono_entry.get().strip()
            email = self.email_entry.get().strip()
            
            contacto = baseContact(
                name=name,
                telephone=telephone,
                email=email if email else None            
            )
        
            ContactoRepository.guardar(contacto.name, contacto.telephone, contacto.email)
            messagebox.showinfo("Éxito", "Contacto guardado")
        
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", "Error al guardar contacto")
                

        self.actualizar_lista_contactos()
        
        # Limpiar campos.
        self.nombre_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        
        # Actualizar estadísticas.
        self.actualizar_estadisticas()
        
        messagebox.showinfo("Éxito", f"Contacto {name} agregado correctamente")
    
    def actualizar_lista_contactos(self) -> None:
        
        # Limpiar lista actual.
        for item in self.contactos_tree.get_children():
            self.contactos_tree.delete(item)
        
        self.contactos = ContactoRepository.obtener_todos()
        # print(contactos)
        
        # Insertar todos los contactos.
        for contacto in self.contactos:
            self.contactos_tree.insert("", tk.END, values=(
                contacto["name"],
                contacto["telephone"],
                contacto["email"]
            ))
    
    def ordenar_contactos(self, criterio: str) -> None:
        
        # Algoritmo de ordenamiento: Merge Sort.
        if not self.contactos:
            messagebox.showinfo("Información", "No hay contactos para ordenar")
            return
        
        self.contactos = self.merge_sort(self.contactos, criterio)
        self.actualizar_lista_contactos()
        messagebox.showinfo("Éxito", f"Contactos ordenados por {criterio}")
    
    def merge_sort(self, arr: List[Dict[str, Any]], criterio: str) -> List[Dict[str, Any]]:
        
        # Implementación del algoritmo Merge Sort.
        if len(arr) <= 1:
            return arr
        
        # Dividir la lista en dos mitades.
        medio = len(arr) // 2
        izquierda = self.merge_sort(arr[:medio], criterio)
        derecha = self.merge_sort(arr[medio:], criterio)
        
        # Combinar las mitades ordenadas.
        return self.merge(izquierda, derecha, criterio)
    
    def merge(self, izquierda: List[Dict[str, Any]], derecha: List[Dict[str, Any]], criterio: str) -> List[Dict[str, Any]]:
        resultado = []
        i = j = 0
        
        while i < len(izquierda) and j < len(derecha):
            
            # Comparación según el criterio elegido.
            if criterio == "name" and izquierda[i]["name"].lower() <= derecha[j]["name"].lower():
                resultado.append(izquierda[i])
                i += 1
            elif criterio == "telephone" and izquierda[i]["telephone"] <= derecha[j]["telephone"]:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1
        
        # Agregar los elementos restantes.
        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])
        
        return resultado
    
    def buscar_contacto(self) -> None:
        texto_busqueda = self.busqueda_entry.get().strip().lower()
        
        if not texto_busqueda:
            messagebox.showerror("Error", "Ingrese un nombre para buscar")
            return
        
        # Algoritmo de búsqueda: Búsqueda Lineal para encontrar coincidencias parciales.
        encontrado = False
        resultados = []
        
        for contacto in self.contactos:
            if texto_busqueda in contacto["name"].lower():
                resultados.append(contacto)
                encontrado = True
        
        if encontrado:
            # Mostrar el primer contacto encontrado.
            primer_resultado = resultados[0]
            self.resultado_texto.set(
                f"Contacto encontrado:\nNombre: {primer_resultado['name']}\n"
                f"Teléfono: {primer_resultado['telephone']}\n"
                f"Email: {primer_resultado['email'] if primer_resultado['email'] else 'No especificado'}"
            )
        else:
            self.resultado_texto.set("No se encontraron contactos con ese nombre")
    
    def encontrar_primer_nombre_recursivo(self, contactos: List[Dict[str, Any]], indice: int = 0, primer_nombre: Optional[str] = None) -> Optional[str]:
        
        # Método recursivo para encontrar el primer nombre alfabéticamente.
        if not contactos:
            return None
        
        # Caso base: llegamos al final de la lista.
        if indice >= len(contactos):
            return primer_nombre
        
        nombre_actual = contactos[indice]["name"].lower()
        
        # Si es el primer contacto o es alfabéticamente anterior al actual primer nombre.
        if primer_nombre is None or nombre_actual < primer_nombre.lower():
            primer_nombre = contactos[indice]["name"]
        
        # Llamada recursiva con el siguiente índice.
        return self.encontrar_primer_nombre_recursivo(contactos, indice + 1, primer_nombre)
    
    def contar_contactos_con_email(self) -> int:
        return sum(1 for contacto in self.contactos if contacto["email"])
    
    def mostrar_estadisticas(self) -> None:
        total_contactos = len(self.contactos)
        contactos_con_email = self.contar_contactos_con_email()
        
        # Encontrar el primer nombre alfabéticamente (recursivamente).
        primer_nombre = self.encontrar_primer_nombre_recursivo(self.contactos) if self.contactos else "Ninguno"
        
        # Actualizar variables de estadísticas
        self.total_contactos_var.set(f"Total de contactos: {total_contactos}")
        self.contactos_email_var.set(f"Contactos con email: {contactos_con_email}")
        self.primer_nombre_var.set(f"Primer nombre alfabéticamente: {primer_nombre}")
        
        messagebox.showinfo("Estadísticas", "Estadísticas actualizadas")
    
    def actualizar_estadisticas(self) -> None:
        # Actualiza las estadísticas sin mostrar mensaje.
        total_contactos = len(self.contactos)
        contactos_con_email = self.contar_contactos_con_email()
        primer_nombre = self.encontrar_primer_nombre_recursivo(self.contactos) if self.contactos else "Ninguno"
        
        self.total_contactos_var.set(f"Total de contactos: {total_contactos}")
        self.contactos_email_var.set(f"Contactos con email: {contactos_con_email}")
        self.primer_nombre_var.set(f"Primer nombre alfabéticamente: {primer_nombre}")
    
    def subir_contactos(self) -> None:
        item = ""
        lista_contactos = []
    
        # Abre el explorador de archivos.
        ruta = filedialog.askopenfilename(
            title="Selecciona un archivo de texto",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
    
        if ruta:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read().replace("\n", ",")
                               
            # print(type(contenido))
            # print(f"Contenido: {contenido}")
                                               
            for i in contenido:
                if i != ",":
                    item += i
                if i == ",":
                    lista_contactos.append(item)
                    item = ""
        
            idx = 0
            contacto = {"name": "", "telephone": "", "email": ""}
            contactos_a_guardar = []
        
            for j in lista_contactos:
                if idx == 0:
                    contacto["name"] = j.strip()
                elif idx == 1:
                    contacto["telephone"] = j.strip()
                elif idx == 2:
                    contacto["email"] = j.strip()
                
                    # Verificar duplicados: comparar con BD actual
                    existe = any(
                        c["name"].lower() == contacto["name"].lower() and
                        c["telephone"] == contacto["telephone"]
                        for c in self.contactos
                    )
                
                    if not existe:
                        contactos_a_guardar.append(contacto.copy())
                
                    idx = -1
                idx += 1
        
        # Guardar solo los contactos nuevos
        for contacto in contactos_a_guardar:
            ContactoRepository.guardar(
                contacto["name"],
                contacto["telephone"],
                contacto["email"]
            )
        
        messagebox.showinfo("Éxito", f"Se importaron {len(contactos_a_guardar)} contactos nuevos")
        self.actualizar_lista_contactos()
    
    def on_contacto_select(self, event) -> None:
        selected_items = self.contactos_tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.contactos_tree.item(item, 'values')
            for c in self.contactos:
                if c['name'] == values[0] and c['telephone'] == values[1]:
                    self.selected_contact_id = c['id']
                    self.nombre_entry.delete(0, tk.END)
                    self.nombre_entry.insert(0, c['name'])
                    self.telefono_entry.delete(0, tk.END)
                    self.telefono_entry.insert(0, c['telephone'])
                    self.email_entry.delete(0, tk.END)
                    if c['email']:
                        self.email_entry.insert(0, c['email'])
                    break

    def actualizar_contacto(self) -> None:
        if not self.selected_contact_id:
            messagebox.showerror("Error", "Selecciona un contacto para actualizar")
            return
        try:
            name : str = self.nombre_entry.get().strip()
            telephone : str = self.telefono_entry.get().strip()
            email = self.email_entry.get().strip()
            contacto = baseContact(
                name=name,
                telephone=telephone,
                email=email if email else None            
            )
            ContactoRepository.actualizar(self.selected_contact_id, contacto.name, contacto.telephone, contacto.email)
            messagebox.showinfo("Éxito", "Contacto actualizado")
            self.selected_contact_id = None
            self.actualizar_lista_contactos()
            self.actualizar_estadisticas()
            self.nombre_entry.delete(0, tk.END)
            self.telefono_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", "Error al actualizar contacto")

    def eliminar_contacto(self) -> None:
        if not self.selected_contact_id:
            messagebox.showerror("Error", "Selecciona un contacto para eliminar")
            return
        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este contacto?"):
            try:
                ContactoRepository.eliminar(self.selected_contact_id)
                messagebox.showinfo("Éxito", "Contacto eliminado")
                self.selected_contact_id = None
                self.actualizar_lista_contactos()
                self.actualizar_estadisticas()
                self.nombre_entry.delete(0, tk.END)
                self.telefono_entry.delete(0, tk.END)
                self.email_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", "Error al eliminar contacto")

