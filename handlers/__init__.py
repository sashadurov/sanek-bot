from aiogram import Router
from .start import router as start_router
from .work import router as work_router
from .shop import router as shop_router
from .casino import router as casino_router
from .business import router as business_router
from .transfer import router as transfer_router

def setup_handlers() -> list[Router]:
    return [start_router, work_router, shop_router, casino_router, business_router, transfer_router]
