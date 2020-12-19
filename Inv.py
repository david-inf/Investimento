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
        self.r = tasso #tasso di sconto
        self.FDC = [C0] + flussi #una volta fatto questo, meglio usare gli array 
        self.f_ar = np.array(self.FDC) #li metto su array, non si sa mai
        self.len = self.f_ar.size #numero di elementi 
        self.anni = []
        for i in range(len(self.f_ar)):
            a = 'anno '
            self.anni.append(a+str(i))
        self.see = pd.Series(self.f_ar,index=self.anni)
        self.statistics = self.see.describe()
       #self.dict = {} #non fa 
       #for j in self.anni:
            #for k in self.f_ar:
             #   self.dict[j] = k
             
        self.van = round(np.npv(self.r,self.f_ar),4)
        self.tir = round(np.irr(self.f_ar),4)
        
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
        #print(self.f_ar)
        return self.f_ar
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
    """
    def VAN(self): #,tasso): #se il tasso è subito noto potrei metterli attributi all'inizio
        #van = round(np.npv(tasso,self.FDC),4)
        van = round(np.npv(self.tasso,self.f_ar),4)
        return van 
    def TIR(self):
        #tir = round(np.irr(self.FDC),4)
        tir = round(np.irr(self.f_ar),4)
        return tir  
    """
    def FD(self): #,tasso,anni): #fattore di rendita
        #anni = self.len
        fd = 1/self.r - 1/(self.r*(1+self.r)**self.len)
        return round(fd,4)
    def EA(self): #,tasso,anni): #ricontrollare!!
        #anni = self.len
        van = round(np.npv(self.r,self.f_ar),4)
        ea = van*(1/Inv.FD(self)) #non so se funziona!!
        return round(ea,4) 
    
    '''Blocco plotter'''
    def plot(self):
        plt.ylabel('VAN')
        plt.xlabel('r')
        print(self.f_ar) #vedi se puoi chiamare getMembers invece
        s = 0.015 #precisione sull'asse di r (step)       
        x = np.arange(0,self.tir,s)
        x1 = np.arange(self.tir,6*s+self.tir,s)
        x = np.append(x,x1)
        y = np.array([])
        for i in x:      #np.append(x,[tir,tir+s,tir+2*s]):
            y0 = np.npv(i,self.f_ar)
            y = np.append(y,y0)
            if np.size(x) == np.size(y):
                xm = 0
                xM = self.tir+6*s
                plt.plot(x,y,'c-') #cyan(c)
                plt.plot(x,y,'rx')
                plt.plot([xm,xM],[0,0],'g--') #asse x, tratteggiato in verde
                plt.plot([xm,self.r],[self.van,self.van]) #asse x dal van, più scuro del ciano
                plt.plot([self.tir,self.tir],[0,y[0]]) #asse y sul tir, in arancione 
                plt.plot([self.r,self.r],[0,self.van]) #asse y sul VAN con r y[0]
                plt.show() 
    def PBP(self):
        plt.ylabel('VAN')
        plt.xlabel('t (anni)')
        vans = np.array([])
        j = 0
        while j < self.len:
            van = round(np.npv(self.r,self.f_ar[:j+1]),4)
            vans = np.append(vans,van)
            if vans[j] >= -100.0 and vans[j] <= 100.0: #è difficile beccare 0.0 
                PBP = j
                print(f'PBP: {PBP}')
            j += 1

        if vans.size == self.len:
            print(f'VAN progressivi: {vans}') 
            anni = np.array(range(self.len))
            plt.plot(anni,vans,'c-')
            plt.plot(anni,vans,'rx')
            plt.plot([0,self.len],[0,0],'g--')
            plt.show()  
            
           
def is_positive(lista): #se la lista è positiva 
    result = True
    for i in lista:
        if i > 0:
            continue
        else:
            result = False
    return result

def from_positive(lista): #deve andare nel PBP 
    c = -1
    if lista[-1] < 0:
        #return print('Non diventa mai positiva')
        return False 
    while c != -len(lista):
        if lista[c] >= 0:
            c -= 1
        else:
            return c+1
    return 0
    
    
    
    
            
            
            
    




        