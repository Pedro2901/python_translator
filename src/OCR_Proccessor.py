import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
from pathlib import Path

class OCRProcessor:
    def __init__(self):
        # Configura la ruta de tesseract si es necesario
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass
    
    def pdf_to_images(self, pdf_path, output_folder='temp'):
        """Convierte PDF a imágenes"""
        try:
            images = convert_from_path(pdf_path, dpi=300)
            image_paths = []
            
            for i, image in enumerate(images):
                image_path = os.path.join(output_folder, f'page_{i}.png')
                image.save(image_path, 'PNG')
                image_paths.append(image_path)
            
            return image_paths
        except Exception as e:
            raise Exception(f"Error convirtiendo PDF a imágenes: {str(e)}")
    
    def extract_text_with_positions(self, image_path):
        """Extrae texto con posiciones usando OCR"""
        try:
            # Usar tesseract con opción de devolver cajas de texto
            data = pytesseract.image_to_data(Image.open(image_path), output_type=pytesseract.Output.DICT)
            
            text_blocks = []
            n_boxes = len(data['text'])
            
            for i in range(n_boxes):
                if int(data['conf'][i]) > 30:  # Solo texto con confianza > 30%
                    text_blocks.append({
                        'text': data['text'][i],
                        'x': data['left'][i],
                        'y': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i],
                        'confidence': data['conf'][i]
                    })
            
            return text_blocks
        except Exception as e:
            raise Exception(f"Error en OCR: {str(e)}")
    
    def process_pdf(self, pdf_path):
        """Procesa un PDF completo y devuelve texto con posiciones"""
        try:
            # Convertir PDF a imágenes
            image_paths = self.pdf_to_images(pdf_path)
            
            all_pages_data = []
            
            for i, image_path in enumerate(image_paths):
                page_data = self.extract_text_with_positions(image_path)
                all_pages_data.append({
                    'page': i + 1,
                    'blocks': page_data
                })
            
            return all_pages_data
            
        except Exception as e:
            raise Exception(f"Error procesando PDF: {str(e)}")