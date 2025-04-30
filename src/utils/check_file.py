from pathlib import Path
import shutil
import uuid
import zipfile

from starlette.datastructures import UploadFile

from src.config import settings
from src.exceptions import (
    BadFileExtException,
    BadFileExtInArchiveException,
    PageFileImageNameException,
)


def check_files_inside(file: str) -> None:
    zip = zipfile.ZipFile(file)
    files_in_zip = zip.namelist()
    for n in files_in_zip:
        file_suffix = Path(n).suffix
        valid_extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
        if file_suffix not in valid_extensions:
            raise BadFileExtInArchiveException


def save_to_tmp(file: UploadFile) -> str:
    Path("./tmp").mkdir(parents=True, exist_ok=True)

    file_location = f"./tmp/{str(uuid.uuid4())}_{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    return file_location


def check_file_ext(file_path: str) -> None:
    file_suffix = Path(file_path).suffix
    if file_suffix not in [".zip"]:
        raise BadFileExtException


def file_inspection(file: UploadFile) -> str:
    file_path = save_to_tmp(file)
    check_file_ext(file_path)
    check_files_inside(file_path)
    return file_path


def rm_file(file_path: str) -> None:
    file_to_rem = Path(file_path)
    Path.unlink(file_to_rem)


def rm_chapter_files(manga_id: int, chapter_id: int) -> None:
    path_to_rm = Path(f"./{settings.SAVE_IMG_FOLDER}/manga/{manga_id}/chapters/{chapter_id}/")
    shutil.rmtree(path_to_rm)


def save_page_files(manga_id: int, chapter_id: int, file_path: str) -> list[str]:
    zip = zipfile.ZipFile(file_path)
    files_in_zip: list[str] = zip.namelist()
    save_path = f"./{settings.SAVE_IMG_FOLDER}/manga/{manga_id}/chapters/{chapter_id}/"
    url_path = f"/{settings.SAVE_IMG_FOLDER}/manga/{manga_id}/chapters/{chapter_id}/"
    Path(save_path).mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(save_path)

    images = [url_path + file for file in files_in_zip]
    images_sorted = sorted(images, key=get_number)
    return images_sorted


def get_number(text: str):
    try:
        return int(text.split("/")[-1].split(".")[0])
    except ValueError:
        raise PageFileImageNameException
