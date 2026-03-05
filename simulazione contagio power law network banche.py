# -*- coding: utf-8 -*-
"""
Created on Mon May 24 02:06:28 2021

@author: Gabriele
"""


import numpy as np
import matplotlib.pyplot as plt
import time
np.random.seed(420) # così con lo stesso seed (qua 420 ma può essere qualunque numero) ottieni sempre gli stessi numeri "casuali". Oppure puoi commentare questa riga, ma i risultati non saranno più riproducibili perchè ogni volta otterrai numeri casuali diversi!
# Importantly, seeding the Python pseudorandom number generator does not impact the NumPy pseudorandom number generator. It must be seeded and used separately. Python ha random.seed() che viene da import random mentre NumPy ha np.random.seed() che viene da import numpy. Se usi qualcosa della prima es random.random() devi specificare il seed di entrambe

# -------
# PER TOGLIERE DUPLICATI DA UNA LISTA:
    # from itertools import filterfalse
    # lista_provacopia = [*filterfalse(lambda i: i == 1, lista_provacopia)]
# -------
# nota che True+True=2 e False+False=0 siccome per Python True=1 e False=0
# import networkx as nx

#import collections
#from mpl_toolkits.mplot3d import Axes3D
#from itertools import combinations
#%%        
import powerlaw
import collections
def istogramma_come_piace_me(vettore):
    # funziona solo per numeri interi
    ordinatodalmaggiorealminore = sorted(vettore, reverse=True)  # ordinati dal più grande al più piccolo
    dizionarioquantevoltesiripeteognivalore = collections.Counter(ordinatodalmaggiorealminore) # qua serve import collections
    valoridelvettore, conteggi = zip(*dizionarioquantevoltesiripeteognivalore.items())
    fig, ax = plt.subplots()
    conteggi_arraynumpy = np.array(conteggi) # per avere il # nodi come percentuale del network. DEVI TOGLIARE IL COMMNETO ALLA RIGA QUA SOTTO e COMMENTARE LA SUCCESSIVA!
#    plt.bar(valoridelvettore, conteggi_arraynumpy/len(vettore), width=0.9, align='edge') # oppure di default il numero viene centrato e la grandezza del bin è width=0.8, così:
    plt.bar(valoridelvettore, conteggi, width=0.9, align='edge') # oppure di default il numero viene centrato e la grandezza del bin è width=0.8, così:
#    plt.bar(valoridelvettore, conteggi)
    fig.tight_layout()
#%%
prova=generatore_matrice_adiacenza_con_z_voluto_da_power_law_preferential_attachment(1000,10)
kappa_degree_sequence = np.sum(prova, axis=1)
jei_degree_sequence = np.sum(prova, axis=0)
istogramma_come_piace_me(kappa_degree_sequence)
istogramma_come_piace_me(jei_degree_sequence)
results = powerlaw.Fit(jei_degree_sequence)
# results = powerlaw.Fit(kappa_degree_sequence, xmin = 7) # per xmin=7, invece che farlo calcolare a lui, viene in entrambe quasi alpha=3. Credo voglia dire che butta via tutti i degree < xmin
print('\n \nL\'esponente della power-law è:', results.power_law.alpha)
print('\n','Il valore minimo stimato da scartare è: ', results.power_law.xmin, sep = '') # sep='' toglie lo spazio che sennò verrebbe prima di "Il valore" dopo l'andare a capo \n
R, p = results.distribution_compare('power_law', 'lognormal')

# PIU' ALTO E' z PIU' LINK CI SONO PIU' TEMPO CI VUOLE
#volte=1000
# for ci in range(volte):
#     prova=generatore_matrice_adiacenza_con_z_voluto_da_power_law_in_preferential_attachment(1000,5)
#%%

