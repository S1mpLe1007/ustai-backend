from fastapi import APIRouter
from app.models.schemas import (
    KafelSo, OboyHisob, GipsokartonHisob, PolQoplama, SuyuqMaterial
)
from app.services.calculator import (
    kafel_hisob, oboy_hisob, gipsokarton_hisob,
    pol_qoplama_hisob, suyuq_material_hisob
)
from app.services.narxlar import (
    kafel_narx, oboy_narx, gipsokarton_narx,
    laminat_narx, suyuq_narx
)

router = APIRouter()


@router.post("/kafel")
def kafel(data: KafelSo):
    natija = kafel_hisob(data)
    narx = kafel_narx(natija["kerakli_dona"])
    return {**natija, **narx}


@router.post("/oboy")
def oboy(data: OboyHisob):
    natija = oboy_hisob(data)
    narx = oboy_narx(natija["kerakli_rulon"])
    return {**natija, **narx}


@router.post("/gipsokarton")
def gipsokarton(data: GipsokartonHisob):
    natija = gipsokarton_hisob(data)
    narx = gipsokarton_narx(
        natija["kerakli_list"],
        natija["ud_profil_dona"],
        natija["cd_profil_dona"],
        natija["samorez_soni"]
    )
    return {**natija, **narx}


@router.post("/pol-qoplama")
def pol_qoplama(data: PolQoplama):
    natija = pol_qoplama_hisob(data)
    narx = laminat_narx(natija["kerakli_taxta"], natija["podlozka_m2"])
    return {**natija, **narx}


@router.post("/suyuq-material")
def suyuq_material(data: SuyuqMaterial):
    natija = suyuq_material_hisob(data)
    narx = suyuq_narx(natija.get("kerakli_idish", 1), data.material_turi)
    return {**natija, **narx}
