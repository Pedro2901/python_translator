import os
import json
import logging
from pathlib import Path

def setup_logging():
    """Configura el sistema de logs"""
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler('logs/processing_log.txt'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def load_config():
    """Carga la configuración del sistema"""
    try:
        with open('config/config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception("Archivo config/config.json no encontrado")

def load_medical_dictionary():
    """Carga el diccionario médico"""
    try:
        with open('config/medical_terms_dict.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def create_directories():
    """Crea las carpetas necesarias si no existen"""
    directories = ['input_pdfs', 'output_pdfs', 'logs', 'temp']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def clean_temp_files():
    """Limpia archivos temporales"""
    temp_dir = Path('temp')
    if temp_dir.exists():
        for file in temp_dir.glob('*'):
            file.unlink()

def get_pdf_files():
    """Obtiene lista de archivos PDF en input_pdfs"""
    input_dir = Path('input_pdfs')
    return list(input_dir.glob('*.pdf'))

def is_processed(filename):
    """Verifica si un archivo ya fue procesado"""
    try:
        if not Path('logs/processed_files.txt').exists():
            return False
        with open('logs/processed_files.txt', 'r') as f:
            processed = f.read().splitlines()
        return filename in processed
    except:
        return False

def mark_as_processed(filename):
    """Marca un archivo como procesado"""
    with open('logs/processed_files.txt', 'a') as f:
        f.write(f"{filename}\n")