# Funzione per generare un network con esattamente z di degree medio e calcolo della probabilità conseguente e aggiustamento della degree sequence
def generatore_matrice_adiacenza_con_z_voluto_da_power_law_preferential_attachment(nodi_totali, z_voluto):
    # se ad esempio ogni nodo/banca deve avere in media 5 link che escono e partono da lui, ne consegue che il network dovrà avere almeno 6 nodi. Esistono 2 diversi modi di calcolare il 
    # average degree o mean degree z=<k>=(Sum_{0}^{n} k_i)/n dove n=# totale di nodi, ma siccome
    # la somma sulla degree sequence in un network diretto è il numero totale di link, abbiamo quindi
    # z = # totale di link / # totale di nodi = m/n perciò  # totale di link = m = zn   (Nei network non diretti è invece <k>=2m/n quindi m = zn/2 )
    link_totali_necessari = z_voluto * nodi_totali # occhio che può non essere un numero intero siccome z può avere la virgola, andrà convertito in int
    # alpha_esponente_powerlaw = 2 + a/c # in Newman manuale dove c è mean out-degree <k>=z e consiglia di prendere a=c oppure in Price viene preso a=1
    alpha_esponente_powerlaw = 3
    # viene una power-law che è p_q = q^{-alpha} = q^-3 dove q è l'in-degree j nella notazione di Newman 
    a_parametro_probabilita = z_voluto * (alpha_esponente_powerlaw - 2) # che è uguale a z così: a=z
    phi_probabilita = z_voluto / (z_voluto + a_parametro_probabilita) # di fatto viene phi= a/2a = 1/2 = 50% = 0.5
    # Questo seguendo Newman e Price e Krapivsky e Redner era per la power-law della distribuzione dell'in-degree ma noi la vogliamo anche per l'out-degree
    # Ora le scegliamo uguali ma costruiamo il programma per permettere il caso che non lo siano
    # p_j = j^{-alpha} = j^-3  per in-degree
    # p_k = k^{-alpha_out} = k^-3  per out-degree
    alpha_out_esponente_powerlaw = 3
    a_out_parametro_probabilita = z_voluto * (alpha_out_esponente_powerlaw - 2) # a = z = <k> = <j>
    phi_out_probabilita = z_voluto / (z_voluto + a_out_parametro_probabilita) # di fatto viene phi= a/2a = 1/2 = 50% = 0.5
    percentuale_link_usare_subito = 1/10 # parametro da impostare, ad esempio 10% del numero totale, considera che se z=1 e n=1000 poi ci sono 1000 link e quindi qua ne bruci 100, però se n=50 sono 5
    link_per_inizializzare = percentuale_link_usare_subito * link_totali_necessari # occhio che non è un numero intero poichè una frazione in Python restituisce sempre un numero decimale, andrà convertito in int
    matrice_adiacenza = np.zeros((nodi_totali,nodi_totali), dtype=int) # matrice quadrata nxn con n=numero nodi del grafo
    lista_link_uscenti_creati = []
    lista_link_entranti_creati = []
    for ni in range(int(round(link_per_inizializzare))):
        while True:
            nodo_da_cui_esce_link = np.random.randint(nodi_totali) # è un int
            nodo_in_cui_entra_link = np.random.randint(nodi_totali) # è un int
            # bisogna proteggersi dai self loop ovvero dal mettere un 1 sulla diagonale della matrice
            if nodo_da_cui_esce_link != nodo_in_cui_entra_link:
                if matrice_adiacenza[nodo_da_cui_esce_link, nodo_in_cui_entra_link] == 0:
                    # bisogna proteggersi dal fatto che quel link sia già stato creato in passato
                    matrice_adiacenza[nodo_da_cui_esce_link, nodo_in_cui_entra_link] = 1
                    lista_link_uscenti_creati.append(nodo_da_cui_esce_link)
                    lista_link_entranti_creati.append(nodo_in_cui_entra_link)
                    break        
    for ci in range(int(round(link_totali_necessari - link_per_inizializzare))):
        while True:
            if phi_out_probabilita > np.random.random():
                nodo_da_cui_esce_link = np.random.choice(lista_link_uscenti_creati)
                if phi_probabilita > np.random.random():
                    nodo_in_cui_entra_link = np.random.choice(lista_link_entranti_creati) # nodo hub potrebbe puntare a nodo hub, accade 1/4 delle volte
                else:
                    nodo_in_cui_entra_link = np.random.randint(nodi_totali) # # nodo hub potrebbe puntare a nodo anonimo qualunque, accade 1/4 delle volte
            else:
                if phi_probabilita > np.random.random():
                    nodo_da_cui_esce_link = np.random.randint(nodi_totali)
                    nodo_in_cui_entra_link = np.random.choice(lista_link_entranti_creati) # nodo anonimo qualunque potrebbe puntare a nodo hub, accade 1/4 delle volte
                else:
                    nodo_da_cui_esce_link = np.random.randint(nodi_totali)
                    nodo_in_cui_entra_link = np.random.randint(nodi_totali) # nodo anonimo qualunque potrebbe puntare a nodo anonimo qualunque, accade 1/4 delle volte
            if nodo_da_cui_esce_link != nodo_in_cui_entra_link:
                if matrice_adiacenza[nodo_da_cui_esce_link, nodo_in_cui_entra_link] == 0:
                    matrice_adiacenza[nodo_da_cui_esce_link, nodo_in_cui_entra_link] = 1
                    lista_link_uscenti_creati.append(nodo_da_cui_esce_link)
                    lista_link_entranti_creati.append(nodo_in_cui_entra_link)
                    break
    return matrice_adiacenza

