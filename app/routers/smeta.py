from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from app.models.schemas import XonaOlchami
from app.services.calculator import (
    kafel_hisob, oboy_hisob, gipsokarton_hisob,
    pol_qoplama_hisob, suyuq_material_hisob,
    KafelSo, OboyHisob, GipsokartonHisob, PolQoplama, SuyuqMaterial
)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io

router = APIRouter()


class SmetaRequest(BaseModel):
    xona: XonaOlchami
    kafel: bool = True
    oboy: bool = True
    gipsokarton: bool = True
    pol_qoplama: bool = True
    kraska: bool = True
    mijoz_ismi: Optional[str] = "Mijoz"


@router.post("/yaratish")
def smeta_yaratish(data: SmetaRequest):
    natijalar = {}

    if data.kafel:
        natijalar["Kafel (devor)"] = kafel_hisob(KafelSo(xona=data.xona))
    if data.oboy:
        natijalar["Oboy"] = oboy_hisob(OboyHisob(xona=data.xona))
    if data.gipsokarton:
        natijalar["Gipsokarton"] = gipsokarton_hisob(GipsokartonHisob(xona=data.xona))
    if data.pol_qoplama:
        natijalar["Pol qoplama"] = pol_qoplama_hisob(PolQoplama(xona=data.xona))
    if data.kraska:
        natijalar["Kraska"] = suyuq_material_hisob(
            SuyuqMaterial(xona=data.xona, material_turi="kraska")
        )

    # PDF yaratish
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Sarlavha
    elements.append(Paragraph(f"REMONT SMETA", styles['Title']))
    elements.append(Paragraph(f"Mijoz: {data.mijoz_ismi}", styles['Normal']))
    elements.append(Paragraph(
        f"Xona: {data.xona.uzunlik}m x {data.xona.kenglik}m x {data.xona.balandlik}m",
        styles['Normal']
    ))
    elements.append(Spacer(1, 12))

    # Har bir material uchun jadval
    for material_nomi, natija in natijalar.items():
        elements.append(Paragraph(f"► {material_nomi}", styles['Heading2']))

        jadval_data = [["Parametr", "Qiymat"]]
        for kalit, qiymat in natija.items():
            jadval_data.append([str(kalit), str(qiymat)])

        jadval = Table(jadval_data, colWidths=[250, 200])
        jadval.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#EFF6FF')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(jadval)
        elements.append(Spacer(1, 16))

    doc.build(elements)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=smeta_{data.mijoz_ismi}.pdf"}
    )
