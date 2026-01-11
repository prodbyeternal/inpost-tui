# inpost-tui

**inpost-tui** to terminalowa aplikacja do monitorowania przesyłek InPost z interaktywnym, tekstowym interfejsem użytkownika (TUI) opartym na bibliotece [Textual](https://github.com/Textualize/textual).
Działa na wielu platformach (Linux/macOS/Windows)

---

## Funkcjonalności

- Monitorowanie wielu numerów paczek jednocześnie
- Automatyczne odświeżanie statusu paczki co 20 sekund
- Powiadomienia systemowe (Windows, macOS, Linux) wyświetlane przy zmianie statusu paczki
- Dwujęzyczny interfejs: polski oraz angielski (beta)
- Formatowanie nie omal bliskie jak na stronie

---

## Wymagania

- Python 3.10 lub nowszy
- Biblioteki Python:
  - `textual`
  - `requests`
  - `plyer`

---

## Instalacja

1. Sklonuj repozytorium:

   ```bash
   git clone https://github.com/prodbyeternal/inpost-tui.git
   cd inpost-tui
   python3 inpost-tui.py
   ```
   
2. Zainstaluj wymagane pakiety:

  ```bash
  pip install textual requests plyer
  ```

3. Uruchom aplikację poleceniem:
  ```bash
  python inpost-tui.py
  ```

---

## Instrukcja inpost-tui 101

Wpisz numer paczki i naciśnij Enter, aby dodać ją do monitoringu.

Historia statusów paczki pojawi się w oknie.

Menu ustawień na dole pozwala zmienić język (PL/EN) oraz włączyć lub wyłączyć powiadomienia.

Powiadomienia systemowe pojawią się tylko, gdy nastąpi zmiana statusu paczki.

Naciśnij q, aby wyjść z aplikacji.
