from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Organization, Activity, Building
from core.schemas.organization import OrganizationSchema


class OrganizationService:
    """
    Сервисный слой для работы с организациями.
    """

    @staticmethod
    async def get_organizations_by_building(
            session: AsyncSession,
            building_id: int
    ) -> list[OrganizationSchema]:
        """
        Возвращает все организации, находящиеся в указанном здании.
        """
        stmt = (
            select(Organization)
            .where(Organization.building_id == building_id)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phone_numbers),
                selectinload(Organization.building)
            )
            .order_by(Organization.id)
        )
        result = await session.scalars(stmt)
        return [OrganizationSchema.model_validate(org) for org in result]

    @staticmethod
    async def get_organizations_by_activity(
            session: AsyncSession,
            activity_id: int
    ) -> list[OrganizationSchema]:
        """
        Возвращает все организации, связанные с указанной деятельностью.
        """
        stmt = (
            select(Activity)
            .where(Activity.id == activity_id)
            .options(
                selectinload(Activity.organizations)
                .selectinload(Organization.phone_numbers),
                selectinload(Activity.organizations)
                .selectinload(Organization.building),
                selectinload(Activity.organizations)
                .selectinload(Organization.activities),
            )
        )
        result = await session.execute(stmt)
        activity = result.scalar_one_or_none()
        if not activity:
            return []
        return [OrganizationSchema.model_validate(org) for org in activity.organizations]

    @staticmethod
    async def get_organizations_nearby(
            session: AsyncSession,
            latitude: float,
            longitude: float,
            radius: float,
    ) -> list[OrganizationSchema]:
        """
        Возвращает организации в радиусе.
        """
        stmt = (
            select(Building)
            .where(
                (func.pow(Building.latitude - latitude, 2) + func.pow(Building.longitude - longitude, 2))
                <= radius ** 2
            )
            .options(
                selectinload(Building.organizations)
                .selectinload(Organization.activities),
                selectinload(Building.organizations)
                .selectinload(Organization.phone_numbers),
            )
        )
        result = await session.scalars(stmt)
        buildings = result.all()

        return [
            OrganizationSchema.model_validate(org)
            for building in buildings
            for org in building.organizations
        ]

    @staticmethod
    async def get_organization_by_id_or_name(
            session: AsyncSession,
            organization_id: int | None,
            organization_name: str | None,
    ) -> OrganizationSchema | None:
        """
        Возвращает информацию об организации.
        """
        if not organization_id and not organization_name:
            return None

        stmt = (
            select(Organization)
            .where(
                or_(
                    Organization.id == organization_id,
                    Organization.name == organization_name)
            )
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phone_numbers),
                selectinload(Organization.building),
            )
        )
        result = await session.execute(stmt)
        organization = result.scalar_one_or_none()

        return OrganizationSchema.model_validate(organization) if organization else None

    @staticmethod
    async def get_organizations_by_activity_tree(
            session: AsyncSession,
            activity_id: int
    ) -> list[OrganizationSchema]:
        """
        Возвращает все организации, связанные с указанной деятельностью
        и всеми её дочерними видами деятельности.
        """
        cte = (
            select(Activity.id)
            .where(Activity.id == activity_id)
            .cte(name="activity_tree", recursive=True)
        )

        cte_alias = cte.alias()
        recursive_part = (
            select(Activity.id)
            .join(cte_alias, Activity.parent_id == cte_alias.c.id)
        )

        full_cte = cte.union_all(recursive_part)

        stmt = (
            select(Organization)
            .join(Organization.activities)
            .where(Activity.id.in_(full_cte.select()))
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phone_numbers),
                selectinload(Organization.building),
            )
            .distinct()
        )

        result = await session.scalars(stmt)
        organizations = result.all()

        return [OrganizationSchema.model_validate(org) for org in organizations]
