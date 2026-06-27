import math
from app.models.schemas import (
    XonaOlchami, KafelSo, OboyHisob,
    GipsokartonHisob, PolQoplama, SuyuqMaterial
)

# Standart eshik va deraza o'lchamlari
ESHIK_YUZA = 2.0 * 0.9   # 2m x 0.9m = 1.8 m²
DERAZA_YUZA = 1.4 * 1.2  # 1.4m x 1.2m = 1.68 m²


def devor_yuzasi(xona: XonaOlchami) -> float:
    """Eshik va derazalar ayirib tashlangan devor yuzasi"""
    umumiy = 2 * (xona.uzunlik + xona.kenglik) * xona.balandlik
    ayirish = (xona.eshiklar * ESHIK_YUZA) + (xona.derazalar * DERAZA_YUZA)
    return round(max(umumiy - ayirish, 0), 2)


def pol_yuzasi(xona: XonaOlchami) -> float:
    return round(xona.uzunlik * xona.kenglik, 2)


def shift_yuzasi(xona: XonaOlchami) -> float:
    return round(xona.uzunlik * xona.kenglik, 2)


def kafel_hisob(data: KafelSo) -> dict:
    if data.devor_uchun:
        yuza = devor_yuzasi(data.xona)
        joy = "Devor"
    else:
        yuza = pol_yuzasi(data.xona)
        joy = "Pol"

    kafel_yuza = data.kafel_uzunlik * data.kafel_kenglik
    zaxira = 1 + data.zaxira_foiz / 100
    kerakli_dona = math.ceil((yuza / kafel_yuza) * zaxira)
    qutidagi_dona = math.floor(1 / kafel_yuza)  # taxminan 1m² uchun
    quti_soni = math.ceil(kerakli_dona / max(qutidagi_dona, 1))

    return {
        "joy": joy,
        "yuza_m2": yuza,
        "kafel_olchami": f"{int(data.kafel_uzunlik*100)}x{int(data.kafel_kenglik*100)} sm",
        "kerakli_dona": kerakli_dona,
        "taxminiy_quti": quti_soni,
        "zaxira_foiz": data.zaxira_foiz,
    }


def oboy_hisob(data: OboyHisob) -> dict:
    yuza = devor_yuzasi(data.xona)
    rulon_yuza = data.rulon_eni * data.rulon_uzunlik
    rulon_soni = math.ceil(yuza / rulon_yuza)

    return {
        "devor_yuzasi_m2": yuza,
        "rulon_olchami": f"{data.rulon_eni}m x {data.rulon_uzunlik}m",
        "rulon_yuza_m2": round(rulon_yuza, 2),
        "kerakli_rulon": rulon_soni,
    }


def gipsokarton_hisob(data: GipsokartonHisob) -> dict:
    devor = devor_yuzasi(data.xona)
    shift = shift_yuzasi(data.xona)
    umumiy_yuza = devor + shift

    list_yuza = data.list_uzunlik * data.list_kenglik
    list_soni = math.ceil(umumiy_yuza / list_yuza)

    # Profil hisob (taxminan)
    perimetr = 2 * (data.xona.uzunlik + data.xona.kenglik)
    ud_profil = math.ceil(perimetr / 3) * 2  # UD profil uchun
    cd_profil = math.ceil(shift_yuzasi(data.xona) / 0.6) + math.ceil(devor / 0.6)

    # Samorez (har listga ~25 dona)
    samorez_soni = list_soni * 25

    return {
        "umumiy_yuza_m2": round(umumiy_yuza, 2),
        "list_olchami": f"{data.list_uzunlik}m x {data.list_kenglik}m",
        "kerakli_list": list_soni,
        "ud_profil_dona": ud_profil,
        "cd_profil_dona": cd_profil,
        "samorez_soni": samorez_soni,
    }


def pol_qoplama_hisob(data: PolQoplama) -> dict:
    yuza = pol_yuzasi(data.xona)
    zaxira = 1 + data.zaxira_foiz / 100
    taxta_yuza = data.taxta_uzunlik * data.taxta_kenglik
    taxta_soni = math.ceil((yuza / taxta_yuza) * zaxira)
    podlozka_m2 = math.ceil(yuza * zaxira)

    return {
        "pol_yuzasi_m2": yuza,
        "taxta_olchami": f"{data.taxta_uzunlik}m x {data.taxta_kenglik}m",
        "kerakli_taxta": taxta_soni,
        "podlozka_m2": podlozka_m2,
        "zaxira_foiz": data.zaxira_foiz,
    }


# Sarflanish me'yorlari (1 m² uchun, kg yoki litr)
SARFLANISH = {
    "kraska":      {"sarflanish": 0.2,  "birlik": "litr",  "idish_hajmi": 3.0},
    "shpaklyovka": {"sarflanish": 1.2,  "birlik": "kg",    "idish_hajmi": 20.0},
    "grunt":       {"sarflanish": 0.15, "birlik": "litr",  "idish_hajmi": 5.0},
    "sement":      {"sarflanish": 4.5,  "birlik": "kg",    "idish_hajmi": 25.0},
}


def suyuq_material_hisob(data: SuyuqMaterial) -> dict:
    yuza = devor_yuzasi(data.xona)
    turi = data.material_turi.lower()

    if turi not in SARFLANISH:
        return {"xato": f"Noma'lum material: {turi}. Mavjudlar: {list(SARFLANISH.keys())}"}

    m = SARFLANISH[turi]
    umumiy_sarflanish = yuza * m["sarflanish"] * data.qatlam_soni
    idish_soni = math.ceil(umumiy_sarflanish / m["idish_hajmi"])

    return {
        "devor_yuzasi_m2": yuza,
        "material": turi,
        "qatlam_soni": data.qatlam_soni,
        "umumiy_sarflanish": round(umumiy_sarflanish, 2),
        "birlik": m["birlik"],
        "idish_hajmi": f"{m['idish_hajmi']} {m['birlik']}",
        "kerakli_idish": idish_soni,
    }
