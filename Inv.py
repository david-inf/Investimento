# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 10:49:41 2020

@author: david
"""

    
import numpy as np
import matplotlib.pyplot as plt 
'''Crea gli oggetti investimento per avere lista dei flussi ed
avere nel main quanti investimenti vuoi''' 

class Inv(object):
    def __init__(self,C0):
        '''Crea l'investimento''' 
        self.C0 = C0
        self.FDC = [C0]
        self.f_vett = np.array(self.FDC) #li metto su array, non si sa mai

    '''Blocco modifiche'''
    def add_tail(self,flussi): #flussi è una lista
        self.FDC = self.FDC + flussi #ricorda che li aggiunge in coda
    def add_here(self,flusso,posizione):
        self.FDC.insert(posizione,flusso)
    def pop(self,anno): 
        self.FDC.pop(anno)
    def remove(self,flusso):
        try:
            self.FDC.remove(flusso)
        except:
            raise ValueError(str(flusso) + ' not found')

    '''Blocco visualizzazione'''
    def getMembers(self):
        '''Stampa la lista'''
        return self.FDC[:] 
    def Member(self,flusso):
        '''True se c'è, False altrimenti'''
        return flusso in self.FDC                 
    def __str__(self): #permette di usare print(oggetto_Inv) 
        '''String representation of self'''
        result = ''
        for f in self.FDC:
            result = result + str(f) + ',' #stringa 'f,f,' , è un elemento 
            return '{' + result[:-1] + '}' #-1 omette l'ultima virgola

    '''Blocco matematica finanziaria'''
    def VAN(self,tasso): #se il tasso è subito noto potrei metterli attributi all'inizio
        van = round(np.npv(tasso,self.FDC),4)
        return van 
    def TIR(self):
        tir = round(np.irr(self.FDC),4)
        return tir  
    def FD(self,tasso,anni): #fattore di rendita
        fd = 1/tasso - 1/(tasso*(1+tasso)**anni)
        return round(fd,4)
    def EA(self,tasso,anni): #ricontrollare!!
        van = round(np.npv(tasso,self.FDC),4)
        ea = van*(1/Inv.FD(tasso,anni)) #non so se funziona!!
        return round(ea,4) 
