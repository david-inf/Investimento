# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 10:49:41 2020

@author: david
"""

import numpy as np, pandas as pd, matplotlib.pyplot as plt, psycopg2


class Inv(object):
    def __init__(self, nome: str, C0: float, flussi: list, tasso=0.1):
        '''Crea l'investimento'''
        self.nome = nome  # almeno lo identifico nel DB
        self.C0 = C0  # pagamento iniziale
        self.flussi = flussi
        self.r = tasso  # tasso di sconto
        self.FDC = [C0] + flussi  # meglio usare gli array
        self.f_ar = np.array(self.FDC)  # li metto su array, non si sa mai
        self.len = self.f_ar.size  # numero di elementi

        self.anni = []
        for i in range(len(self.f_ar)):
            a = 'anno '
            self.anni.append(a+str(i))

        self.series = pd.Series(self.f_ar, index=self.anni)
        self.statistics = self.series.describe()

        self.dict = {}  # controllare
        for j in range(len(self.anni)):
            self.dict[self.anni[j]] = self.f_ar[j]

        self.van = round(np.npv(self.r, self.f_ar), 4)
        self.tir = round(np.irr(self.f_ar), 4)

    '''Blocco modifiche'''

    def add_tail(self, flussi):  # flussi è una lista
        # self.FDC = self.FDC + flussi #ricorda che li aggiunge in coda
        # for i in flussi:
        #   self.FDC.append(i)
        self.f_ar = np.append(self.f_ar, flussi)

    def add_here(self, posizione, flusso):
        # self.FDC.insert(posizione,flusso)
        self.f_ar = np.insert(self.f_ar, posizione, flusso)

    def pop(self, anno):  # np.delete(array,index)
        self.f_ar = np.delete(self.f_ar, anno)

    '''Blocco visualizzazione'''

    def getMembers(self):
        '''Stampa la lista'''
        # return self.FDC[:]
        # print(self.f_ar)
        return self.f_ar

    def Member(self, flusso):
        '''True se c'è, False altrimenti'''
        # return flusso in self.FDC
        return flusso in self.f_ar

    def __str__(self):  # permette di usare print(oggetto_Inv)
        '''CONTROLLA SE FUNZIONA'''
        return f'{self.series}\nTasso: {self.r}\nVAN: {self.van}\nTIR: {self.tir}'       

    '''Blocco matematica finanziaria'''  # anche se è tutto su __init__

    def FD(self):  # fattore di rendita
        # anni = self.len
        fd = 1/self.r - 1/(self.r*(1+self.r)**self.len)
        return round(fd, 4)

    def EA(self):
        # anni = self.len
        van = round(np.npv(self.r, self.f_ar), 4)
        ea = van*(1/Inv.FD(self))  # non so se funziona!!
        return round(ea, 4)

    '''Blocco plotter'''

    def van_tasso(self):
        '''Grafico VAN asse y, tasso r asse x'''
        plt.ylabel('VAN')
        plt.xlabel('r')
        # print(self.f_ar)  # vedi se puoi chiamare getMembers invece
        Inv.getMembers()
        s = 0.015  # precisione sull'asse di r (step)
        x = np.arange(0, self.tir, s)
        x1 = np.arange(self.tir, 6*s+self.tir, s)
        x = np.append(x, x1)
        y = np.array([])
        for i in x:
            y0 = np.npv(i, self.f_ar)
            y = np.append(y, y0)
            if np.size(x) == np.size(y):
                xm = 0
                xM = self.tir+6*s
                plt.plot(x, y, 'c-')  # cyan(c)
                plt.plot(x, y, 'rx')
                plt.plot([xm, xM], [0, 0], 'g--')  # asse x
                plt.plot([xm, self.r], [self.van, self.van])  # asse x dal van
                plt.plot([self.tir, self.tir], [0, y[0]])  # asse y sul tir
                plt.plot([self.r, self.r], [0, self.van])  # asse y sul VAN
                plt.show()

    def barre_box(self):
        '''Grafico a barre e box-plot'''
        self.series.plot(kind='bar')
        plt.show()
        self.series.plot.box(vert=False, whis='range')
        plt.show()

    def PBP(self):
        plt.ylabel('VAN')
        plt.xlabel('t (anni)')
        vans = np.array([])
        j = 0
        while j < self.len:
            van = round(np.npv(self.r, self.f_ar[:j+1]), 4)
            vans = np.append(vans, van)
            if vans[j] >= -100.0 and vans[j] <= 100.0:
                PBP = j
                print(f'PBP: {PBP}')
            j += 1
        if vans.size == self.len:
            print(f'VAN progressivi: {vans}')
            anni = np.array(range(self.len))
            plt.plot(anni, vans, 'c-')
            plt.plot(anni, vans, 'rx')
            plt.plot([0, self.len], [0, 0], 'g--')
            plt.show()


def is_positive(lista):  # se la lista è positiva
    result = True
    for i in lista:
        if i > 0:
            continue
        else:
            result = False
    return result


def from_positive(lista):  # deve andare nel PBP
    c = -1
    if lista[-1] < 0:
        # return print('Non diventa mai positiva')
        return False
    while c != -len(lista):
        if lista[c] >= 0:
            c -= 1
        else:
            return c+1
    return 0


def hey_db(query: str):  # query sul database Azienda
    con = psycopg2.connect(
    host = '127.0.0.1',
    database = 'Azienda',
    user = 'postgres',
    password = 'david25',
    port = '5432')

    cur = con.cursor()
    q = query
    cur.execute(q)
    rows = cur.fetchall()  # lista di tuple

    for r in rows:
        print(r)

    con.commit()  # refresh poi su pgadmin4
    cur.close()
    con.close()

'''non fa'''
def to_db(nome_inv: str, flussi):
    con = psycopg2.connect(
    host = '127.0.0.1',
    database = 'Azienda',
    user = 'postgres',
    password = 'david25',
    port = '5432')
    cur = con.cursor()

    for i in range(len(flussi)):
        j = flussi[i]
        cur.execute(f"insert into investimento values ({nome_inv}, {i}, {j})")
    
    cur.fetchall()

    con.commit()  # refresh poi su pgadmin4
    cur.close()
    con.close()















