;; Implements Contagion in Financial Networks based on the article
;; by Gai and Kapadia. Version 3.1: multiple iterations with banks of
;; the same size. Reports statistics and plot comparing default
;; extent to connectivity parameter (pp. 2415)

;; Developed by:
;; Axel Szmulewiez, Blake LeBaron
;; Brandeis University
;; Modifiche e correzioni by:
;; Gabriele Coppini


; Weight in links determines % of asset the link represents to each bank
links-own [ weight ]
; Banks have assets and liabilities (each sums up to 1)
turtles-own [ interbank-assets illiquid-assets interbank-liabilities deposits ]
; Keeps track of defaulted banks for while loop and adds buffer
; Also defines statistics variables
globals [ defaulted-banks-prev defaulted-banks-current buffer avg med mode minimum maximum]

to execute

  ; Execute simulations based on different interconnectiveness levels (z). Run multiple
  ; iterations for each z level, and then construct plot and statistics
  let z-index [ 0.5 1 1.5 2 2.5 3 3.5 4 4.5 5 5.5 6 6.5 7 7.5 8 8.5 9 9.5 10 10.5 ] ; prende un z ogni 0.5 in pratica, questo in python lo fai con un solo comando
  ; Arrays hold default results for each level simulations
  let contagion [] ; "contagion" sarà poi graficato come frequency of contagion
  let all-fail []  ; "all-fail" verrà poi graficato come extent of contagion
  let default-records []
  let extent-of-contagion [] ; mia prova
  ; Run simulation and store results for each z value
  ; ovunque compare ?1 sta al posto del z attuale dell'array z nel loop e ?1 -> serve a dare i comandi cioè prendi sto z che è chiamato ?1 e usalo nelle istruzioni dopo la -> che sarebbero come la funzione: è come dire z->f(z)
  foreach z-index [ ?1 ->
    let all-fail-dummy [] ; sono array che esistono solo nel loop e servono a portare fuori dal loop i risultati della simulazione per poi copiarli nelle versioni "non-dummy" dichiarate sopra che sono gli array "permanenti" che poi saranno i dati graficati
    let contagion-dummy [] ; questi 2 array momentanei vengono svuotati alla fine delle Iterations per un dato z per incamerare i nuovi dati delle simulazioni dello z successivo
    let extent-of-contagion-dummy [] ; mia prova
    ; a questo punto sta usando un valore di z dell'array indicato in maniera fittizia da ?1 (sarebbe il primo die punti interrogativi "alias", potrebbe essere necessario di altri come ?2 e ?3)
    ; ora per ogni z deve fare iterations-volte esperimenti con un loop attraverso il comando "repeat":
    ; estraggo, ad esempio 1000, volte un network con un z e faccio la simulazione poi calcola i risultati medi per quelle 1000 volte e
    ; cancella i dummy inizializzandoli ad array vuoti e poi cambia z ed estrae 1000 network con quello, e così via...
    repeat Iterations [
      setup-and-launch ?1 ; siccome "setup-and-launch" ha bisogno di usare z (che chiama z-local nell'argomento della sua funzione) prende lo z attuale con ?1
      ; "setup-and-launch" crea il network che abbia il giusto z poi chiama altre procedure che creano i bilanci di ciascuna banca, ne fanno fallire una banca a caso e guardano l'ondata di fallimenti conseguente.
      ; A questo punto tutte le banche che dovevano fallire per le perdite degli asset sono GIA' fallite e si ha il numero totale di fallite memorizzato in "defaulted-banks-current", che comprende anche quella fatta fallire a forza scelta a caso. Infatti dopo chiede se defaulted-banks-current=1 perchè questa potrebbe essere l'unica fallita se non è partito nessun contagio!
      if defaulted-banks-current = 1 [ set defaulted-banks-current 0 ]
      ; attento qua! Se la cosa dopo if è vera fa le istruzioni in [] e va avanti sennò va avanti direttamente. Invece se fosse stato ifelse se è vero esegue la prima [], se è falso la seconda []
      set default-records lput defaulted-banks-current default-records ; questo NON è dentro e non fa parte dell'if di sopra, sta solo andando avanti col codice
      ; ifelse defaulted-banks-current > (Banks * .05) [ set contagion-dummy lput 1 contagion-dummy ] [ set contagion-dummy lput 0 contagion-dummy ]
      ifelse defaulted-banks-current > (Banks * .05) [ set contagion-dummy lput 1 contagion-dummy set extent-of-contagion-dummy lput (defaulted-banks-current / Banks) extent-of-contagion-dummy ] [ set contagion-dummy lput 0 contagion-dummy ]
      ifelse defaulted-banks-current = Banks and defaulted-banks-current > (Banks * .05) [ set all-fail-dummy lput 1 all-fail-dummy ] [ set all-fail-dummy lput 0 all-fail-dummy ]
      ; questi 2 ifelse non sono mutualmente esclusivi, non hanno niente a che fare tra loro, li esegue entrambi: di ciascuno esegue o la prima o la seconda [] a seconda che la proposizione sia vera o falsa
    ]
    ; a questo punto hai tutte le simulazioni di un certo z e bisogna estrarre le statistiche da questi dati dummy e metterli negli array definitivi
    ifelse mean contagion-dummy = 0
    ; [ set all-fail lput (1 * 100) all-fail ]
    ; [ set all-fail lput ((mean all-fail-dummy  / mean contagion-dummy) * 100) all-fail ]
    [ set extent-of-contagion lput (0 * 100) extent-of-contagion set all-fail lput (1 * 100) all-fail ]
    ; comunque all-fail non lo usi ed è sbagliato però l'ho lasciato come era fatto da lui, stessa cosa qua sotto
    [ set extent-of-contagion lput (( (reduce + extent-of-contagion-dummy) / (length extent-of-contagion-dummy) ) * 100) extent-of-contagion   set all-fail lput ((mean all-fail-dummy  / mean contagion-dummy) * 100) all-fail ]
    ; o anche "sum" al posto di "reduce +"
    ; E comunque siccome "extent-of-contagion-dummy" conta la percentuale di falliti SOLO quando c'è un'ondata >5%, ovvero non è detto che la dimensione dell'array sia =Iterations, bastava fare:
    ; [ set extent-of-contagion lput ((mean extent-of-contagion-dummy) * 100) extent-of-contagion ]
    ; mean di "all-fail-dummy" è quante volte in media è fallito tutto il network con dato z cioè è (#fallito tutto network)/Iterations
    ; mean di "contagion-dummy" è quate volte in media c'è stato un contagio: si definisce contagio se nell'ondata di fallimenti sono fallite, compresa la banca fallita a forza, più
    ; del 5% del network, se ciò è avvenuto allora in quella simulazione è avvenuto un contagio e può avvenire al massimo un contagio a simulazione poichè non si ripete il fallimento della banca scelta a forza!
    ; Perciò mean di "contagion-dummy" è (#contagi)/Iterations
    ; La cosa però che NON CAPISCO è perchè "all-fail" che è l'estensione del contagio per tutta le Iterations di un dato z viene trovato facendo il rapporto tra
    ; la media di quante volte è fallito tutto il network e tra la media di quante volte c'è stato un contagio. Come questo possa dire la percentuale del network fallita in media per me è un mistero!!!
    ; Io avrei fatto: prendo il numero delle banche fallite e lo divido per quello totale delle banche ad ogni contagio >5% poi finite le Iterations li sommo tutti e divido per il numero dei dati ovvero le volte in cui è avvenuto un contagio >5%
    ; Per me "Extent of Contagion" e "all-fail" sono sbagliati infatti mentre il grafico di "Frequency of Contagion" è compatibile con quello di Kapadia, questo per bassi z no! Già a z<1 dovrebbe cominciare ad esserci una percentuale di network fallita.
    set contagion lput ((mean contagion-dummy) * 100) contagion
  ]

  ; Plot extent and frequency of contagion against z parameter (pp. 2415)
  set-current-plot "Clustering-Default Comparison"
  clear-plot
  set-current-plot-pen "Frequency of Contagion"
    plotxy 0 0
    ( foreach z-index contagion [ [?1 ?2] -> plotxy ?1 ?2 ] )
  set-current-plot-pen "Extent of Contagion"
    plotxy 0 0
    ; ( foreach z-index all-fail [ [?1 ?2] -> plotxy ?1 ?2 ] )
    ( foreach z-index extent-of-contagion [ [?1 ?2] -> plotxy ?1 ?2 ] )

  ; Report statistical results on simulations
  set avg mean default-records
  set med median default-records
  set mode modes default-records
  set minimum min default-records
  set maximum max default-records

end

; Sets up initial states: configures interface and bank financial states
; (with weighed links). Calibrates for desired interconnectedness degree
to setup-and-launch [ z-local ]

  clear-all
  ask patches [ set pcolor white ]
  setup-bank-structure
  ; Randomly link banks (ingoing and outgoing links)
  ask n-of (random (banks)) turtles [
    ; chiede ad un numero casuale di turtle banche di eseguire per ciscuna di esse il comando all'interno della [ aperta sopra. random 3 ad esempio estrae un numero da zero a 3 ESCLUSO quindi o 0 o 1 o 2
    create-links-to n-of (random (banks - 1)) other turtles
    ; ciascuna turtle/banca del numero scelto a caso di banche crea dei link a caso con le altre
  ]
  ; Calibrate z: Delete any exceding links / add more links
  while [ (z-local * count turtles) != count links ]
    [ ifelse z-local * count turtles < count links
        [ ask one-of links [ die ] ]
        [ ask one-of turtles [ create-link-to one-of other turtles ] ]

    ]
  setup-financial-states
  exogenous-shock
  contagion-start
  ; exogenous-shock è chiamato una volta sola quindi viene fatta fallire una sola banca a caso con la forza, tu pensavi invece che ogni volta che non c'erano più fallimenti a catena si facesse fallire una nuova banca con la forza!!!

end

; Creates banks and aligns them in a circle, all blue since
; at t=0 all banks are solvent
to setup-bank-structure

  create-turtles banks
  ; ATTENTO che "banks" è diverso da "Banks"!!! "banks" indica gli agenti ed è il nome delle turtles invece "Banks" è un numero ed indica quante banche hai impostato dallo slide
  layout-circle turtles (max-pxcor - 1)
  ask turtles [
    set color blue
    set size 2
  ]
  set-default-shape turtles "house"

end

; Sets up financial state of each bank. If bank has no links,
; then there are no interbank claims, and all states are
; determined by deposits and mortages (illiquid assets).
; Otherwise, make interbank assets 20% of total and distribute
; evenly among randomly generated links (interbank liabilities
; determined endogenously, one bank's asset is another's liability)
to setup-financial-states

  ask turtles [
    let number-of-ins count (my-in-links)
    ifelse number-of-ins = 0
      [ set illiquid-assets 1 set interbank-assets 0 ]
      [ set illiquid-assets .8 set interbank-assets .2
        ask my-in-links [ set weight .2 / number-of-ins ]
      ]

    let number-of-outs count (my-out-links)
    ifelse number-of-outs = 0
      [ set interbank-liabilities 0 set deposits 1]
      [ set interbank-liabilities sum [weight] of my-out-links
        set deposits 1 - interbank-liabilities
      ]
    ; cioè ha creato il bilancio di una banca. I link sono pesati e fissa i pesi dei link entranti e a questo punto sono fissati i pesi anche dei link uscenti per cui basta sommare sui link uscenti da ogni banca per vedere il totale dell'esposizione dei suoi debiti alle altre banche
  ]

end

; Initial exogenous shock, one bank is chosen
; at random and defaults (turns red)
to exogenous-shock
  ask one-of turtles [
    set color red
    ask my-in-links [ set color red ]
    ask my-out-links [ set color red ]
    ; fa diventare rossa una banca cioè fallisce poichè conta come fallite le banche rosse
  ]
end

; Starts contagion. If a bank is not solvent once an interbank asset defaults,
; then it defaults as well
to contagion-start

 ; Allow for a new contagion wave while the number of banks defaulted on this
 ; wave is greater than the number of banks defaulted on the last wave (implies we
 ; reached steady state). Then, end round and restart simulation
 set defaulted-banks-prev 0
 set defaulted-banks-current 1
 while [ defaulted-banks-current > defaulted-banks-prev ]
   [ set buffer .04 ; da qua credo che potresti cambiare il buffer e fare anche le altre figure
     ask turtles with [ color = blue and count(my-in-links with [ color = red ]) > 0][
       let phi count(my-in-links with [ color = red ]) / count(my-in-links)
       if (1 - phi) * interbank-assets + illiquid-assets + buffer - interbank-liabilities - deposits < 0
         [ set color red ask my-out-links [ set color red ] ]
     ]
     ; Update number of defaults on previous and current wave
     set defaulted-banks-prev defaulted-banks-current
     set defaulted-banks-current count turtles with [ color = red ]
     ; in pratica questo serve per vedere quali banche falliscono a seguito del fallimento artificiale/imposto di una banca a caso
     ; siccome quando valuta una banca questa potrebbe sopravvivere se un'altra banca che doveva fallire di cui lei aveva degli asset non è ancora fallita perchè non è stata ancora valutata
     ; io credo ma non ne sono certo che continui a valutare le banche finchè il numero sale e smette quando diventa uguale
     ; In pratica usa "defaulted-banks-prev" e "defaulted-banks-current" come contatori, al primo giro mette prev a 0 e current a 1 poichè viene fatta fallire una banca a caso credo
     ; poi ricalcola i bilanci di tutte le banche in successione casuale data da ask turtles (credo!), e calcola in quanti bilanci le perdite superano il capital buffer a causa del fallimento della banca scelta a caso che non può rimborsare più il debito
     ; queste banche <0 falliscono e le colora di rosso poi conta tutte le banche rosse quindi ANCHE quella fatta fallire forzatamente a caso e mette questo valore in current dopo avere passato il current precedente in prev
     ; e quindi se il current attuale (dopo i fallimenti) è > del prev (cioè prima dei falliemnti) fa un altro giro di valutazioni, MA
     ; NON FA FALLIRE UNA NUOVA BANCA A CASO, sta ancora valutando l'ondata dei fallimenti della vecchia!!! Secondo me, per assicurarsi che nessuna banca che dovrebbe fallire, sfugga.
     ; E' invece "exogenous-shock" che fa fallire una banca a caso con la forza e qua non è invocato infatti.
     ; VIENE FATTA FALLIRE UNA SOLA BANCA A CASO CON LA FORZA e questo avviene prima di "contagion-start" che serve proprio a studiarne le conseguenze: a contagio finito si butta
     ; via il network e si estrae un nuovo network (con lo stesso z o diverso) e NON si continua a far fallire banche con la forza in questo! Viene fatta fallire UNA SOLA VOLTA A SIMULAZIONE!
     ; INFATTI nel paper dice che avviene iterativamente il contagio da una banca all'altra (l'onda dei contagi cioè) e NON che viene ripetuto iterativamente il fallimento forzato di una banca!!!
   ]

end
@#$#@#$#@
GRAPHICS-WINDOW
704
84
874
255
-1
-1
4.63
1
10
1
1
1
0
0
0
1
-17
17
-17
17
1
1
1
ticks
30.0

SLIDER
13
118
379
151
Banks
Banks
2
300
150.0
2
1
NIL
HORIZONTAL

BUTTON
15
240
382
273
Run Model After Choosing # of Iterations and Banks
execute
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
14
160
380
193
Iterations
Iterations
1
300
300.0
1
1
NIL
HORIZONTAL

MONITOR
17
296
84
341
Mean
avg
2
1
11

MONITOR
91
296
159
341
Median
med
1
1
11

MONITOR
166
295
234
340
Modes
mode
17
1
11

MONITOR
242
295
309
340
Minimum
minimum
17
1
11

MONITOR
316
295
385
340
Maximum
maximum
17
1
11

PLOT
409
17
1166
383
Clustering-Default Comparison
Average Degree (connectivity parameter Z)
Defaults (%)
0.0
10.0
0.0
10.0
true
true
"" ""
PENS
"Frequency of Contagion" 1.0 0 -16777216 true "" "plot count turtles"
"Extent of Contagion" 1.0 0 -2674135 true "" ""

@#$#@#$#@
## WHAT IS IT?

The following program recreates the behavior of financial contagion described by Gai and Kapadia (2010). This model differs from the model described in the paper in that the user has the liberty to choose the number of banks in the network (in the original model, everything is randomly determined). This model assumes there are no fire sales (hence q = 1). Defaulted banks are represented by the color red, solvent banks are represented by the color blue.

This third version runs multiple default simulations with banks of the same size, collects and reports statistics and shows the relationship between extent and frequency of contagion against interconnectiveness

## THINGS TO NOTICE

To run the model, simply adjust the desired number of banks in the network and the number of iterations (i.e. default simulations). Then, hit the “Run Model After Choosing # of Iterations and Banks” button. Statistical measures (mean, median, mode, min and max) of the experiment are reported in the interface, as well as the graph described in page 2415 of the research paper.

One note on running time: Since the program needs to adjust for the number of links in the network, it runs on an O(n^2) algorithm, meaning that running time increases relatively quickly as input size rises. A round with 100 banks and 100 iterations takes less than 2 minutes, while having 200 iterations takes between 2 and 6 minutes (depending on your machine). Increase the input size only if necessary, the results in the statistics and the plot are the same (the graph is smoother with a greater input size but presents the correct outline with 100 banks and 100 iterations already)

## EXTENDING THE MODEL

Extensions of the model could include: sliders to choose the number of links (in order to adjust the parameter of interconnectedness "z"), making banks have different sizes, allow interbank assets not to be evenly distributed among incoming links. Please see other implementation versions.

## RELATED MODELS

-

## CREDITS AND REFERENCES

* Gai, Prasanna and Kapadia, Sujit, Contagion in Financial Networks (March 23, 2010). Bank of England Working Paper No. 383. Available at SSRN: http://ssrn.com/abstract=1577043 or http://dx.doi.org/10.2139/ssrn.1577043
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.1.1
@#$#@#$#@
setup-simple-random
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@
