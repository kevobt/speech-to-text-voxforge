import argparse
import os
import tarfile
import urllib3

from concurrent.futures import ThreadPoolExecutor, wait

from urllib.request import urlopen

from bs4 import BeautifulSoup


def download_and_extract(url: str, target_directory: str, current_item=0, items_count=0):
    """
    Downloads the speaker file and extracts it into the target directory
    :param url: url to the speaker directory
    :param target_directory:
    :param current_item: this items index for logging
    :param items_count: total amount of items to download. Displayed for logging
    """
    print('Downloading %s / %s' % (current_item, items_count))

    http = urllib3.PoolManager()

    with http.request('GET', url, preload_content=False) as r, tarfile.open(fileobj=r, mode="r|gz") as tar:
        for item in tar:
            tar.extract(item, target_directory)
    return


def ensure_directory(path: str):
    """
    Creates a directory if does not exist
    :param path: Path of the directory
    """
    if not os.path.exists(path):
        os.makedirs(path)


def download_corpus(target_directory: str,
                    max_workers: int,
                    amount: int,
                    voxforge_url="http://www.repository.voxforge1.org/"
                                 "downloads/SpeechCorpus/Trunk/Audio/Main/16kHz_16bit"):
    """
    Initiates download of the voxforge speech corpus
    :param target_directory: target directory for the files
    :param max_workers: amount of threads to be used for the download and extraction
    :param amount: amount of speaker files to be downloaded
    :param voxforge_url: url to the voxforge corpus
    """
    # input validation
    if not max_workers:
        max_workers = 10
    if not target_directory:
        target_directory = "voxforge-corpus"

    ensure_directory(target_directory)

    # collect links from voxforge
    html_page = urlopen(voxforge_url)
    soup = BeautifulSoup(html_page, "html5lib")
    links = soup.findAll('a')
    speaker_refs = [link['href'] for link in links if '.tgz' in link['href']]

    # run multiple threads which download and extract the speaker files
    executor = ThreadPoolExecutor(max_workers)
    futures = []

    if not amount:
        amount = len(speaker_refs)

    for i, ref in enumerate(speaker_refs):
        if i < amount:
            futures.append(executor.submit(
                download_and_extract,
                os.path.join(voxforge_url, ref).replace('\\', '/'),
                target_directory,
                i + 1,
                amount))
        else:
            break

    wait(futures)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Downloader for the voxforge speech corpus")
    parser.add_argument('directory', help='directory where to store the downloaded corpus')
    parser.add_argument('-n', '--number', type=int, help="amount of files to download")
    parser.add_argument('-w', '--workers', type=int, help="amount of parallel downloads")
    args = parser.parse_args()

    download_corpus(args.directory, args.workers, args.number)
