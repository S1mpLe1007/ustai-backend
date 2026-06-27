# Toshkent bozori o'rtacha narxlari (so'm)
# Oxirgi yangilanish: 2025

NARXLAR = {
    "kafel": {
        "30x30": 45000,    # so'm/dona (o'rtacha)
        "40x40": 65000,
        "60x60": 120000,
        "default": 45000,
        "birlik": "dona",
        "izoh": "O'rtacha sifat, Toshkent bozori"
    },
    "oboy": {
        "oddiy": 35000,    # so'm/rulon
        "viniliy": 55000,
        "flizelinli": 75000,
        "default": 45000,
        "birlik": "rulon",
        "izoh": "O'rtacha sifat, Toshkent bozori"
    },
    "gipsokarton": {
        "list": 85000,     # so'm/list (2.5x1.2m)
        "ud_profil": 18000,  # so'm/dona (3m)
        "cd_profil": 22000,  # so'm/dona (3m)
        "samorez": 150,      # so'm/dona
        "birlik": "list",
        "izoh": "Knauf yoki o'xshash"
    },
    "laminat": {
        "8mm": 85000,      # so'm/m²
        "10mm": 120000,
        "12mm": 160000,
        "default": 95000,
        "podlozka": 15000,  # so'm/m²
        "birlik": "m²",
        "izoh": "O'rtacha sifat laminat"
    },
    "kraska": {
        "oddiy": 45000,    # so'm/litr
        "premium": 85000,
        "default": 55000,
        "birlik": "litr",
        "idish": 3,        # litr
        "izoh": "Devor bo'yoq, o'rtacha sifat"
    },
    "shpaklyovka": {
        "start": 35000,    # so'm/kg (qopda)
        "finish": 45000,
        "default": 40000,
        "birlik": "kg",
        "idish": 20,       # kg
        "izoh": "Quruq aralashma, 20kg qop"
    },
    "grunt": {
        "default": 38000,  # so'm/litr
        "birlik": "litr",
        "idish": 5,        # litr
        "izoh": "Universal grunt, 5 litr"
    },
    "sement": {
        "M400": 12000,     # so'm/kg (qopda)
        "M500": 14000,
        "default": 12500,
        "birlik": "kg",
        "idish": 25,       # kg
        "izoh": "Portland sement, 25kg qop"
    },
}

# Ishchi kuchi narxlari (so'm/m²)
ISHCHI_NARXLARI = {
    "kafel_yopish": 35000,
    "oboy_yopish": 15000,
    "gipsokarton": 25000,
    "laminat": 20000,
    "bo_yash": 12000,
    "shpaklyovka": 18000,
}


def kafel_narx(dona_soni: int, olcham: str = "30x30") -> dict:
    narx = NARXLAR["kafel"].get(olcham, NARXLAR["kafel"]["default"])
    jami = dona_soni * narx
    return {
        "birlik_narxi": f"{narx:,} so'm/dona",
        "jami_material": f"{jami:,} so'm",
        "izoh": NARXLAR["kafel"]["izoh"]
    }


def oboy_narx(rulon_soni: int, tur: str = "oddiy") -> dict:
    narx = NARXLAR["oboy"].get(tur, NARXLAR["oboy"]["default"])
    jami = rulon_soni * narx
    return {
        "birlik_narxi": f"{narx:,} so'm/rulon",
        "jami_material": f"{jami:,} so'm",
        "izoh": NARXLAR["oboy"]["izoh"]
    }


def gipsokarton_narx(list_soni: int, ud: int, cd: int, samorez: int) -> dict:
    jami = (
        list_soni * NARXLAR["gipsokarton"]["list"] +
        ud * NARXLAR["gipsokarton"]["ud_profil"] +
        cd * NARXLAR["gipsokarton"]["cd_profil"] +
        samorez * NARXLAR["gipsokarton"]["samorez"]
    )
    return {
        "list_narxi": f"{NARXLAR['gipsokarton']['list']:,} so'm/list",
        "ud_profil_narxi": f"{NARXLAR['gipsokarton']['ud_profil']:,} so'm/dona",
        "cd_profil_narxi": f"{NARXLAR['gipsokarton']['cd_profil']:,} so'm/dona",
        "jami_material": f"{jami:,} so'm",
        "izoh": NARXLAR["gipsokarton"]["izoh"]
    }


def laminat_narx(taxta_soni: int, podlozka_m2: float) -> dict:
    taxta_m2 = 1.2 * 0.19  # bir taxtaning yuzasi
    umumiy_m2 = taxta_soni * taxta_m2
    jami = (
        umumiy_m2 * NARXLAR["laminat"]["default"] +
        podlozka_m2 * NARXLAR["laminat"]["podlozka"]
    )
    return {
        "laminat_narxi": f"{NARXLAR['laminat']['default']:,} so'm/m²",
        "podlozka_narxi": f"{NARXLAR['laminat']['podlozka']:,} so'm/m²",
        "jami_material": f"{int(jami):,} so'm",
        "izoh": NARXLAR["laminat"]["izoh"]
    }


def suyuq_narx(idish_soni: int, material_turi: str) -> dict:
    tur = material_turi.lower()
    if tur not in NARXLAR:
        tur = "kraska"
    narx_info = NARXLAR[tur]
    narx = narx_info.get("default", 50000)
    idish = narx_info.get("idish", 1)
    jami = idish_soni * narx * idish
    return {
        "birlik_narxi": f"{narx:,} so'm/{narx_info['birlik']}",
        "jami_material": f"{jami:,} so'm",
        "izoh": narx_info.get("izoh", "")
    }
