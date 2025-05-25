# HomeDefender

HomeDefender je odprtokodni sistem za domačo varnost, zgrajen na osnovi `Home Assistant <https://www.home-assistant.io/>`\_ kot integracija. Omogoča inteligentno zaznavanje vlomilcev in obveščanje z AI-podprto video analizo ter tesno integracijo z avtomatizacijskim sistemom Home Assistant.

S HomeDefenderjem lahko nadzorujete svoj dom preko IP-kamer, zaznavate sumljive dejavnosti (kot so vlomilci ali nevarni predmeti) in prejemate opozorila ali sprožite alarme preko Home Assistanta. Oddaljen dostop je podprt preko Home Assistant Cloud (Nabu Casa), kar omogoča preverjanje stanja vašega doma od kjerkoli.

## Značilnosti

* **AI-podprto zaznavanje vlomilcev**
  Uporablja Ultralytics YOLOv8 model za zaznavanje ljudi in hišnih ljubljenčkov.

* **Zaznavanje nevarnih zvokov (lom stekla)**
  Uporablja analizo zvoka za prepoznavanje nevarnih dogodkov, kot je lom stekla.

* **Integracija s Home Assistant**
  Implementirano kot integracija Home Assistanta; dogodki zaznavanja so vidni neposredno v uporabniškem vmesniku.

* **Oddaljen nadzor**
  Dostop možen od kjerkoli prek Home Assistant Cloud (Nabu Casa).

* **E-poštna in push-opozorila**
  Pošiljanje e-poštnih sporočil in potisnih obvestil prek mobilne aplikacije Home Assistant.

## Navodila za postavitev razvojnega okolja

Predpogoji
^^^^^^^^^^

* Namestite `Docker Desktop <https://www.docker.com/products/docker-desktop>`\_ (ali katerikoli Docker Engine) in ga pustite zagnanega.

Nastavitev razvojnega okolja preko Home Assistanta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

\#. Obiščite uradno stran za nastavitev: `Razvojno okolje Home Assistant <https://developers.home-assistant.io/docs/development_environment/>`\_.
\#. V polje za vnos repozitorija prilepite:

`https://github.com/TPO-2024-2025/HomeDefender`

\#. Kliknite **Open in Dev Container** in dovolite brskalniku, da zažene Visual Studio Code.
\#. Če vas sistem pozove, namestite razširitev **Remote - Containers**.
\#. Počakajte, da se kontejner zgradi (lahko traja nekaj minut).

Popravek datoteke modela YOLOv8
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Izvorno naložena datoteka `yolov8n.pt` morda ni veljavna zaradi stiskanja na GitHubu. Za zamenjavo izvedite:

.. code-block:: bash

cd custom\_components/tpo\_home\_sec
rm yolov8n.pt  # če obstaja
wget [https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8n.pt](https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8n.pt) -O yolov8n.pt

Zagon Home Assistanta
^^^^^^^^^^^^^^^^^^^^^

1. V Visual Studio Code odprite ukazno vrstico (`Ctrl+Shift+P` ali `Cmd+Shift+P`).
2. Izberite `Tasks: Run Task` → `Run HomeAssistant Core`.

Home Assistant bo nato dostopen na `http://localhost:8123`\_.

## Nastavitev kamere

Privzeto ni povezane nobene kamere, zato bo ustrezna kartica v nadzorni plošči prazna.

\#. Odprite integracijo **Generic Camera** v nadzorni plošči.
\#. Kliknite na **Settings**, vnesite URL vaše IP-kamere in shranite.

.. tip:: Za testiranje lahko uporabite aplikacijo **DroidCam** za Android, ki simulira IP-kamero v lokalnem omrežju.

## Oddaljen dostop do sistema

Za dostop od kjerkoli uporabite Home Assistant Cloud (Nabu Casa):

`https://10q88uinbelha2kghc5bd5dvqybqo6ec.ui.nabu.casa/`\_

## Licenciranje

* **Home Assistant Core**
  Licencirano pod Apache License 2.0: `LICENSE <https://github.com/home-assistant/core/blob/dev/LICENSE.md>`\_

* **Ultralytics YOLOv8**
  Licencirano pod GNU AGPL-3.0: `LICENSE <https://github.com/ultralytics/ultralytics/blob/main/LICENSE>`\_

Vsako prispevanje mora biti v skladu z zgoraj navedenimi licencami.

.. note::
HomeDefender je študentski projekt, razvit v okviru TPO 2024/2025 za izobraževalne namene. Pokaže, kako lahko AI-vizija izboljša domačo varnost s pomočjo Home Assistanta.
