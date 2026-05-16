# Testiranje AI konfiguracij

Mapa `test/` vsebuje skripte, konfiguracije in datasete za testiranje natančnosti inteligentne komponente. Namen testiranja je primerjati različne kombinacije labelov, risk labelov in thresholdov ter ugotoviti, katera konfiguracija najbolje loči primerne in neprimerne slike.

## Struktura mape

```text
test/
├── configs/
│   ├── config1/
│   │   ├── labels.txt
│   │   ├── risk_labels.txt
│   │   └── threshold.txt
│   ├── config2/
│   │   ├── labels.txt
│   │   ├── risk_labels.txt
│   │   └── threshold.txt
│   └── ...
├── datasets/
│   ├── appropriate/
│   │   ├── expected.txt
│   │   └── images/
│   │       ├── 1.jpg
│   │       ├── 2.png
│   │       └── ...
│   ├── inappropriate1/
│   │   ├── expected.txt
│   │   └── images/
│   │       ├── 1.jpg
│   │       ├── 2.png
│   │       └── ...
│   └── ...
├── quick_test/
│   ├── images/
│   ├── test_images.sh
│   └── test_images.ps1
├── configurations_to_evaluate.txt
├── configurations_evaluation_result.txt
├── evaluate_config.py
└── evaluate_configurations.py
```

## Namen posameznih map

### configs/

Mapa configs/ vsebuje različne konfiguracije AI komponente. Vsaka konfiguracija ima svoje labele, risk labele in pragove odločanja.

```text
test/
├── configs/
│   ├── config1/
│   │   ├── labels.txt
│   │   ├── risk_labels.txt
│   │   └── threshold.txt
│   ├── config2/
│   │   ├── labels.txt
│   │   ├── risk_labels.txt
│   │   └── threshold.txt
│   └── ...
```

### datasets/

Mapa datasets/ vsebuje testne datasete slik. Vsak dataset ima expected.txt, images/

expected.txt pove, kateri odgovori AI komponente se štejejo kot pravilni za ta dataset.

Primer expected.txt (lahko vsebuje več pričakovanih rezultatov):
```text
ustrezno
neprepoznano
```

images/ vsebuje slike, nad katerimi se izvede testiranje.

### quick_test/

Mapa quick_test/ je namenjena hitremu testiranju API endpointa z curl. Te skripte pošiljajo slike na že zagnan FastAPI strežnik.

To ni enako kot evaluate_config.py.
quick_test testira API, evaluate_config.py pa testira AI pipeline direktno v Pythonu brez HTTP requestov.

## Konfiguracije

Vsaka konfiguracija mora imeti tri datoteke:

- labels.txt
- risk_labels.txt
- threshold.txt

### labels.txt

Vsebuje vse labele, s katerimi CLIP primerja sliko.

Primer:
```text
a photo of a harmless object
a photo of a household item
a photo of a weapon
a photo of illegal drugs
a photo of alcohol
a photo of a person
```

### risk_labels.txt

Vsebuje samo tiste labele, ki predstavljajo sumljivo ali prepovedano vsebino.

Primer:
```text
a photo of a weapon
a photo of illegal drugs
a photo of alcohol
a photo of a person
```

Pomembno: label, ki je v risk_labels.txt, mora obstajati tudi v labels.txt.

### threshold.txt

Vsebuje dva praga:
- Prva vrstica pomeni prag za neprepoznano.
- Druga vrstica pomeni prag za neustrezno.

Primer:
```text
0.3
0.7
```
Pomen:
- score < 0.3 → ustrezno
- 0.3 <= score < 0.7 → neprepoznano
- score >= 0.7 → neustrezno

## Dataseti

Vsak dataset mora imeti takšno strukturo:
```text
test/datasets/ime_dataseta/
├── expected.txt
└── images/
    ├── 1.jpg
    ├── 2.png
    └── ...
```

Slike morajo biti v mapi images/.

Podprte končnice so:

- .jpg
- .jpeg
- .png
- .webp

### expected.txt

Datoteka expected.txt določa, kateri odgovori AI komponente se štejejo kot pravilni.

Dovoljene vrednosti so:

- ustrezno
- neustrezno
- neprepoznano

Možno je zapisati tudi več pravilnih odgovorov, vsakega v svojo vrstico.

Primer za dataset neprimernih slik:
```text
neustrezno
neprepoznano
```

To pomeni, da se šteje kot pravilno, če AI sliko označi kot neustrezno ali neprepoznano.

To je smiselno, ker se v obeh primerih objava ne objavi direktno, ampak gre v administratorski pregled ali pa se zavrne.

Primer za dataset primernih slik:
```text
ustrezno
```
To pomeni, da mora AI sliko označiti kot ustrezno. Če jo označi kot neustrezno ali neprepoznano, se to šteje kot napačen rezultat.

