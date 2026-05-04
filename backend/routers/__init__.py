from routers.auth_router import router as auth_router
from routers.user_router import router as user_router
from routers.class_router import router as class_router
from routers.attendance_router import router as attendance_router
from routers.message_router import router as message_router
from routers.contact_router import router as contact_router

__all__ = [
    "auth_router",
    "user_router",
    "class_router",
    "attendance_router",
    "message_router",
    "contact_router",
]