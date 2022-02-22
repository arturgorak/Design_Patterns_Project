# Project for Design Pattern

Projekt stworzony z myślą o przedmiocie Wzorce Projektowe. Celem projektu było stworzenie aplikacji umożliwiającej zarządzanie szkołą

## Uruchamianie programu
Aby uruchomić aplikacje należy kolejno wpisać w terminal będąc w lokalizacji projektu następujące komendy: 
1. python3 manage.py makemigrations
2. python3 manage.py migrate
3. python3 manage.py runserver

## Funkcjonalności
- Każdy użytkownik może:
  - logować się przy pomocy logina i hasła
  - zmienić hasło 
  - zmianić dane konta
  - zobaczyć swój plan zajęć
  - zobaczyć listę nauczycieli 
  - zobaczyć listę przedmiotów ze szczegółowymi danymi
- Nauczyciel może:
  - wystawiać oceny uczniom z przedmiotów, ale tylko z przedmiotów, których uczy
  - edytować wcześniej wystawione przez siebie oceny
  - usunąć wcześniej wystawione przez siebie oceny
  - zobaczyć listę wszystkich studentów
- Uczeń może:
  - zobaczyć swoje oceny wraz ze szczególowymi danymi
  - zobaczyć listę uczniów ze swojej klasy
- Dyrektor może:
  - to samo co nauczyciel, gdyż dyrektor jest również nauczycielem
  - dodawać nowych nauczycieli
  - zmieniać dane nauczycieli
  - usuwać nauczycieli
  - dodawać nowych uczniów
  - zmieniać dane uczniów
  - usuwać uczniów
  - widzieć oceny wystawione przez wszystkich nauczycieli, przy czym może tylko usuwać/ edytować własne
  - dodać rok akademicki
  - edytować rok akademicki
  - usuwać rok akademicki
- Admin może:
  - dodawać nowych nauczycieli
  - zmieniać dane nauczycieli
  - usuwać nauczycieli
  - dodawać nowych uczniów
  - zmieniać dane uczniów
  - usuwać uczniów
  - dodać rok akademicki
  - edytować rok akademicki
  - usuwać rok akademicki

## Dane logowania użytkowników
* admin
  * login: admin 
  * hasło: admin123

UWAGA! Każdy z poniższych użytkowników ma hasło: "designpatterns123"
* dyrektor (jest również nauczycielem)
  * login: director
* nauczyciele
  * Nauczyciel nr 1 
    * login: teacher1
  * Nauczyciel nr 2
    * login: teacher2
  * Nauczyciel nr 3
    * login: teacher3
* uczniowie
  * Uczeń nr 1 z klasy 1a
    * login: student1
  * Uczeń nr 2 z klasy 1a
    * login: student2
  * Uczeń nr 3 z klasy 1a
    * login: student3
  * Uczeń nr 4 z klasy 1a
    * login: student4
  * Uczeń nr 5 z klasy 1b
    * login: student5
  * Uczeń nr 6 z klasy 1b
    * login: student6
  * Uczeń nr 7 z klasy 1c
    * login: student7
  * Uczeń nr 8 z klasy 1c
    * login: student8

# Design Patterns:
 - MVT/MVC 
 - Singleton - models.py
 - Decorator - decorators.py
 - Adapter - views.py
 - Observer - models.py / wbudowane
 - Proxy - models.py
 - Iterator - models.py / views.py
 - Command - wbudowane / requesty
 - Template Method - wbudowane / klasy w views.py

