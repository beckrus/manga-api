from sqlalchemy import func, select, or_
from src.models.authors import AuthorsOrm
from src.schemas.manga import MangaResponseDTO
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
        hotels = [self.mapper.map_to_domain_entity(data=hotel) for hotel in result.scalars().all()]

        return hotels
