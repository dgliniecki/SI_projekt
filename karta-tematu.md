---
share_link: https://share.note.sx/mdxqmhwe#9dalkcKZZG9oTSGt+Dqi/zjv8lvS1SslMGr78DAE6fY
share_updated: 2026-09-27T09:38:22+02:00
---
# Karta zgłoszenia tematu projektu

> **Instrukcja dla zespołu.** Skopiujcie ten plik do swojego repozytorium pod nazwą `karta-tematu.md`, wypełnijcie i zacommitujcie. Punkty 1–4 wypełniacie na pierwszych zajęciach (wpisujecie je też do arkusza). Całość — do kolejnego zjazdu (L3: 3.10, L2: 15.10). Zatwierdzenie tematu dostaniecie jako komentarz w repozytorium.
> 
> Usuńcie ten blok po wypełnieniu.

**Grupa:** L3 (niestacjonarna) **Data zgłoszenia: 03.10.2026**

---

## 1. Skład zespołu

|Imię i nazwisko|Nr albumu|Rola w zespole|
|---|---|---|
|Patryk Szymański|32113|Reprezentacja, funkcja oceny, kary, walidator i metryki, dokumentacja|
|Miłosz Musiał|31988|Operatory genetyczne, pętla ewolucyjna, projektuje chromosom, dokumentacja|
|Daniel Gliniecki|31883|instancje testowe, algorytm zachłanny, zapis i odczyt, wykresy, koordynacja repozytorium, dokumentacja|

Rola to nie stanowisko, tylko deklaracja, za co ta osoba odpowiada: dane, implementacja, ewaluacja, dokumentacja, koordynacja.

## 2. Tytuł projektu

**Po polsku: Harmonogram jazd w szkole jazdy**

**Po angielsku: Driving school scheduling**

## 3. Problem

Szkoła jazdy ma 12 instruktorów, 8 samochodów i 35 kursantów. Każdy kursant ma własne okna dostępności i wymaganą liczbę godzin jazd w tygodniu. Instruktorzy mają swoje godziny pracy i tygodniowe limity. Kierownik układa grafik ręcznie, co zajmuje mu pół dnia. System ma automatycznie układać tygodniowy grafik, każda jazda dostaje kursanta, instruktora i wolne auto. Czas oczekiwania instruktorów ma być jak najmniejszy.

## 4. Dlaczego zwykły algorytm nie wystarczy

- [ ] nie umiemy zapisać reguły krok po kroku
- [x] przepis istnieje, ale jest obliczeniowo za drogi
- [ ] reguł jest za dużo i zmieniają się w czasie

_Uzasadnienie, 2–3 zdania:_

Każda jazda wymaga wyboru terminu, instruktora i auta naraz. Dla kilkudziesięciu jazd kombinacji są miliardy, więc przegląd zupełny odpada. Algorytm zachłanny, który przydziela jazdy po kolei, zajmuje szczytowe godziny na początku. Na końcu tygodnia brakuje aut i instruktorów, a kursanci z wąskimi oknami zostają bez terminu.


---

> Punkty poniżej wypełniacie do 3.10.

---

## 5. Technologia SI

- [ ] sieć neuronowa
- [ ] system ekspertowy / wnioskowanie regułowe
- [x] algorytm genetyczny
- [ ] klasyczne uczenie maszynowe
- [ ] inne:

_Dlaczego akurat ta technologia pasuje do tego problemu, 2–3 zdania:_

To problem dyskretny, z ograniczeniami twardymi i miękkimi. Ograniczenia wchodzą do funkcji oceny jako kary. Populacja wielu grafików pozwala stopniowo usuwać konflikty przez krzyżowanie i mutację.

## 6. Dane

|||
|---|---|
|Źródło|Generator syntetyczny|
|Rozmiar i format|Pliki JSON/CSV. Duża instancja: 12 instruktorów, 8 aut, 35 kursantów, 7 dni po 12 slotów 1-godzinnych. Mała instancja: 3 instruktorów, 2 auta, 6 kursantów, 2 dni|
|Czy są już dostępne?|nie|
|Jeśli nie — plan pozyskania|Skrypt w Pythonie losuje okna dostępności i wymagane godziny z zadanych rozkładów|

