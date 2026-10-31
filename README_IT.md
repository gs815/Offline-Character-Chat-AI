# Offline Character Chat

Chat con personaggi AI che funziona interamente sul tuo computer: **browser + Ollama**, senza account e senza cloud. Le conversazioni restano sul tuo PC, salvate nel browser, e dopo aver scaricato Ollama e un modello non serve internet.

Puoi creare o importare personaggi (roleplay o assistente), tenere più chat separate e far ricordare la storia al personaggio con riassunto automatico, ricordi fissi e lorebook. Ci sono un Creatore Personaggi, il supporto al thinking e l'interfaccia in italiano e inglese. Si usa dal PC e, sulla stessa Wi-Fi, anche dal telefono.

## Indice

1. [File inclusi](#1-file-inclusi)
2. [Cosa serve](#2-cosa-serve)
3. [Avvio rapido (Windows)](#3-avvio-rapido-windows)
4. [Avvio manuale (Windows, Mac, Linux)](#4-avvio-manuale-windows-mac-linux)
5. [Uso dal telefono (stessa rete Wi-Fi)](#5-uso-dal-telefono-stessa-rete-wi-fi)
6. [Spegnere tutto](#6-spegnere-tutto)
7. [Come si usa l'app](#7-come-si-usa-lapp)
8. [Memoria e riassunto automatico](#8-memoria-e-riassunto-automatico)
9. [Lorebook](#9-lorebook)
10. [Impostazioni](#10-impostazioni)
11. [Import, export e backup](#11-import-export-e-backup)
12. [Dove sono i dati](#12-dove-sono-i-dati)
13. [Problemi comuni](#13-problemi-comuni)
14. [Limiti noti](#14-limiti-noti)
15. [Funzionamento senza internet](#15-funzionamento-senza-internet)
16. [Creare i file `.bat` da zero](#16-creare-i-file-bat-da-zero)

## 1. File inclusi

Tienili tutti nella stessa cartella, con questi nomi.

| File | Cos'è |
|---|---|
| `offline-character-chat.html` | l'intera app (HTML, CSS, JavaScript) |
| `server.py` | server usato da `avvia-chat-rete.bat` |

Per usare solo il PC bastano l'HTML e `avvia-chat.bat`.

## 2. Cosa serve

- **Ollama** ([ollama.com](https://ollama.com)), acceso, con almeno un modello scaricato:

  ```bash
  ollama pull qwen3:8b       # scaricare un modello
  ollama pull llama3.2:3b    # un modello più leggero
  ollama list                # vedere quelli installati
  ```

- **Python 3.7 o più recente** ([python.org](https://www.python.org)). Su Windows spunta *Add Python to PATH* durante l'installazione.
- Un browser recente (Chrome, Edge, Firefox, Safari).
- Internet serve solo per scaricare Ollama e i modelli. Dopo, tutto funziona offline.

## 3. Avvio rapido (Windows)

1. Accendi Ollama (a parte: l'app non lo avvia).
2. Doppio clic su uno di questi:
   - `avvia-chat.bat`: solo dal PC
   - `avvia-chat-rete.bat`: dal PC e anche dal telefono ([sezione 5](#5-uso-dal-telefono-stessa-rete-wi-fi))
3. Si apre il browser. Tieni aperta la finestra nera finché usi la chat.

Usa un solo `.bat` alla volta: entrambi usano la porta 8000 (il secondo ti avvisa se è occupata).

> Windows o il browser possono segnalare i `.bat` come file potenzialmente pericolosi: è normale. Puoi aprirli con Blocco note per vedere che contengono solo pochi comandi. Se non li hai o ne hai perso uno, vedi la [sezione 16](#16-creare-i-file-bat-da-zero).

## 4. Avvio manuale (Windows, Mac, Linux)

Accendi Ollama, poi apri un terminale nella cartella dei file. Su Windows, se `python` non va, usa `py`. Su Mac/Linux usa `python3`.

**Solo dal PC:**

```bash
python server.py
```

poi apri <http://localhost:8000/>

**Anche dal telefono** (il terminale mostra l'indirizzo da aprire sul telefono):

```bash
python server.py --lan
```

**Altra porta** (se la 8000 è occupata):

```bash
python server.py 9000
python server.py --lan 9000
```

**Alternativa semplice**, solo PC, senza `server.py`:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

poi apri <http://localhost:8000/offline-character-chat.html>

Usa sempre lo stesso indirizzo: i dati sono legati ad esso ([sezione 12](#12-dove-sono-i-dati)).

> Aprire l'HTML con doppio clic, senza server, è sconsigliato: Ollama rifiuta le richieste, a meno di impostare la variabile d'ambiente `OLLAMA_ORIGINS=*` e riavviarlo. Anche i dati sarebbero separati da quelli salvati su `localhost`.

## 5. Uso dal telefono (stessa rete Wi-Fi)

1. Accendi Ollama sul PC.
2. Avvia `avvia-chat-rete.bat` (oppure `python server.py --lan`). Se Windows chiede l'accesso di rete, consenti le reti **private**.
3. Sul telefono apri l'indirizzo *Dal telefono* mostrato nella finestra, qualcosa come `http://192.168.1.23:8000/`.
4. Non devi impostare altro: l'URL di Ollama si compila da solo.

**Come funziona:** `server.py` serve la pagina e inoltra a Ollama **solo** `/api/chat`, `/api/tags` e `/api/show` (quest'ultimo serve a sapere se il modello supporta il thinking). Ollama non viene aperto alla rete, quindi non servono le variabili `OLLAMA_HOST` o `OLLAMA_ORIGINS`. Ogni altro percorso risponde 404.

> **Attenzione:** chiunque sia sulla tua Wi-Fi può usare la chat e quindi il tuo Ollama. Usalo solo su una rete di casa fidata.

Le chat del telefono sono separate da quelle del PC (i dati stanno nel browser di ciascun dispositivo). Per spostarle usa esporta e importa ([sezione 11](#11-import-export-e-backup)). Importando un backup del PC sul telefono, l'URL di Ollama del telefono non viene toccato.

**Se l'indirizzo mostrato non funziona:** telefono e PC devono essere sulla stessa Wi-Fi; se il PC ha più schede di rete (per esempio una VPN) prova l'indirizzo IPv4 che vedi con `ipconfig`; controlla che il firewall abbia consentito la rete privata.

## 6. Spegnere tutto

- **Chat:** chiudi la finestra nera (oppure `Ctrl+C` al suo interno). Chiudere solo la scheda del browser non ferma il server.
- **Ollama:** icona vicino all'orologio, tasto destro, *Quit Ollama*. Finché è acceso occupa memoria, soprattutto con un modello caricato.

Chat e memoria restano salvate nel browser.

## 7. Come si usa l'app

### Barra sinistra

Su telefono si apre con il pulsante in alto.

- **Scheda Chat:** tutte le chat, dalla più recente. In alto scegli il personaggio e premi **+ Chat** per iniziarne una nuova. Su ogni chat: ✎ = rinomina, ⇩ = esporta, × = elimina.
- **Scheda Personaggi:** ricerca, **+ Nuovo personaggio**. Su ogni personaggio: **+** = nuova chat, ✎ = modifica. Cliccare il nome crea subito una nuova chat e passa alla scheda Chat.
- **In fondo:** importa personaggio, chat o backup; sotto, il menu della lingua e il pulsante **Reset**.

### Chat separate

Ogni chat è indipendente: ha cronologia, ricordi fissi, riassunto e interruttori di memoria e riassunto propri. Puoi avere quante chat vuoi con lo stesso personaggio, senza che si influenzino. Sono invece globali: lorebook, tua persona e impostazioni.

### Scrivere

- `Invio` manda il messaggio, `Maiusc+Invio` va a capo. Su telefono Invio va a capo: usa il pulsante **Invia**.
- Campo vuoto + **Invia**, oppure `/ai`: risponde il personaggio senza che tu scriva.
- `/sys testo`: istruzione valida solo per la prossima risposta (esempio: `/sys descrivi la stanza`).
- **Stop** interrompe la risposta e conserva quanto generato. Premere Invio mentre il modello risponde **non** la ferma: usa il pulsante.
- **Continua** riprende l'ultima risposta da dove si è fermata (attivo solo se l'ultimo messaggio è del personaggio).

### Sui messaggi

- **Modifica**, **Elimina**.
- **Rigenera:** sull'ultimo messaggio crea una variante e le frecce scorrono tra le varianti. Su un messaggio più vecchio elimina quelli successivi (chiede conferma). Non è disponibile per i messaggi già riassunti nella memoria.
- **Copia:** sui blocchi di codice.
- **Ragionamento (thinking):** se era acceso, sopra la risposta c'è un blocco richiudibile con il ragionamento del modello.
- **Testo:** blocchi di codice, `` `codice` ``, `**grassetto**`, `*azioni*`. Con un personaggio in modalità Assistente anche titoli (`#`) e liste. Le tabelle non vengono disegnate.

### Personaggio

Matita, oppure **+ Nuovo personaggio**.

| Modalità | Cosa fa |
|---|---|
| **Roleplay** | regole di roleplay: resta nel personaggio, non scrive per te, azioni tra `*asterischi*` |
| **Assistente** | niente regole di roleplay, temperatura bassa (0.4), codice in blocchi |
| **Creatore** | modalità speciale: trasforma una descrizione in una scheda personaggio (vedi *Creatore Personaggi*) |

- **Descrizione**, **Personalità**, **Scenario**.
- **Primo messaggio:** più saluti separati da una riga con `---`; il primo è mostrato, gli altri sono varianti.
- **Regole extra:** istruzioni aggiuntive per il modello.
- **Reminder:** testo ripetuto in fondo al prompt a ogni risposta; aiuta molto i modelli piccoli a restare nel personaggio.
- **Dialogo di esempio:** serve solo come stile.
- Nei testi puoi usare `{{char}}` (nome del personaggio) e `{{user}}` (il tuo nome).
- Modificare un personaggio non cambia il primo messaggio delle chat già iniziate.

### Personaggi di serie

Di serie ci sono solo due personaggi:

- **Assistente:** aiuto per programmazione e domande.
- **Creatore Personaggi:** crea nuovi personaggi.

Puoi modificarli o eliminarli: se li elimini non ricompaiono.

### Creatore Personaggi

Aprilo (scheda Personaggi, oppure scegli il Creatore e premi **+ Chat**) e descrivi nel messaggio chi vuoi, anche in poche parole, ed eventualmente uno scenario. Esempio:

> una detective cinica in una città cyberpunk

Il modello attivo (menu in alto) scrive la scheda completa: nome, descrizione, personalità, scenario, primo messaggio, dialogo di esempio e reminder. Il personaggio viene aggiunto alla lista Personaggi e in chat compare un riepilogo con i pulsanti **Nuova chat con …** e **Apri scheda**.

- Se la richiesta è breve, i dettagli mancanti (età, aspetto come il colore dei capelli, carattere, scenario…) vengono completati dal modello e scritti nella scheda, **senza cambiare nulla di quello che hai chiesto**.
- Ogni messaggio crea un **nuovo** personaggio. Per ritoccarne uno usa **Apri scheda** (o ✎ nella lista).
- La scheda è scritta nella lingua della tua richiesta.
- Nel Creatore non ci sono Rigenera e Continua: per un'altra versione scrivi di nuovo la richiesta. **Stop** interrompe la creazione senza aggiungere nulla.
- Nella scheda del Creatore, **Regole extra** accetta istruzioni tue su come creare (esempio: "scrivi sempre tre righe di dialogo di esempio").
- Se il modello non rispetta il formato, vedrai un avviso e il testo che ha scritto: riprova, oppure usa un modello più grande. I modelli piccoli seguono il formato meno bene.

### Thinking (ragionamento del modello)

Alcuni modelli (per esempio qwen3 o deepseek-r1) possono "ragionare" prima di rispondere. L'app lo permette solo per i personaggi in modalità **Assistente** e **Creatore**, compresi l'Assistente e il Creatore Personaggi di serie.

- Sopra il campo messaggio compare il pulsante **Thinking: spento / Thinking: acceso**. Appare solo se il modello scelto in alto supporta il thinking (l'app lo chiede a Ollama). Se la tua versione di Ollama non sa dirlo, il pulsante resta visibile: se il modello in realtà non lo supporta, la risposta arriva comunque, senza ragionamento.
- È **spento di default** e la scelta si ricorda per ogni personaggio.
- Nei personaggi **Roleplay** il thinking è sempre spento e non c'è nessuna opzione.
- Acceso, la risposta è più lenta e usa più token. L'app alza da sola il limite di risposta (almeno 2048 token, 3000 per il Creatore, entro metà del context) così il ragionamento non consuma tutta la risposta.
- Il ragionamento compare in un blocco richiudibile **Ragionamento (thinking)** sopra la risposta: aperto mentre il modello ragiona, chiuso a risposta finita.
- Il ragionamento non viene rimandato al modello nei messaggi successivi, e i riassunti della memoria non usano mai il thinking.

### Nome in questa chat

**Memoria e opzioni > Memoria > Il tuo nome in questa chat.** Vale solo per quella chat (non è globale): è il nome che il modello vede al posto di "User" e quello mostrato sui tuoi messaggi; anche `{{user}}` nelle schede diventa questo nome.

- Vuoto = vale il nome della tua persona (*Tua persona*).
- Le altre chat non cambiano, nemmeno quelle dello stesso personaggio. Il primo messaggio di una chat nuova usa il nome della tua persona.
- Massimo 40 caratteri. Viene salvato anche nell'export della chat.

### Tua persona

**Memoria e opzioni > Tua persona.** Nome e descrizione di chi sei, valgono per tutte le chat. Se lasci il nome predefinito ("You" in inglese, "Tu" in italiano), al modello arriva come "User". In ogni chat puoi usare un nome diverso (vedi *Nome in questa chat*).

### Lingua

In fondo alla barra sinistra. Menu a tendina: **English** (predefinita) e **Italiano**. Cambia subito tutta l'interfaccia e la scelta viene ricordata. Chi usava già l'app senza aver mai scelto una lingua passa all'inglese: per tornare all'italiano scegli Italiano nel menu.

- I personaggi di serie (Assistente e Creatore Personaggi in italiano, Assistant e Character Creator in inglese) cambiano nome e testo di benvenuto con la lingua, ma solo se non li hai modificati: i campi che hai cambiato tu restano come sono.
- Le chat già scritte restano nella lingua in cui sono state scritte.
- La lingua dell'interfaccia non decide in che lingua risponde il modello: risponde nella lingua in cui scrivi tu.
- **Aggiungere una lingua:** apri `offline-character-chat.html` con un editor di testo, cerca `LANGS` e aggiungi una voce accanto a `it` ed `en`:
  - `n` = nome mostrato nel menu
  - `loc` = formato delle date (esempio `fr-FR`)
  - `you` = nome predefinito di chi scrive
  - `m` = le traduzioni (testo italiano: testo nella nuova lingua; la voce `en` mostra come)

  Le voci non tradotte restano in italiano. La nuova lingua compare da sola nel menu.

### Reset

Pulsante rosso in fondo alla barra sinistra. Chiede conferma, poi cancella **tutto** (chat, personaggi, lorebook, tua persona, impostazioni) e riparte come al primo avvio: solo i due personaggi di serie, lingua inglese, nessuna chat. Dopo il reset non c'è nessuna chat aperta: scegli un personaggio e premi **+ Chat**.

> Non si può annullare: fai prima un backup ([sezione 11](#11-import-export-e-backup)).

### Modello

Menu in alto: elenca i modelli installati in Ollama. Se avvii Ollama dopo la pagina, l'elenco si aggiorna da solo.

## 8. Memoria e riassunto automatico

Ollama non ricorda nulla tra una richiesta e l'altra: la memoria la gestisce l'app.

- La chat completa è **sempre** salvata. Al modello, a ogni risposta, arrivano: regole e scheda, tua persona, ricordi fissi, riassunto, lore pertinente, gli ultimi messaggi che stanno nel context e il reminder (ricordi fissi e riassunto solo se attivi per quella chat, vedi sotto).
- **Ricordi fissi** (**Memoria e opzioni > Memoria**): li scrivi tu e il riassunto automatico non li tocca mai. Mettici i fatti che non devono sparire.
- **Riassunto automatico:** quando i messaggi non ancora riassunti occupano circa tre quarti dello spazio disponibile, i più vecchi vengono riassunti dal modello in punti elenco (circa 25 al massimo), tenendo interi gli ultimi messaggi (fino a 12). Il testo è modificabile a mano.
- **Riassumi ora i messaggi vecchi** forza un riassunto; **Annulla ultimo riassunto** ripristina quello precedente.
- **Interruttori per chat** (**Memoria e opzioni > Memoria**): ogni chat ha due caselle indipendenti, entrambe attive di default. Memoria e riassunto sono cose diverse:
  - **Memoria in questa chat:** se la spegni, i ricordi fissi non vengono inviati al modello (il testo resta salvato e modificabile).
  - **Riassunto in questa chat:** se lo spegni, il riassunto non viene né creato né usato e **Riassumi ora** si disattiva. Al modello vanno gli ultimi messaggi che stanno nel context, anche quelli già riassunti prima, e si può rigenerare anche da quei messaggi.
  - Gli ultimi messaggi della chat vengono **sempre** inviati al modello, qualunque cosa scegli. Le voci del lorebook non si attivano con le parole che si trovano nei testi spenti.
  - Valgono solo per quella chat: le altre, anche dello stesso personaggio, non cambiano. Vengono salvati anche nell'export della chat.
  - L'opzione **Riassunto automatico dei messaggi vecchi** nelle Impostazioni resta l'interruttore generale.
- Un modello piccolo può omettere o sbagliare dettagli nel riassunto: controllalo ogni tanto e sposta le cose importanti nei ricordi fissi.
- I riassunti non usano mai il thinking. Nei riassunti, i tuoi messaggi portano il nome che usi in quella chat.
- Il pannello mostra quanti messaggi sono stati riassunti e quanti token ha usato l'ultimo prompt.
- Avvisi in basso: se scheda, memoria e lore occupano troppo context, o se il prompt arriva al limite (in quel caso Ollama potrebbe scartare parte della cronologia): aumenta il context.

## 9. Lorebook

**Memoria e opzioni > Lorebook.** Ogni voce ha parole chiave (separate da virgola) e un contenuto.

- La voce entra nel prompt se una parola chiave compare negli ultimi messaggi, nei ricordi o nel riassunto.
- La parola chiave vale dall'inizio della parola: `dra` trova "drago", ma `rago` no.
- Parole chiave vuote = voce sempre attiva.
- Il lorebook è globale (vale per tutte le chat). Il testo inserito è limitato a circa il 15% del context.
- **Esporta lore** salva le voci in un file.

## 10. Impostazioni

**Memoria e opzioni > Impostazioni.**

| Impostazione | Cosa fa |
|---|---|
| **URL di Ollama** | predefinito `http://localhost:11434`. Da telefono con `avvia-chat-rete` si imposta da solo |
| **Temperature** | creatività (più alto = più vario) |
| **Top P**, **Top K** | campionamento delle parole |
| **Context (token)** | token massimi del prompt (predefinito 8192). Più context = più memoria RAM/VRAM e risposte più lente. Se il PC fatica prova 4096 |
| **Max token risposta** | lunghezza massima di una risposta (col thinking acceso viene alzata da sola, vedi [sezione 7](#7-come-si-usa-lapp)) |
| **Repeat penalty** | riduce le ripetizioni |
| **Riassunto automatico dei messaggi vecchi** | sì/no |
| **Taglia a fine frase le risposte interrotte dal limite di token…** | solo roleplay: se la risposta si ferma per il limite, viene tagliata all'ultima frase completa e puoi proseguire con **Continua** |
| **Esporta backup completo** | vedi [sezione 11](#11-import-export-e-backup) |

## 11. Import, export e backup

### Esportare

| Cosa | Come |
|---|---|
| **Personaggio** | ✎ sul personaggio > **Esporta**. Solo la scheda, senza chat |
| **Chat** | ⇩ nella lista chat. Contiene messaggi, varianti, ricordi fissi, riassunto, il nome usato in quella chat e la scheda del personaggio |
| **Lorebook** | **Memoria e opzioni > Lorebook > Esporta lore** |
| **Tutto** | **Memoria e opzioni > Impostazioni > Esporta backup completo**: personaggi, chat, lorebook, tua persona e impostazioni |

### Importare

Un solo pulsante, in fondo alla barra sinistra. Puoi scegliere più file insieme: il tipo viene riconosciuto da solo. I file esportati hanno un numero di versione: l'app importa anche quelli delle versioni precedenti (li adegua da sola) e rifiuta quelli creati da una versione più recente.

| File | Cosa succede |
|---|---|
| **Personaggio** | file dell'app e card JSON in stile SillyTavern (se la card contiene un lorebook, le voci vengono importate). Le card PNG non sono supportate |
| **Chat** | viene collegata al personaggio con lo stesso nome e descrizione; se non esiste viene creato |
| **Lorebook** | le voci vengono aggiunte a quelle esistenti |
| **Backup completo** | **sostituisce** tutti i dati (chiede conferma). L'URL di Ollama del dispositivo non viene cambiato |

Fai un backup ogni tanto: i dati stanno nel browser ([sezione 12](#12-dove-sono-i-dati)).

## 12. Dove sono i dati

- Chat, personaggi, lorebook e impostazioni sono salvati nel browser (`localStorage`), **non** nella cartella dei file.
- Sono legati all'indirizzo: `localhost:8000`, l'indirizzo di rete del telefono e un file aperto con doppio clic hanno archivi separati. Usa sempre lo stesso indirizzo.
- Lo spazio è di circa 5 MB (dipende dal browser): bastano per molte chat, ma un avviso *Spazio del browser pieno* significa che devi fare un backup e liberare spazio.
- Se i dati salvati risultassero illeggibili, l'app riparte da zero e conserva una copia grezza nel browser (chiave `occ_corrotto`).
- All'avvio l'app sistema da sola i dati incompleti o modificati a mano (liste o testi non validi, impostazioni numeriche sbagliate): i dati validi non vengono toccati. Un backup con la struttura sbagliata viene rifiutato all'import.
- **Non tenere due schede** della stessa app aperte insieme nello stesso browser: ognuna salva tutti i dati e l'ultima che salva cancella le modifiche dell'altra. Se compare l'avviso *Un'altra scheda ha modificato i dati*, ricarica la pagina prima di continuare.
- I dati hanno un **numero di versione**: quando aggiorni l'app si convertono da soli. Prima di convertire, l'app tiene nel browser una copia dei vecchi dati (chiave `occ_pre_migrazione`), se non superano circa 1,2 MB.
- Se i dati sono stati creati da una versione **più recente** dell'app, l'app non li tocca e mostra un avviso: aggiornala.
- Pulire i dati del sito dal browser cancella tutto.
- Il pulsante **Reset** ([sezione 7](#7-come-si-usa-lapp)) cancella tutto e riparte da zero: fai prima un backup.

## 13. Problemi comuni

- **"Impossibile collegarsi a Ollama"**: Ollama è spento, oppure l'URL in Impostazioni non è quello giusto. L'app riprova da sola ogni pochi secondi.

- **"Modello non trovato"**: Scaricalo con `ollama pull nome-modello` e riprova.

- **"Ollama: …" con un motivo (per esempio memoria insufficiente)**: È l'errore reale di Ollama. Prova un modello più piccolo o abbassa il context.

- **"Risposta vuota"**: Il modello non ha prodotto testo. Con i modelli che ragionano prova ad alzare **Max token**.

- **Il pulsante "Thinking" non compare**: Il personaggio deve essere in modalità Assistente o Creatore e il modello scelto deve supportare il thinking (esempio: qwen3). Se usi il telefono, aggiorna anche `server.py`: deve inoltrare `/api/show`.

- **Col thinking acceso la risposta è vuota o si ferma**: Il ragionamento ha usato tutti i token: alza **Max token** nelle Impostazioni, oppure spegni il thinking.

- **Risposte lente o il PC si blocca**: Abbassa il context, usa un modello più piccolo (3B-8B), chiudi altri programmi pesanti.

- **"Python non trovato"** (nel `.bat`): Installa Python da python.org spuntando *Add Python to PATH*.

- **"La porta 8000 e' gia' in uso"**: Un altro server è attivo (anche l'altro `.bat`): chiudi la sua finestra, oppure usa un'altra porta ([sezione 4](#4-avvio-manuale-windows-mac-linux)).

- **Dal telefono non si apre**: Vedi la fine della [sezione 5](#5-uso-dal-telefono-stessa-rete-wi-fi).

- **Ho riaperto l'app e non vedo le mie chat**: Stai usando un indirizzo diverso da quello usato prima ([sezione 12](#12-dove-sono-i-dati)).

- **Avviso «dati creati da una versione più recente»**: Stai usando un file dell'app più vecchio dei dati salvati. Usa l'ultima versione del file `offline-character-chat.html`: nel frattempo i dati restano intatti.

## 14. Limiti noti

Non ci sono ancora: avatar, ramificazione delle conversazioni (branching), più personaggi nella stessa chat, card PNG, tabelle markdown, import del formato nativo di Perchance. I `.bat` sono per Windows; su Mac e Linux usa l'avvio manuale.

## 15. Funzionamento senza internet

L'app funziona **senza internet**: basta una rete locale (per esempio il Wi-Fi di casa anche se il router non è collegato a internet), oppure il PC da solo.

- **Niente viene caricato da internet:** nessun font, script, immagine o servizio esterno. L'unico indirizzo nel codice è quello di Ollama sul tuo PC. È stato provato bloccando ogni richiesta verso internet e usando chat, thinking, Creatore, cambio lingua e import/export, anche da un altro indirizzo della rete locale come fa il telefono: nessuna richiesta è uscita.
- **Internet serve solo una volta**, per scaricare Ollama, i modelli e Python ([sezione 2](#2-cosa-serve)).
- **Wi-Fi senza internet:** PC e telefono devono stare nella stessa rete. `server.py` parte anche quando non c'è nessun servizio di nomi (DNS) raggiungibile. Se non trova nessuna rete, lo scrive nella finestra nera.
- **Se il router cambia l'indirizzo del PC:** usa l'indirizzo mostrato nella finestra nera, che si aggiorna a ogni avvio (oppure riserva un indirizzo fisso al PC nelle impostazioni del router).
- **Se la pagina non si apre dal telefono** e il telefono dice «connesso, senza internet»: alcuni telefoni, con una Wi-Fi senza internet, preferiscono i dati mobili anche per le pagine locali. Spegni i dati mobili e riprova.
- **Senza nessuna rete** (né Wi-Fi né cavo) puoi usare l'app solo dal PC con `avvia-chat.bat`; il telefono non può collegarsi.

## 16. Creare i file `.bat` da zero

Se hai perso un `.bat`, o lo zip ti è arrivato senza, puoi ricrearlo in due minuti con il Blocco note.

### Cosa sono

Un file `.bat` (batch) è un normale **file di testo** con una lista di comandi di Windows. Quando fai doppio clic, Windows li esegue uno dopo l'altro, come se li scrivessi tu in un terminale. Non è un programma compilato e non installa nulla: dentro c'è solo il testo che vedi sotto, che puoi leggere e controllare. Serve a non dover aprire il terminale e digitare i comandi a mano ([sezione 4](#4-avvio-manuale-windows-mac-linux)). I `.bat` funzionano solo su Windows; su Mac e Linux usa l'avvio manuale.

### Cosa fanno

Nessuno dei due accende Ollama: va acceso a parte.

**`avvia-chat.bat`** (solo dal PC):

1. Va nella cartella in cui si trova e controlla che `offline-character-chat.html` ci sia.
2. Se sulla porta 8000 c'è già un server acceso, apre solo il browser e finisce.
3. Cerca Python (`py` o `python`). Se non lo trova, lo scrive e indica dove scaricarlo.
4. Dopo un paio di secondi apre il browser e avvia un piccolo server web (`python -m http.server`) raggiungibile **solo da questo PC**.
5. La finestra nera resta aperta finché usi la chat: chiuderla spegne il server. Se il server si ferma per un errore, la finestra aspetta un tasto così puoi leggerlo.

**`avvia-chat-rete.bat`** (dal PC e dal telefono):

1. Controlla che `server.py` e `offline-character-chat.html` siano nella cartella.
2. Se la porta 8000 è già occupata, lo scrive e si ferma, senza avviare un secondo server.
3. Cerca Python come sopra.
4. Apre il browser sul PC e avvia `python server.py --lan`: serve la pagina a tutti i dispositivi della tua Wi-Fi e inoltra a Ollama solo `/api/chat`, `/api/tags` e `/api/show` ([sezione 5](#5-uso-dal-telefono-stessa-rete-wi-fi)). Nella finestra compare l'indirizzo da aprire sul telefono.

### Come crearli (Windows)

1. Metti `offline-character-chat.html` in una cartella. Per il `.bat` di rete serve nella stessa cartella anche `server.py`. I `.bat` devono stare **nella stessa cartella** di questi file.
2. Apri il **Blocco note** (menu Start, scrivi *Blocco note*).
3. Copia tutto il codice di `avvia-chat.bat` (blocco sotto) e incollalo nel Blocco note vuoto.
4. Scegli **File, Salva con nome** e vai nella cartella del punto 1.
5. Dal menu *Tipo file* scegli **Tutti i file (\*.\*)**. Se non lo fai, Windows aggiunge `.txt` e il file non parte.
6. In *Nome file* scrivi esattamente `avvia-chat.bat`. Se vedi il menu *Codifica*, scegli **ANSI**. Poi premi *Salva*.
7. Ripeti i punti 2-6 per `avvia-chat-rete.bat`, se ti serve l'uso da telefono.
8. Controlla il nome in Esplora file. Se si chiama `avvia-chat.bat.txt`, le estensioni sono nascoste: da *Visualizza, Mostra* attiva **Estensioni nomi file** e togli `.txt` dal nome.
9. Doppio clic sul `.bat`. Si apre la finestra nera e poi il browser.

Copia il codice **senza modificarlo**. Le lettere accentate sono scritte senza accento (`e'` al posto di `è`) di proposito: così funziona con qualsiasi codifica del file.

### Codice di `avvia-chat.bat` (solo PC)

```bat
@echo off
setlocal
title Offline Character Chat
cd /d "%~dp0"

if not exist "offline-character-chat.html" (
  echo Non trovo offline-character-chat.html in questa cartella.
  echo Metti questo file .bat nella stessa cartella dell'HTML.
  pause
  exit /b 1
)

set "PORT=8000"
set "URL=http://localhost:%PORT%/offline-character-chat.html"

rem Se il server e' gia' acceso, apri solo il browser
netstat -ano | findstr /R /C:":%PORT% .*0.0.0.0:0" >nul 2>&1
if %errorlevel%==0 (
  echo Il server e' gia' attivo. Apro il browser.
  start "" "%URL%"
  exit /b 0
)

set "PY="
where py >nul 2>&1 && set "PY=py"
if not defined PY where python >nul 2>&1 && set "PY=python"
if not defined PY (
  echo Python non trovato. Installalo da https://www.python.org/downloads/
  echo e spunta "Add Python to PATH" durante l'installazione.
  pause
  exit /b 1
)

echo Offline Character Chat: %URL%
echo.
echo Tieni aperta questa finestra mentre usi la chat.
echo Chiudila per spegnere il server. Ollama va acceso a parte.
echo.

rem Apre il browser dopo 2 secondi, quando il server e' pronto
start "" /min cmd /c "ping -n 3 127.0.0.1 >nul & start %URL%"

%PY% -m http.server %PORT% --bind 127.0.0.1
echo.
echo Il server si e' fermato. Se vedi un errore qui sopra, copialo e mandamelo.
pause
```

### Codice di `avvia-chat-rete.bat` (PC + telefono)

```bat
@echo off
setlocal
title Offline Character Chat (rete)
cd /d "%~dp0"

if not exist "server.py" (
  echo Non trovo server.py in questa cartella.
  pause
  exit /b 1
)
if not exist "offline-character-chat.html" (
  echo Non trovo offline-character-chat.html in questa cartella.
  pause
  exit /b 1
)

set "PORT=8000"
netstat -ano | findstr /R /C:":%PORT% .*0.0.0.0:0" >nul 2>&1
if %errorlevel%==0 (
  echo La porta %PORT% e' gia' in uso: un altro server e' attivo.
  echo Chiudi la sua finestra e riprova.
  pause
  exit /b 1
)

set "PY="
where py >nul 2>&1 && set "PY=py"
if not defined PY where python >nul 2>&1 && set "PY=python"
if not defined PY (
  echo Python non trovato. Installalo da https://www.python.org/downloads/
  echo e spunta "Add Python to PATH" durante l'installazione.
  pause
  exit /b 1
)

echo Se Windows chiede l'accesso di rete, consenti le reti PRIVATE.
echo.
start "" /min cmd /c "ping -n 3 127.0.0.1 >nul & start http://localhost:%PORT%/"
%PY% server.py --lan %PORT%
echo.
echo Il server si e' fermato. Se vedi un errore qui sopra, copialo e mandamelo.
pause
```
