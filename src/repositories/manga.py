from sqlalchemy import func, select, or_
from sqlalchemy.exc import NoResultFound
from src.exceptions import ObjectNotFoundException
from src.models.read_progress import ReadProgressOrm
from src.models.authors import AuthorsOrm
from src.schemas.manga import MangaResponseDTO, MangaResponseWithRelDTO
from src.repositories.mappers.mappers import MangaMapper
from src.repositories.base import BaseRepository
from src.models.manga import MangaOrm


class MangaRepository(BaseRepository):
    model = MangaOrm
    mapper = MangaMapper

    async def get_filtered(
        self,
        limit: int = 1,
        offset: int = 10,
        name: str | None = None,
        author: str | None = None,
    ) -> list[MangaResponseDTO]:
        """
        Retrieve a filtered list of manga from the database.

        Parameters:
        - **limit** (int): The maximum number of manga to retrieve. Default is 1.
        - **offset** (int): The number of manga to skip before starting to retrieve results. Default is 10.
        - **name** (str | None): Filter manga by their main or secondary name. Partial matches are allowed (case-insensitive).
        - **author** (str | None): Filter manga by the author's name. Partial matches are allowed (case-insensitive).

        Returns:
        - A list of MangaResponseDTO objects that match the specified filters.

        Notes:
        - If both `name` and `author` are provided, the results will include manga that match either filter.
        - If no filters are provided, all manga will be retrieved (up to the specified limit and offset).
        """
        manga_filters = []
        if name:
            manga_filters.append(func.lower(self.model.main_name).contains(name.strip().lower()))
            manga_filters.append(
                func.lower(self.model.secondary_name).contains(name.strip().lower())
            )
        if author:
            authors_ids = select(AuthorsOrm.id).where(
                func.lower(AuthorsOrm.name).contains(author.strip().lower())
            )
            manga_filters.append(MangaOrm.author.in_(authors_ids))
        query = select(MangaOrm)
        if manga_filters:
            query = query.where(or_(*manga_filters))
        query = query.limit(limit).offset(offset)
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        manga = [self.mapper.map_to_domain_entity(data=hotel) for hotel in result.scalars().all()]

        return manga

    async def get_filtered_by_ids(self, manga_list: list[int]) -> list[MangaResponseDTO]:
        """
        Retrieve a filtered list of manga from the database.

        Parameters:
        - **limit** (int): The maximum number of manga to retrieve. Default is 1.
        - **offset** (int): The number of manga to skip before starting to retrieve results. Default is 10.
        - **name** (str | None): Filter manga by their main or secondary name. Partial matches are allowed (case-insensitive).
        - **author** (str | None): Filter manga by the author's name. Partial matches are allowed (case-insensitive).

        Returns:
        - A list of MangaResponseDTO objects that match the specified filters.

        Notes:
        - If both `name` and `author` are provided, the results will include manga that match either filter.
        - If no filters are provided, all manga will be retrieved (up to the specified limit and offset).
        """
        query = select(MangaOrm)
        query = query.where(MangaOrm.id.in_(manga_list))
        result = await self.session.execute(query)
        manga = [self.mapper.map_to_domain_entity(data=hotel) for hotel in result.scalars().all()]

        return manga

    async def get_one_by_id_with_progress(
        self, manga_id: int, user_id: int
    ) -> MangaResponseWithRelDTO:
        try:
            stmt = select(self.model).filter_by(id=manga_id)
            result = await self.session.execute(stmt)
            manga = result.scalars().one()
            stmt_progress = select(ReadProgressOrm).where(
                ReadProgressOrm.manga_id == manga_id, ReadProgressOrm.user_id == user_id
            )
            progress_result = await self.session.execute(stmt_progress)
            progress = progress_result.scalars().one_or_none()
            # print(stmt.compile(compile_kwargs={"literal_binds": True}))
            c_r_chapter = progress.chapter_id if progress else None
            return MangaResponseWithRelDTO.model_validate(
                {**manga.__dict__, "current_reading_chapter": c_r_chapter}
            )
        except NoResultFound as e:
            raise ObjectNotFoundException from e