# Funzione per creare i bilanci della banche del network
def generatore_matrice_pesi_bilanci_banche(matrice_adiacenza, capital_buffer):
    numero_banche = len(matrice_adiacenza) # la matrice di adiacenza ovviamente è quadrata
    # per la direzione uso la convenzione che A_{i,j}=1 significa che c'è un link che va DAL nodo i AL nodo j. Newman usa l'opposto!
    out_degree_delle_banche_lista_debiti = np.sum(matrice_adiacenza, axis=1) # perciò la somma degli elementi di ogni riga della matrice indica tutti i link che ESCONO dal nodo associato a quella riga e la sommatoria avviene sull'indice della colonna: k^{out}_{i}=Sum_{j=1}^{n} A_{i,j}  poi vabbè in Python parte da j=0 e finisce a n-1
    in_degree_delle_banche_lista_asset = np.sum(matrice_adiacenza, axis=0) # la somma degli elementi di ogni colonna della matrice indica tutti i link che ENTRANO nel nodo associato a quella colonna e la sommatoria avviene sull'indice della riga: k^{in}_{j}=Sum_{i=1}^{n} A_{i,j}
    # Ricordati che i soldi seguono la direzione dei link quindi
    # i link uscenti da una banca sono i suoi debiti interbancari (è come se la banca perdesse soldi)
    # e quelli entranti sono i suoi asset cioè i crediti che vanta dalle altre banche poichè ha prestato soldi a loro. Infatti quei link sono uscenti per quelle banche poichè sono loro debiti
    asset_interbanc_totale_di_ogni_banca_A_IB_i_percentuale_bilancio = 0.2 # 20% del bilancio ed è distribuita sui link ENTRANTI nella banca i ovvero ogni peso w_i della matrice dei pesi W vale 0.2/j_i o 0.2/k^{in}_{i} e quindi nella colonna i della matrice W ci saranno, al posto degli 1 della matrice di adiacenza, tanti numeri tuti uguali che sono i pesi w_i della banca i
    # capital_buffer = 0.04 # 4% è la riserva per coprire le perdite sugli asset interbancari, se queste perdite totali sono >4% la banca fallise perciò vanno nel bilancio col segno + così se il bilancio <0 la banca è fallita!
    mutui_A_M_i_illiquid_external_assets_mortgages_percentuale_bilancio = 1-asset_interbanc_totale_di_ogni_banca_A_IB_i_percentuale_bilancio # ovvero 0.8 cioè 80% del bilancio della voce attivi 
    W_matrice_pesi_esposizioni_bancarie = matrice_adiacenza.copy() # però ci dovranno andare dei pesi con la virgola per cui non puà più essere int come era A ma deve diventare float
    W_matrice_pesi_esposizioni_bancarie = W_matrice_pesi_esposizioni_bancarie.astype(dtype=float) # oppure astype(numpy.float32)
    bilanci_bancari_matrice_n_x_5 = np.ones((numero_banche,3), dtype=float) # per ora le colonne sono solo 3 perchè mettiamo le percentuali fissate che sono gli attivi: in ordine capital buffer, asset interbancari, mutui ovvero 0.04, 0.2 e 0.8 (se hanno link entranti, sennò è 0 e 1). Poi dopo le altre due colonne che mancano saranno date CON SEGNO - da i debiti interbancari e i depositi
    bilanci_bancari_matrice_n_x_5[:,0] = bilanci_bancari_matrice_n_x_5[:,0]*capital_buffer
    bilanci_bancari_matrice_n_x_5[:,1] = bilanci_bancari_matrice_n_x_5[:,1]*asset_interbanc_totale_di_ogni_banca_A_IB_i_percentuale_bilancio
    bilanci_bancari_matrice_n_x_5[:,2] = bilanci_bancari_matrice_n_x_5[:,2]*mutui_A_M_i_illiquid_external_assets_mortgages_percentuale_bilancio
    for indice_colonna in range(numero_banche):
        if in_degree_delle_banche_lista_asset[indice_colonna] == 0:
            bilanci_bancari_matrice_n_x_5[indice_colonna,2] = 1
            bilanci_bancari_matrice_n_x_5[indice_colonna,1] = 0            
        else:
            W_matrice_pesi_esposizioni_bancarie[:,indice_colonna] = W_matrice_pesi_esposizioni_bancarie[:,indice_colonna]*(asset_interbanc_totale_di_ogni_banca_A_IB_i_percentuale_bilancio / in_degree_delle_banche_lista_asset[indice_colonna]) # è stato necessario l'if sopra perchè se in_degree_delle_banche_lista_asset[indice_colonna]=0 poichè quella banca non ha asset interbancari ovvero link entranti poi ti trovi a dividere 0.2 per zero e viene inf che dopo crea dei nan quando viene sommato e le banche diventano immortali e non falliscono mai
    debiti_interbanc_vettore_L_IB = - np.sum(W_matrice_pesi_esposizioni_bancarie, axis=1) # i debiti interbancari di ogni banca sono dati dalla somma degli elementi della corrispondente riga della matrice W dei pesi cioè i link uscenti dalla banca quindi l'indice della sommatoria che varia è il j (cioè delle colonne) mentre l'indice i delle righe è tenuto fisso, qua il risultato è il vettore dei debiti di ogni banca. Il segno meno indica che andranno nel passivo del bilancio!
    debiti_interbanc_vettore_L_IB = debiti_interbanc_vettore_L_IB[:, np.newaxis] # il grosso problema nascosto di Python è che esiste differenza tra array (n,) e (n,1) e molte funzioni come np.sum() creano array (n,) ma se poi questo array lo devi aggiungere ad una matrice che è un array (n,5) allora np.hstack() fornisce errore perchè la matrice ha un indice per le colonne ma il vettore (n,) per l'appunto no! Con np.newaxis crei questo indice e dopo l'array diventa (n,1) e non ci sono problemi ad aggiungere questo vettore colonna come nuova colonna della matrice
    depositi_dei_clienti_vettore_D_passività = - (1+debiti_interbanc_vettore_L_IB) # deve avere segno meno poichè nel bilancio va nelle passività e sarebbe 1-L_IB e col meno -(1-L_IB) ma siccome hai dato segno - a L_IB diventa -(1 - (-L_IB))=-(1+L_IB)=-1-L_IB
    bilanci_bancari_matrice_n_x_5 = np.hstack((bilanci_bancari_matrice_n_x_5, debiti_interbanc_vettore_L_IB, depositi_dei_clienti_vettore_D_passività)) # così passa da essere una matrice nx3 a essere finalmente nx5 cioè ho aggiunto due colonne alla fine
    return W_matrice_pesi_esposizioni_bancarie, bilanci_bancari_matrice_n_x_5
