from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from groq import Groq
import base64

import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
client = Groq(api_key=GROQ_API_KEY)

router = APIRouter()


class DizaynSorov(BaseModel):
    uzunlik: float
    kenglik: float
    balandlik: float
    xona_turi: str = "yotoq xona"
    uslub: str = "zamonaviy"


@router.post("/dizayn-maslahat")
async def dizayn_maslahat(data: DizaynSorov):
    yuza = data.uzunlik * data.kenglik
    hajm = yuza * data.balandlik

    prompt = f"""Sen professional interior dizayner va qurilish mutaxassisisisan.
O'zbek tilida javob ber.

Mijozning xonasi haqida ma'lumot:
- Xona turi: {data.xona_turi}
- O'lchamlari: {data.uzunlik}m x {data.kenglik}m x {data.balandlik}m balandlik
- Umumiy yuza: {yuza:.1f} m²
- Hajm: {hajm:.1f} m³
- Istalgan uslub: {data.uslub}

Quyidagilar haqida aniq va amaliy maslahat ber:

1. **Rang sxemasi** — devor, shift va pol uchun mos ranglar
2. **Pol qoplamasi** — mos material va sababi
3. **Devor bezagi** — oboy, bo'yoq yoki kafel tavsiyasi
4. **Yoritish** — asosiy va qo'shimcha yoritish
5. **Mebel joylashuvi** — xona o'lchamiga mos mebel
6. **Qurilish materiallari** — eng mos materiallar

Javobni qisqa, aniq va amaliy qil. Har bir bo'lim uchun 2-3 ta tavsiya yoz."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
        )
        return {
            "muvaffaqiyat": True,
            "maslahat": response.choices[0].message.content,
        }
    except Exception as e:
        return {"muvaffaqiyat": False, "xato": f"AI xizmatida xatolik: {str(e)}"}


@router.post("/rasm-tahlil")
async def rasm_tahlil(
    rasm: UploadFile = File(...),
    xona_turi: str = Form(default="yotoq xona"),
    uslub: str = Form(default="zamonaviy"),
):
    try:
        rasm_bytes = await rasm.read()
        base64_rasm = base64.b64encode(rasm_bytes).decode("utf-8")
        media_type = rasm.content_type or "image/jpeg"

        prompt = """Sen professional interior dizayner va qurilish mutaxassisisisan.
O'zbek tilida javob ber.

Bu xona rasmini ko'rib quyidagilarni tahlil qil:

1. **Xona o'lchamlari (taxminiy)** — rasmdan ko'rinayotgan xonaning taxminiy uzunlik, kenglik va balandligini metrda ayt
2. **Hozirgi holat** — xonaning hozirgi holati qanday
3. **Rang sxemasi tavsiyasi** — bu xona uchun mos ranglar
4. **Pol qoplamasi tavsiyasi** — mos material
5. **Devor bezagi** — oboy, bo'yoq yoki kafel
6. **Yaxshilash tavsiyalari** — xonani qanday yaxshilash mumkin

Javobni qisqa va amaliy qil."""

        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{media_type};base64,{base64_rasm}"
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            max_tokens=1500,
        )

        return {
            "muvaffaqiyat": True,
            "tahlil": response.choices[0].message.content,
        }

    except Exception as e:
        return {"muvaffaqiyat": False, "xato": f"Rasm tahlilida xatolik: {str(e)}"}
