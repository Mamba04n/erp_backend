from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.report_service import ReportService
from app.utils.exporter import DataExporter

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    return ReportService(db).get_dashboard_stats()

# --- NUEVOS ENDPOINTS JSON PARA TABLAS ---
@router.get("/recent-orders")
def recent_orders(db: Session = Depends(get_db)):
    return ReportService(db).get_recent_orders()

@router.get("/low-stock")
def low_stock_list(db: Session = Depends(get_db)):
    return ReportService(db).get_low_stock()
# -----------------------------------------

@router.get("/export/pdf")
def export_pdf(db: Session = Depends(get_db)):
    data = ReportService(db).get_low_stock()
    pdf = DataExporter.to_pdf(data, "Reporte de Stock Bajo")
    return StreamingResponse(pdf, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=report.pdf"})