#%%

tempo_dinizio = time.time()
#z_average_degree_voluti_vettore = np.linspace(0.25, 10.5, 42) # 0.25, 0.5, 0.75, 1, 1.25, ..., 10.25, 10.5
# PARE CHE IL PRIMO SIA TROPPO PER QUESTA VERSIONE: ci vogliono 16 minuti per generare 1000 matrici di adiacenza con tutte z=5
z_average_degree_voluti_vettore = np.linspace(0.5, 10.5, 21) # 0.5, 1, 1.5, 2, 2.5, ..., 10, 10.5
#z_average_degree_voluti_vettore = [1,2,3,4,5,6,7,8,9,10]

numero_banche_n_ogni_simulazione = 1000 # 1000 
numero_simulazioni_per_ogni_valore_di_z = 1000 # 1000
# Già solo per 100 simulazioni con 1000 banche ci vogliono 1 ora e 17 minuti. Per 500 simulazioni e 500 banche serve 1 ora e 33 minuti
# Infine, per quella esatta, 1000 simulazioni con 1000 banche servono ben 14 ore e 20 minuti !!!
capital_buffer = 0.04 # poi diventerà un vettore nel programma successivo!
frequenza_contagio = []
estensione_contagio_percentuale_banche_fallite = []

for z_voluto in z_average_degree_voluti_vettore:
    frequenza_contagio_raccolta_dati = 0
    estensione_contagio_raccolta_dati = []
    for simulazione in range(numero_simulazioni_per_ogni_valore_di_z):
        # range parte da 0 e arriva a numero_simulazioni_per..-1 quindi a 999 però incluso lo zero sono comunque 1000 ripetizioni/simulazioni/esperimenti, perciò va bene. 
        matrice_adiacenza_network_bancario = generatore_matrice_adiacenza_con_z_voluto_da_power_law_preferential_attachment(numero_banche_n_ogni_simulazione, z_voluto)
        W_matrice_pesi_esposizioni_bancarie, bilanci_bancari_matrice_n_x_5 = generatore_matrice_pesi_bilanci_banche(matrice_adiacenza_network_bancario, capital_buffer) # anche se hanno gli stessi nomi che comparivano all'interno del codice della funzione non preoccuparti non entrano in conflitto perchè non ha accesso ai nomi del codice della funzione, non sono globali: l'hai testato!
        banca_casuale_da_far_fallire = np.random.randint(numero_banche_n_ogni_simulazione) # va da 0 al numero-1 in parentesi
        numero_banche_fallite_adesso = 1 # per ora c'è solo una che è "banca_casuale_da_far_fallire" fatta fallire a forza però poi qua aggiorneremo col numero totale ad ogni ondata di fallimenti 
        numero_banche_fallite_prima = 0
        lista_banche_fallite = [ banca_casuale_da_far_fallire ]
        W_matrice_pesi_esposizioni_bancarie[banca_casuale_da_far_fallire,:] = 0 # è sufficiente far così per mettere dei 0.0 su tutta una riga
        while numero_banche_fallite_adesso > numero_banche_fallite_prima:
            # ora devo ricalcolare i bilanci di tutte le banche a seguito della perdita dei crediti persi per il fallimento della banca che ha cancellato la sua riga corrispondente ovvero i suoi debiti, i link pesati uscenti da lei
            # in pratica però solo 2 voci del bilancio vanno ricalcolate: asset interbancari e debiti interbancari. Gli asset interb. sono le colonne di W e i debiti interb. sono le righe di W. Invece i mutui A_M e i depositi D rimangono tali, sono fissati per tutta la simulazione
            asset_interb_vettore_A_IB_dopo_fallimento = np.sum(W_matrice_pesi_esposizioni_bancarie, axis=0)
            debiti_interb_vettore_L_IB_dopo_fallimento = np.sum(W_matrice_pesi_esposizioni_bancarie, axis=1)
            bilanci_bancari_matrice_n_x_5[:,1]= asset_interb_vettore_A_IB_dopo_fallimento
            bilanci_bancari_matrice_n_x_5[:,3]= -debiti_interb_vettore_L_IB_dopo_fallimento
            stato_patrimoniale_banche_saldo_balance_sheet= np.sum(bilanci_bancari_matrice_n_x_5, axis=1) # le banche fallite ORA hanno saldo < 0. Poi dopo quando verranno effettivamente fatte fallire cancellando con zeri la loro riga corrispondente della matrice W e ricalcolati asset e debiti, a quel punto il loro bilancio diventerà >0 poichè perdono i loro debiti interb. (abbiamo appena detto che la riga di W viene riempita di 0) però rimangono asset interb., quindi se non salvi gli indici delle banche fallite ora, poi in futuro non potrai più saperlo!!!!
            # attento che la banca estratta a caso fallita con la forza NON ha un bilancio negativo bensì è aumentato ed è divenatto ancora più positivo poichè sono scomparsi i suoi debiti ma rimasti i suoi asset (che comunque devono rimanere), quindi paradossalmente la sua posizione è migliorata anch se è fallita. Una soluzione potrebbe essere quella di aggiornare il bilancio bancario solo alla voce asset interb. e NON a quella debiti interbancari che effettivamente potrebbe che essere non servano
            indici_banche_fallite = np.transpose((stato_patrimoniale_banche_saldo_balance_sheet<0).nonzero())
            indici_banche_fallite = indici_banche_fallite.reshape(len(indici_banche_fallite))
            indici_banche_fallite = indici_banche_fallite.tolist() # ora non è più un array ma così diventa una lista
            for indice_lista in indici_banche_fallite:
                # hai fatto bene ad usare un contatore per indici_banche_fallite che prenda singolarmente ogni elemento della lista perchè se tu avessi aggiunto direttamente la lista sarebbe venuta una lista in una lista tipo così [..[]..]
                if indice_lista not in lista_banche_fallite:
                    lista_banche_fallite.append(indice_lista)
                    W_matrice_pesi_esposizioni_bancarie[indice_lista,:] = 0 # è sufficiente far così per mettere dei 0.0 su tutta una riga
            numero_banche_fallite_prima = numero_banche_fallite_adesso
            # numero_banche_fallite_adesso = numero_banche_fallite_adesso + len(indici_banche_fallite) # se non ti fidi che la lista indici_banche_fallite contenga effettivamente le banche fallite giuste è meglio usare il metodo qua sotto
            numero_banche_fallite_adesso = len(lista_banche_fallite) # dovrebbe essere indifferente quale metodo usare
            # ATTENTO che è possibile che una banca già fallita, ritornata positiva perchè vengono cancellati i suoi debiti come detto sopra, poi rifallisca siccome il bilancio torna negativo a causa del fallimento di altre banche di cui aveva asset! Però non dovrebbe creare un problema siccomec'è la lista che tiene conto delle banche già fallite e aggiunge la nuova banca solo se non presente
        if len(lista_banche_fallite) > (0.05*numero_banche_n_ogni_simulazione):
            frequenza_contagio_raccolta_dati = 1 + frequenza_contagio_raccolta_dati
            percentuale_banche_fallite = (len(lista_banche_fallite))/numero_banche_n_ogni_simulazione
            estensione_contagio_raccolta_dati.append(percentuale_banche_fallite)
    if frequenza_contagio_raccolta_dati == 0:
        estensione_contagio_percentuale_banche_fallite.append(0)
    else:
        estensione_contagio_percentuale_banche_fallite.append(sum(estensione_contagio_raccolta_dati)/frequenza_contagio_raccolta_dati)
    frequenza_contagio.append(frequenza_contagio_raccolta_dati/numero_simulazioni_per_ogni_valore_di_z)

