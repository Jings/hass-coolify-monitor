# Home Assistant Custom Integration: Coolify Monitor

## Ziel

Eine Custom Component für Home Assistant, die eine selbst gehostete
Coolify-Instanz überwacht: Server, Applications, Services und Datenbanken
werden automatisch erkannt (Auto-Discovery) und als Entities dargestellt.
Der Nutzer gibt nur Instanz-URL und API-Token an; danach wählt er per
Options Flow aus, welche Ressourcen er als Entities/Dashboard sehen möchte.

Datenquelle: offizielle, dokumentierte Coolify REST-API (`/api/v1`) –
kein Scraping, keine rechtlichen Fragezeichen.

## Tech-Stack

- Python 3.12+, Home Assistant Custom Component Architektur
- `DataUpdateCoordinator` für zentrales Polling (ein Coordinator pro
  Coolify-Instanz, versorgt alle Entities)
- `config_flow.py` mit mehrstufigem Flow: 1) Verbindungsdaten, 2)
  Auto-Discovery-Ergebnis anzeigen, 3) Auswahl der zu überwachenden
  Ressourcen
- `voluptuous` für Schema-Validierung
- HTTP-Client: `aiohttp` (in HA core bereits vorhanden, kein zusätzliches
  Requirement)

## Domain

`coolify`

## Authentifizierung

- Bearer-Token-Auth (Laravel Sanctum), kein OAuth
- Nutzer erstellt Token selbst in Coolify UI unter "Keys & Tokens" →
  "API tokens"
- Token wird im Config Flow als Passwort-Feld abgefragt (`vol.Required
mit selector.TextSelector(TextSelectorConfig(type="password"))`)
- Empfehlung in der Doku: Token mit "Read Only"-Ability erstellen, da die
  Integration nur liest (kein Deploy/Restart in v1)
- Rate Limit beachten: Coolify limitiert standardmäßig auf 200
  Requests/Minute – bei Polling weit darunter bleiben (siehe
  Update-Intervall unten)
- Token wird via `entry.data` gespeichert; für zukünftige HA-Versionen
  ggf. `entry.options` für nicht-sensible Auswahl-Daten nutzen

## Ordnerstruktur

```sh
custom_components/coolify/
├── __init__.py           # Setup/Unload, Coordinator-Instanziierung
├── manifest.json         # Metadata, iot_class: local_polling
├── const.py              # DOMAIN, CONF_-Konstanten, Defaults
├── config_flow.py         # Mehrstufiger Flow: Connect → Discover → Select
├── coordinator.py          # DataUpdateCoordinator, ruft api.py auf
├── api.py                 # Dünner Client-Wrapper um die Coolify-REST-API
├── binary_sensor.py        # Running/Stopped-Status pro Ressource
├── sensor.py               # Metriken (CPU/RAM, letzter Deploy, etc.)
├── entity.py               # Gemeinsame CoolifyEntity-Basisklasse
├── strings.json            # UI-Texte
└── translations/de.json    # Deutsche Übersetzung
```

## Schritt-für-Schritt-Plan

### 1. API-Layer (`api.py`)

- Dünner async Client um die relevanten Endpoints:
  - `GET /api/v1/version` — für Verbindungstest im Config Flow
  - `GET /api/v1/servers` — Serverliste inkl. Status
  - `GET /api/v1/applications` — Applications inkl. Status, letzter Deploy
  - `GET /api/v1/databases` — Datenbank-Ressourcen
  - `GET /api/v1/services` — Services (z.B. Immich, Home Assistant selbst)
- Eigene Exception-Hierarchie: `CoolifyConnectionError` (Netzwerk/Timeout),
  `CoolifyAuthError` (401/403 → falscher/abgelaufener Token)
- Alle Responses in `dataclasses` oder `TypedDict` typisieren, damit
  Discovery und Sensoren dieselbe Struktur nutzen
- Timeout großzügig genug für VPS-Instanzen mit vielen Ressourcen (z.B. 15s)

### 2. Config Flow – Schritt 1: Verbindung (`config_flow.py`)

- Formular: `url` (Instanz-URL, z.B. `https://coolify.example.com`),
  `api_token` (Passwort-Feld)
- `async def validate_input`: Testaufruf gegen `/api/v1/version`, um Host
  - Token gemeinsam zu prüfen, bevor der Entry angelegt wird
- Fehlerbehandlung: `cannot_connect` (URL falsch/nicht erreichbar) vs.
  `invalid_auth` (Token falsch) als getrennte Fehlermeldungen im Formular

### 3. Config Flow – Schritt 2: Auto-Discovery

- Nach erfolgreicher Verbindung: alle vier Endpoints (`servers`,
  `applications`, `databases`, `services`) parallel abfragen
  (`asyncio.gather`)
