#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def pobierz_dane(plikcsv):
    """
    Funkcja zwraca tuplę tupli zawierających dane pobrane z pliku csv
    do zapisania w tabeli.
    """
    dane = []  
    with open(os.path.join(APP_ROOT, plikcsv), "r", encoding='UTF-8') as zawartosc: 
        for linia in zawartosc:
            linia = linia.replace("\n", "")  
            linia = linia.replace("\r", "")  
            #linia = linia.decode("utf-8")  
            dane.append(tuple(linia.split(",")))

    return tuple(dane) 

from itertools import islice

def pobierz_opisy(plikcsv, amount = 5):
    """
    Funkcja zwraca tuplę tupli zawierających dane pobrane z pliku csv
    do zapisania w tabeli.
    """
    lines = []  
    with open(os.path.join(APP_ROOT, plikcsv), "r", encoding='UTF-8') as zawartosc:  
        while True:
            line = list(islice(zawartosc, amount)) 
            if line:                     
                lines.append(line)        
            else:
                break
        
    

    return tuple(["".join(line) for line in lines]) 

def pobierz_short(plikcsv):
    """
    Funkcja zwraca tuplę tupli zawierających dane pobrane z pliku csv
    do zapisania w tabeli.
    """
    dane = []  
    with open(os.path.join(APP_ROOT, plikcsv), "r", encoding='UTF-8') as zawartosc:  
        for linia in zawartosc:
            linia = linia.replace("\n", "")  
            linia = linia.replace("\r", "")  
            #linia = linia.decode("utf-8")  
            dane.append(tuple(linia.split(",")))

    return tuple(dane) 
