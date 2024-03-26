# Full Stack App with FastAPI and Vercel

Sto lavorando in Windows quindi non ho bisogno di installare postgress con brew

Ho avuto problemi con i permessi dell'utente user12, ho risolto con PgAdmin aggiungendo superuser tra i Privilegi

Alembic
Il comando alembic init alembic serve a inizializzare Alembic in un progetto. 
Alembic è una libreria di migrazione di database per Python, 
comunemente usata con SQLAlchemy (uno strumento di mappatura oggetti-relazionali per Python). 
Questo comando imposta Alembic in modo che possa essere usato per gestire il 
versioning del database (https://www.sqlinpillole.it/2022/05/18/database-versioning/) nel progetto.

Quando si esegue alembic init alembic, avviene quanto segue:

Creazione della struttura della directory: Il comando crea una nuova directory denominata alembic nel progetto. 
All'interno di questa directory, alembic memorizza gli script di migrazione e alcuni file di configurazione.

File di configurazione: genera un file alembic.ini nella directory principale del progetto. 
Questo file contiene la configurazione necessaria ad Alembic per connettersi al database e altre impostazioni rilevanti.

Directory delle versioni: All'interno della directory alembic, viene creata una sottodirectory denominata versions. 
Questa directory ospiterà i singoli script di migrazione creati per modificare il database 
(ad esempio, per aggiungere tabelle, modificare schemi, ecc.)

File env.py: nella directory alembic viene creato anche un file env.py. 
Questo file è il punto di ingresso per Alembic ed è usato per configurare il contesto di migrazione, 
la connessione al database e altri aspetti dell'ambiente di migrazione.

Lo scopo dell'uso di Alembic è quello di facilitare il tracciamento e l'applicazione delle modifiche allo schema del database 
in modo controllato e coerente. 
Consente di applicare versioni incrementali al database, il che è fondamentale negli ambienti di sviluppo, test e produzione, 
soprattutto nei team di grandi dimensioni in cui più sviluppatori possono apportare modifiche al database.

Creazione in postgres db da terminale:
1. createdb -U postgres mydatabase
2. psql -d mydatabase
3.psql -U postgres -h localhost -d mydatabase 
Creazione nuovo user:
1.mydatabase=# CREATE USER user12 WITH PASSWORD 'pass12';
CREATE ROLE
2.mydatabase=# GRANT ALL PRIVILEGES ON DATABASE mydatabase TO user12;
GRANT
3.mydatabase=# \q

Impostare gli schemi
Creare il file schemas.py nella cartella principale dell'applicazione.
Definisce il modello di dati: struttura dei dati, tipo, convalida e configurazione aggiuntiva
ToDoRequest è un modello di dati con 2 tipi di dati
ToDoResponse è un modello di dati con 3 tipi di dati
Config definisce una configurazione aggiuntiva in ToDoResponse
orm_mode = True permette al modello di lavorare con ORM come SQLAlchemy. 
Utile quando si recuperano i dati da un database usando un ORM (Object-Relational Mapping) 
e si forniscono questi dati in un formato strutturato attraverso un'API.
perché vogliamo serializzare le nostre entità del database (convertire gli oggetti Python in formato JSON)

Creare l'ORM (Object-Relational Mapping)
Creare il file database.py nella cartella principale dell'applicazione
create_engine si connette con il database
sessionmaker permette di interagire con il database
declarative_base crea una classe base per i modelli del database, che saranno tutte le tabelle

Creare models.py
Qui definiremo il modello di database usando SQLAlquemy, una libreria ORM molto popolare in Python.
Utilizzando SQLAlchemy possiamo interagire con la tabella utilizzando gli oggetti ToDo, invece di scrivere manualmente i comandi SQL.
Il modello rappresenta la tabella ToDo in un database.
I tipi di colonna sono Column, Integer, String e Boolean.
__tablename__ assegna un nome alla tabella


Creare crud.py
Con i nostri helper CRUD (Create, Read, Update, Delete) 

importiamo il modello e lo schema che abbiamo definito in precedenza

Session è usato per gestire le operazioni sul database

create_todo crea un nuovo task todo nel database

db: Session è una sessione SQLAlchemy per interagire con il database
todo: schemas.ToDoRequest è un oggetto Pydantic con i dati del nuovo compito todo
db_todo crea un nuovo compito ToDo
db_add aggiunge il nuovo task ToDo alla sessione del database
db.commit salva le modifiche nel database
db.refresh aggiorna il database
restituisce l'oggetto db_todo
read_todos visualizza tutte le attività da fare non completate

se tutti completati, visualizza tutti i compiti completati
read_todo visualizza l'attività todo identificata con l'id

uddate_todo aggiorna il todo identificato con l'id

se l'attività non esiste, restituisce Nessuno
se il compito esiste, lo aggiorna e lo salva
delete_todo elimina l'attività todo identificata con l'id

se il compito non esiste, restituisce Nessuno
se il compito esiste, lo elimina e salva le modifiche


Configurare il router
Creare il nuovo file routers/todos.py
Percorsi CRUD dell'API FastAPI
APIRouter crea il router API con il prefisso /todos
get_db apre e chiude una sessione SQLAlchemy
Depends(get_db) inietta una sessione db su ogni rotta
@router.post: rotta per la creazione di un nuovo task todo
    schemas.ToDoRequest è il modello che convalida i tipi di dati
    utilizza la funzione create_todo definita in crud.py
@router.get("") it /todos: rotta per visualizzare tutti i compiti
    utilizza la funzione read_todos definita in crud.py
    può filtrare i compiti in base allo stato completato
@router.get("/{id}"): rotta per visualizzare un compito in base all'id
    utilizza la funzione read_todo definita in crud.py
    se non viene trovata, restituisce un messaggio di errore 404
@router.put("/{id}"): rotta per aggiornare un compito per id
    utilizza la funzione update_todo definita in crud.py
@router.delete("/{id}"): rotta per visualizzare un compito per id
    utilizza la funzione delete_todo definita in crud.py

Ho avuto problemi con pydantic. Ho dinstallato la libreria e installata con la versione 1.9.2
Poi in config avevo from pydantic_settings import BaseSettings
ma corretto è: from pydantic import BaseSettings

Una volta terminato il backend. 
Run the server from the terminal

uvicorn main:app --reload 

Ho avuto problemi quindi:
cd c:\Users\alfie\Desktop\AI_project\backend
uvicorn main:app --reload --port 8001

In a second terminal window, make the following tests (need httpie installed)

pip install httpie

Create one to-do task:

http POST http://localhost:8001/todos name="walk Fido" completed=false

Display all the to-do tasks:

http GET http://localhost:8001/todos

Display the to-do task with the id=1:

http GET http://localhost:8001/todos/1

Update it changing completed to true:

http PUT http://localhost:8001/todos/1 name="walk Fido" completed=true

Display all the to-do tasks:

http GET http://localhost:8001/todos

Create a second to-do task:

http POST http://localhost:8001/todos name="feed Fido" completed=false

Display all the to-do tasks:

http GET http://localhost:8001/todos

Delete the to-do task with the id=1:

http DELETE http://localhost:8001/todos/1

Display all the to-do tasks:

http GET http://localhost:8001/todos

The following should get a "to do not found" message

http GET http://localhost:8001/todos/1

N.B: aggiungi per gli step di controllo funzionamento backend le immagini che hai in images

Terminal: npx create-next-app@latest

√ What is your project named? ... ai_app
√ Would you like to use TypeScript? ... No
√ Would you like to use ESLint? ... Yes
√ Would you like to use Tailwind CSS? ... No
√ Would you like to use `src/` directory? ... No 
√ Would you like to use App Router? (recommended) ... No 
√ Would you like to customize the default import alias (@/*)? ... No 

Si crea automaticamente la cartella ai_app per la parte front-end

Creare .env con url dell'API backend

Modificare pages/index.js
Rimuovere il contenuto predefinito fornito per questo file, il contenuto seguente importa 2 componenti next.js 
che non abbiamo ancora creato:
    Layout (possiamo riutilizzare questo componente in qualsiasi pagina).
    ToDoList (tutte le nostre funzionalità TODO).
Il componente ToDoList sarà all'interno del componente Layout. Questa operazione si chiama "composizione".

Creare components/layout.js
Il {props.children} è dove usiamo composition, 
il che significa che possiamo sostituirlo con un altro componente React.

Creazione di components/ai_list.js e spiegazione componenti
Questo codice è per un componente React chiamato ToDoList, 
che fa parte di web application per la gestione di un elenco di compiti o "todos". 
Ecco una semplice descrizione di ciò che fa questo componente:

Imports and Setup:
Importa stili CSS.
Vengono importati diversi hook da React (useState, useEffect, useCallback, useRef) e un utility (debounce da lodash). 
Questi sono utilizzati per managing state, side effects, and optimizing function calls.
Viene importato anche il componente ToDo, che viene usato per render ogni todo item.

Component State Management:

useState è usato per creare diversi state variables: 
todos (l'elenco dei todo), mainInput (il valore di un campo di input principale per aggiungere nuovi todos)
e filter (per filtrare i todos visualizzati).
useRef è usato per creare un ref (didFetchRef) per verificare se i todos sono stati fetch.

Fetching dei todos sul montaggio del componente:

useEffect è usato per fetch l'elenco dei todos al primo rendering del componente. 
Controlla didFetchRef per assicurarsi che il fetch avvenga una sola volta.

Functions for Handling Todos:

fetchTodos fetch i todos da un'API, eventualmente filtrati in base completion status.
debouncedUpdateTodo è una versione debounced di una funzione updateTodo,
usata per aggiornare i todos, con un ritardo, per migliorare le prestazioni.
handleToDoChange gestisce le modifiche agli elementi di un todo (mark come 'completato').
updateTodo aggiorna un todo nel backend.
addToDo aggiunge un nuovo todo all'elenco.
handleDeleteToDo elimina un todo.

Handling User Input:

handleMainInputChange aggiorna lo stato mainInput quando l'utente digita in input.
handleKeyDown check la presenza del tasto 'Invio' per aggiungere un nuovo todo.

Filtering Todos:

handleFilterChange aggiorna lo stato del filtro e fetch i todo in base al filtro selezionato.

Rendering del componente:

L'istruzione return contiene il JSX (sintassi simile all'HTML) per il rendering del componente.
Include un campo di input per aggiungere nuovi todos, un messaggio di caricamento, 
un elenco di todos (utilizzando il componente ToDo per ogni elemento) 
e pulsanti per filtrare i todos in base a diversi criteri (tutti, attivi, completati).
In parole povere, il componente ToDoList consente agli utenti di aggiungere, visualizzare, filtrare e cancellare i todo. 
Interagisce con un'API per il recupero e l'aggiornamento dei dati 
e utilizza varie funzionalità di React per handling state, effects and user interactions.

Il codice precedente è un tipico utilizzo degli hook useState e useRef di React in un componente funzionale. 
Vediamo cosa fa ogni riga in termini semplici:

const [todos, setTodos] = useState(null):

Questa riga crea una variabile di stato chiamata todos con una corrispondente funzione setTodos. 
useState(null) inizializza todos con il valore null.
Si può usare setTodos per aggiornare il valore di todos in un secondo momento nel componente. 
In questo modo, il componente viene renderizzato nuovamente con il nuovo valore.

const [mainInput, setMainInput] = useState(''):

Allo stesso modo, questa riga crea un'altra variabile di stato mainInput con la sua funzione setMainInput.
È inizializzata con una stringa vuota ''. 
Potrebbe essere utilizzata, ad esempio, per tracciare il valore di un campo di input di testo nell'interfaccia utente.
setMainInput può essere usato per aggiornare mainInput, attivando un re-render con il valore aggiornato.

const [filter, setFilter] = useState():

Questa riga crea una variabile di stato filter con un setFilter.
Poiché useState() viene chiamato senza alcun argomento, filter viene inizializzato come undefined.
setFilter può essere usato per aggiornare il valore di filter per vari scopi, 
come l'applicazione di un filtro all'elenco dei todos.

const didFetchRef = useRef(false):

Questa riga utilizza l'hook useRef per creare un oggetto ref mutabile chiamato didFetchRef.
Il ref è inizializzato con il valore false. A differenza delle variabili di stato, 
la modifica del valore di un ref non causa un re-render del componente.
Questo oggetto ref può essere usato per verificare se una certa azione (come il recupero dei dati) è già stata eseguita, 
senza dover ripetere il rendering.

In sintesi, questo codice imposta due parti di stato (todos e mainInput, con il filtro opzionale) 
per tracciare e aggiornare i dati del componente e utilizza un ref (didFetchRef) come variabile persistente 
che non causa un nuovo rendering quando il suo valore cambia. 
Questo schema è comune nei componenti funzionali, per gestire sia lo stato dell'interfaccia utente, sia alcune azioni come il recupero dei dati.

useEffect(() => {...}, []):

useEffect è un hook che esegue del codice in base a determinate condizioni.
L'array vuoto [] come secondo parametro di useEffect significa che il codice all'interno di useEffect verrà eseguito solo una volta, 
subito dopo il rendering iniziale del componente.
Questo è simile al metodo del ciclo di vita componentDidMount della classe components.
if (didFetchRef.current === false) {...}:

All'interno di useEffect, c'è un'istruzione if che controlla il valore di didFetchRef.current.
didFetchRef è un ref creato con hook useRef ed è usato per verificare se un'azione è già stata eseguita.
In questo caso, si controlla se è stata chiamata una funzione per recuperare i dati (fetchTodos).

didFetchRef.current = true:

Se didFetchRef.current è false (cioè fetchTodos non è ancora stato chiamato), il codice imposta didFetchRef.current su true.
Questo per garantire che la funzione di recupero dei dati venga eseguita una sola volta.

fetchTodos():

Si tratta di una chiamata a una funzione chiamata fetchTodos, che probabilmente recupera i dati da un'API o da una fonte esterna.
La funzione viene chiamata all'interno dell'istruzione if, 
per assicurarsi che venga eseguita solo la prima volta che il componente viene reso.

In parole povere, questo hook useEffect è usato per eseguire la funzione fetchTodos solo una volta 
dopo che il componente è stato render per la prima volta 
e didFetchRef è usato per assicurarsi che questa funzione non venga eseguita più di una volta. 
Questo schema è utile per recuperare dati che devono essere caricati una sola volta,
quando il componente appare inizialmente sullo schermo.

Funzione asincrona denominata fetchTodos, utilizzata per recuperare un elenco di cose da fare (task) 
da una fonte esterna (come un server o un'API):

async function fetchTodos(completed) {...}:

async indica che questa funzione è asincrona, cioè può eseguire operazioni che richiedono un certo tempo per essere completate 
(come il recupero di dati da un'API) senza bloccare l'esecuzione di altro codice.

completed --> è un parametro che la funzione può accettare. 
Viene utilizzato per determinare quali todos completati recuperare.

Determinare il percorso dell'API:
Inizialmente, il percorso è impostato su '/todos', che sembra essere l'endpoint per recuperare i todos.

Se completed non è undefined, la funzione modifica il percorso per includere un parametro di query completed. 
Questo parametro è probabilmente usato per filtrare i todos in base al fatto che siano stati completati o meno sul lato server.

Recuperare i dati:
La funzione usa l'API fetch per fare una richiesta di rete all'URL fornito, 
che è costruito usando process.env.NEXT_PUBLIC_API_URL (l'URL di base dell'API) e il percorso.
Attendere la risposta di fetch. Questo è possibile perché la funzione è asincrona.
Elaborare la risposta:
Una volta ricevuta la risposta, viene richiamato res.json() per convertire la risposta in un formato JSON. 
Anche in questo caso, si utilizza await per attendere il completamento del processo.
I dati JSON, presumibilmente un elenco di cose da fare, vengono quindi memorizzati in una variabile chiamata json.

Aggiornamento dello stato con i dati recuperati:
Infine, la funzione aggiorna lo stato del componente chiamando setTodos(json). 
Questo aggiorna lo stato dei todos con i dati recuperati, causando probabilmente un nuovo rendering del componente 
e la visualizzazione del nuovo elenco di todos.

In parole povere, fetchTodos è una funzione che recupera un elenco di todo da un server 
e aggiorna lo stato del componente con questi elementi. 
La funzione può anche filtrare i todos in base al loro stato di completamento, se viene fornito il parametro completed.

La riga di codice precedente utilizza due hook di React, 
useCallback e debounce della libreria lodash, per creare una versione debounced di una funzione updateTodo:

Funzione updateTodo: Si tratta di una funzione che esegue qualche operazione di aggiornamento, 
come l'aggiornamento di una voce todo. Tali operazioni sono spesso legate all'input dell'utente o ad altre interazioni rapide.

debounce(updateTodo, 500):

debounce è una funzione della libreria lodash che limita la velocità di esecuzione di una funzione.
Quando si avvolge updateTodo con debounce, si crea una nuova funzione che esegue updateTodo 
solo dopo che non è stata chiamata per 500 millisecondi.
Questo è utile per ridurre il numero di volte in cui updateTodo viene chiamato, 
il che può essere vantaggioso per le prestazioni, soprattutto se updateTodo comporta richieste di rete o altri calcoli pesanti.

Hook useCallback:

useCallback è un hook di React che restituisce una versione memorizzata della funzione di callback 
che cambia solo se una delle dipendenze è cambiata.
In questo caso, useCallback è usato per memorizzare la versione debounced di updateTodo. 
L'array di dipendenze vuoto [] significa che la funzione memorizzata sarà creata una sola volta 
e non cambierà nei rendering successivi del componente. 

const debouncedUpdateTodo:

La funzione debounced è memorizzata in una costante denominata debouncedUpdateTodo.
È ora possibile utilizzare debouncedUpdateTodo nel componente, al posto di updateTodo, 
per le operazioni che si desidera debounzare, come la gestione delle modifiche di input in tempo reale.

In parole povere, questo codice crea una versione della funzione updateTodo che viene attivata solo se c'è una pausa di 500 millisecondi
tra un'invocazione e l'altra, evitando che venga eseguita troppo frequentemente. 
Questo può migliorare le prestazioni e l'esperienza dell'utente, soprattutto nei casi di eventi che si verificano rapidamente, 
come la digitazione di una barra di ricerca o il ridimensionamento di una finestra.

Function Definition:

handleToDoChange è una funzione che accetta due parametri: 
e (un oggetto evento proveniente da un'interazione dell'utente, come la digitazione di un campo di testo 
o la selezione di una casella di controllo) 
id (l'identificatore univoco di un elemento todo).

Extracting Information from the Event:

const target = e.target: Ottiene l'elemento di destinazione che ha trigger l'evento.
const value = target.type === 'checkbox' ? target.checked : target.value: Determina il valore da aggiornare. 
Se l'elemento di destinazione è una casella di controllo, utilizza la proprietà checked; altrimenti, utilizza la proprietà value.
const name = target.name: ottiene il nome dell'elemento di destinazione, 
che probabilmente corrisponde a una proprietà dell'item todo (come 'completato' o 'titolo').

Finding and Updating the Todo Item:

const copy = [...todos]: Crea una copia dell'elenco corrente dei todos. 
Questo è importante per l'immutabilità, un concetto chiave di React.
const idx = todos.findIndex((todo) => todo.id === id): Trova l'indice dell'oggetto todo che deve essere aggiornato in base al suo id.
Costruisce un nuovo oggetto todo (changedToDo) copiando l'item todo esistente e aggiornando la proprietà corrispondente
al nome dell'elemento di destinazione con il nuovo valore.

Updating the State:

copy[idx] = changedToDo: Ripone l'elemento aggiornato nella posizione corretta nella copia della todo list.
debouncedUpdateTodo(changedToDo): Richiama una funzione debounced per aggiornare l'elemento da fare, 
probabilmente rendendo le modifiche persistenti in un database o in un backend (questa funzione è definita altrove).
setTodos(copy): Aggiorna lo stato dell'elenco di cose da fare con il nuovo elenco modificato.
Questo attiva una nuova resa del componente con i dati aggiornati.

In parole povere, handleToDoChange è una funzione che aggiorna lo stato di una voce todo 
quando l'utente interagisce con essa (ad esempio spuntandola o modificandone il testo). 
Assicura che le modifiche siano riflesse sia nell'interfaccia utente sia, tramite debouncedUpdateTodo, 
potenzialmente in un backend o in un database. 
L'uso del debouncing aiuta a ottimizzare le prestazioni, soprattutto in caso di modifiche frequenti e rapide.

Asynchronous Function (async) updateTodo:

La parola chiave async indica che la funzione è asincrona, 
cioè può eseguire operazioni che potrebbero richiedere del tempo per essere completate, 
come l'invio di una richiesta a un server, senza bloccare l'esecuzione di altro codice.

Function Purpose:

La funzione updateTodo accetta un argomento todo, che è un oggetto che rappresenta un item todo.

Preparing the Data for Update:

All'interno della funzione, viene creato un nuovo oggetto dati, contenente il name e le proprietà completed del todo. 
Questi dati saranno inviati al server per aggiornare il todo corrispondente.

Making an HTTP Request:

La funzione effettua quindi una richiesta HTTP utilizzando la funzione fetch.
process.env.NEXT_PUBLIC_API_URL + /todos/${todo.id}``: Costruisce l'URL per la richiesta, 
combinando un URL API di base memorizzato in una variabile d'ambiente con l'endpoint specifico per l'aggiornamento di un todo 
(identificato da todo.id).
La richiesta viene effettuata con il metodo PUT, comunemente usato per aggiornare le risorse nelle API RESTful.

Sending the Data:

body: JSON.stringify(data): L'oggetto dati viene convertito in una stringa JSON e incluso nel corpo della richiesta.
header: {"Content-Type": "application/json" }: Le intestazioni della richiesta indicano che il corpo della richiesta è in formato JSON.

Awaiting the Response:

const res = await fetch(...): La parola chiave await è usata per attendere la risposta del server. 
La risposta viene memorizzata nella variabile res, anche se questo codice non fa nulla con res dopo averla ricevuta.

In parole povere, updateTodo è una funzione che invia una voce aggiornata a un server. 
Utilizza una richiesta HTTP asincrona per inviare i dati aggiornati (come il nome dell'impegno e se è stato completato) 
a un endpoint API specifico. Il server può quindi elaborare la richiesta e aggiornare l'impegno nel database o nel sistema di backend.

Asynchronous Function addToDo:

funzione async addToDo(nome) {...}: Questa è una funzione asincrona chiamata addToDo. 
Richiede un parametro, name, che rappresenta il nome dell'elemento da aggiungere.
Essendo asincrona, può eseguire operazioni come le richieste di rete senza bloccare altre operazioni.

Making a Network Request:

La funzione invia una richiesta di rete a un server utilizzando l'API fetch.
L'URL per la richiesta è costruito a partire da una variabile d'ambiente (process.env.NEXT_PUBLIC_API_URL) 
e dal percorso endpoint /todos/. È qui che verrà inviato l'elemento todo.
Si utilizza il metodo POST, comunemente usato per inviare dati per creare una nuova risorsa (in questo caso, un nuovo todo).

Sending Data:

Il body della richiesta è una stringa JSON contenente i dati del nuovo todo. 
Include il name dell'impegno e lo stato di completed, inizialmente impostato su false.
Le intestazioni specificano che il contenuto inviato è in formato JSON.

Handling the Server Response:

await è utilizzato per attendere la risposta del server. La risposta viene memorizzata nella variabile res.
Se la risposta ha esito positivo (res.ok), la funzione procede all'elaborazione della risposta.
await res.json() converte il corpo della risposta in un oggetto JavaScript, memorizzato in json. 
Questo oggetto rappresenta probabilmente l'item todo appena creato.

Updating the Todo List:

La funzione crea una nuova copy dell'array, estendendo l'array di todos corrente e aggiungendo il nuovo elemento (json) alla fine.
setTodos(copy) viene richiamato per aggiornare lo stato dell'elenco dei todo con questo nuovo array. 
Questo farà sì che il componente venga nuovamente renderizzato e visualizzi l'elenco aggiornato, comprensivo dei nuovi todo aggiunti.

In parole povere, la funzione addToDo aggiunge un nuovo todo a un elenco, inviandolo a un server 
e aggiornando poi lo stato locale per riflettere questa aggiunta. 
Si tratta di uno schema comune nelle applicazioni React per la gestione degli input dell'utente 
e la sincronizzazione con un server backend.

Asynchronous Function handleDeleteToDo:

funzione async handleDeleteToDo(id) {...}: Questa è una funzione asincrona, cioè può eseguire operazioni che richiedono
un certo tempo per essere completate (come l'invio di una richiesta a un server) senza bloccare l'esecuzione di altro codice.
La funzione accetta un parametro, id, che probabilmente è l'identificatore univoco dell'elemento da cancellare.

Sending a Network Request:

La funzione invia una richiesta di rete a un server utilizzando l'API fetch.
Utilizza il metodo DELETE, comunemente usato nelle API web per rimuovere una risorsa (in questo caso, un item todo).

Setting Request Headers:

Le intestazioni indicano che il tipo di contenuto della richiesta è JSON. 
Questo fa parte del protocollo HTTP e aiuta il server a capire il formato della richiesta.

Handling the Server Response:

Attendere la risposta del server. La risposta viene memorizzata nella variabile res.
Se la risposta ha esito positivo (res.ok), la funzione procede all'aggiornamento dello stato locale.

Updating the Local State:

La funzione trova l'indice (idx) del todo da cancellare nell'elenco corrente dei todos (todos).
Crea quindi una copia dell'array todos e rimuove l'elemento all'indice trovato usando splice(idx, 1).
Infine, viene richiamato setTodos(copy) per aggiornare lo stato con il nuovo array di todos, 
che non include più l'elemento cancellato. In questo modo si attiva una nuova re-render del componente con l'elenco dei todo aggiornato.

In parole povere, la funzione handleDeleteToDo cancella un elemento specifico di un todo inviando una richiesta a un server e, 
in caso di successo, aggiorna l'elenco locale di todos per riflettere la cancellazione.
Questo schema è comune nelle applicazioni React per gestire la sincronizzazione dei dati con un server backend, 
mantenendo l'interfaccia utente aggiornata.

function handleMainInputChange(e) {...}: È una funzione che viene richiamata ogni volta che si verifica 
una modifica in uno specifico campo di input del componente.
Prende un parametro, e, che rappresenta l'oggetto evento che contiene le informazioni sull'evento di modifica.

Updating Component State:

setMainInput(e.target.value): Questa riga aggiorna lo stato del componente.
e.target si riferisce all'elemento DOM che ha scatenato l'evento (in questo caso, il campo di input).
e.target.value è il valore corrente del campo di input dopo la modifica.
setMainInput è una funzione che aggiorna la variabile di stato mainInput con il nuovo valore del campo di input.
Questo aggiornamento dello stato causerà un nuovo rendering del componente, se mainInput è utilizzato nell'output di rendering.

In parole povere, handleMainInputChange è una funzione che aggiorna lo stato mainInput del componente 
con il nuovo valore di un campo di input di testo ogni volta che l'utente digita o modifica il contenuto del campo. 
Si tratta di uno schema comune in React per gestire l'input dell'utente e mantenere lo stato del componente sincronizzato 
con l'interfaccia utente.

function handleKeyDown(e) {...}: 
È una funzione che viene richiamata ogni volta che viene premuto un tasto in un elemento a cui questa funzione è collegata (come un campo di input).
Il parametro 'e' rappresenta l'oggetto evento che contiene informazioni sull'evento di pressione del tasto.

Checking the Pressed Key:

if (e.key === 'Enter') {...}: Questa riga verifica se il tasto premuto è il tasto 'Invio'. 
La proprietà key dell'oggetto event contiene il valore del tasto premuto.

Conditionally Adding a Todo Item:

if (mainInput.length > 0) {...}: Questa condizione verifica se mainInput 
(presumibilmente una variabile di stato che tiene traccia del valore corrente di un campo di input) non è vuoto.
Se mainInput non è vuoto e il tasto 'Invio' è stato premuto, la funzione procede all'esecuzione di due azioni:
addToDo(mainInput): Richiama una funzione addToDo e passa mainInput come argomento. 
setMainInput(''): Riporta lo stato di mainInput a una stringa vuota, cancellando il campo di input. 
In genere, questa operazione viene eseguita dopo che il valore di input è stato utilizzato 
(ad esempio dopo l'aggiunta di un elemento da fare).

In parole povere, la funzione handleKeyDown è progettata per ascoltare un evento di pressione di un tasto e, 
quando viene premuto il tasto 'Invio', controlla se c'è del testo in mainInput. 
Se c'è, aggiunge un nuovo elemento todo con questo testo e poi cancella il campo di input. 
Questo tipo di funzionalità è comune nelle applicazioni per gli elenchi di cose da fare, 
che consentono agli utenti di aggiungere elementi all'elenco digitando il testo in un campo di input e premendo 'Invio'.

function handleFilterChange(value) {...}: È una funzione che probabilmente viene richiamata quando l'utente interagisce 
con un qualche tipo di controllo del filtro, come i pulsanti o un menu a discesa.
Il parametro value rappresenta la nuova opzione di filtro selezionata dall'utente.

Updating the Filter State:

setFilter(valore): Questa riga aggiorna lo stato del componente per i criteri del filtro.
setFilter è una funzione che cambia la variabile filter con il nuovo valore fornito. 
Questo probabilmente controlla quali todos vengono mostrati in base al filtro (come 'all', 'completed', 'active').

Fetching Filtered Todos:

fetchTodos(value): Dopo aver aggiornato lo stato del filtro, la funzione chiama fetchTodos, passando il nuovo valore del filtro.
fetchTodos è probabilmente una funzione che recupera i todo in base ai criteri del filtro selezionato. 
Ad esempio, potrebbe fare una richiesta di rete a un server per ottenere tutti i todo, 
only completed todos, or only active todos, depending on the filter value.

In parole povere, handleFilterChange è una funzione che aggiorna gli elementi dei todo visualizzati in base al filtro selezionato. 
Lo fa aggiornando lo stato del filtro e quindi recuperando i todo che corrispondono ai nuovi criteri del filtro. 
Si tratta di uno schema comune nelle applicazioni in cui è necessario visualizzare sottoinsiemi diversi di dati in base alla selezione
o all'interazione dell'utente.

Il componente ToDoList crea l'interfaccia utente dell'applicazione per l'elenco delle cose da fare. 
Include un campo di input per l'aggiunta di nuovi todos, visualizza un messaggio di caricamento se i todos sono ancora 
in fase di acquisizione, mostra l'elenco dei todos una volta disponibili e fornisce pulsanti per filtrare i todos visualizzati.

Creare /components/todo.js file

Il componente ToDo fa parte dell'interfaccia utente di una todo list application. 
Esso visualizza ogni todo con un checkbox per contrassegnarlo come completo, 
un campo di testo modificabile per il nome del todo e un pulsante di cancellazione con un'icona. 
Il componente consente di interagire con l'elemento da completare, tra cui la modifica dello stato di completamento, 
la modifica del nome e la rimozione dall'elenco.

Delete the content in the default css files.

Creare layout.module.css, todo-list.module.css, todo.module.css

Load the delete icon in the public folder

Run the full-stack app