plt.scatter(z_average_degree_voluti_vettore, estensione_contagio_percentuale_banche_fallite, marker='o', c='red', label='Extent of contagion') # depthshade=True provare
plt.scatter(z_average_degree_voluti_vettore, frequenza_contagio, marker='x', c='black', label='Frequency of contagion') # depthshade=True provare
plt.scatter(0, 0, marker='o', c='red') # depthshade=True provare
plt.scatter(0, 0, marker='x', c='black') # depthshade=True provare
# PER METTERE LA LEGENDA FUORI DAL GRAFICO e salvare correttamente l'immagine senza tagliarla
plt.legend(bbox_to_anchor=(1.01,1), loc="upper left") # senza "borderaxespad=0" la posiziona poco sotto all'asse orizzontale in alto, con invece a filo
# plt.legend(bbox_to_anchor=(1.04,1), loc="upper left", borderaxespad=0, prop={'size': 9})
#plt.legend(loc='upper right', prop={'size': 6}) # upper right o center right. size=7 o 8 o 6
#plt.legend()
#font = {'family':'serif','color':'darkred','weight':'normal','size': 10.7,}
#plt.title('Figure 3: The benchmark case 1000 banche 1000 simulazioni ogni z',fontdict = font)
plt.xlabel('Average degree $z$')
plt.ylabel('Defaults (%)')
plt.grid()
plt.xlim(-0.2,10.8)
# plt.savefig('contagio grafico 1000 banche 1000 simulazioni ogni z da 0.5 powerlaw in e out.jpg', dpi=950, transparent=False, bbox_inches="tight")
# Per caso senza legenda fuori dal grafico:
#plt.savefig('contagio grafico 1000 banche 500 simulazioni ogni z corretto.jpg', dpi=850, transparent=False)
plt.show()

