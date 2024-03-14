import os
import datetime
import boto3
import requests

def download_data():
    # Configurar el cliente S3
    s3 = boto3.client('s3')
    
    # URL base del sitio web
    base_url = 'https://casas.mitula.com.co/casas/fincas-servicio-raiz'
    
    # Descargar las primeras 5 páginas
    for page_num in range(1, 6):
        url = f"{base_url}?page={page_num}"
        response = requests.get(url)
        html_content = response.text
        
        # Guardar el HTML en S3
        key = f"contenido-pag-{page_num}-{datetime.datetime.now().strftime('%Y-%m-%d')}.html"
        s3.put_object(Bucket='bucket-rawj', Key=key, Body=html_content)
        
download_data()