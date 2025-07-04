import logging
import os
from pathlib import Path
import shutil
import uuid
import zipfile

from starlette.datastructures import UploadFile

from src.config import settings
from src.exceptions import (
    BadFileExtException,
    BadFileExtInArchiveException,
    BadImageFileExtException,
    PageFileImageNameException,
)

ALLOWED_EXTENSIONS: list[str] = settings.ALLOWED_IMAGE_EXTENSIONS


def check_files_inside(file: str) -> None:
    zip = zipfile.ZipFile(file)
    files_in_zip = zip.namelist()
    for n in files_in_zip:
        file_suffix = Path(n).suffix
        if file_suffix not in ALLOWED_EXTENSIONS:
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


def file_inspection_and_save(file: UploadFile) -> str:
    file_path = save_to_tmp(file)
    check_file_ext(file_path)
    check_files_inside(file_path)
    return file_path


def rm_file(file_path: str) -> None:
    file_to_rem = Path(file_path)
    Path.unlink(file_to_rem)


def rm_chapter_files(manga_id: int, chapter_id: int) -> None:
    path_to_rm = Path(f"./{settings.SAVE_IMG_FOLDER}/manga/{manga_id}/chapters/{chapter_id}/")
    if os.path.exists(path_to_rm) and os.path.isdir(path_to_rm):
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
    logging.info(f"Images extracted: {images_sorted}")
    return images_sorted


def save_manga_poster(manga_id: int, file: UploadFile) -> str:
    file_ext = Path(file.filename).suffix
    if file_ext not in ALLOWED_EXTENSIONS:
        raise BadImageFileExtException
    save_path = f"./{settings.SAVE_IMG_FOLDER}/manga/{manga_id}/"
    Path(save_path).mkdir(parents=True, exist_ok=True)
    saved_file = f"{save_path}poster{file_ext}"
    url_path = saved_file[1:]
    with open(saved_file, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    return url_path


def get_number(text: str):
    try:
        return int(text.split("/")[-1].split(".")[0])
    except ValueError:
        raise PageFileImageNameException
