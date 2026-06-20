## Gearly
Gearly je web servis za organizaciju i osnovnu analizu opreme video igre.
Omogućava korištenje osnovnih CRUD operacija nad opremom (dodavanje, dohvaćanje, ažuriranje, brisanje), te filtriranje i sortiranje opreme pri dohvaćanju.
Gearly sadrži vizualizaciju 'snage' opreme grupirane po 'mjestu' opreme putem bar charta (stupčastog grafikona), što omogućuje uvid u distribuciju opreme.
## Use case
![static/usecase.png](https://github.com/torlakivan2008-source/Gearly/blob/main/static/usecase.png)
## Instalacija
Preuzimanje koda s GitHub-a:
```
git clone https://github.com/torlakivan2008-source/Gearly
cd Gearly
```

Koraci za Docker:
```bash
docker build -t gearly .
docker run -p 8080:8080 gearly
docker ps #provjera radi li kontenjer
```
