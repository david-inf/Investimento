# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 12:20:44 2020

@author: david
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

r = 0.0826 #0.1 #tasso di sconto, 10%

def VAN(C0,flussi):
    van = C0
    global r
    den = 1 + r
    i  = 0
    while i < len(flussi):
        esp = i + 1
        add = (flussi[i])/(den**esp)
        van += add
        i += 1     
    print(round(van,4))
'''
def VAN2(C0,flussi,tasso): #meglio usare np.npv(rate,values)  
    van = C0
    den = 1 + tasso
    i  = 0
    while i < len(flussi):
        esp = i + 1
        add = (flussi[i])/(den**esp)
        van += add
        i += 1     
    #print(round(van,4))
    return round(van,4)
'''
def FD(anni): #fattore di rendita
    global r
    fd = 1/r - 1/(r*(1+r)**anni)
    return round(fd,4)
    
def EA(van,anni):
    global r
    ea = van*(1/FD(anni))
    print(round(ea,4))

def main():
    global r
    flussi = [] #investimento A
    #flussiB = [] #investimento B
    Co0 = -4000 #valore per prove, ricordati di toglierlo anche nelle choice magari 
    fusis = [-1000,-300,200,400,500,1000,1400,3000,6000,9000] #lista di flussi per prove
    C0 = 0
    choice = ' '    
    while choice != '0':
        print('1) Aggiungi dei flussi')
        print('2) Visualizza i flussi')
        print('3) Attualizza')
        print('4) Aggiungi dei flussi a quelli già esistenti (in coda)') 
        print('5) Rimuovi uno o più flussi')
        print('6) Calcola il TIR')
        print('7) Grafico VAN-r')
        print('8) PayBack Period')
        #print('9) Inserisci altri flussi e confrontali con i precedenti')
        print('10) Altra visualizzazione dei dati')
        print('0) Esci')
    
        choice = input('Scelta: ')
        
        if choice == '1':
            F0 = float(input('Primo flusso: '))
            C0 = F0
            a = str(input('Altri? si/no '))
            if a == 'si':
                n = int(input('Quanti? '))
                i = 0
                while i < n:
                    Fj = float(input('Flusso: '))
                    flussi.append(Fj) 
                    i += 1
            else:
                pass
                
        elif choice == '2':
            print(f'C_0: {C0}€') #AltGr + E; AltGr + 5
            for i in flussi:
                d = flussi.index(i) + 1
                print(f'F_{d}: {i}')
                
        elif choice == '3': #np.npv(rate,values)
            if len(set(flussi)) != 1:
                VAN(C0,flussi)
                print(f'Attualizzato secondo il metodo del VAN.\nFattore di sconto: {r}')
                
            else:  #len(set(flussi)) == 1:
                anni = len(flussi)
                att = C0 + flussi[0]*FD(anni)
                print(att)
                print('Rendita costante, attualizzato col fattore di rendita.\nFattore di sconto: {r}')
        
        elif choice == '4':
            c0 = str(input('Rimpiazzare il primo flusso? si/no '))
            if c0 == 'si':
                C0 = float(input('Primo flusso: '))
            else:
                pass
            
            n = int(input('Quanti ne aggiungi? '))
            i = 0
            while i < n:
                Fj = float(input('Flusso: '))
                flussi.append(Fj) 
                i += 1
                
        elif choice == '5':
            p = int(input('Anno del flusso: '))
            if p == 0:
                C0 = 0
            elif p < 0:
                print('Anno non valido')
            else: #p > 0 
                a = p - 1
                flussi.pop(a)
                
        elif choice == '6':
            flussi.insert(0,C0)
            tir = round(np.irr(flussi),4)  #np.irr(values)
            flussi.pop(0)
            print(tir)
            
        elif choice == '7': #vediamo se riesco a plottare
            plt.ylabel('VAN')
            plt.xlabel('r')
            print(f'C_0: {C0}')
            print(f'Flussi: {flussi}')
            flussi.insert(0,C0)
            van = round(np.npv(r,flussi),4)
            print(f'VAN: {van}')

            tir = round(np.irr(flussi),4)  
            print(f'TIR: {tir}')
               
            s = float(input('Considera il valore del TIR e scegli uno step sul tasso di sconto adeguato, così da aumentare la precisione della curva.\nStep: '))           
            x = np.arange(0,tir,s)
            x = list(x)
            x.append(tir)
            x.append(tir+s)
            x.append(tir+2*s)
            y = []
            for i in x:      #np.append(x,[tir,tir+s,tir+2*s]):
                y0 = np.npv(i,flussi)
                y.append(y0)
                if len(x) == len(y):
                    #ym = C0
                    #yM = y[0] + 5
                    xm = 0
                    xM = tir+3*s
                    #plt.axis([xm,xM,ym,yM])
                    flussi.pop(0)
                    plt.plot(x,y,'c-') #cyan(c)
                    plt.plot(x,y,'rx')
                    plt.plot([xm,xM],[0,0],'g--') #asse x
                    plt.plot([xm,r],[van,van]) #asse x dal van 
                    plt.plot([tir,tir],[0,y[0]]) #asse y sul tir
                    plt.plot([r,r],[0,y[0]]) #asse y sul VAN con r
                    plt.show() 
                    
        elif choice == '8': #payback period
            plt.ylabel('VAN')
            plt.xlabel('t (anni)')
            print(f'C_0: {C0}')
            print(f'Flussi: {flussi}')
            flussi.insert(0,C0)
            print(f'VAN: {round(np.npv(r,flussi),4)}')
            
            vans = []
            j = 0
            while j < len(flussi):
                van = round(np.npv(r,flussi[:j+1]),4)
                vans.append(van)
                if vans[j] == 0.0:
                    PBP = j
                    print(f'PBP: {PBP}')
                j += 1
            if len(vans) == len(flussi):
                print(f'VAN progressivi: {vans}') 
                anni = list(range(len(flussi)))
                plt.plot(anni,vans,'c-')
                plt.plot(anni,vans,'rx')
                plt.plot([0,len(flussi)],[0,0],'g--')
                #plt.plot([PBP,PBP],[0,vans[-1]])
                plt.show()
                flussi.pop(0)  

        #elif choice == '9':
        
        elif choice == '10': #vediamo se uso i pandas
            fusis.insert(0,Co0) #rimetti qui e sotto flussi e C0
            #pd.Series(flussi,relativi_anni)
            ind = {}
            for f in range(len(fusis)): #da qui tiro fuori gli indici
                a = str(f)
                d = 'Anno ' + a
                ind[d] = fusis[f]
            
            S = pd.Series(ind) 
            print(S)
            print()
            #print(f'Flusso massimo: {S.max()}, {S.argmax()}')
            #print(f'Media: {S.mean()}')
            #print(f'Deviazione Standard: {S.std()}')
            H = str(input('Statistiche? si/no: '))
            if H == 'si':
                print(S.describe()) #S.describe(exclude=) in caso non ne voglio qualcuno
                S.plot(kind='bar') #diagramma a barre 
                plt.show()
                S.plot.box(vert=False, whis='range')
                plt.show()
                print()
                print("Scorri in su, c'è altra roba")
                print()
            
            
                
                
                
                
                
            #flussi.pop(0) 
                
            
                            
            
        elif choice == '0':
           pass   
main() 