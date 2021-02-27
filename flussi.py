# -*- coding: utf-8 -*-

import Inv as iv, random

a = iv.Inv('mario',-10000.00,[-300,-200,-200,0,50,300,800,1200,3000,4000,6000,12000,14000,20000,30000])
b = iv.Inv('gigio',-50000.00,[-300,-200,-500,0,50,300,800,1100,3000,4000,9000,12000,14000,20000,30000])
c = iv.Inv('c',-30000.00,[-300,-500,-200,0,100,300,800,1200,2000,4000,60000,12000,14000,20000,30000])
d = iv.Inv('d',-6000.00,[-1000,-200,-2000,0,500,400,700,60000,3000,44000,6000,17000,14000,20000,30000])
e = iv.Inv('e',-800000.00,[-300,-2000,-200,0,50,300,800,1200,3000,400000,6000,12000,14000,20000,30000])


def main():
    global a, b, c, d, e
    choice = ' '
    Invs = {a.nome: a, b.nome: b, c.nome: c}  # nome: oggetto

    while choice != '0':
        print("1) Genera l'Inv")
        print('2) Visualizza Invs')
        print('3) Visualizza un Inv')
        '''
        
        print('4) Aggiungi dei flussi a quelli già esistenti (in coda)')
        print('5) Rimuovi uno o più flussi')
        print('6) Calcola il TIR')
        print('7) Grafico VAN-r')
        print('8) PayBack Period')
        #print('9) Inserisci altri flussi e confrontali con i precedenti')
        print('10) Altra visualizzazione dei dati')
        '''
        print('0) Esci')

        choice = input('Scelta: ')

        if choice == '1':
            N = input('Nome: ')
            A = int(input('Anni: '))
            flussi = [random.randint(-500000, 2000000) for i in range(a)]
            I = iv.Inv(N, flussi[0], flussi[1:])
            Invs[I.nome] = I

        elif choice == '2':
            for i in Invs:
                print()
                print(Invs[i])
                print()

        elif choice == '3':
            q = input('Nome: ')
            Invs.get(q, 'Inv non presente')

        elif choice == '0':
           pass
main()


Invs = {a.nome: a, b.nome: b, c.nome: c}
#Invs['a'] = 22
