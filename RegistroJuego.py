#!/usr/bin/python
# -*- coding: utf-8 -*-
#Author José Manuel Rodriguez Rodriguez, Program Name: Victimas de Conan


"""
	Clase: RegistroConan
	- Define un registro de la tabla: Victimas
	- Los atributos definen los campos del registro (id, Nombre, Genero, plataforma Lanzamiento, Caratula)
"""
class RegistroJuego:
    #Constructor por defecto
    def __init__(self):
        self.__id__ = 0
        self.__titulo__ = None
        self.__genero__ = None
        self.__plataforma__ = None
        self.__lanzamiento__ = None
        self.__caratula__ = None

    #Métodos públicos
    def getId(self):
		return self.__id__

    def setId(self,pId):
		self.__id__ = pId

    def getTitulo(self):
		return self.__titulo__

    def setTitulo(self, pTitulo):
		self.__titulo__ = pTitulo

    def getGenero(self):
		return self.__genero__

    def setGenero(self,pGenero):
		self.__genero__ = pGenero

    def setPlataforma(self,pPlataforma):
		self.__plataforma__ = pPlataforma

    def getPlataforma(self):
		return self.__plataforma__

    def setLanzamiento(self,pLanzamiento):
		self.__lanzamiento__ = pLanzamiento

    def getLanzamiento(self):
		return self.__lanzamiento__

    def setCaratula(self,pCaratula):
		self.__caratula__ = pCaratula

    def getCaratula(self):
		return self.__caratula__