## 7. Stos technologiczny

_Język, biblioteki, środowisko uruchomieniowe. Pamiętajcie: wszystko ma działać na CPU, bez karty graficznej._

Python 3.11+. NumPy do chromosomu i operacji macierzowych. pandas do danych i eksportu. matplotlib do wykresów.

## 8. Kryterium sukcesu

_Po czym poznamy, że projekt działa. Jaka metryka, jaki próg. Liczba, nie deklaracja._

0 naruszeń twardych ograniczeń. Brak podwójnej rezerwacji auta lub instruktora. Jazda tylko w oknie kursanta. Limity godzin instruktorów nieprzekroczone.
Pokrycie zapotrzebowania ≥ 95%. Tyle wymaganych godzin jazd musi być zrealizowane. Pusty grafik tego nie spełnia.
Okienka poniżej 1 godz. dziennie na instruktora. Okienko to liczba wolnych godzin między pierwszą a ostatnią jazdą w danym dniu. Średnia liczona po instruktorach i dniach pracy.
Mała instancja: GA osiąga koszt równy ręcznie wyliczonemu optimum w co najmniej 9 z 10 uruchomień.

## 9. Zakres minimalny

_Co powstanie na pewno. To jest obietnica, z której będziecie rozliczeni._

Mała instancja z ręcznie wyliczonym rozwiązaniem wzorcowym.
Reprezentacja grafiku jako osobnika.
Funkcja oceny z karami za naruszenia.
Pętla ewolucyjna: selekcja turniejowa, krzyżowanie dla grafików, mutacja, warunek stopu.
Prosty algorytm zachłanny jako punkt odniesienia.

## 10. Zakres opcjonalny

_Co dorobicie, jeśli starczy czasu. Brak realizacji tej części nie obniża oceny._

Eksport grafiku do tabeli CSV/HTML z widokiem dla kursanta, instruktora i auta.
Porównanie selekcji turniejowej i ruletki pod względem szybkości zbieżności.
Wczytywanie dostępności z zewnętrznego pliku CSV.

## 11. Repozytorium

_Link:_

https://github.com/dgliniecki/SI_projekt

## 12. Główne ryzyko i plan awaryjny

_Co najprawdopodobniej pójdzie nie tak i co wtedy zrobicie._

Ryzyko: Źle wyważona funkcja oceny. Algorytm zmniejsza okienka kosztem łamania ograniczeń twardych, np. przypisuje auto dwóm osobom naraz.
Plan awaryjny: Bardzo wysokie kary za naruszenia twarde albo prosty operator naprawczy. Wagi kalibrujemy na małej instancji z ręcznie wyliczonym optimum. Dopiero potem uruchamiamy pełny eksperyment.

## 13. Podział pracy w czasie

|Etap|Kto|Szacowany czas|
|---|---|---|
|Dane i przygotowanie|Patryk Szymański, Miłosz Musiał, Daniel Gliniecki|4h, 3h, 10h|
|Implementacja|Patryk Szymański, Miłosz Musiał, Daniel Gliniecki|11h, 12h, 6h|
|Eksperymenty i ewaluacja|Patryk Szymański, Miłosz Musiał, Daniel Gliniecki|6h, 6h, 5h|
|Dokumentacja PL|Patryk Szymański, Miłosz Musiał, Daniel Gliniecki|4h|
|Dokumentacja EN|Patryk Szymański, Miłosz Musiał, Daniel Gliniecki|2h|
|Prezentacja|Patryk Szymański, Miłosz Musiał, Daniel Gliniecki|1h|
|**Razem na osobę**||**28–30 h**|

---

## Decyzja prowadzącego

_Wypełnia prowadzący — nie edytujcie tej sekcji._

- [ ] zatwierdzony
- [ ] do poprawy

**Uwagi:**
.
