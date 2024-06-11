# PROJEKT SO2 
## Symulacja środowiska leśnego z wykorzystaniem wątków

### Opis projektu

[//]: # (Trzech Aktorów:)

[//]: # (- Drzewo owocowe)

[//]: # (- Ptak)

[//]: # (- Robak)
Projekt *Symulacja środowiska leśnego z wykorzystaniem wątków* jest symulacją agentową
środowiska leśnego, w którym poszczególne typy agentów wchodzą ze sobą w interakcje modyfikując swoje parametry.
Każdy z agentów biorących udział w symulacji jest reprezentowany przez osobny wątek.
W symulacji biorą udział 3 typy agentów:
- Robak - Żywi się obecnymi na planszy drzewami. Jest pożywieniem ptaków. Jego głównym atrybutym jest *fatness*, które zwiększa się wraz ze zdobywaniem pokarmu, 
oraz spada w czasie reprodukcji, poruszania się oraz bycia atakowanym. jeśli spadnie do 0, wtedy robak umiera.
Posiada dostępne 3 akcje: porusz się (*move*), jedz drzewo (*eat*), rozmnóż się (*reproduce*).
- Ptak - Żywi się obecnymi na planszy robakami oraz owocami drzew. Po zjedzeniu owoców z drzew jest w stanie zasiać
nowe drzewo. Głównym atrybutem ptaka jest *hp*, które traci w trakcie poruszania się oraz zyskuje podczas pożywiania się robakami lub owocami.
Jeśli spadnie do 0, ptak umiera.
Ponadto posiada licznik *reproducible* wskazujący za jaki czas dany agent będzie mógł rozmnożyć się. 
Posiada dostępne 5 akcji: porusz się (*move*), jedz robaka (*eat*), jedz owoc (*eat_f*), zrzuć nasiono (*populate*)
rozmnóż się (*reproduce*)
- Drzewo - Żywi się za pomocą fotosyntezy. Tworzy owoce za pomocą których się rozmnaża. Jego głównym atrybutem jest *hp*, które traci w trakcie bycia atakowanym oraz odnawia poprzez fotosyntezę.
Posiada dostępne 2 akcje: przeprowadź fotosyntezę (*eat*) oraz stwórz owoc (*fruit_create*) 

Poza agentami, na symulacje ma wpływ także losowe wydarzenie, podczas którego z podziemi wyłania się Czerw pustyni,
który pochłania wszystkich agentów na obszarze swojego działania.
Ponadto symulacja zbiera dane o liczebności poszczególnych grup agentów,
które na koniec symulacji są przedstawiane na wykresie, zapisywanym w pliku png

### Interfejs

Interfejs składa się z planszy ograniczonej znakami # po której poruszają się agenci reprezentowani w następujący sposób:
 Robak - *-*, Ptak - *B*, Drzewo - *T*, Czerw - *X*. Przykładowy widok interfejsu przedstawia poniższa ilustracja.

[//]: # (ilustracja)

### Wątki
W symulacji zostały wykorzystane następujące wątki:
- *worker* Ptaka - jest tworzony dla każdego genta typu Ptak. Wykonuje dostępne akcje agenta co interwał czasowy
- *worker* Robaka - jest tworzony dla każdego genta typu Robaka. Wykonuje dostępne akcje agenta co interwał czasowy
- *worker* Drzewa - jest tworzony dla każdego genta typu Drzewo. Wykonuje dostępne akcje agenta co interwał czasowy
- Czerw pustyni - jeden wątek sprawdzający co interwał czasowy czy zaszły okoliczności dla wykonania wydarzenia Czerwa,
oraz przeprowadzający wydarzenie
- Keyboard listener - nasłuchuje wprowadzeń użytkownika oraz odpowiednio na nie reaguje
- Data collector - zbiera dane o liczebności poszczególnych typów agentów

### Sekcje krytyczne
W symulacji zostały wykorzystane następujące sekcje krytyczne
- Plansza - mutex 
- Drzewo - mutex
- Robak - mutex
- Ptak - mutex