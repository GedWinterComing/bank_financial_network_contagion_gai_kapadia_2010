# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 15:52:29 2021

@author: Gabriele
"""


import numpy as np
import matplotlib.pyplot as plt
np.random.seed(420) # così con lo stesso seed (qua 420 ma può essere qualunque numero) ottieni sempre gli stessi numeri "casuali". Oppure puoi commentare questa riga, ma i risultati non saranno più riproducibili perchè ogni volta otterrai numeri casuali diversi!

import collections

from mpl_toolkits.mplot3d import Axes3D

from itertools import combinations
import networkx as nx
# nota che True+True=2 e False+False=0 siccome per Python True=1 e False=0
#%%
def istogramma_come_piace_me(vettore):
    # funziona solo per numeri interi
    ordinatodalmaggiorealminore = sorted(vettore, reverse=True)  # ordinati dal più grande al più piccolo
    dizionarioquantevoltesiripeteognivalore = collections.Counter(ordinatodalmaggiorealminore) # qua serve import collections
    valoridelvettore, conteggi = zip(*dizionarioquantevoltesiripeteognivalore.items())
    fig, ax = plt.subplots()
    plt.bar(valoridelvettore, conteggi, width=0.9, align='edge') # oppure di default il numero viene centrato e la grandezza del bin è width=0.8, così:
#    plt.bar(valoridelvettore, conteggi)
    fig.tight_layout()
    
#%%
# r numero casuale uniformemente distribuito fra 0<=r<1.
# Vogliamo trasformarlo in un altro numero reale random R ma distribuito tra R_{min}<=R<R_{max}
Rmin = 50
Rmax = 100
R = Rmin + (Rmax-Rmin) * np.random.random(size=100000) # con size=1000000 un milione comincia a vedersi un istogramma piatto
numero_bin = Rmax-Rmin
plt.hist(R,100) # oppure plt.hist(R, numero_bin)
# occhio che R sono numeri con la virgola!
#%%
# numeri interi

approssimato = np.rint(R) # approssima un numero al successivo intero se la parte decimale è >.5
intR = approssimato.astype(int)
plt.hist(intR,numero_bin)
#I = Rmin + (1+Rmax-Rmin) * np.random.random(size=100000) # sicome toglie la parte decimale bisogna prendere Rmax+1 poichè tutti i numeri che si avvicinano ad esse diventeranno Rmax 
#Intero = I.astype(int) # toglie la parte decimale 
#plt.hist(Intero,numero_bin)
#%%
# numeri interi con funzione predefinita di Python
#plt.hist( np.random.randint(Rmin,Rmax, size=100000) , numero_bin) # occhio che randint(1,3) ad esempio genera solo 1 o 2 poichè l'ultimo è escluso per il solito problema che non arriva alla fine quindi devi dare +1 !!!
# numeri reali con funzione predefinita di Python
#plt.hist( np.random.uniform(Rmin,Rmax, size=100000) , numero_bin)

fig, axs = plt.subplots(2, 2)
axs[0, 0].hist(R,numero_bin, color='skyblue')
axs[0, 0].set_title('Axis [0,0]')
axs[0, 1].hist( np.random.uniform(Rmin,Rmax, size=100000) , numero_bin,color='orange')
axs[0, 1].set_title('Axis [0,1]')
axs[1, 0].hist(intR,numero_bin,color='green')
axs[1, 0].set_title('Axis [1,0]')
axs[1, 1].hist( np.random.randint(Rmin,Rmax+1, size=100000) , numero_bin, color='red')
axs[1, 1].set_title('Axis [1,1]')

#for ax in axs.flat:
#    ax.set(xlabel='x-label', ylabel='y-label')
# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()
plt.savefig('prova istogrammi.pdf', dpi=650, transparent=False)
#%%
istogramma_come_piace_me(np.random.randint(Rmin,Rmax+1, size=100000))
istogramma_come_piace_me(intR)

#%%
#%%
# estrarre direzioni dall'origine nello spazio 3D. Generate a unit vector which points in a random direction in three-dimensional space.
campione = 1000/2 # quanti numeri vuoi estrarre dalla distribuzione?
phi = 2*np.pi * np.random.random(size=campione)
# phi = 0.0 + (2*np.pi - 0.0) * np.random.random(size=100000)
theta = np.arccos(1 - 2*np.random.random(size=campione))
# x_vett = np.sin(theta)*np.cos(phi)
# y_vett = np.sin(theta)*np.sin(phi)
# z_vett = np.cos(theta)
vett3D = np.array([ np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta) ])
# vett3D è una matrice 3 x campione poichè ciascuno dei [.., .., ..] è un array di "campione" elementi essendo stato generato sopra con np.random(size=campione)
# OCCHIO che invece questo è un tensore infatti vett3D.shape dà (3, 1, 10) cioè ognuno dei vettori "x","y" e "z" è messo per la profondità questo perchè avendo usato le funzioni sopra che davano un vettore non c'è bisogno di annidare [ [vettore]..
# vett3D = np.array([ [np.sin(theta)*np.cos(phi)],[np.sin(theta)*np.sin(phi)],[np.cos(theta)] ])

origine = np.zeros((3,campione))
# origine = np.array([np.zeros(campione),np.zeros(campione),np.zeros(campione)]) # uguale ma più macchinoso
fig = plt.figure(num=None, figsize=(8, 6), dpi=800, facecolor='w', edgecolor='k')
#ax = Axes3D(fig)
ax = fig.gca(projection='3d') # oppure anche così, non so che differenza ci sia
# ax.plot_wireframe([0,x_vett], [0,y_vett], [0,z_vett], color='red') # per disegnare solo l'asta del vettore
ax.quiver(origine[0],origine[1],origine[2], vett3D[0],vett3D[1],vett3D[2], normalize=False)
# ax.quiver(origine, vett3D, length=1, arrow_length_ratio=0.3, normalize=False)
# INVECE NON FUNZIONA! A quanto pare anche se sia origine che vett3D sono array di 3 array [ [..],[..],[..] ] le coordinate delle frecce devono essere date come singolo array, ad esempio [x1,x2,x3,...] e uguale per y e z, dove x1 è per la prima freccia, ecc... Per quello ax.quiver(origine, vett3D) non funziona
# ax.quiver(*origine, *vett3D) # questo invece funziona poichè l'asterisco spacchetta l'array che lo segue negli array che lo compongono, cioè fa questo: origine[0],origine[1],origine[2], vett3D[0],vett3D[1],vett3D[2] ed infatti è funziona!
ax.scatter(0,0,0,'o', color='red')
ax.set_xlim(-1.5,1.5)
ax.set_ylim(-1.5,1.5)
ax.set_zlim(-1.5,1.5) # oppure anche così, non so che differenza ci sia
# ax.set_xlim3d([-1.5, 1.5])
# ax.set_ylim3d([-1.5, 1.5])
# ax.set_zlim3d([-1.5, 1.5])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
# ax.set_aspect("equal") # serve ad usare un'unica scala vedere se usare o meno, far la prova se piace o no: se attiva schiaccia la figura
plt.show()

# for e in range(3): print( gino[:,e] ) # le colonne di gino. range parte da 0 e arriva a 2, a 3 ferma il tutto.

#%%
# estrarre numeri casuali da una distribuzione gaussiana col metodo della trasformata 2D

sigma_dev_standard = 1
raggio = np.sqrt( -2*(sigma_dev_standard**2) * np.log(1 - np.random.random(size=1000000)) )
theta1 = 2*np.pi * np.random.random(size=1000000)
# theta1 = 0.0 + (2*np.pi - 0.0) * np.random.random(size=1000000)
x = raggio * np.sin(theta1)
y = raggio * np.cos(theta1)
# questo è il caso con valore atteso o media mi=0, se invece la media non dovessere essere nulla, allora nell'exp(- (x - mi)^2/(2*sigma^2) ) ci sarebbe anche mi invece di essere solo x^2
# però non è un gran problema. Infatti puoi ridenominare con una nuova variabile chi=(x - mi) per cui passi a exp(- chi^2/(2*sigma^2) ) e ritrovi il caso appena trattato con l'unica differenza che poi:
# chi = x - mi = raggio * np.sin(theta1) per cui per generare il tuo x devi aggiungere la media che ora non sarà nulla, stessa cosa per y... La media quindi shifta in avanti o indietro la distribuzione normale N(0,1) centrata sullo zero e con deviazione unitaria
# x = mi + raggio * np.sin(theta1)
# y = mi + raggio * np.cos(theta1)
# Inoltre è possibile adattare x e y generati sopra per una qualsiasi deviazione standard senza necessariamente cambiare il sigma_dev_standard = 1 sopra
# questo perchè x, o anche y, può essere scritto portando fuori sigma^2 dal raggio e quindi x = sigma_dev_standard* np.sqrt( -2 * np.log(1 - np.random.random()) ) * np.sin(theta1) e i nuovi x e y con una sigma diversa da 1 sono dati da quelli calcolati prima moltiplicati per la nuova sigma:
# x_segue_sigma_diversa_da_uno = nuova_sigma * x
# y_segue_sigma_diversa_da_uno = nuova_sigma * y

plt.figure()
plt.hist(x,100)
#plt.show
# plt.clf()
plt.figure()
plt.hist(y,100,color='orange')
#plt.show
plt.figure()
plt.hist(np.random.normal(0, 1, size=1000000) ,100, color='green') # confronto con la funzione già fatta
#%%
# The rejection method

def funzione_da_usare_anche_non_normalizzata_va_bene(x):
    # in questo caso usiamo la Gaussiana normalizzata
    media = 0
    sigma = 1
    return (1/(np.sqrt(2* np.pi * sigma**2)) ) * np.exp(- ( (x - media)**2/(2*sigma**2) ) )
from scipy.integrate import quad # per dopo fare l'integrale
#%%
estremo_minore = -6*1 # dove 1=sigma che però hai dichiarato dentro la funzione
estremo_maggiore = 6*1
intervallo = np.linspace(estremo_minore, estremo_maggiore, 1000*(estremo_maggiore-estremo_minore)) # l'estremo maggiore e minore sono inclusi
f_max_nell_intervallo = max(funzione_da_usare_anche_non_normalizzata_va_bene(intervallo) )
quanti_numeri_vuoi_estrarre = 100000
numeri_estratti_dalla_distribuzione = []
contatore = 0
while len(numeri_estratti_dalla_distribuzione) < quanti_numeri_vuoi_estrarre:
    contatore +=1 # permette anche di decidere l'incremento ad ogni giro. Comunque è analogo al:
    # contatore = 1 + contatore # il più tradizionale
    numero_estratto = estremo_minore + (estremo_maggiore - estremo_minore) * np.random.random()
    if np.random.random() < (funzione_da_usare_anche_non_normalizzata_va_bene(numero_estratto)/f_max_nell_intervallo):
        numeri_estratti_dalla_distribuzione.append(numero_estratto)
# Ora converto la lista dei miei nuemri estratti in un array/vettore di np così può essere usato per le operazioni su vettori, mentre la lista no!
# Infatti se fai funzione_da_usare_anche_non_normalizzata_va_bene(numeri_estratti_dalla_distribuzione) dà errore!
numeri_estratti_dalla_distribuzione_nparray = np.array(numeri_estratti_dalla_distribuzione)
print('Hai fatto', contatore, 'operazioni di estrazione e hai estratto ben', 2*contatore, 'numeri casuali uniformi tra [0,1) per tenerne in totale solo', len(numeri_estratti_dalla_distribuzione))
# print('I numeri estratti tenuti sono', numeri_estratti_dalla_distribuzione, 'che sono in totale', len(numeri_estratti_dalla_distribuzione))
plt.hist(numeri_estratti_dalla_distribuzione, 100) # gli istogrammi possono anche essere fatti dalle liste non importa che siano array np

# np.empty((0,3), int) # per inizializzare un np.array vuoto
#%%
risultato_dell_integrale_della_funzione_da_usare = quad(funzione_da_usare_anche_non_normalizzata_va_bene, estremo_minore, estremo_maggiore)
print('L\'errore (absolute error) nell\'integrale calcolato con la funzione quad di Scipy è', risultato_dell_integrale_della_funzione_da_usare[1])
chiamate_totali_teoriche = (2*f_max_nell_intervallo*(estremo_maggiore-estremo_minore) )/risultato_dell_integrale_della_funzione_da_usare[0]
print('Ci vogliono', chiamate_totali_teoriche, 'chiamate del generatore uniforme [0,1) per generare un numero estratto dalla Gaussiana col rejection method') # invece il secondo argomento [1] è l'errore assoluto
# significa che ci vogliono quasi 10 chiamate (è 9.57) del generatore uniforme [0,1) per generare un numero gaussiano: infatti per generare 100000 numeri avresti bisogno all'incirca di 957461 tentativi e lanciando l'algoritmo sopra ce ne sono voluti, ad esempio, 957066. Più o meno torna
    
    
#%%

# COSTRUIRE GRAFO DA FUNZIONE GENERATRICE
numero_nodi = 200
probabilità_edge_link = 2/100 # 2%
degree_distribuzione = np.random.binomial(numero_nodi-1, probabilità_edge_link, size=numero_nodi)
plt.figure()
plt.hist(degree_distribuzione)
plt.figure()
istogramma_come_piace_me(degree_distribuzione)


def ER(n, p):
    V = set([v for v in range(n)])
    E = set()
    for combination in combinations(V, 2):
        a = random()
        if a < p:
            E.add(combination)

#%%
def generatore_grafo_matrice_adiacenza_da_binomiale(quanti_nodi, probabilità_di_un_edge):
    degree_distribuzione = np.random.binomial(quanti_nodi-1, probabilità_di_un_edge, size=quanti_nodi)
    lista_nodi = [v for v in range(quanti_nodi)] # il primo nodo della lista sarà "zero" e l'ultimo "quanti_nodi - 1". Se vuoi invece che parta da 1 e arrivi all'ultimo compreso devi fare: [v for v in range(1,quanti_nodi+1)]
    contatore = lista_nodi[0] # inizializzo il contatore al primo elemento della lista cioè al nodo 0 o al nodo 1 a seconda che abbia fatto prima range(quanti_nodi) oppure range(1,quanti_nodi+1)
    matrice_adiacenza = np.zeros((quanti_nodi,quanti_nodi), dtype=int) # matrice quadrata NxN con N=numero nodi del grafo
    for degree in degree_distribuzione:
        lista_nodi_mescolata = []
        lista_nodi_mescolata = lista_nodi.copy() # questo è il modo giusto, invece quello sotto è sbagliato:
        # lista_nodi_mescolata = lista_nodi # ATTENTO che questo copia l'indirizzo della lista_nodi non crea una nuova lista, per cui tutte le modifiche che farai a lista_nodi_mescolata in reltà verranno fatte su lista_nodi spolpandola man mano!!!
        lista_nodi_mescolata.remove(contatore)
        np.random.shuffle(lista_nodi_mescolata) # attento che non crea una nuova lista ma scombussola quella originale!
        for colonna_matrice in range(degree):
            matrice_adiacenza[contatore, lista_nodi_mescolata[colonna_matrice]] = 1
        contatore +=1 # contatore = contatore + 1
    return matrice_adiacenza
# se ad esempio ogni nodo/banca deve avere in media 5 link che escono e partono da lui, ne consegue che il network dovrà avere almeno 6 nodi. Esistono 2 diversi modi di calcolare il 
# average degree o mean degree z=<k>=(Sum_{0}^{n} k_i)/n dove n=# totale di nodi, ma siccome
# la somma sulla degree sequence in un network diretto è il numero totale di link, abbiamo quindi
# z = # totale di link / # totale di nodi = m/n perciò  # totale di link = m = zn
# z = (n-1)p questo risultato vale per i random network non diretti,
# non so se vale anche per quelli diretti poichè nei non diretti <k>=2m/n !!!
#%%
adjacency_matrix = generatore_grafo_matrice_adiacenza_da_binomiale(100, 8/100) # (5, 50/100)
print(adjacency_matrix)
# G = nx.from_numpy_matrix(adjacency_matrix) # ATTENZIONE che pur essendo la matrice di adiacenza quella di un grafo diretto, se non specifichi DiGraph come metodo ti disegna comunque un grafo non diretto
G = nx.from_numpy_matrix(adjacency_matrix, create_using=nx.DiGraph())
pos = nx.spring_layout(G)

fig=plt.gcf()
ax=plt.gca()
pos=nx.circular_layout(G, center=(0, 0))
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'))

nx.draw_networkx(G, pos, arrows=True, arrowstyle = '-|>')
plt.title("Direct Binomial Graph Generation Example")
plt.show()