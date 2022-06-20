# Fotogrāfa pasūtījumu datu uzskaites sistēma

## Projekta apraksts
Kvalifikācijas darba uzdevums ir izveidot fotogrāfa pasūtījumu datu uzskaites sistēmu, kur klienti var pasūtīt fotogrāfa pakalpojumus, savukārt fotogrāfs tos var apskatīt un izpildīt atbilstoši klienta vēlmēm. Šī sistēma palīdzētu fotogrāfam vairāk fokusēties uz savu tiešo darbu, mazinot nepieciešamo konsultēšanās laiku ar klientu, kā arī veicinātu fotogrāfam sava laika grafika veidošanu un uzturēšanu, jo visa nepieciešamā informācija par piedāvātajiem pakalpojumiem būtu pieejama caur sistēmas mājaslapu, kā arī tur varētu veikt un automātiski uzskaitīt klientu veiktos pasūtījumus.

Šai fotogrāfa pasūtījumu uzskaites sistēmai ir jāizpilda vairākas funkcionalitātes:
* pakalpojumu pasūtīšana (no klientu puses) un to apskatīšana (gan no fotogrāfa, gan no klienta puses);
* bilžu galeriju automātiska izveide katram pasūtījumam, ievērojot tiesības tās apskatīt (no klientu puses);
* bilžu augšupielādes, apskatīšanas, lejupielādes un dzēšanas opcijas katram pasūtījumam bilžu galerijā, ievērojot tiesības dzēst un augšupielādēt bildes (gan no fotogrāfa, gan no klienta puses);
* informācijas attēlošana par fotogrāfu un katru piedāvāto pasūtījuma veidu mājaslapā;
* automātiska cenas aprēķināšana bilžu izdrukas pakalpojumam (balstoties uz to, cik bildes jāizdrukā);
* jaunu fotogrāfu pakalpojumu veidu izveide, kā arī jaunu fotogrāfu izveide sistēmā un veco fotogrāfu noņemšana (no administratora puses);
* klientu pieslēgšanās, reģistrēšanās, izrakstīšanās un profila rediģēšanas opcijas.

## Izmantotās tehnoloģijas
Projektā tiek izmantotas šādas tehnoloģijas:
* Django
* Python
* PyCharm
* HTML
* CSS
* JavaScript
* jQuery
* Font Awesome
* BootStrap
* SQLite

## Izmantotie avoti
Projekta veidošanas laikā tika izmantoti šādi informācijas avoti:
 1. [Informācija par ietvariem](https://www.monocubed.com/blog/most-popular-web-frameworks/)
 2. [Informācija par Django](https://en.wikipedia.org/wiki/Django_(web_framework))
 3. [Informācija par PyCharm](https://www.jetbrains.com/help/pycharm/quick-start-guide.html#meet)
 4. [Informācija par jQuery](https://jquery.com/)
 5. [Django dokumentācija](https://docs.djangoproject.com/en/4.0/contents/)
 6. [Bootstrap dokumentācija](https://getbootstrap.com/docs/5.2/getting-started/introduction/)
 7. [Font Awesome ikonu bibliotēka un rīku komplekts](https://fontawesome.com/docs/web/)
 8. [Diagrammu veidošanas rīks](https://app.diagrams.net/)
 9. [Čena notācija diagrammu veidošanai](https://vertabelo.com/blog/chen-erd-notation/)
10. [Izglītojoša vietne kodēšanas apguvei](https://www.w3schools.com/)
11. [Dokumentācijas krātuve un mācību resurss tīmekļa izstrādātājiem](https://developer.mozilla.org/en-US/docs/Web)
12. [Bezmaksas fotogrāfiju vietne](https://pixabay.com/)
13. [Pamācība par Django vietņu mitināšanu](https://studygyaan.com/django/host-django-website-application-for-free-in-5-minutes#google_vignette)
14. [Tīmekļa vietņu mitināšanas pakalpojums Python programmām](https://www.pythonanywhere.com/)
15. [Mājaslapu skiču veidošanas rīks](https://balsamiq.cloud/)
16. [Minimālās aparatūras prasības](https://ssiddique.info/ideal-computer-specs-for-python-programming.html/)

## Uzstādīšanas instrukcijas
Sistēmas palaišana no administratora puses:
1. Sākumā visi sistēmas faili ir jālejupielādē uz servera, to var izdarīt, lejupielādējot visus failus no github repozitorijas
2. Jāpārliecinās, ka uz servera ir pareizi uzinstalēta kāda no Python 3.8., 3.9. vai 3.10. versijām, ja tas nav izdarīts, tad to var instalēt caur [oficiālo Python mājaslapu](https://www.python.org/downloads/release/python-397/)
3. Caur termināli ir jāatver sistēmas failu mapīte, kur atrodas manage.py fails
4. Terminālī ir jāieraksta zemāk minētā komanda, lai instalētu sistēmai nepieciešamās failu pakotnes
```
python -m pip install -r requirements.txt
```
5. Lai palaistu sistēmu - terminālī ir jāieraksta zemāk minētā komanda
```
python manage.py runserver
```
6. Sistēmas mājaslapu var apskatīt atbalstītā pārlūkprogrammā, ievadot un meklējot mājaslapas lokālo saiti - http://127.0.0.1:8000/

Sistēmas palaišana no lietotāja puses:
1. Jāievada un jāmeklē mājaslapas saite atbalstītā pārlūkprogrammā (līdz 2022. gada 7. septembrim ir iespēja apskatīt mājaslapu, izmantojot saiti - http://blazychan.pythonanywhere.com/)

Izveidoto lietotāju pieslēgšanās informācija pēc lomām:
*	**Klients** ar e-pastu - **janis.bebsis@fotopelle.lv** un paroli - **Parole123**
*	**Fotogrāfs** ar e-pastu - **peteris.mantons@fotopelle.lv** un paroli - **Parole123**
* **Administrators** ar e-pastu - **admin@fotopelle.lv** un paroli - **Parole123**