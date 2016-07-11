#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import os
import sys
import sqlite3

from RegistroJuego import RegistroJuego

class Catalogo_GUI:
    builder = None
    registroJuego = None
    entryTitulo = None
    entryGenero = None
    entryPlataforma = None
    entryLanzamiento = None
    dialogAviso = None
    botonAccion = None
    ventanaBuscar = None
    botonCerrarVentanaBuscar = None
    criterioBuscar = None
    radioId = None
    radioTitulo = None
    radioGenero = None
    radioLanzamiento = None
    radioPlataforma = None
    entryBuscar = None
    store = None
    treeView = None
    scrollBar = None
    filaSeleccionada = None

    def __init__(self):
        self.registroJuego = RegistroJuego()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("catalogoVideojuegos.glade")
        self.handlers = {"onDeleteWindow": self.onDeleteWindow,
                            "onCrearActivate": self.onCrearActivate,
                            "onBuscarActivate": self.onBuscarActivate,
                            "onBorrarActivate": self.onBorrarActivate,
                            "onEditarActivate": self.onEditarActivate,
                            "onAboutActivate": self.onAboutActivate,
                            "onCloseAbout": self.onCloseAbout,
                            "onBotonCerrarVentanaBuscarClicked": self.onBotonCerrarVentanaBuscarClicked,
                            "onBotonAccionVentanaBuscarClicked": self.onBotonAccionVentanaBuscarClicked,
                            "onBotonDialogCamposVaciosClicked": self.onBotonDialogCamposVaciosClicked,
                            "onBotonAccionClicked": self.onBotonAccionClicked,
                            "onBotonAsignarImagenClicked": self.onBotonAsignarImagenClicked,
                            "onFilaChanged": self.onFilaChanged,}

        self.builder.connect_signals(self.handlers)

        #Inicializacion widgets y valores por defecto
        self.entryTitulo = self.builder.get_object("entryTituloDetalles")
        self.entryGenero = self.builder.get_object("entryGeneroDetalles")
        self.entryPlataforma = self.builder.get_object("entryPlataformaDetalles")
        self.entryLanzamiento = self.builder.get_object("entryLanzamientoDetalles")
        self.registroJuego.setCaratula("resources/seleccionar_imagen.jpg")
        self.dialogAviso = self.builder.get_object("dialogCamposVacios")
        self.botonAccion = self.builder.get_object("botonAccion")
        self.botonAccion.set_sensitive(True)
        self.ventanaBuscar = self.builder.get_object("ventanaBuscar")
        self.botonCerrarVentanaBuscar = self.builder.get_object("botonCerrarVentanaBuscar")
        self.radioId = self.builder.get_object("radioId")
        self.radioId.connect("toggled",self.onRadioActivado)
        self.radioTitulo = self.builder.get_object("radioTitulo")
        self.radioTitulo.connect("toggled",self.onRadioActivado)
        self.radioGenero = self.builder.get_object("radioGenero")
        self.radioGenero.connect("toggled",self.onRadioActivado)
        self.radioPlataforma = self.builder.get_object("radioPlataforma")
        self.radioPlataforma.connect("toggled",self.onRadioActivado)
        self.radioLanzamiento = self.builder.get_object("radioLanzamiento")
        self.radioLanzamiento.connect("toggled",self.onRadioActivado)
        self.entryBuscar = self.builder.get_object("entryBuscar")
        self.criterioBuscar = self.radioId.get_label()
        self.store =  self.builder.get_object("liststore1")
        self.treeView = self.builder.get_object("treeview2")
        self.filaSeleccionada = self.builder.get_object("filaSeleccionada")
        #Consultamos numero de tablas que hay en la base de datos
        conexion = sqlite3.connect("juegos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name;")
        tablas = map(lambda t: t[0], cursor.fetchall())
        print "Numero de tablas en la base de Datos:" + str(len(tablas))

        #Si no hay tablas la creamos
        if len(tablas) == 0:
            cursor.execute("CREATE TABLE Juegos (id, Titulo, Genero, Plataforma, Lanzamiento, Caratula);")

        # Extraemos todos los registros de la tabla
        cursor.execute("SELECT * FROM Juegos;")

        # Rellenamos la estructura de la tabla con el resultado de la consulta
        contador = 0
        for fila in cursor:
            self.store.append([fila[0], fila[1], fila[2], fila[3], fila[4], fila[5]])
            # Actualiza datos con la fila seleccionada por defecto
            if contador == 0:
                #Actualizamos valores de registro seleccionado
                self.registroJuego.setId(fila[0])
                self.entryTitulo.set_text(fila[1])
                self.registroJuego.setTitulo(fila[1])
                self.entryGenero.set_text(fila[2])
                self.registroJuego.setGenero(fila[2])
                self.entryPlataforma.set_text(fila[3])
                self.registroJuego.setPlataforma(fila[3])
                self.entryLanzamiento.set_text(fila[4])
                self.registroJuego.setLanzamiento(fila[4])
                self.registroJuego.setCaratula(fila[5])
                botonAsignarImagen = self.builder.get_object("botonAsignarImagen")
                img = self.builder.get_object("imageDetallesCaratula")
                img.set_from_file(self.registroJuego.getCaratula())
                img.show()

            contador += 1

        if contador == 0:
            self.limpiarDetalles()

        # Insertamos Columnas
        for i,tituloColumnas in enumerate(["id", "Título", "Género", "Plataforma", "Lanzamiento", "Carátula" ]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(tituloColumnas, renderer, text=i)
            self.treeView.append_column(column)

        self.scrollBar = self.builder.get_object("scrollBar")
        self.scrollBar.set_vexpand(True)

        #Cerramos cursor
        cursor.close()
        #Cerramos conexión
        conexion.close()

        self.window = self.builder.get_object("ventanaPrincipal")
        self.window.show_all()

    def borrarTabla(self):
        # Limpiamos la Tabla
        self.store.clear()

    def limpiarDetalles(self):
        etiquetaBoton = self.botonAccion.get_label()
        if etiquetaBoton == "Editar juego" or etiquetaBoton == "Borrar juego":
            self.botonAccion.set_sensitive(False)
        self.entryTitulo.set_text("")
        self.entryGenero.set_text("")
        self.entryPlataforma.set_text("")
        self.entryLanzamiento.set_text("")
        botonAsignarImagen = self.builder.get_object("botonAsignarImagen")
        img = self.builder.get_object("imageDetallesCaratula")
        img.set_from_file("resources/seleccionar_imagen.jpg")
        img.show()
    """
    	Función que comprueba si una cadena es Nula o Vacía
    	-Parámetros:
    		cadena -- cadena de caractéres

    	-Devuelve:
    		True -- si detecta cadena vacía o nula
    		False -- si la cadena no está vacía o no es nula
    """
    def cadenaVacia(self, cadena):

    	if cadena is None:
    		return True

    	if cadena is "":
    		return True

    	return False

    """
    	Función que comprueba si alguno de los campos de un registro es Nulo o Vacío
    	-Parámetros:
    		registro -- objeto de tipo RegistroJuego

    	-Devuelve:
    		True -- si detecta alguno de los campos vacío o nulo
    		False -- si no detecta campos vacíos o nulos
    """
    def camposVacios(self, registro):
    	campoVacio = False

    	# Comprobamos que el campo no está vacíó
    	campoVacio = self.cadenaVacia(registro.getTitulo())

    	if not campoVacio:
    		campoVacio = self.cadenaVacia(registro.getGenero())

    	if not campoVacio:
    		campoVacio = self.cadenaVacia(registro.getPlataforma())

    	if not campoVacio:
    		campoVacio = self.cadenaVacia(registro.getLanzamiento())

    	if not campoVacio:
    		campoVacio = self.cadenaVacia(registro.getCaratula())

    	return campoVacio

    # Acción al seleccionar una fila de la tabla
    def onFilaChanged(self,button):
        seleccion = self.treeView.get_selection()
        self.store, paths = seleccion.get_selected_rows()
        # Desde glade se ha definido que solos e puede selecccionar una fila con el cursor
        # Por lo que este bucle solo iterará una vez
        # Actualiza Detalles de la selección
        for path in paths:
            iterador = self.store.get_iter(path)
            txt = self.store.get_value(iterador,0)
            self.registroJuego.setId(txt)
            txt = self.store.get_value(iterador,1)
            self.entryTitulo.set_text(txt)
            txt = self.store.get_value(iterador,2)
            self.entryGenero.set_text(txt)
            txt = self.store.get_value(iterador,3)
            self.entryPlataforma.set_text(txt)
            txt = self.store.get_value(iterador,4)
            self.entryLanzamiento.set_text(txt)
            txt = self.store.get_value(iterador,5)
            botonAsignarImagen = self.builder.get_object("botonAsignarImagen")
            img = self.builder.get_object("imageDetallesCaratula")
            img.set_from_file(txt)
            self.registroJuego.setCaratula(txt)
            img.show()
        # Botóm Acción solo está activo si se ha seleccionado una fila
        self.botonAccion.set_sensitive(True)

    # Acción de submenu Crear
    def onCrearActivate(self, submenuCatalogoCrear):
        self.botonAccion.set_label("Añadir juego")

    # Acción de submenu buscar
    def onBuscarActivate(self, submenuCatalogoBuscar):
        self.ventanaBuscar.show_all()

    # Acción de submenu Editar
    def onEditarActivate(self, submenuCatalogoEditar):
        self.botonAccion.set_label("Editar juego")

    # Acción de submenu Borrar
    def onBorrarActivate(self, submenuCatalogoBorrar):
        self.botonAccion.set_label("Borrar juego")

    def onAboutActivate(self, submenuAyudaAbout):
		self.about = self.builder.get_object("dialogAbout")
		self.about.show_all()

    def onCloseAbout(self, *args):
        self.about = self.builder.get_object("dialogAbout")
        self.about.hide()

    def onBotonDialogCamposVaciosClicked(self, button):
        self.dialogAviso.hide()

    def onRadioActivado(self, button):
        if button.get_active():
            #Definimos criterio de búsqueda
            self.criterioBuscar = button.get_label()

    def onBotonAccionVentanaBuscarClicked(self, button):
        buscar = self.entryBuscar.get_text()

        if not self.cadenaVacia(buscar):
            conexion = sqlite3.connect("juegos.db")
            cursor = conexion.cursor()
            #Definimos consulta según criterio seleccionado
            if self.criterioBuscar == "id":
                cursor.execute("SELECT * FROM Juegos WHERE id = ?;", (int(buscar),))

            if self.criterioBuscar == "Título":
                cursor.execute("SELECT * FROM Juegos WHERE Titulo = ?;",(buscar,))

            if self.criterioBuscar == "Género":
                cursor.execute("SELECT * FROM Juegos WHERE Genero = ?;",(buscar,))

            if self.criterioBuscar == "Plataforma":
                cursor.execute("SELECT * FROM Juegos WHERE Plataforma = ?;",(buscar,))

            if self.criterioBuscar == "Lanzamiento":
                cursor.execute("SELECT * FROM Juegos WHERE Lanzamiento = ?;",(buscar,))

            # Borramos valores antíguos
            self.borrarTabla()

            # Rellenamos la estructura de la tabla con el resultado de la consulta
            contador = 0
            for fila in cursor:
                self.store.append([fila[0], fila[1], fila[2], fila[3], fila[4], fila[5]])
                # Actualiza datos con la fila seleccionada por defecto
                if contador == 0:
                    #Actualizamos valores de registro seleccionado
                    self.registroJuego.setId(fila[0])
                    self.entryTitulo.set_text(fila[1])
                    self.registroJuego.setTitulo(fila[1])
                    self.entryGenero.set_text(fila[2])
                    self.registroJuego.setGenero(fila[2])
                    self.entryPlataforma.set_text(fila[3])
                    self.registroJuego.setPlataforma(fila[3])
                    self.entryLanzamiento.set_text(fila[4])
                    self.registroJuego.setLanzamiento(fila[4])
                    self.registroJuego.setCaratula(fila[5])
                    botonAsignarImagen = self.builder.get_object("botonAsignarImagen")
                    img = self.builder.get_object("imageDetallesCaratula")
                    img.set_from_file(self.registroJuego.getCaratula())
                    img.show()

                contador += 1

            if contador == 0:
                self.limpiarDetalles()

            #Cerramos cursor
        	cursor.close()
        	#Cerramos conexión
        	conexion.close()
            #Cerramos ventana
            self.ventanaBuscar.hide()
        else:
            self.dialogAviso.show_all()

    def onBotonCerrarVentanaBuscarClicked(self, button):
        self.ventanaBuscar.hide()

    def onBotonAsignarImagenClicked(self, button):
        dialog = Gtk.FileChooserDialog("Elige fichero", None,
                 Gtk.FileChooserAction.OPEN,
                 (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            botonAsignarImagen = self.builder.get_object("botonAsignarImagen")
            img = self.builder.get_object("imageDetallesCaratula")
            #Trunca la ruta del fichero hasta el directorio local de la app
            img.set_from_file("resources/" + os.path.basename(dialog.get_filename()))
            self.registroJuego.setCaratula("resources/" + os.path.basename(dialog.get_filename()))
            #Asignar a bd datos
            img.show()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

        dialog.destroy()

    def onDeleteWindow(self):
        Gtk.main_quit

    def add_filters(self, dialog):
        #Definimos el filtro para ficheros de tipo imágen
        filter_img = Gtk.FileFilter()
        filter_img.set_name("Imágenes")
        filter_img.add_mime_type("image/png")
        filter_img.add_mime_type("image/jpeg")
        filter_img.add_mime_type("image/gif")
        filter_img.add_pattern("*.png")
        filter_img.add_pattern("*.jpg")
        filter_img.add_pattern("*.gif")
        filter_img.add_pattern("*.tif")
        dialog.add_filter(filter_img)

    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Elige carpeta", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select pulsado")
            print("Carpeta seleccionada: " + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancelar pulsado")
            dialog.destroy()

        dialog.destroy()

    def onBotonAccionClicked(self, button):

        etiquetaBoton = button.get_label()
        # Crear Juego
        if etiquetaBoton == "Añadir juego":
            # Actualizamos datos de Detalles
            self.registroJuego.setTitulo(self.entryTitulo.get_text())
            self.registroJuego.setGenero(self.entryGenero.get_text())
            self.registroJuego.setPlataforma(self.entryPlataforma.get_text())
            self.registroJuego.setLanzamiento(self.entryLanzamiento.get_text())

            #Si no hay campos vacíós realizamos inserción
            if not self.camposVacios(self.registroJuego):

                conexion = sqlite3.connect("juegos.db")
                cursor = conexion.cursor()
            	#Consultamos los datos para extraer último id de la tabla Victimas
            	cursor.execute("SELECT * FROM Juegos;")

            	#Extraemos longitud de la lista del cursor que coincide con el último id introducido en la tabla
            	ultimoId = len(cursor.fetchall())
                ultimoId += 1
                # Realizamos insercion de nuevo registro
                cursor.execute("INSERT INTO Juegos VALUES (?,?,?,?,?,?);",(ultimoId, self.registroJuego.getTitulo(), self.registroJuego.getGenero(), self.registroJuego.getPlataforma(), self.registroJuego.getLanzamiento(), self.registroJuego.getCaratula()))
                # Hacemos commit
                conexion.commit()

                #Consultamos para actualizar nuevos valores
                cursor.execute("SELECT * FROM Juegos;")

                # Borramos valores antíguos
                self.borrarTabla()

                # Rellenamos la estructura de la tabla con el resultado de la consulta
                contador = 0
                for fila in cursor:
                    self.store.append([fila[0], fila[1], fila[2], fila[3], fila[4], fila[5]])
                    # Actualiza datos con la fila seleccionada por defecto
                    if contador == 0:
                        #Actualizamos valores de registro seleccionado
                        self.registroJuego.setId(fila[0])
                        self.entryTitulo.set_text(fila[1])
                        self.registroJuego.setTitulo(fila[1])
                        self.entryGenero.set_text(fila[2])
                        self.registroJuego.setGenero(fila[2])
                        self.entryPlataforma.set_text(fila[3])
                        self.registroJuego.setPlataforma(fila[3])
                        self.entryLanzamiento.set_text(fila[4])
                        self.registroJuego.setLanzamiento(fila[4])
                        self.registroJuego.setCaratula(fila[5])
                        botonAsignarImagen = self.builder.get_object("botonAsignarImagen")
                        img = self.builder.get_object("imageDetallesCaratula")
                        img.set_from_file(self.registroJuego.getCaratula())
                        img.show()

                    contador += 1

                if contador == 0:
                    self.limpiarDetalles()


                #Cerramos cursor
            	cursor.close()
            	#Cerramos conexión
            	conexion.close()
            else:
                #Si hay campos vacíós mostramos aviso al usuario
                self.dialogAviso.show_all()
        # Editar juego
        if etiquetaBoton == "Editar juego":
            # Actualizamos datos de Detalles
            self.registroJuego.setTitulo(self.entryTitulo.get_text())
            self.registroJuego.setGenero(self.entryGenero.get_text())
            self.registroJuego.setPlataforma(self.entryPlataforma.get_text())
            self.registroJuego.setLanzamiento(self.entryLanzamiento.get_text())
            #Si no hay campos vacíós realizamos Edición
            if not self.camposVacios(self.registroJuego):
                print "Entrando editar"

                conexion = sqlite3.connect("juegos.db")
                cursor = conexion.cursor()

                # Realizamos Edicion del registro seleccionado
                cursor.execute("UPDATE Juegos SET Titulo = ?, Genero = ?, Plataforma = ?, Lanzamiento = ?, Caratula = ? WHERE id = ?;",(self.entryTitulo.get_text(),self.entryGenero.get_text(),self.entryPlataforma.get_text(),self.entryLanzamiento.get_text(),self.registroJuego.getCaratula(), int(self.registroJuego.getId())))
                print "EDITADO"
                # Hacemos commit
                conexion.commit()

            	#Consultamos para actualizar nuevos valores
            	cursor.execute("SELECT * FROM Juegos;")

                # Borramos valores antíguos
                self.borrarTabla()

                # Rellenamos la estructura de la tabla con el resultado de la consulta
                contador = 0
                for fila in cursor:
                    self.store.append([fila[0], fila[1], fila[2], fila[3], fila[4], fila[5]])
                    # Actualiza datos con la fila seleccionada por defecto
                    if contador == 0:
                        #Actualizamos valores de registro seleccionado
                        self.registroJuego.setId(fila[0])
                        self.entryTitulo.set_text(fila[1])
                        self.registroJuego.setTitulo(fila[1])
                        self.entryGenero.set_text(fila[2])
                        self.registroJuego.setGenero(fila[2])
                        self.entryPlataforma.set_text(fila[3])
                        self.registroJuego.setPlataforma(fila[3])
                        self.entryLanzamiento.set_text(fila[4])
                        self.registroJuego.setLanzamiento(fila[4])
                        self.registroJuego.setCaratula(fila[5])
                        botonAsignarImagen = self.builder.get_object("botonAsignarImagen")
                        img = self.builder.get_object("imageDetallesCaratula")
                        img.set_from_file(self.registroJuego.getCaratula())
                        img.show()

                    contador += 1

                if contador == 0:
                    self.limpiarDetalles()


                #Cerramos cursor
            	cursor.close()
            	#Cerramos conexión
            	conexion.close()
            else:
                #Si hay campos vacíós mostramos aviso al usuario
                self.dialogAviso.show_all()

        if etiquetaBoton == "Borrar juego":
            #Si no hay campos vacíós realizamos borrado
            if not self.camposVacios(self.registroJuego):

                conexion = sqlite3.connect("juegos.db")
                cursor = conexion.cursor()

                # Realizamos Borrado del registro seleccionado
                buscar = self.registroJuego.getId()
                cursor.execute("DELETE FROM Juegos WHERE id = ?;",(int(buscar),))
                # Hacemos commit
                conexion.commit()

                #Consultamos para actualizar nuevos valores
                cursor.execute("SELECT * FROM Juegos;")

                # Borramos valores antíguos
                self.borrarTabla()

                # Rellenamos la estructura de la tabla con el resultado de la consulta
                contador = 0
                for fila in cursor:
                    self.store.append([fila[0], fila[1], fila[2], fila[3], fila[4], fila[5]])
                    # Actualiza datos con la fila seleccionada por defecto
                    if contador == 0:
                        #Actualizamos valores de registro seleccionado
                        self.registroJuego.setId(fila[0])
                        self.entryTitulo.set_text(fila[1])
                        self.registroJuego.setTitulo(fila[1])
                        self.entryGenero.set_text(fila[2])
                        self.registroJuego.setGenero(fila[2])
                        self.entryPlataforma.set_text(fila[3])
                        self.registroJuego.setPlataforma(fila[3])
                        self.entryLanzamiento.set_text(fila[4])
                        self.registroJuego.setLanzamiento(fila[4])
                        self.registroJuego.setCaratula(fila[5])
                        botonAsignarImagen = self.builder.get_object("botonAsignarImagen")
                        img = self.builder.get_object("imageDetallesCaratula")
                        img.set_from_file(self.registroJuego.getCaratula())
                        img.show()

                    contador += 1

                if contador == 0:
                    self.limpiarDetalles()

                #Cerramos cursor
                cursor.close()
                #Cerramos conexión
                conexion.close()
            else:
                #Si hay campos vacíós mostramos aviso al usuario
                self.dialogAviso.show_all()
def main():
    window = Catalogo_GUI()
    Gtk.main()
    return 0

if __name__ == '__main__':
    main()
