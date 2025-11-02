from fastapi import APIRouter, Depends, Path, Query, HTTPException
from typing import List, Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from api.get_or_404 import _get_or_404
from api.services.check_api_key_service import check_api_key
from api.services.organization_service import OrganizationService
from core.config import settings
from core.models import db_helper
from core.schemas.organization import OrganizationSchema


router = APIRouter(
    prefix=settings.api.organizations,
    tags=["organizations"],
    dependencies=[Depends(check_api_key)],
)

@router.get(
    "/building/{building_id}/",
    response_model=List[OrganizationSchema],
    summary="Организации в здании",
)
async def get_organizations_by_building(
    building_id: Annotated[int, Path(description="ID здания")],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    organization_service: Annotated[OrganizationService, Depends()],
) -> List[OrganizationSchema]:
    """
    Возвращает список всех организаций, находящихся в указанном здании.
    """
    result = await organization_service.get_organizations_by_building(
        session=session, building_id=building_id
    )
    await _get_or_404(result, "Organizations not found")
    return result


@router.get(
    "/activity/{activity_id}/",
    response_model=List[OrganizationSchema],
    summary="Организации по деятельности",
)
async def get_organizations_by_activity(
    activity_id: Annotated[int, Path(description="ID вида деятельности")],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    organization_service: Annotated[OrganizationService, Depends()],
) -> List[OrganizationSchema]:
    """
    Возвращает список организаций, связанных с указанным видом деятельности.
    """
    result = await organization_service.get_organizations_by_activity(
        session=session, activity_id=activity_id
    )
    await _get_or_404(result, "Organizations not found")
    return result


@router.get(
    "/tree/activity/",
    response_model=List[OrganizationSchema],
    summary="Список организаций по указанному виду деятельности и всех его дочерних классов.",
)
async def get_organizations_by_activity_tree(
    activity_id: Annotated[int, Query(description="ID корневой деятельности")],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    organization_service: Annotated[OrganizationService, Depends()],
) -> List[OrganizationSchema]:
    """
    Возвращает все организации, связанные с указанной деятельностью и всеми её дочерними деятельностями.
    """
    result = await organization_service.get_organizations_by_activity_tree(
        session=session, activity_id=activity_id
    )
    await _get_or_404(result, "Organizations not found")
    return result


@router.get(
    "/nearby/",
    response_model=List[OrganizationSchema],
    summary="Организации рядом",
)
async def get_organizations_nearby(
    latitude: Annotated[float, Query(ge=1, le=90, description="Широта центра поиска (1-90)")],
    longitude: Annotated[float, Query(ge=1, le=180, description="Долгота центра поиска (1-180)")],
    radius: Annotated[
        float, Query(ge=1, le=50000, description="Радиус (1–50000)")
    ],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    organization_service: Annotated[OrganizationService, Depends()],
) -> List[OrganizationSchema]:
    """
    Возвращает организации в указанном радиусе.
    """
    result = await organization_service.get_organizations_nearby(
        session=session,
        latitude=latitude,
        longitude=longitude,
        radius=radius,
    )
    await _get_or_404(result, "Organizations not found")
    return result


@router.get(
    "/search/",
    response_model=OrganizationSchema,
    summary="Организация по названию или ID",
)
async def get_organization_by_id_or_name(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    organization_service: Annotated[OrganizationService, Depends()],
    organization_name: Annotated[str, Query(description="Название организации")] = None,
    organization_id: Annotated[int, Query(description="ID организации")] = None,
) -> OrganizationSchema:
    """
    Возвращает информацию об организации по её названию или ID.
    """
    if not organization_name and not organization_id:
        raise HTTPException(status_code=400, detail="Необходимо указать название или ID.")
    elif organization_name and organization_id:
        raise HTTPException(status_code=400, detail="Необходимо указать либо название, либо ID.")
    result = await organization_service.get_organization_by_id_or_name(
        session=session, organization_id=organization_id, organization_name=organization_name,
    )
    await _get_or_404(result, "Organization not found")
    return result