print("--- %s seconds ---" % (time.time() - tempo_dinizio))
print("--- %s minutes ---" % (((time.time() - tempo_dinizio))/60) )
print("--- %s hours ---" % (((time.time() - tempo_dinizio))/(60*60) ) )
#%%

# GRAFICI CON 3 DIVERSI CAPITAL BUFFER 3%, 4% e 5% A CONFRONTO. In pratica è la copia del programma precedente, ma con l'aggiunta di un ciclo per i diversi capital buffer.
z_average_degree_voluti_vettore = np.linspace(0.5, 13.5, 27) # 0.5, 1, 1.5, 2, 2.5, ..., 13, 13.5
# z_average_degree_voluti_vettore = np.linspace(0.25, 13.5, 54) # 0.25, 0.5, 0.75, 1, 1.25, ..., 10.25, 10.5
#z_average_degree_voluti_vettore = np.linspace(0.25, 10.5, 42) # 0.25, 0.5, 0.75, 1, 1.25, ..., 10.25, 10.5
#z_average_degree_voluti_vettore = np.linspace(0.5, 10.5, 21) # 0.5, 1, 1.5, 2, 2.5, ..., 10, 10.5
#z_average_degree_voluti_vettore = [1,2,3,4,5,6,7,8,9,10]

numero_banche_n_ogni_simulazione = 1000 # 1000 
numero_simulazioni_per_ogni_valore_di_z = 1000 # 1000 # già 1000 simulazioni è abbastanza in durata del calcolo per 500 banche
vettore_dei_capital_buffer = [0.03, 0.04, 0.05] # ora è un vettore, una lista in realtà
frequenza_contagio = []
estensione_contagio_percentuale_banche_fallite = []

