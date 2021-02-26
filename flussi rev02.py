# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 22:14:06 2020

@author: david
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import Inv

#come metto il tasso? 
#r = 0.1 #per ora lo metto qui

def main():
    #global r
    invs = []
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
        print('9) Inserisci altri flussi e confrontali con i precedenti') #questo penso che lo toglierò 
        print('10) Altra visualizzazione dei dati')
        print('11) Altra visualizzazione del confronto')
        print('0) Esci')
    
        choice = input('Scelta: ')
        
        if choice == '1': #Aggiungi dei flussi
            C0 = float(input('Primo flusso: '))
            invo = Inv(C0)
            a = str(input('Altri? si/no '))
            if a == 'si':
                n = int(input('Quanti? '))
                i = 0
                F = []
                while i < n:
                    Fj = float(input('Flusso: '))
                    F.append(Fj)
                    i += 1
                invo.add_tail(F)
                invs.append(invo)
            else:
                pass
                
        elif choice == '2': #Visualizza i flussi
            for i in invs:
                print(f'Investimento {invs.index(i)}:')
                invs[i].getMembers()
                #print(f'Investimento {invs.index(i) + 1}: {i}')
                print()
                
        elif choice == '3': #Attualizza
            for i in invs:
                print(f'Investimento {invs.index(i) + 1}:')
                i.VAN(r)
                print()

        elif choice == '4': #Aggiungi dei flussi a quelli già esistenti (in coda) 
            p = int(input('Posizione investimento: '))
            c0 = str(input('Rimpiazzare il primo flusso? si/no '))
            if c0 == 'si':
                invs[p].pop(0)  
                C0 = float(input('Primo flusso: '))
                invs[p].add_here(C0,0)
                
            #else:
             #   pass
           
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

        elif choice == '9':
            F0B = float(input('Primo flusso: '))
            C0B = F0B
            b = str(input('Altri? si/no '))
            if b == 'si':
                N = int(input('Quanti? '))
                k = 0
                while k < N:
                    Fk = float(input('Flusso: '))
                    flussiB.append(Fk) 
                    k += 1
            else:
                pass
            print()
            
            flussi.insert(0,C0)
            flussiB.insert(0,C0B)
            VAN_A = round(np.npv(r,flussi),4)
            VAN_B = round(np.npv(r,flussiB),4)
            print('EA del primo investimento: ') 
            EA(VAN_A,len(flussi))
            print(f'VAN del primo investimento: {VAN_A}')
            print(f'Durata: {len(flussi)} anni')
            print()
            print('EA del secondo investimento: ')
            EA(VAN_B,len(flussiB))
            print(f'VAN del secondo investimento: {VAN_B}')
            print(f'Durata: {len(flussiB)} anni')
            print()
            
            flussi.pop(0)
            flussiB.pop(0)
        
        elif choice == '10': #vediamo se uso i pandas
            flussi.insert(0,C0)
            #pd.Series(flussi,relativi_anni)
            ind = {} #{'anno 1': flusso 1}
            for f in range(len(flussi)): #da qui tiro fuori gli indici
                a = str(f)
                d = 'Anno ' + a
                ind[d] = flussi[f]
            
            S = pd.Series(ind) 
            print(S)
            print()
            #print(f'Flusso massimo: {S.max()}, {S.argmax()}')
            #print(f'Media: {S.mean()}')
            #print(f'Deviazione Standard: {S.std()}')
            H = str(input('Statistiche? si/no: '))
            print()
            if H == 'si':
                print(S.describe()) #S.describe(exclude=) in caso non ne voglio qualcuno
                S.plot(kind='bar') #diagramma a barre 
                plt.show()
                S.plot.box(vert=False, whis='range')
                plt.show()
                print()
                print("SCORRI IN SU, C'E' ALTRA ROBA!")
                print()     
                
            flussi.pop(0)     

        elif choice == '11': #vedo se butto tutto in un DataFrame
            flussi.insert(0,C0)
            flussiB.insert(0,C0B)
            A_B = {'Flussi_1°' : flussi, 'Flussi_2°' : flussiB}
            
            index = []
            if len(flussi) == len(flussiB):
                for i in range(len(flussi)): 
                    a = str(i)
                    D = 'Anno ' + a
                    index.append(D)
            elif len(flussi) > len(flussiB):
                for i in range(len(flussi)): 
                    a = str(i)
                    D = 'Anno ' + a
                    index.append(D)
            else:
                for i in range(len(flussiB)): 
                    a = str(i)
                    D = 'Anno ' + a
                    index.append(D)
            
            dfA_B = pd.DataFrame(A_B, index=index)
            print(dfA_B)
            print()
            
            flussi.pop(0)
            flussiB.pop(0)
                    
        elif choice == '0':
            pass   
main()
