from gdown import download
from zipfile import ZipFile
from os import rename, remove
# ID del archivo de Google Drive
file_id = '1ig2ngoXFTxP5Pa8muXo02mDTFexZzsis'
# Nombre con el que deseas guardar el archivo descargado
output = 'data.zip'

# Construir la URL de descarga
url = f'https://drive.google.com/uc?id={file_id}'

# Descargar el archivo
download(url, output, quiet=False)

# Extraer .zip
with ZipFile("data.zip","r") as zip_ref:
    zip_ref.extractall("data")
remove("data.zip")


rename("data/farmers-protest-tweets-2021-2-4.json", "data/data.json")
