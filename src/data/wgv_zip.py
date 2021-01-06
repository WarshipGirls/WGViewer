import logging
import os
import zipfile

import urllib.request

from PyQt5.QtCore import pyqtSignal

equip_zip_url = "https://github.com/WarshipGirls/WGViewer/raw/master/zip/E.zip"
ship_zip_url = "https://github.com/WarshipGirls/WGViewer/raw/master/zip/S.zip"
init_zip_url = "https://github.com/WarshipGirls/WGViewer/raw/master/zip/init.zip"
my_urls = [equip_zip_url, ship_zip_url, init_zip_url]

# ================================
# Exports
# ================================


def _download(url: str, progress_bar: pyqtSignal) -> str:
    logging.debug(f'Downloading {url}')
    # download from Github
    l = url.rindex('/') + 1
    filename = url[l:]
    filepath = os.path.join(get_zip_dir(), filename)

    def _progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        progress = int((downloaded / total_size) * 100)
        progress_bar.emit(progress)

    local_filename, _ = urllib.request.urlretrieve(url=url, filename=filepath, reporthook=_progress)
    return filename


def _download_all(urls: list, progress_bar: pyqtSignal) -> list:
    res = []
    for url in urls:
        res.append(_download(url, progress_bar))
    return res


def _unzip_file(filename: str) -> None:
    # filename with extension
    path = os.path.join(get_zip_dir(), filename)
    if os.path.exists(path):
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(get_zip_dir())
    else:
        logging.error(f'Filepath not exists: {path}')


def _unzip_all(filenames: list) -> None:
    for filename in filenames:
        _unzip_file(filename)

# ================================
# Exports
# ================================


def init_resources(progress_bar: pyqtSignal) -> None:
    res = _download_all(my_urls, progress_bar)
    _unzip_all(res)


if __name__ == "__main__":
    from src.data.wgv_path import get_zip_dir
else:
    from .wgv_path import get_zip_dir

# End of File
