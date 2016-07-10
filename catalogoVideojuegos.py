#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import os
import sqlite3

class Catalogo_GUI:
    builder=None
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("catalogoVideojuegos.glade")
        self.handlers = {"onDeleteWindow": Gtk.main_quit,
                            "onAboutActivate": self.onAboutActivate,
                            "onCloseAbout": self.onCloseAbout,
                            "onBotonAsignarImagenClicked": self.onBotonAsignarImagenClicked,}

        self.builder.connect_signals(self.handlers)

        self.window = self.builder.get_object("ventanaPrincipal")
        self.window.show_all()

    def onAboutActivate(self, submenuAyudaAbout):
		self.about = self.builder.get_object("dialogAbout")
		self.about.show_all()

    def onCloseAbout(self, *args):
        self.about = self.builder.get_object("dialogAbout")
        self.about.hide()

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
            #Asignar a bd datos
            img.show()
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

def main():
    window = Catalogo_GUI()
    Gtk.main()
    return 0

if __name__ == '__main__':
    main()
