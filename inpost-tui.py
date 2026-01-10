# no siema
import requests
from datetime import datetime
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static, Button
from textual.containers import Vertical, VerticalScroll
from plyer import notification

# sprawdzam sb co 20 sekund
CHECK_INTERVAL = 20


# tutaj se tlumacze statusy bo kogo obchodzi raw api
STATUS_TRANSLATION = {
    "confirmed": ("Potwierdzona", "Confirmed", "📦"),
    "collected_from_sender": ("Odebrana od nadawcy", "Collected from sender", "📬"),
    "adopted_at_source_branch": ("Przyjęta w centrum logistycznym", "Adopted at source branch", "🏢"),
    "sent_from_source_branch": ("W trasie / Wysłana z oddziału", "In transit / Sent from branch", "🚚"),
    "in_transit": ("W drodze", "In transit", "🚚"),
    "ready_for_pickup": ("Gotowa do odbioru", "Ready for pickup", "📪"),
    "out_for_delivery": ("W doręczeniu", "Out for delivery", "🚛"),
    "delivered": ("Doręczona", "Delivered", "✅")
}

# nwm czy to bede robic do konca xd
LANGUAGE = "PL"


# siema rafal brzoska
def get_tracking_details(tracking_number):
    url = f"https://api-shipx-pl.easypack24.net/v1/tracking/{tracking_number}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()["tracking_details"]

# tutaj powiadamiam czy cos kurierzy szponcą
def send_notification(title, message):
    try:
        notification.notify(title=title, message=message, timeout=5)
    except Exception:
        pass


# aimbot na paczke tutaj
class PackageWidget(Static):
    def __init__(self, tracking_number: str):
        super().__init__()
        self.tracking_number = tracking_number
        self.details = []
        self.last_status = None

    def on_mount(self):
        self.update_content()
        self.set_interval(CHECK_INTERVAL, self.update_content)

    def update_content(self):
        try:
            tracking_details = get_tracking_details(self.tracking_number)
            self.details = tracking_details
            self.render_history()
        except Exception as e:
            self.update(f"[red]Błąd: {e}[/red]")

    def render_history(self):
        lines = []
        current_status = None

        # od gory do dolu
        for d in reversed(self.details):
            dt_raw = d.get("date") or d.get("datetime")
            dt = datetime.fromisoformat(dt_raw.split(".")[0])
            dt_str = dt.strftime("%d-%m-%Y %H:%M")
            status = d.get("status")
            desc = d.get("description", "")
            status_pl, status_en, emoji = STATUS_TRANSLATION.get(status, (status, status, ""))
            status_text = status_pl if LANGUAGE == "PL" else status_en

            lines.append(f"{dt_str} → {emoji} {status_text} | {desc}\n•\n•\n•")

            if current_status is None:
                current_status = status

        if self.last_status is not None and current_status != self.last_status:
            title = "📦 Zmiana statusu paczki" if LANGUAGE == "PL" else "📦 Package status update"
            send_notification(title, f"{status_text} | {desc}")

        self.last_status = current_status

        self.update("\n".join(lines))


class SettingsWidget(Static):
    def compose(self) -> ComposeResult:
        yield Button("Zmień język PL/EN", id="btn_lang") # naprawde nie wiem czy chce mi sie te tlumaczenia robic xdddd
        yield Button("Włącz/Wyłącz powiadomienia", id="btn_notify") # jak ci paczka wyfantoli to nie moja wina hehe

class InPostTUI(App): # o jeny.
    CSS_PATH = None
    BINDINGS = [("q", "quit", "Wyjdź")]

    def __init__(self):
        super().__init__()
        self.packages = {}
        self.notifications_enabled = True

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Input(placeholder="Wpisz numer paczki i naciśnij Enter", id="input_tracking")
            yield Static("")
            self.packages_container = VerticalScroll()
            yield self.packages_container
            yield Static("")
            self.settings = SettingsWidget()
            yield self.settings
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        number = event.value.strip()
        if not number:
            return
        if number in self.packages:
            return  # paka dodana
        package_widget = PackageWidget(number)
        self.packages[number] = package_widget
        self.packages_container.mount(package_widget)
        event.input.value = ""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        global LANGUAGE
        if event.button.id == "btn_lang":
            LANGUAGE = "EN" if LANGUAGE == "PL" else "PL"
            for pkg in self.packages.values():
                pkg.render_history()
        elif event.button.id == "btn_notify":
            self.notifications_enabled = not self.notifications_enabled
            text = "                             Powiadomienia: TAK" if self.notifications_enabled else "                             Powiadomienia: NIE"
            self.settings.update(f"[bold]{text}[/bold]")

    def send_notification(self, title, message):
        if self.notifications_enabled:
            send_notification(title, message)


if __name__ == "__main__":
    InPostTUI().run()
