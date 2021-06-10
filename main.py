import requests
import os
import atexit
import re
import time
import tqdm

index = 0
BASE_URL = "https://1001ebooks.club/account/direct_download/"


def savecounter():
    with open("latest.txt", "w") as fd:
        fd.write(str(index))

def downloadfile(url):
    with requests.get(url, stream=True) as r:
        initial_pos = 0
        if r.status_code == 200:
            total_size = int(r.headers.get('content-length'))
            d = r.headers['content-disposition']
            fname = re.findall("filename=(.+)", d)[0][1:-1].encode("iso-8859-1").decode("utf-8")
            with open(fname, "wb") as f:
                with tqdm.tqdm(total=total_size, unit='KB', unit_scale=True, desc=fname, initial=initial_pos, ascii=True) as pbar:
                    for chunck in r.iter_content(chunk_size=8192):
                        if chunck:
                            f.write(chunck)          
                            pbar.update(len(chunck))
            return True
        else:
            return False


def main():
    global index

    if os.path.exists("latest.txt"):
        with open("latest.txt", "r") as fd:
            tmp = fd.read()
        if tmp != '':
            index = int(tmp)

    while downloadfile(BASE_URL + str(index)):
        index = index + 1
        time.sleep(1)

    print("Download finished")

    return

if __name__ == "__main__":
    atexit.register(savecounter)
    main()




