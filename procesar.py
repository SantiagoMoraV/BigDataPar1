import os
import boto3
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def procesardato():
    s3 = boto3.client('s3')
    bucket_name = "bucket-rawj"

    data = []

    for page_num in range(1, 6):
        key = f"contenido-pag-{page_num}-{datetime.now().strftime('%Y-%m-%d')}.html"
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        body = obj['Body'].read()
        soup = BeautifulSoup(body, 'html.parser')

        properties = soup.find_all('div', {'class': 'listing-card__information-main'})

        for property in properties:
            price = property.find('div', {'class': 'listing-card__price-wrapper'}).text.strip()
            sqft = property.find_all('div', {'class': 'listing-card__property'})
            sqft2 = sqft
            casa = [price]
            for property2 in sqft2:
                casa.append(property2.text.strip())
            data.append(casa)

    s = "Precio, num_habitaciones, num_banos, metros_cuadrados\n"
    for fila in data:
        if len(fila) >= 4:
            s += f"{fila[0]}, {fila[1].replace('.', '')}, {fila[2].replace('.', '')}, {fila[3]}\n"

    s3.put_object(Bucket="bucket-finalj", Key=f"{datetime.now().strftime('%Y-%m-%d')}.csv", Body=s)

procesardato()