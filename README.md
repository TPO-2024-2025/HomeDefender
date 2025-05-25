# HomeDefender

**HomeDefender** je odprtokodni sistem za domačo varnost, zgrajen na osnovi [Home Assistant](https://www.home-assistant.io/) kot **Integracija**. Omogoča inteligentno zaznavanje vsiljivcev in obveščanje s pomočjo AI-podprte video analize ter tesne integracije z avtomatizacijskim sistemom Home Assistant.

S HomeDefenderjem lahko nadzorujete svoj dom preko IP kamer in senzorjev, zaznavate sumljive dejavnosti (kot so vsiljivci ali živali) in prejemate opozorila ali sprožite alarme preko Home Assistanta. Oddaljen dostop je podprt preko Home Assistant Cloud (Nabu Casa), kar vam omogoča, da preverite stanje vašega doma od kjerkoli.

## 🔐 Značilnosti

* **AI-podprto zaznavanje vsiljivcev**
  Uporablja Ultralytics YOLOv8 nevronsko mrežo za zaznavanje ljudi in ljubljenčkov (ali drugih žival).

* **Zaznavanje nevarnih zvokov (lom stekla)**
  Sistem uporablja analizo zvoka da določi ali je prišlo do nevarnih dogodkov (lom stekla) ali nenevarnih kot so ljubljenčki ali govor ljudi. Vsi podatki so obdelani na lokalnem strežniku, nič se ne pošlje zunaj lokalnega sistema, s čem zagotavljamo integritet osebnih podatkov uporabnika.

* **Integracija v Home Assistant**
  Narejeno kot Integracija v Home Assistant okolju.

* **Oddaljen nadzor**
  Dostopno od kjerkoli preko Home Assistant Cloud (Nabu Casa).

* **E-mail in Push obvestila**
  Sistem lahko pošlje e-mail sporočila ali push obvestila preko HA aplikacije.

---

## 🛠️ Navodila za postavitev razvojnega okolja

### 1. Predpogoji

Namestite [Docker Desktop](https://www.docker.com/products/docker-desktop) (ali katerikoli Docker Engine) in **ga pustite zagnanega**.

### 2. Nastavitev razvojnega okolja preko Home Assistanta

1. Obiščite uradno stran za nastavitev:
   👉 [https://developers.home-assistant.io/docs/development\_environment/](https://developers.home-assistant.io/docs/development_environment/)

2. V polje za vnos prilepite naslednji URL repozitorija:

   ```text
   https://github.com/TPO-2024-2025/HomeDefender
   ```

3. Kliknite **Open** in dovolite brskalniku, da zažene **Visual Studio Code**.

4. Če vas vpraša, odobrite namestitev razširitve **Remote - Containers**.

5. Počakajte, da se kontejner zgradi. To lahko traja nekaj minut.

### 3. Popravek datoteke modela YOLOv8

Prednaložena datoteka `yolov8n.pt` morda ni veljavna zaradi stiskanja z strani GitHub-a. Zamenjajte jo z:

```bash
cd config/custom_components/tpo_home_security
rm yolov8n.pt  # če obstaja
wget https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8n.pt -O yolov8n.pt
```

S tem boste prenesli YOLOv8n model, ki se uporablja za zaznavanje ljudi in živali.

### 4. Zagon Home Assistanta

V Visual Studio Code:

* Odprite ukazno vrstico (`Ctrl+Shift+P` ali `Cmd+Shift+P`)
* Izberite: `Tasks: Run Task` → `Run HomeAssistant Core`

To zažene Home Assistant, ki bo na voljo na:

👉 [http://localhost:8123](http://localhost:8123)

---

## 📷 Nastavitev kamere

Privzeto ni povezana nobena kamera in je ta prostor v Dashboard-u prazen.

1. Odprite kartico **Generic Camera** v nadzorni plošči Home Assistanta.
2. Kliknite nastavitve in vnesite URL toka vaše IP kamere.

💡 Za razvoj:
Uporabite aplikacijo **DroidCam** za Android, da simulirate IP kamero v vašem lokalnem omrežju z uprabo osebnega telefona.

---

## 🌐 Oddaljen dostop do sistema

HomeDefender je dostopen tudi na daljavo preko Nabu Casa:

👉 [https://10q88uinbelha2kghc5bd5dvqybqo6ec.ui.nabu.casa/](https://10q88uinbelha2kghc5bd5dvqybqo6ec.ui.nabu.casa/)

Uporabite to varno povezavo za dostop do nadzorne plošče Home Assistanta od kjerkoli.

---

## 📄 Licenciranje

Ta repozitorij vključuje kodo in modele z naslednjimi licencami:

* **Home Assistant Core**
  Licencirano pod Apache License 2.0
  → [https://github.com/home-assistant/core/blob/dev/LICENSE.md](https://github.com/home-assistant/core/blob/dev/LICENSE.md)

* **Ultralytics YOLOv8**
  Licencirano pod GNU AGPL-3.0
  → [https://github.com/ultralytics/ultralytics/blob/main/LICENSE](https://github.com/ultralytics/ultralytics/blob/main/LICENSE)

Vsako prispevanje k temu projektu mora biti v skladu z zgoraj navedenimi licencami.

---

> HomeDefender je študentski projekt, razvit za izobraževalne namene (TPO 2024/2025). Pokaže, kako lahko AI-vizija izboljša domačo varnost s pomočjo Home Assistanta.
