import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env_kafka_connect')

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = "us-east-1"

s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region_name
)

bucket_name = "desafio-silver-gold-cesteves"
folder_name = "analytics/ipca/gold/"

try:
    s3.put_object(Bucket=bucket_name, Key=folder_name)
    print(f"Sucesso: Pasta '{folder_name}' criada no bucket '{bucket_name}'.")
    
    # Check if silver exists too, just in case
    silver_folder = "processed-data/ipca/silver/"
    s3.put_object(Bucket=bucket_name, Key=silver_folder)
    print(f"Garantia: Pasta '{silver_folder}' verificada/recriada.")
    
except Exception as e:
    print(f"Erro ao criar pasta: {e}")
