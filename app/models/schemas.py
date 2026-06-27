from pydantic import BaseModel
from typing import Optional


class XonaOlchami(BaseModel):
    uzunlik: float        # metr
    kenglik: float        # metr
    balandlik: float      # metr
    eshiklar: int = 1     # soni
    derazalar: int = 1    # soni


class KafelSo(BaseModel):
    xona: XonaOlchami
    kafel_uzunlik: float = 0.3   # metr (masalan 30x30)
    kafel_kenglik: float = 0.3
    devor_uchun: bool = True      # False bo'lsa pol uchun
    zaxira_foiz: float = 10.0


class OboyHisob(BaseModel):
    xona: XonaOlchami
    rulon_eni: float = 0.53       # standart oboy eni (metr)
    rulon_uzunlik: float = 10.5   # standart rulon uzunligi (metr)


class GipsokartonHisob(BaseModel):
    xona: XonaOlchami
    list_uzunlik: float = 2.5    # metr
    list_kenglik: float = 1.2    # metr


class PolQoplama(BaseModel):
    xona: XonaOlchami
    taxta_uzunlik: float = 1.2   # metr
    taxta_kenglik: float = 0.19  # metr
    zaxira_foiz: float = 10.0


class SuyuqMaterial(BaseModel):
    xona: XonaOlchami
    material_turi: str = "kraska"  # kraska, shpaklyovka, grunt, sement
    qatlam_soni: int = 2