for capital_buffer in vettore_dei_capital_buffer:
    for z_voluto in z_average_degree_voluti_vettore:
        frequenza_contagio_raccolta_dati = 0
        estensione_contagio_raccolta_dati = []
        for simulazione in range(numero_simulazioni_per_ogni_valore_di_z):
            # range parte da 0 e arriva a numero_simulazioni_per..-1 quindi a 999 però incluso lo zero sono comunque 1000 ripetizioni/simulazioni/esperimenti, perciò va bene. 
            matrice_adiacenza_network_bancario = generatore_matrice_adiacenza_con_z_voluto_da_power_law_preferential_attachment(numero_banche_n_ogni_simulazione, z_voluto)
            W_matrice_pesi_esposizioni_bancarie, bilanci_bancari_matrice_n_x_5 = generatore_matrice_pesi_bilanci_banche(matrice_adiacenza_network_bancario, capital_buffer) # anche se hanno gli stessi nomi che comparivano all'interno del codice della funzione non preoccuparti non entrano in conflitto perchè non ha accesso ai nomi del codice della funzione, non sono globali: l'hai testato!
            banca_casuale_da_far_fallire = np.random.randint(numero_banche_n_ogni_simulazione) # va da 0 al numero-1 in parentesi
            numero_banche_fallite_adesso = 1 # per ora c'è solo una che è "banca_casuale_da_far_fallire" fatta fallire a forza però poi qua aggiorneremo col numero totale ad ogni ondata di fallimenti 
            numero_banche_fallite_prima = 0
            lista_banche_fallite = [ banca_casuale_da_far_fallire ]
            W_matrice_pesi_esposizioni_bancarie[banca_casuale_da_far_fallire,:] = 0 # è sufficiente far così per mettere dei 0.0 su tutta una riga
            while numero_banche_fallite_adesso > numero_banche_fallite_prima:
                # ora devo ricalcolare i bilanci di tutte le banche a seguito della perdita dei crediti persi per il fallimento della banca che ha cancellato la sua riga corrispondente ovvero i suoi debiti, i link pesati uscenti da lei
                # in pratica però solo 2 voci del bilancio vanno ricalcolate: asset interbancari e debiti interbancari. Gli asset interb. sono le colonne di W e i debiti interb. sono le righe di W. Invece i mutui A_M e i depositi D rimangono tali, sono fissati per tutta la simulazione
                asset_interb_vettore_A_IB_dopo_fallimento = np.sum(W_matrice_pesi_esposizioni_bancarie, axis=0)
                debiti_interb_vettore_L_IB_dopo_fallimento = np.sum(W_matrice_pesi_esposizioni_bancarie, axis=1)
                bilanci_bancari_matrice_n_x_5[:,1]= asset_interb_vettore_A_IB_dopo_fallimento
                bilanci_bancari_matrice_n_x_5[:,3]= -debiti_interb_vettore_L_IB_dopo_fallimento
                stato_patrimoniale_banche_saldo_balance_sheet= np.sum(bilanci_bancari_matrice_n_x_5, axis=1) # le banche fallite ORA hanno saldo < 0. Poi dopo quando verranno effettivamente fatte fallire cancellando con zeri la loro riga corrispondente della matrice W e ricalcolati asset e debiti, a quel punto il loro bilancio diventerà >0 poichè perdono i loro debiti interb. (abbiamo appena detto che la riga di W viene riempita di 0) però rimangono asset interb., quindi se non salvi gli indici delle banche fallite ora, poi in futuro non potrai più saperlo!!!!
                # attento che la banca estratta a caso fallita con la forza NON ha un bilancio negativo bensì è aumentato ed è divenatto ancora più positivo poichè sono scomparsi i suoi debiti ma rimasti i suoi asset (che comunque devono rimanere), quindi paradossalmente la sua posizione è migliorata anch se è fallita. Una soluzione potrebbe essere quella di aggiornare il bilancio bancario solo alla voce asset interb. e NON a quella debiti interbancari che effettivamente potrebbe che essere non servano
                indici_banche_fallite = np.transpose((stato_patrimoniale_banche_saldo_balance_sheet<0).nonzero())
                indici_banche_fallite = indici_banche_fallite.reshape(len(indici_banche_fallite))
                indici_banche_fallite = indici_banche_fallite.tolist() # ora non è più un array ma così diventa una lista
                for indice_lista in indici_banche_fallite:
                    # hai fatto bene ad usare un contatore per indici_banche_fallite che prenda singolarmente ogni elemento della lista perchè se tu avessi aggiunto direttamente la lista sarebbe venuta una lista in una lista tipo così [..[]..]
                    if indice_lista not in lista_banche_fallite:
                        lista_banche_fallite.append(indice_lista)
                        W_matrice_pesi_esposizioni_bancarie[indice_lista,:] = 0 # è sufficiente far così per mettere dei 0.0 su tutta una riga
                numero_banche_fallite_prima = numero_banche_fallite_adesso
                numero_banche_fallite_adesso = len(lista_banche_fallite) # dovrebbe essere indifferente quale metodo usare
                # ATTENTO che è possibile che una banca già fallita, ritornata positiva perchè vengono cancellati i suoi debiti come detto sopra, poi rifallisca siccome il bilancio torna negativo a causa del fallimento di altre banche di cui aveva asset! Però non dovrebbe creare un problema siccomec'è la lista che tiene conto delle banche già fallite e aggiunge la nuova banca solo se non presente
            if len(lista_banche_fallite) > (0.05*numero_banche_n_ogni_simulazione):
                frequenza_contagio_raccolta_dati = 1 + frequenza_contagio_raccolta_dati
                percentuale_banche_fallite = (len(lista_banche_fallite))/numero_banche_n_ogni_simulazione
                estensione_contagio_raccolta_dati.append(percentuale_banche_fallite)
        if frequenza_contagio_raccolta_dati == 0:
            estensione_contagio_percentuale_banche_fallite.append(0)
        else:
            estensione_contagio_percentuale_banche_fallite.append(sum(estensione_contagio_raccolta_dati)/frequenza_contagio_raccolta_dati)
        frequenza_contagio.append(frequenza_contagio_raccolta_dati/numero_simulazioni_per_ogni_valore_di_z)