- Ergebnis dem Nutzer nicht nur "durchwinken", sondern in einem
  Zwischenschritt zusammenfassen (z.B. "Gefunden: 1 Server, 4
  Applications, 2 Databases, 1 Service") — schafft Vertrauen, dass
  Discovery funktioniert hat

### 4. Config Flow – Schritt 3: Auswahl der Ressourcen

- Multi-Select-Formular (`selector.SelectSelector` mit `multiple: true`),
  gruppiert nach Kategorie (Server / Applications / Databases / Services),
  vorbelegt mit "alles ausgewählt" als sinnvollem Default
- Ausgewählte UUIDs werden in `entry.data["selected_resources"]`
  gespeichert
- **Options Flow** repliziert exakt diesen Auswahlschritt, inkl. erneuter
  Discovery (falls seit der Ersteinrichtung neue Apps hinzugekommen sind)
  — so kann der Nutzer jederzeit nachjustieren, ohne die Integration neu
  einzurichten

### 5. Coordinator (`coordinator.py`)

- Ein Coordinator pro Config Entry, `update_interval` konfigurierbar
  (Default z.B. 60s – Coolify-Metriken ändern sich schneller als
  Heizölpreise, aber 200 req/min Limit im Hinterkopf behalten, siehe
  Rate-Limit-Hinweis oben)
- `_async_update_data()`: ruft nur die vom Nutzer ausgewählten Ressourcen
  ab (kein unnötiger Traffic für abgewählte Items), aggregiert in einem
  Dict pro Ressourcen-UUID
- `UpdateFailed` bei Verbindungsfehlern; bei `CoolifyAuthError` gezielt
  eine Reauth-Flow triggern (`async_start_reauth`), falls der Token
  abgelaufen/widerrufen wurde

### 6. Entities

- **`entity.py`**: `CoolifyEntity(CoordinatorEntity)` als Basisklasse,
  liest die eigene Ressource per UUID aus `coordinator.data`, setzt
  `device_info` (ein HA-"Device" pro Coolify-Ressource, damit Sensoren
  sauber gruppiert erscheinen, z.B. "App: recipe-app")
- **`binary_sensor.py`**: Running/Stopped/Degraded-Status je Server,
  Application, Database, Service
- **`sensor.py`**:
  - Applications: Status-Text, letzter Deployment-Zeitpunkt,
    Deployment-Ergebnis (success/failed)
  - Server: CPU/RAM-Auslastung (falls API das liefert), Anzahl laufender
    Container
  - Databases/Services: Status, ggf. Version
- Entities werden dynamisch nur für ausgewählte Ressourcen erstellt
  (`async_setup_entry` iteriert über `entry.data["selected_resources"]`)

### 7. Dashboard-Aspekt ("auf dem Dashboard darstellen")

- Für v1: keine eigene Lovelace-Card programmieren, sondern die
  Device-Gruppierung (Schritt 6) so sauber gestalten, dass HA's
  Auto-Dashboard direkt brauchbare Karten pro Ressource erzeugt
- Optional für später: ein eigenes Lovelace-Strategy-Element oder eine
  Doku mit Beispiel-Dashboard-YAML (kein Muss für die erste Version)

### 8. Testing

- Gegen deine reale Coolify-Instanz testen: Config Flow durchlaufen,
  prüfen ob Discovery alle aktuellen Apps/Services findet
  (Rezept-App, ehemalige Heizöl-App-Reste, etc.)
- Fehlerfälle: falscher Token, Instanz offline, Token nachträglich in
  Coolify widerrufen (Reauth-Flow sollte greifen)
- Prüfen, ob neu hinzugefügte Coolify-Apps über die Options-Flow-Discovery
  nachträglich auswählbar werden

### 9. Optional (später, nicht für v1 nötig)

- Action-Entities zum Neustarten/Redeployen einer Application direkt aus
  HA (`write`/`deploy`-Ability des Tokens erfordert dann höhere Rechte —
  bewusste Entscheidung, ob das gewünscht ist, da mehr Risiko als
  Read-Only)
- Diagnostics-Support für Debug-Export (Token maskiert)
- HACS-Veröffentlichung, sobald v1 stabil läuft — hier gibt es anders als
  beim Heizöl-Projekt keine rechtlichen Hürden, nur Code-Qualität/Docs

## Offene Punkte, die du vor dem Start klären solltest

- Welche Felder liefert `/api/v1/servers` tatsächlich für
  CPU/RAM-Auslastung? (In der API-Referenz gegenprüfen, ob das
  überhaupt vorhanden ist oder ob dafür der separate "Sentinel"-Agent
  nötig ist, den Coolify für Server-Metriken nutzt)
- Token-Berechtigungsstufen in deiner Coolify-Version testen (ältere
  Versionen hatten laut Community-Diskussion nur "Read Only" vs. "\*" ohne
  granularere Abstufung – relevant für die Doku-Empfehlung an Nutzer)
