from fastapi import APIRouter
from app.api.routes import departments, auth, complaints, admin, superadmin

api_router = APIRouter()
api_router.include_router(departments.router, tags=["departments"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(complaints.router, tags=["complaints"])
api_router.include_router(admin.router, tags=["admin"])
api_router.include_router(superadmin.router, tags=["superadmin"])
