import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

class PDFGenerator:
    def __init__(self, config):
        self.config = config
    
    def create_translated_pdf(self, original_pdf_path, translated_data, output_path):
        """Crea un nuevo PDF con el texto traducido"""
        try:
            # Abrir el PDF original para obtener dimensiones
            doc = fitz.open(original_pdf_path)
            
            # Crear nuevo PDF
            new_doc = fitz.open()
            
            for page_num, page_data in enumerate(translated_data):
                # Obtener dimensiones de la página original
                original_page = doc[page_num]
                page_rect = original_page.rect
                
                # Crear nueva página con las mismas dimensiones
                new_page = new_doc.new_page(width=page_rect.width, height=page_rect.height)
                
                # Agregar texto traducido manteniendo posiciones
                for block in page_data['blocks']:
                    if block['text'].strip():
                        # Crear rectángulo para el texto
                        rect = fitz.Rect(
                            block['x'], 
                            block['y'], 
                            block['x'] + block['width'], 
                            block['y'] + block['height']
                        )
                        
                        # Insertar texto
                        new_page.insert_text(
                            (block['x'], block['y'] + block['height'] * 0.8),  # Ajustar posición Y
                            block['text'],
                            fontsize=10,  # Puedes calcular tamaño basado en altura original
                            color=(0, 0, 0)  # Negro
                        )
            
            # Guardar el nuevo PDF
            new_doc.save(output_path)
            new_doc.close()
            doc.close()
            
        except Exception as e:
            raise Exception(f"Error creando PDF traducido: {str(e)}")
    
    def create_simple_text_pdf(self, translated_data, output_path):
        """Crea un PDF simple con solo texto traducido"""
        try:
            c = canvas.Canvas(output_path, pagesize=letter)
            width, height = letter
            
            y_position = height - 50
            
            for page_data in translated_data:
                for block in page_data['blocks']:
                    if block['text'].strip():
                        # Escribir texto
                        c.drawString(50, y_position, block['text'])
                        y_position -= 15
                        
                        # Nueva página si es necesario
                        if y_position < 50:
                            c.showPage()
                            y_position = height - 50
            
            c.save()
            
        except Exception as e:
            raise Exception(f"Error creando PDF simple: {str(e)}")