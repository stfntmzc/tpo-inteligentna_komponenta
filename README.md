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
  -F "file=@test/images/image01.jpg"
```
Če želiš testirati več slik iz mape test/images, lahko uporabiš testno skripto:
```bash
chmod +x test/test_images.sh
./test/test_images.sh
```
Testna skripta lahko prejme argument o url-ju, če testeramo ai komponento, ki ne teče lokalno.
Drugi argumnet je lahko mapa, ker se nahajajo slike, če nočeš testerat default mape.

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
  inteligentna-komponenta:latest
```
Po tem je inteligentna komponenta dosegljiva na localhost:13000. Endpoint za moderacoijo je /api/moderate. "Dokumantacija" je na /docs.

## Kratka razlaga datotek

```text
.
├── inteligent_component
│   ├── image_classifier.py - izvaja klasifikacijo slike z AI modelom in vrne rezultate
│   ├── __init__.py - označi mapo kot Python paket
│   ├── labels.txt - seznam vseh labelov, s katerimi CLIP primerja sliko
│   ├── models.py - inicializacija AI modela, preprocesorja / gpu-ja, naprave in labelov
│   ├── moderation.py - glavna AI pipeline funkcija, ki poveže klasifikacijo in odločitev
│   └── risk_labels.txt - seznam labelov, ki predstavljajo prepovedano ali sumljivo vsebino
├── server
│   ├── api
│   │   ├── __init__.py - označi api mapo kot Python paket
│   │   └── routes.py - definira API endpoint-e in usmerja requeste
│   ├── __init__.py - označi server mapo kot Python paket
│   ├── main.py - inicializacija FastAPI strežnika in zagon workerja
│   └── queue
│       ├── moderation_queue.py - definira FIFO čakalno vrsto in strukturo moderacijskega joba
│       └── worker.py - jemlje slike iz čakalne vrste in jih pošilja v AI pipeline
├── README.md - dokumentacija projekta, zagon, testiranje in deployment navodila
├── requirements.txt - seznam Python knjižnic, potrebnih za zagon aplikacije
├── Dockerfile - izdelava Docker image-a in zagon aplikacije v kontejnerju
└── test
    ├── images - mapa slik za testeranje
    │   ├── image01.jpg
    │   ├── image02.jpg
    │   ├── image03.png
    │   ├── image04.jpg
    │   ├── image05.png
    │   ├── image06.jpg
    │   ├── image07.jpg
    │   ├── image08.jpg
    │   ├── image09.png
    │   ├── image10.png
    │   └── image11.jpg
    ├── test_images.ps1 - powershel skripta za testeranje slik
    └── test_images.sh - bash skripta za testeranje slik
```
