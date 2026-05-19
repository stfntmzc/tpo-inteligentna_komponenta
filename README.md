# TPO inteligentna komponenta (ai sistem za avtomatsko moderacijo slik)
Del projekta pri predmetu TPO. Sistem za prepoznavanje neprimerne vsebine na slikah za objave za platformo Soseska+

## Kaj trenutno vrača

Trenutno vrača json dgvor v obliki:
```json
{
  "job_id": "f91a0fb7-2f40-432c-8ade-00593c060e21",
  "filename": "image10.png",
  "result": {
    "decision": "neustrezno",
    "reasons": [
      {
        "label": "a photo of illegal drugs",
        "score": 0.984631359577179
      }
    ]
  }
}
```
"decision" je lahko "neustrezno", "neprepoznano", "ustrezno".

## Za nadaljni development in lokalni deployment
(disclamer: nekatere komande tukej so mogoče drugačne na windows)
Najprej kloniraj repozitorij in se premakni v mapo projekta.
V root direktoriju naredi .env datoteko z API ključem, naprimer:
```text
API_KEY=primerapikljuca123
```
Nato utvari virtualno okolje:
```bash
python3 -m venv .venv
```
Aktiviraj virtualno okolje:
```bash
source .venv/bin/activate
```
Namesti potrebne knjižnice:
```bash
pip install -r requirements.txt
```
Zaženi aplikacijo lokalno:
```bash
uvicorn server.main:app --reload --host 127.0.0.1 --port 12000
```
Po zagonu je API dosegljiv na:
```text
http://127.0.0.1:12000
```
Swagger dokumentacija je dosegljiva na:
```text
http://127.0.0.1:12000/docs
```
Health check:
```text
curl http://127.0.0.1:12000/api/
```
Test moderacije slike:
```text
curl -X POST "http://127.0.0.1:12000/api/moderate" \
  -H "X-API-Key: primerapiklica123" \
  -F "file=@test/quick_test/images/image01.jpg"
```

## Deployment inteligentne komponente

### Build Docker image
Iz root direktorija repozitorija poženi:

```bash
docker build -t inteligentna-komponenta:latest .
```

### Zaženi Docker container
```bash
docker run -d \
  --name inteligentna-komponenta \
  --restart unless-stopped \
  -p 13000:12000 \
  --env-file .env \
  inteligentna-komponenta:latest
```
Po tem je inteligentna komponenta dosegljiva na localhost:13000. Endpoint za moderacoijo je /api/moderate. "Dokumantacija" je na /docs.

## Testiranje in konfiguracije

Beri README.md v mapi test/.

## Kratka razlaga datotek

```text
.
├── .env - enviorment file z api ključem
├── Dockerfile - izdelava Docker image-a in zagon aplikacije v kontejnerju
├── inteligent_component
│   ├── config
│   │   ├── labels.txt - produkcijski seznam vseh labelov, s katerimi CLIP primerja sliko
│   │   ├── risk_labels.txt - produkcijski seznam labelov, ki predstavljajo prepovedano ali sumljivo vsebino
│   │   └── threshold.txt - produkcijski pragovi za odločanje: neprepoznano in neustrezno
│   ├── config.py - branje konfiguracije iz datotek labels.txt, risk_labels.txt in threshold.txt
│   ├── image_classifier.py - izvaja klasifikacijo slike z AI modelom in vrne odločitev ter razloge
│   ├── __init__.py - označi mapo inteligent_component kot Python paket
│   ├── models.py - inicializacija CLIP modela, preprocesorja in naprave CPU/GPU
│   └── moderation.py - glavna AI pipeline funkcija, ki poveže konfiguracijo, klasifikacijo in odločitev
├── README.md - glavna dokumentacija projekta, zagon, testiranje in deployment navodila
├── requirements.txt - seznam Python knjižnic, potrebnih za zagon aplikacije
├── server
│   ├── api
│   │   ├── __init__.py - označi api mapo kot Python paket
│   │   └── routes.py - definira FastAPI endpoint-e in sprejema requeste za moderacijo slik
│   ├── __init__.py - označi server mapo kot Python paket
│   ├── main.py - inicializacija FastAPI strežnika in zagon background workerja
│   └── queue
│       ├── moderation_queue.py - definira FIFO čakalno vrsto in strukturo moderacijskega joba
│       └── worker.py - jemlje slike iz čakalne vrste, jih pošlje v AI pipeline in vrne rezultat
└── test
    ├── configs
    │   ├── conf1
    │   │   ├── labels.txt - testni seznam vseh labelov za konfiguracijo conf1
    │   │   ├── risk_labels.txt - testni seznam risk labelov za konfiguracijo conf1
    │   │   └── threshold.txt - testni pragovi za konfiguracijo conf1
    │   ├── conf2
    │   │   ├── labels.txt
    │   │   ├── risk_labels.txt
    │   │   └── threshold.txt
    │   └── ... - ostale testne konfiguracije
    ├── configurations_evaluation_result.txt - rezultat primerjave več konfiguracij; ena accuracy vrednost na vrstico
    ├── configurations_to_evaluate.txt - seznam konfiguracij, ki jih evaluate_configurations.py požene eno za drugo
    ├── datasets
    │   ├── appropriate1
    │   │   ├── expected.txt - pravilni pričakovani odgovori za ta dataset, npr. ustrezno
    │   │   ├── images - slike za testiranje primernih objav
    │   │   └── result_confX.txt - rezultati testiranja posameznih konfiguracij na tem datasetu
    │   ├── appropriate2
    │   │   ├── expected.txt
    │   │   ├── images
    │   │   └── result_confX.txt
    │   ├── inappropriate1
    │   │   ├── expected.txt - pravilni pričakovani odgovori za ta dataset, npr. neustrezno in neprepoznano
    │   │   ├── images - slike za testiranje neprimernih objav
    │   │   └── result_confX.txt - rezultati testiranja posameznih konfiguracij na tem datasetu
    │   └── inappropriate2
    │       ├── expected.txt
    │       ├── images
    │       └── result_confX.txt
    ├── evaluate_config.py - testira eno konfiguracijo nad enim datasetom in zapiše podroben rezultat
    ├── evaluate_configurations.py - prebere configurations_to_evaluate.txt in požene evaluate_config.py za več konfiguracij
    ├── quick_test
    │   ├── images - slike za hitro testiranje API endpointa
    │   ├── test_images.ps1 - PowerShell skripta za testiranje API endpointa na Windows
    │   └── test_images.sh - Bash skripta za testiranje API endpointa na Linuxu
    └── README.md - dokumentacija za testiranje konfiguracij, datasetov in quick test skript
```
