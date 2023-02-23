from fastapi import APIRouter, Depends

from ..schemas.admin import SuperUserIn, SuperUserOut

from ..services.admin import AdminService


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


@router.post(
    '/superusers/',
    response_model=SuperUserOut
)
async def create_superuser(
    create_superuser: SuperUserIn,
    admin_service: AdminService = Depends()
) -> SuperUserOut:
    return await admin_service.create_superuser(
        create_superuser=create_superuser
    )