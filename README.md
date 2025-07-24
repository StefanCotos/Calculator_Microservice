
# Calculator Microservice

## Descriere generală

Acest proiect reprezintă un microserviciu de tip calculator, dezvoltat cu ajutorul framework-ului **FastAPI**. Aplicația oferă funcționalități de calcul matematic de bază și avansate, expuse atât printr-o interfață web, cât și printr-un API REST. Soluția este modulară, cu separare clară între logica de business, rutare, autentificare, modele de date și servicii auxiliare.

## Structura proiectului

- **app/**: Conține codul sursă principal al aplicației, organizat pe module:
  - **api/**: Expune rutele pentru operații matematice și funcționalități de calculator.
  - **auth/**: Gestionează autentificarea utilizatorilor (login, înregistrare, utilitare).
  - **db/**: Inițializează și gestionează conexiunea la baza de date.
  - **models/**: Definește modelele de date folosite în aplicație (user, request).
  - **schemas/**: Definește schemele de validare pentru datele de intrare/ieșire.
  - **services/**: Implementează logica de business pentru operațiile matematice.
  - **static/**: Fișiere statice (CSS, JS, imagini) folosite de interfața web.
  - **templates/**: Șabloane HTML pentru paginile web (index, login, register).
- **run.py**: Punct de pornire pentru rularea aplicației.
- **requirements.txt**: Lista de dependințe necesare pentru rularea proiectului.
- **app.db**: Baza de date SQLite folosită pentru stocarea datelor utilizatorilor și a cererilor.

## Funcționalități principale

- Operații matematice de bază și avansate, accesibile prin API și interfață web.
- Autentificare și înregistrare utilizatori.
- Stocarea și gestionarea cererilor de calcul în baza de date.
- Interfață web modernă cu stilizare CSS și funcționalități JavaScript.

## Tehnologii folosite

- Python 3
- FastAPI
- Jinja2 (pentru template-uri HTML)
- SQLite (baza de date)
- HTML, CSS, JavaScript (frontend)

## Instrucțiuni de rulare

1. Instalează dependențele din `requirements.txt`.
2. Rulează aplicația cu:
   ```bash
   python run.py
   ```
3. Accesează interfața web la adresa [http://localhost:8000/](http://localhost:8000/).
4. Accesează documentația API (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)

Proiectul este ușor de extins, modular și potrivit pentru a fi folosit ca bază pentru aplicații web cu funcționalități matematice sau de calcul.

---

## Deploy cu Docker & Google Cloud

Aplicația a fost containerizată folosind Docker și a fost deployată pe Google Cloud. Poate fi accesată online la adresa:

[http://34.56.34.63/](http://34.56.34.63/)

### Instrucțiuni de rulare cu Docker

1. Asigură-te că ai instalat Docker.
2. Creează imaginea Docker:
   ```bash
   docker build -t calculator-fastapi .
   ```
3. Rulează containerul:
   ```bash
   docker run -d -p 8000:8000 calculator-fastapi
   ```
4. Accesează aplicația la [http://localhost:8000/](http://localhost:8000/) sau, dacă ești pe cloud, la adresa publică de mai sus.

---

## Funcționalități extinse

- Export CSV al calculelor per utilizator
- Ștergere istoric per utilizator (inclusiv anonim)
- Salvare calcule în funcție de utilizator