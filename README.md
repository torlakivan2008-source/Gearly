## Gearly
---
Gearly je web servis za organizaciju i osnovnu analizu opreme video igre.
Omogućava osnovne CRUD operacije nad opremom (dodavanje, dohvaćanje, ažuriranje, brisanje), te filtriranje i sortiranje opreme pri dohvaćanju.
Gearly sadrži vizualizaciju 'snage' opreme grupirane po 'mjestu' opreme putem bar charta (stupčastog grafikona), što omogućuje uvid u distribuciju opreme.
## Use case
---
![static/usecase.png](https://github.com/torlakivan2008-source/Gearly/blob/main/static/usecase.png)
## Instalacija
---
Preuzimanje koda s GitHub-a:
```
git clone https://github.com/torlakivan2008-source/Gearly
cd Gearly
```

Koraci za Docker:
```bash
sudo docker build -t gearly .
sudo docker run -p 8080:8080 gearly
sudo docker ps #provjera radi li kontenjer
```
