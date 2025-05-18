import asyncio
from contextlib import asynccontextmanager
from functools import wraps
from pathlib import Path
import os
import time
from typing import Any, AsyncGenerator
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from httpx import AsyncClient

API_URL = "http://127.0.0.1:8000"
USERNAME = ""
PASSWORD = ""
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}


def get_src_and_dst() -> tuple[Path, Path]:
    input_src = input("Folder with manga chapters: ")
    input_dest = input("Destination folder: ")
    src = Path(input_src)
    dest = Path(input_dest)

    if not src.is_dir():
        raise Exception(f"Source folder does not exist: {src}")
    if not dest.is_dir():
        Path(dest).mkdir(parents=True, exist_ok=True)
    return src, dest


def save_to_zip(chapter_number: int, folder_name: str, src: Path, dest: Path):
    ch_pictures = []
    ch_dir_src = Path(src).joinpath(folder_name)
    ch_file_dest = Path(dest).joinpath(str(chapter_number) + ".zip")
    if ch_dir_src.is_dir():
        for p in os.listdir(ch_dir_src):
            p_path = Path(ch_dir_src).joinpath(p)
            file_suffix = Path(p_path).suffix
            if file_suffix in ALLOWED_EXTENSIONS:
                ch_pictures.append(p_path)
            else:
                print(f"WARNING: {p_path} bad extension {file_suffix}, not in {ALLOWED_EXTENSIONS}")
        with zipfile.ZipFile(ch_file_dest, "w") as zipf:
            for file in ch_pictures:
                zipf.write(file, arcname=file.name)
        return f"INFO: {ch_file_dest} saved"


def show_execute_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = start - time.time()
        print(f"--- {func.__name__} {end:.0f} seconds ---")
        return res

    return wrapper


ch_list = []


@show_execute_time
def run_with_pools(src: Path, dest: Path):
    with ThreadPoolExecutor() as tp:
        tasks = {tp.submit(save_to_zip, k, n, src, dest) for k, n in enumerate(os.listdir(src))}
        for task in as_completed(tasks):
            print(task.result())


@asynccontextmanager
async def ac_auth() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(base_url=API_URL) as ac:
        res = await ac.post("/auth/login", data={"username": USERNAME, "password": PASSWORD})
        assert res.status_code == 200, res.status_code
        res_data = res.json()
        access_token = res_data.get("access_token")

        async with AsyncClient(
            base_url=API_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=60,
        ) as ac_auth:
            yield ac_auth


async def post_chapter(client: AsyncClient, manga_id: int, data: dict, zip_path: Path):
    with open(zip_path, "rb") as f:
        async with sem:
            res_post = await client.post(
                f"/manga/{manga_id}/chapters",
                files={"file": (f"{manga_id}-{f.name}", f, "application/zip")},
                data=data,
            )
            assert res_post.status_code == 200 or res_post.status_code == 409, res_post.text
            print(data["number"], res_post.status_code)
            return (data["number"], res_post.status_code)


async def create_chapters(manga_id: int, source: Path):
    async with ac_auth() as client:
        ch_list = os.listdir(source)
        ch_list.sort(key=lambda x: int(x.split(".")[0]))
        tasks = []
        for n in os.listdir(source):
            zip_path = Path(source).joinpath(n)
            ch_number = n.split(".")[0]
            data = {"number": ch_number, "price": 0, "is_premium": False}
            tasks.append(asyncio.create_task(post_chapter(client, manga_id, data, zip_path)))
        result = await asyncio.gather(*tasks)
        for n in result:
            print(n)


sem = asyncio.Semaphore(10)

if __name__ == "__main__":
    src, dest = get_src_and_dst()
    run_with_pools(src, dest)
    asyncio.run(create_chapters(manga_id=1, source=dest))
