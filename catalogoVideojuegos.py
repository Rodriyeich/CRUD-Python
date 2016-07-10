#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import os
import sqlite3

from RegistroJuego import RegistroJuego

class Catalogo_GUI:
    builder = None
    registroJuego = None
    entryTitulo = None
    entryGenero = None
    entryDesarrolladora = None
    entryPlataforma = None
    entryLanzamiento = None
    dialogAviso = None
    def __init__(self):
        self.registroJuego = RegistroJuego()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("catalogoVideojuegos.glade")
        self.handlers = {"onDeleteWindow": Gtk.main_quit,
                            "onAboutActivate": self.onAboutActivate,
                            "onCloseAbout": self.onCloseAbout,
                            "onBotonDialogCamposVaciosClicked": self.onBotonDialogCamposVaciosClicked,
                            "onBotonAccionClicked": self.onBotonAccionClicked,
                            "onBotonAsignarImagenClicked": self.onBotonAsignarImagenClicked,}

        self.builder.connect_signals(self.handlers)

        #Inicializacion widgets y valores por defecto
        self.entryTitulo = self.builder.get_object("entryTituloDetalles")
        self.entryGenero = self.builder.get_object("entryGeneroDetalles")
        self.entryPlataforma = self.builder.get_object("entryPlataformaDetalles")
        self.entryDesarrolladora = self.builder.get_object("entryDesarrolladoraDetalles")
        self.entryLanzamiento = self.builder.get_object("entryLanzamientoDetalles")
        self.registroJuego.setCaratula("resources/seleccionar_imagen.jpg")
        self.dialogAviso = self.builder.get_object("dialogCamposVacios")

        #Consultamos numero de tablas que hay en la base de datos
        conexion = sqlite3.connect("juegos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name;")
        tablas = map(lambda t: t[0], cursor.fetchall())
        print "Numero de tablas en la base de Datos:" + str(len(tablas))

        #Si no hay tablas la creamos
        if len(tablas) == 0:
            cursor.execute("CREATE TABLE Juegos (id, Titulo, Genero, Desarrolladora, Plataforma, Lanzamiento, Caratula);")

        #Cerramos cursor
        cursor.close()
        #Cerramos conexión
        conexion.close()

        self.window = self.builder.get_object("ventanaPrincipal")
        self.window.show_all()

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
    		campoVacio = self.cadenaVacia(registro.getDesarrolladora())

    	if not campoVacio:
    		campoVacio = self.cadenaVacia(registro.getPlataforma())

    	if not campoVacio:
    		campoVacio = self.cadenaVacia(registro.getLanzamiento())

    	if not campoVacio:
    		campoVacio = self.cadenaVacia(registro.getCaratula())

    	return campoVacio

    def onAboutActivate(self, submenuAyudaAbout):
		self.about = self.builder.get_object("dialogAbout")
		self.about.show_all()

    def onCloseAbout(self, *args):
        self.about = self.builder.get_object("dialogAbout")
        self.about.hide()

    def onBotonDialogCamposVaciosClicked(self, button):
        print "Cerrando"
        self.dialogAviso.hide()

    def onBotonAsignarImagenClicked(self, button):
        dialog = Gtk.FileChooserDialog("Elige fichero", None,
                 Gtk.FileChooserAction.OPEN,
                 (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Abrir pulsado")
            print("Fichero seleccionado: " + dialog.get_filename())
            # cambiamos la imagen asociada al botón
            image = Gtk.Image()
            image.set_from_file(dialog.get_filename())
            image.show()
            botonAsignarImagen = self.builder.get_object("botonAsignarImagen")
            img = self.builder.get_object("imageDetallesCaratula")
            print("resources/" + os.path.basename(dialog.get_filename()))
            #Trunca la ruta del fichero hasta el directorio local de la app
            img.set_from_file("resources/" + os.path.basename(dialog.get_filename()))
            self.registroJuego.setCaratula("resources/" + os.path.basename(dialog.get_filename()))
            #Asignar a bd datos
            img.show()
            print "NOMBRE -> " + img.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancelar pulsado")

        dialog.destroy()

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

    def onBotonAccionClicked(self, button):

        #Actualizamos valores de registro seleccionado
        txt = self.entryTitulo.get_text()
        self.registroJuego.setTitulo(txt)
        txt = self.entryDesarrolladora.get_text()
        self.registroJuego.setDesarrolladora(txt)
        txt = self.entryGenero.get_text()
        self.registroJuego.setGenero(txt)
        txt = self.entryPlataforma.get_text()
        self.registroJuego.setPlataforma(txt)
        txt = self.entryLanzamiento.get_text()
        self.registroJuego.setLanzamiento(txt)

        etiquetaBoton = button.get_label()
        if etiquetaBoton == "Añadir juego":

            if not self.camposVacios(self.registroJuego):

                conexion = sqlite3.connect("juegos.db")
                cursor = conexion.cursor()
            	#Consultamos los datos para extraer último id de la tabla Victimas
            	cursor.execute("SELECT * FROM Juegos; ")

            	#Extraemos longitud de la lista del cursor que coincide con el último id introducido en la tabla
            	ultimoId = len(cursor.fetchall())
                ultimoId += 1
                # Realizamos insercion de nuevo registro
                #cursor.execute("INSERT INTO Juegos(id,Titulo,Genero,Desarrolladora, Plataforma, Lanzamiento, Caratula) VALUES (%s, %s, %s, %s, %s, %s, %s);",
                #                (ultimoId, self.registroJuego.getTitulo(), self.registroJuego.getGenero(), self.registroJuego.getDesarrolladora(), self.registroJuego.getPlataforma(), self.registroJuego.getLanzamiento(), self.registroJuego.getCaratula()))

            	#Cerramos cursor
            	cursor.close()
            	#Cerramos conexión
            	conexion.close()
            else:
                self.dialogAviso.show_all()
def main():
    window = Catalogo_GUI()
    Gtk.main()
    return 0

if __name__ == '__main__':
    main()