# L'array z_average_degree è sempre lo stesso per tutti i plot ma gli altri due vettori sono unici e in successione hanno i capital buffer diversi, quindi dividere come esempio sotto: 
# es.: estensione_contagio_percentuale_banche_fallite[0:42*1] poi [42*1:42*2] poi [42*2:42*3] 
# poichè ad esempio vettore[0:3] fornisce tre elementi quello con indice 0, quello con 1 e quello con 2 MA NON quello con 3
# z_average_degree_voluti_vettore ha 42 elementi per ogni k(=capital buffer) cioè 3*42=126. Il primo ha indici da 0 a 41 ma vettore[0:41] restituisce fino al 40 poichè l'estremo è escluso, allora per richiamare la prima tornata di dati devi fare vettore[0:42] che non dà 42 ma fino a 41, la seconda vettore[42:84] che dà 83 e vettore[84:126] che dà 125
plt.scatter(z_average_degree_voluti_vettore, frequenza_contagio[0:27*1], marker='+', c='b', label='Frequency of contagion (3% capital buffer)')
plt.scatter(z_average_degree_voluti_vettore, estensione_contagio_percentuale_banche_fallite[0:27*1], marker='d', c='m', label='Extent of contagion (3% capital buffer)') # depthshade=True provare

plt.scatter(z_average_degree_voluti_vettore, frequenza_contagio[27*1:27*2], marker='x', c='black', label='Frequency of contagion (4% capital buffer)')
plt.scatter(z_average_degree_voluti_vettore, estensione_contagio_percentuale_banche_fallite[27*1:27*2], marker='o', c='red', label='Extent of contagion (4% capital buffer)')

plt.scatter(z_average_degree_voluti_vettore, frequenza_contagio[27*2:27*3], marker='2', c='green', label='Frequency of contagion (5% capital buffer)')
plt.scatter(z_average_degree_voluti_vettore, estensione_contagio_percentuale_banche_fallite[27*2:27*3], marker='^', c='orange', label='Extent of contagion (5% capital buffer)')

plt.scatter(0, 0, marker='+', c='b')
plt.scatter(0, 0, marker='d', c='m')
plt.scatter(0, 0, marker='2', c='green')
plt.scatter(0, 0, marker='^', c='orange')
plt.scatter(0, 0, marker='x', c='black')
plt.scatter(0, 0, marker='o', c='red')

plt.legend(bbox_to_anchor=(1.01,1), loc="upper left") # senza "borderaxespad=0" la posiziona poco sotto all'asse orizzontale in alto, con invece a filo
# plt.legend(bbox_to_anchor=(1.04,1), loc="upper left", borderaxespad=0, prop={'size': 9})
#plt.legend(loc='upper right', prop={'size': 6}) # upper right o center right. size=7 o 8 o 6
#plt.title('Figure 5: Varying the capital buffer 1000 banche 1000 simulazioni ogni z',fontdict = font)
plt.xlabel('Average degree $z$')
plt.ylabel('Defaults (%)')
plt.grid()
plt.xlim(-0.2,14.2)
# plt.savefig('contagio grafico 1000 banche 1000 simulazioni ogni z capital buffer diversi da 0.5.jpg', dpi=950, transparent=False, bbox_inches="tight")
#plt.savefig('contagio grafico 1000 banche 500 simulazioni ogni z capital buffer diversi.jpg', dpi=850, transparent=False)
plt.show()

# Fine.