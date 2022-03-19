import requests
from datetime import datetime
from pygdrive3 import service

def get_detection(url, img_path):
    if url[-1] != '/':
        url = url + '/'
    r = requests.post(url + 'img_rec', files = {
        'image': open(img_path, 'rb')
    })

    return r.json()

res = get_detection("http://b9ed-35-233-188-114.ngrok.io/", 'C:/Users/259699/Desktop/20220224_085549.jpg')

#################

drive_service = service.DriveService('./credentials.json')
drive_service.auth()

dest_file_name = 'image-{}'.format(datetime.now().strftime("%Y%m%d_%H%M%S"))
file = drive_service.upload_file(
    # Destination file name on google drive without extention.
    dest_file_name,
    # Source file name on local machine. Full path is needed.
    'C:/Users/259699/Desktop/20220224_085549.jpg',
    # Go to google drive and id is the last part of the url.
    # E.g.
    # https://drive.google.com/drive/folders/1XT4FDITnRY6z1eNgzPFiKQKCW9iGJWiS
    # 1XT4FDITnRY6z1eNgzPFiKQKCW9iGJWiS
    '1o378hWQSb31jG3QvUxbbsfNTHtkDwjcu'
)

def request_inference(dest_file_name):
    if url[-1] != '/':
        url = url + '/'
    r = requests.get(url + 'img_rec_drive?file_name=' +  dest_file_name)
    return r.json()

#################

def get_detection_drive_all():
    if url[-1] != '/':
        url = url + '/'
    r = requests.get(url + 'all_inference')

    return r.json()

def get_detection_drive(dest_file_name):
    if url[-1] != '/':
        url = url + '/'
    r = requests.get(url + 'get_inference?file_name=' +  dest_file_name)

    return r.json()

