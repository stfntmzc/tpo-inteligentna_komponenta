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

Primer labels.txt:
```text
a photo of a harmless object
a photo of a household item
a photo of a weapon
a photo of illegal drugs
a photo of alcohol
a photo of a person
a photo of a child
```

Primer risk_labels.txt:
```text
a photo of a weapon
a photo of illegal drugs
a photo of alcohol
a photo of a person
a photo of a child
```

Primer threshold.txt:
```text
0.2
0.7
```

### datasets/

Mapa datasets/ vsebuje testne datasete slik. Vsak dataset ima:

expected.txt
images/

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