import os
import sys
from pathlib import Path
from utils import setup_logging, load_config, load_medical_dictionary, create_directories, get_pdf_files, is_processed, mark_as_processed, clean_temp_files
from ocr_processor import OCRProcessor
from translator import MedicalTranslator
from pdf_generator import PDFGenerator

def process_single_pdf(pdf_path, config, medical_dict, logger):
    """Procesa un solo PDF"""
    try:
        pdf_name = pdf_path.name
        logger.info(f"Procesando: {pdf_name}")
        
        # Inicializar componentes
        ocr_processor = OCRProcessor()
        translator = MedicalTranslator(config, medical_dict)
        pdf_generator = PDFGenerator(config)
        
        # Paso 1: OCR
        logger.info("  - Extrayendo texto con OCR...")
        pdf_data = ocr_processor.process_pdf(str(pdf_path))
        
        # Paso 2: Traducción
        logger.info("  - Traduciendo texto...")
        translated_data = translator.translate_pdf_data(pdf_data)
        
        # Paso 3: Generar PDF
        logger.info("  - Generando PDF traducido...")
        output_path = os.path.join('output_pdfs', pdf_name)
        
        if config.get('preserve_format', True):
            pdf_generator.create_translated_pdf(str(pdf_path), translated_data, output_path)
        else:
            pdf_generator.create_simple_text_pdf(translated_data, output_path)
        
        # Marcar como procesado
        mark_as_processed(pdf_name)
        logger.info(f"  ✓ Completado: {pdf_name}")
        
    except Exception as e:
        logger.error(f"  ✗ Error procesando {pdf_path.name}: {str(e)}")
        raise

def main():
    """Función principal"""
    # Setup
    logger = setup_logging()
    create_directories()
    clean_temp_files()
    
    try:
        # Cargar configuración
        config = load_config()
        medical_dict = load_medical_dictionary()
        
        logger.info("=== Iniciando Traductor Médico de PDFs ===")
        
        # Obtener archivos PDF
        pdf_files = get_pdf_files()
        
        if not pdf_files:
            logger.warning("No se encontraron archivos PDF en input_pdfs/")
            return
        
        logger.info(f"Encontrados {len(pdf_files)} archivos para procesar")
        
        # Procesar cada PDF
        processed_count = 0
        error_count = 0
        
        for pdf_file in pdf_files:
            if is_processed(pdf_file.name):
                logger.info(f"  - {pdf_file.name} ya fue procesado, saltando...")
                continue
            
            try:
                process_single_pdf(pdf_file, config, medical_dict, logger)
                processed_count += 1
            except Exception as e:
                error_count += 1
                logger.error(f"Error fatal en {pdf_file.name}: {str(e)}")
                continue
        
        # Limpiar archivos temporales
        clean_temp_files()
        
        # Resumen
        logger.info("=== Proceso completado ===")
        logger.info(f"✓ Procesados: {processed_count}")
        logger.info(f"✗ Errores: {error_count}")
        logger.info(f"Total: {len(pdf_files)} archivos")
        
    except KeyboardInterrupt:
        logger.info("Proceso interrumpido por el usuario")
        clean_temp_files()
    except Exception as e:
        logger.error(f"Error crítico: {str(e)}")
        clean_temp_files()

if __name__ == "__main__":
    main()
