
from app.main import app
from app.admin_manage import router as admin_manage_router

app.include_router(admin_manage_router)
