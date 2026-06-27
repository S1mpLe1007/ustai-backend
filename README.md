# 🏗️ Remont Kalkulyator API

## O'rnatish

```bash
pip install -r requirements.txt
```

## Ishga tushirish

```bash
uvicorn app.main:app --reload
```

## API hujjatlari

Brauzerda oching: http://localhost:8000/docs

## Endpointlar

| Method | URL | Tavsif |
|--------|-----|--------|
| POST | /hisob/kafel | Kafel hisoblash |
| POST | /hisob/oboy | Oboy hisoblash |
| POST | /hisob/gipsokarton | Gipsokarton hisoblash |
| POST | /hisob/pol-qoplama | Pol qoplama hisoblash |
| POST | /hisob/suyuq-material | Kraska/shpaklyovka hisoblash |
| POST | /smeta/yaratish | PDF smeta yuklash |

## Misol so'rov (kafel)

```json
{
  "xona": {
    "uzunlik": 5,
    "kenglik": 4,
    "balandlik": 2.7,
    "eshiklar": 1,
    "derazalar": 2
  },
  "kafel_uzunlik": 0.3,
  "kafel_kenglik": 0.3,
  "devor_uchun": true,
  "zaxira_foiz": 10
}
```
