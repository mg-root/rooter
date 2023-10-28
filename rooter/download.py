import requests, os, time

def download_file_url(url, file_name=None, destination=''):
    start = time.time()
    response = requests.get(url)
    end = time.time()
    duration = end - start

    if response.status_code == 200:
        os.makedirs(destination, exist_ok=True)
        file_name = file_name if file_name != None else url.split('/')[-1]
        extension = '' if file_name == None else '.' + url.split('/')[-1].split('.')[1]
        destination_path = os.path.join(destination, file_name + extension)
        with open(destination_path, "wb") as file:
            file.write(response.content)
        return True, duration
    else:
        return False, 0