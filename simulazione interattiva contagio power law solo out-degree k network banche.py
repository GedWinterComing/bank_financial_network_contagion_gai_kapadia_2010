# -*- coding: utf-8 -*-
"""
Created on Thu May 27 18:57:59 2021

@author: Gabriele
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
np.random.seed(420) # così con lo stesso seed (qua 420 ma può essere qualunque numero) ottieni sempre gli stessi numeri "casuali". Oppure puoi commentare questa riga, ma i risultati non saranno più riproducibili perchè ogni volta otterrai numeri casuali diversi!
#%%

# Funzione per generare un network con esattamente z di degree medio e calcolo della probabilità conseguente e aggiustamento della degree sequence
def generatore_matrice_adiacenza_con_z_voluto_da_power_law_out_preferential_attachment(nodi_totali, z_voluto):
    # se ad esempio ogni nodo/banca deve avere in media 5 link che escono e partono da lui, ne consegue che il network dovrà avere almeno 6 nodi. Esistono 2 diversi modi di calcolare il 
    # average degree o mean degree z=<k>=(Sum_{0}^{n} k_i)/n dove n=# totale di nodi, ma siccome
    # la somma sulla degree sequence in un network diretto è il numero totale di link, abbiamo quindi
    # z = # totale di link / # totale di nodi = m/n perciò  # totale di link = m = zn   (Nei network non diretti è invece <k>=2m/n quindi m = zn/2 )
    link_totali_necessari = z_voluto * nodi_totali # occhio che può non essere un numero intero siccome z può avere la virgola, andrà convertito in int
    # alpha_esponente_powerlaw = 2 + a/c  In Newman manuale dove c è mean out-degree <k>=z e consiglia di prendere a=c oppure in Price viene preso a=1
    # viene una power-law che è p_q = q^{-alpha} = q^-3 dove q è l'in-degree j nella notazione di Newman 
    # a_parametro_probabilita = z_voluto * (alpha_esponente_powerlaw - 2) # che è uguale a z così: a=z
    # phi_probabilita = z_voluto / (z_voluto + a_parametro_probabilita)  di fatto viene phi= a/2a = 1/2 = 50% = 0.5
    # Questo seguendo Newman e Price e Krapivsky e Redner era per la power-law della distribuzione dell'in-degree INVECE qua noi la vogliamo SOLO per l'out-degree
    # La distribuzione per l'in-degree è omogenea, tutti i nodi stessa probabilità
    # p_j = 1/n  per in-degree
    # p_k = k^{-alpha_out} = k^-3  per out-degree
    alpha_out_esponente_powerlaw = 3
    a_out_parametro_probabilita = z_voluto * (alpha_out_esponente_powerlaw - 2) # a = z = <k> = <j>
    phi_out_probabilita = z_voluto / (z_voluto + a_out_parametro_probabilita) # di fatto viene phi= a/2a = 1/2 = 50% = 0.5
    percentuale_link_usare_subito = 1/10 # parametro da impostare, ad esempio 10% del numero totale, considera che se z=1 e n=1000 poi ci sono 1000 link e quindi qua ne bruci 100, però se n=50 sono 5
    link_per_inizializzare = percentuale_link_usare_subito * link_totali_necessari # occhio che non è un numero intero poichè una frazione in Python restituisce sempre un numero decimale, andrà convertito in int
    matrice_adiacenza = np.zeros((nodi_totali, nodi_totali), dtype=int) # matrice quadrata nxn con n=numero nodi del grafo
    lista_link_uscenti_creati = []
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
                    break        
    for ci in range(int(round(link_totali_necessari - link_per_inizializzare))):
        while True:
            if phi_out_probabilita > np.random.random():
                nodo_da_cui_esce_link = np.random.choice(lista_link_uscenti_creati)
                nodo_in_cui_entra_link = np.random.randint(nodi_totali) # # nodo hub potrebbe puntare a nodo anonimo qualunque, accade 1/2 delle volte
            else:
                nodo_da_cui_esce_link = np.random.randint(nodi_totali)
                nodo_in_cui_entra_link = np.random.randint(nodi_totali) # nodo anonimo qualunque potrebbe puntare a nodo anonimo qualunque, accade 1/2 delle volte
            if nodo_da_cui_esce_link != nodo_in_cui_entra_link:
                if matrice_adiacenza[nodo_da_cui_esce_link, nodo_in_cui_entra_link] == 0:
                    matrice_adiacenza[nodo_da_cui_esce_link, nodo_in_cui_entra_link] = 1
                    lista_link_uscenti_creati.append(nodo_da_cui_esce_link)
                    break
    return matrice_adiacenza

# Funzione per creare i bilanci della banche del network
def generatore_matrice_pesi_bilanci_banche(matrice_adiacenza, capital_buffer):
    numero_banche = len(matrice_adiacenza) # la matrice di adiacenza ovviamente è quadrata
    # per la direzione uso la convenzione che A_{i,j}=1 significa che c'è un link che va DAL nodi i AL nodo j. Newman usa l'opposto!
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

capital_buffer = 0.04 # soglia tolleranza perdite nel bilancio è al 4%
print('\n','--------------------','Inizio Simulazione','--------------------', sep='\n')
numero_banche_n_ogni_simulazione = int(input('Inserire il numero di banche desiderato (es.30): '))
z_voluto = float(input('Inserire l\'average degree desiderato (es.2.5): ')) # infatti input restituisce un tipo string che deve essere convertito in un numero
# numero_banche_n_ogni_simulazione = int(numero_banche_n_ogni_simulazione)
# z_voluto = float(z_voluto)
print('Sto creando il network bancario...')
print('Questo è il network estratto:', '(ogni nodo è una banca, ogni link entrante in una banca è un credito interbancario e ogni link uscente un debito interbancario)', sep='\n')
matrice_adiacenza_network_bancario = generatore_matrice_adiacenza_con_z_voluto_da_power_law_out_preferential_attachment(numero_banche_n_ogni_simulazione, z_voluto)
# G = nx.from_numpy_matrix(adjacency_matrix) # ATTENZIONE che pur essendo la matrice di adiacenza quella di un grafo diretto, se non specifichi DiGraph come metodo ti disegna comunque un grafo non diretto
G = nx.from_numpy_matrix(matrice_adiacenza_network_bancario, create_using=nx.DiGraph())

fig=plt.gcf()
ax=plt.gca()
if numero_banche_n_ogni_simulazione > 70:
    pos = nx.spring_layout(G) # ma è meglio usare l'altro se le banche sono poche, questo è l'unica possibilità se le banche sono molte
else:
    pos = nx.circular_layout(G, center=(0, 0)) # funziona bene quando le banche sono poche tipo 50, già a 100 viene una macchia di colore incomprensibile!
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'))

nx.draw_networkx(G, pos, arrows=True, arrowstyle = '-|>')
font = {'family':'serif','color':'darkred','weight':'normal','size': 13.7,}
plt.title("Network bancario prima dei fallimenti", fontdict = font)
plt.show()

W_matrice_pesi_esposizioni_bancarie, bilanci_bancari_matrice_n_x_5 = generatore_matrice_pesi_bilanci_banche(matrice_adiacenza_network_bancario, capital_buffer) # anche se hanno gli stessi nomi che comparivano all'interno del codice della funzione non preoccuparti non entrano in conflitto perchè non ha accesso ai nomi del codice della funzione, non sono globali: l'hai testato!
lista_banche_fallite = [ ] # qua deve essere vuota da sola, senza banca casuale, perchè è l'estrazione della banca che deve essere ripetuta su richiesta dell'utente
lista_nodi = [v for v in range(numero_banche_n_ogni_simulazione)]
contatore_volte_scritta_mostrata = 0

while True:
    np.random.shuffle(lista_nodi)
    banca_casuale_da_far_fallire = lista_nodi[0]
    lista_nodi.remove(banca_casuale_da_far_fallire)
    print('Verrà estratta a caso una banca che fallirà e i suoi debiti interbancari (link uscenti da essa) perderanno valore con conseguente perdita dei crediti per le banche connesse.','\n','La banca estratta è la numero', banca_casuale_da_far_fallire)
    numero_banche_fallite_adesso = 1 # per ora c'è solo una che è "banca_casuale_da_far_fallire" fatta fallire a forza però poi qua aggiorneremo col numero totale ad ogni ondata di fallimenti 
    numero_banche_fallite_prima = 0
    lista_banche_fallite.append(banca_casuale_da_far_fallire)
    W_matrice_pesi_esposizioni_bancarie[banca_casuale_da_far_fallire,:] = 0 # è sufficiente far così per mettere dei 0.0 su tutta una riga
    while numero_banche_fallite_adesso > numero_banche_fallite_prima:
        # ora devo ricalcolare i bilanci di tutte le banche a seguito della perdita dei crediti persi per il fallimento della banca che ha cancellato la sua riga corrispondente ovvero i suoi debiti, i link pesati uscenti da lei
        # in pratica però solo 2 voci del bilancio vanno ricalcolate: asset interbancari e debiti interbancari. Gli asset interb. sono le colonne di W e i debiti interb. sono le righe di W. Invece i mutui A_M e i depositi D rimangono tali, sono fissati per tutta la simulazione
        asset_interb_vettore_A_IB_dopo_fallimento = np.sum(W_matrice_pesi_esposizioni_bancarie, axis=0)
        debiti_interb_vettore_L_IB_dopo_fallimento = np.sum(W_matrice_pesi_esposizioni_bancarie, axis=1)
        bilanci_bancari_matrice_n_x_5[:,1]= asset_interb_vettore_A_IB_dopo_fallimento
        bilanci_bancari_matrice_n_x_5[:,3]= -debiti_interb_vettore_L_IB_dopo_fallimento
        stato_patrimoniale_banche_saldo_balance_sheet= np.sum(bilanci_bancari_matrice_n_x_5, axis=1) # le banche fallite ORA hanno saldo < 0. Poi dopo quando verranno effettivamente fatte fallire cancellando con zeri la loro riga corrispondente della matrice W e ricalcolati asset e debiti, a quel punto il loro bilancio diventerà >0 poichè perdono i loro debiti interb. (abbiamo appena detto che la riga di W viene riempita di 0) però rimangono asset interb., quindi se non salvi gli indici delle banche fallite ora, poi in futuro non potrai più saperlo!!!!
        # attento che la banca estratta a caso fallita con la forza NON ha un bilancio negativo bensì è aumentato ed è diventato ancora più positivo poichè sono scomparsi i suoi debiti ma rimasti i suoi asset (che comunque devono rimanere), quindi paradossalmente la sua posizione è migliorata anch se è fallita. Una soluzione potrebbe essere quella di aggiornare il bilancio bancario solo alla voce asset interb. e NON a quella debiti interbancari che effettivamente potrebbe che essere non servano
        indici_banche_fallite = np.transpose((stato_patrimoniale_banche_saldo_balance_sheet<0).nonzero())
        indici_banche_fallite = indici_banche_fallite.reshape(len(indici_banche_fallite))
        indici_banche_fallite = indici_banche_fallite.tolist() # ora non è più un array ma così diventa una lista
        for indice_lista in indici_banche_fallite:
            # hai fatto bene ad usare un contatore per indici_banche_fallite che prenda singolarmente ogni elemento della lista perchè se tu avessi aggiunto direttamente la lista sarebbe venuta una lista in una lista tipo così [..[]..]
            if indice_lista not in lista_banche_fallite:
                lista_banche_fallite.append(indice_lista)
                lista_nodi.remove(indice_lista)
                W_matrice_pesi_esposizioni_bancarie[indice_lista,:] = 0 # è sufficiente far così per mettere dei 0.0 su tutta una riga
        numero_banche_fallite_prima = numero_banche_fallite_adesso
        # numero_banche_fallite_adesso = numero_banche_fallite_adesso + len(indici_banche_fallite) # se non ti fidi che la lista indici_banche_fallite contenga effettivamente le banche fallite giuste è meglio usare il metodo qua sotto
        numero_banche_fallite_adesso = len(lista_banche_fallite) # dovrebbe essere indifferente quale metodo usare
        # ATTENTO che è possibile che una banca già fallita, ritornata positiva perchè vengono cancellati i suoi debiti come detto sopra, poi rifallisca siccome il bilancio torna negativo a causa del fallimento di altre banche di cui aveva asset! Però non è un problema siccome c'è la lista che tiene conto delle banche già fallite e aggiunge la nuova banca solo se non presente 
    fig=plt.gcf()
    ax=plt.gca()
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'))
    nx.draw_networkx(G, pos, arrows=True, arrowstyle = '-|>')
    # nx.draw_networkx_nodes(G, pos, nodelist=lista_banche_fallite, node_color="r") # alla fine potresti mettere width=0.7, alpha=0.9) ma non serve
    
    edge_differenza_colori_fallimenti = ['red' if e[0] in lista_banche_fallite else 'black' for e in G.edges]
    nx.draw(G, pos=pos, nodelist=lista_banche_fallite, edge_color=edge_differenza_colori_fallimenti, node_color="r")
    
    plt.title("Network bancario a seguito dell'ondata di fallimenti", fontdict = font)
    plt.show()
    
    if len(lista_banche_fallite)/numero_banche_n_ogni_simulazione > 0.05:
        if contatore_volte_scritta_mostrata > 0:
            print('La percentuale del network fallito è: ', round(100*(len(lista_banche_fallite)/numero_banche_n_ogni_simulazione), 1), '%. Ovvero ', len(lista_banche_fallite), ' su ', numero_banche_n_ogni_simulazione, sep='') # per non avere lo spazio " " che separa un argomento dall'altro del print
        elif contatore_volte_scritta_mostrata == 0:
            print('A causa del fallimento della banca è avvenuto un contagio finanziario e, a seguito dell\'ondata di fallimenti, il ', round(100*(len(lista_banche_fallite)/numero_banche_n_ogni_simulazione), 1), '% del network è fallito. Ovvero ', len(lista_banche_fallite), ' banche su ', numero_banche_n_ogni_simulazione, sep='') # per non avere lo spazio " " che separa un argomento dall'altro del print
        contatore_volte_scritta_mostrata +=1
    else:
        print('Non è avvenuto un contagio poichè non è fallito più del 5% del network')
    if len(lista_banche_fallite) == numero_banche_n_ogni_simulazione:
        print('Tutte le banche sono fallite','Simulazione terminata', sep='\n')
        break
    risposta = input('Vuoi far fallire un\'altra banca casuale oppure vuoi concludere la simulazione? [y/n] ')
    if risposta != 'y':
        print('Non sono fallite le banche numero:', sorted(lista_nodi)) # con "sorted" viene creata una nuova lista con i numeri di lista_nodi ordinati in maniera crescente, è necesario poichè sopra si era fatto "shuffle" della lista originaria per estrarre ogni volta la banca da far fallire come primo elemento della lista, dopo essere stata shakerata
        print('Simulazione terminata')
        break
# Fine.