import logging
import os
import zipfile

import urllib.request

equip_zip_url = "https://github.com/WarshipGirls/WGViewer/raw/master/zip/E.zip"
ship_zip_url = "https://github.com/WarshipGirls/WGViewer/raw/master/zip/S.zip"
init_zip_url = "https://github.com/WarshipGirls/WGViewer/raw/master/zip/init.zip"
my_urls = [equip_zip_url, ship_zip_url, init_zip_url]


def _download(url: str) -> str:
    # download from Github
    l = url.rindex('/') + 1
    filename = url[l:]
    filepath = os.path.join(get_zip_dir(), filename)

    # TODO: maybe show this on GUI
    def _progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        progress = int((downloaded / total_size) * 100)
        logging.info("Download Progress", str(progress), "%")

    local_filename, _ = urllib.request.urlretrieve(url=url, filename=filepath, reporthook=_progress)
    return filename


def _download_all(urls) -> list:
    res = []
    for url in urls:
        logging.info(f'Downloading {url}')
        res.append(_download(url))
    return res


def _unzip_file(filename: str):
    # filename with extension
    path = os.path.join(get_zip_dir(), filename)
    if os.path.exists(path):
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(get_zip_dir())
    else:
        logging.error(f'Filepath not exists: {path}')


def _unzip_all(filenames: list):
    for filename in filenames:
        _unzip_file(filename)


def init_resources():
    res = _download_all(my_urls)
    _unzip_all(res)


if __name__ == "__main__":
    from src.data.wgv_path import get_zip_dir
else:
    from .wgv_path import get_zip_dir

# End of File
