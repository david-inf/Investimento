# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 10:49:41 2020

@author: david
"""

    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
'''Crea gli oggetti investimento per avere lista dei flussi ed
avere nel main quanti investimenti vuoi''' 

class Inv(object):
    def __init__(self,C0,flussi,tasso=0.1):
        '''Crea l'investimento''' 
        self.C0 = C0 #pagamento iniziale
        self.flussi = flussi 
        self.tasso = tasso #tasso di sconto
        self.FDC = [C0] + flussi #una volta fatto questo, meglio usare gli array 
        self.f_ar = np.array(self.FDC) #li metto su array, non si sa mai
        self.len = self.f_ar.size #numero di elementi 
        self.see = pd.Series(self.f_ar)
        self.statistics = self.see.describe()

    '''Blocco modifiche'''
    def add_tail(self,flussi): #flussi è una lista
        #self.FDC = self.FDC + flussi #ricorda che li aggiunge in coda
        #for i in flussi:
            #self.FDC.append(i) 
        self.f_ar = np.append(self.f_ar,flussi)
    def add_here(self,posizione,flusso):
        #self.FDC.insert(posizione,flusso)
        self.f_ar = np.insert(self.f_ar,posizione,flusso)
    #def pop(self,anno): #rimuove con l'indice
        #self.FDC.pop(anno)
    def remove(self,flusso): #rimuove un valore
        self.f_ar = np.delete(self.f_ar,flusso)
        '''
        try:
            self.FDC.remove(flusso)
        except:
            raise ValueError(str(flusso) + ' not found')
        '''
    '''Blocco visualizzazione'''
    def getMembers(self):
        '''Stampa la lista'''
        #return self.FDC[:] 
        print(self.f_ar) 
    '''
    def see(self): #pandas 
        ind = list(range(self.len))
        s = pd.Series(self.f_ar,ind) #RICONTROLLARE 
        return s 
    '''
    def Member(self,flusso):
        '''True se c'è, False altrimenti'''
        #return flusso in self.FDC     
        return flusso in self.f_ar 
    """             
    def __str__(self): #permette di usare print(oggetto_Inv) 
        '''String representation of self'''
        result = ''
        for f in self.FDC:
            result = result + str(f) + ',' #stringa 'f,f,' , è un elemento 
            return '{' + result[:-1] + '}' #-1 omette l'ultima virgola
    """
    '''Blocco matematica finanziaria'''
    def VAN(self): #,tasso): #se il tasso è subito noto potrei metterli attributi all'inizio
        #van = round(np.npv(tasso,self.FDC),4)
        van = round(np.npv(self.tasso,self.f_ar),4)
        return van 
    def TIR(self):
        #tir = round(np.irr(self.FDC),4)
        tir = round(np.irr(self.f_ar),4)
        return tir  
    def FD(self): #,tasso,anni): #fattore di rendita
        #anni = self.len
        fd = 1/self.tasso - 1/(self.tasso*(1+self.tasso)**self.len)
        return round(fd,4)
    def EA(self): #,tasso,anni): #ricontrollare!!
        #anni = self.len
        van = round(np.npv(self.tasso,self.f_ar),4)
        ea = van*(1/Inv.FD(self.tasso,self.len)) #non so se funziona!!
        return round(ea,4) 