from googletrans import Translator
import re

class MedicalTranslator:
    def __init__(self, config, medical_dict=None):
        self.config = config
        self.translator = Translator()
        self.medical_dict = medical_dict or {}
    
    def preprocess_text_with_dictionary(self, text):
        """Preprocesa texto usando diccionario médico"""
        if not self.config.get('use_medical_dictionary', True):
            return text
        
        processed_text = text
        # Reemplazar términos médicos del diccionario
        for spanish_term, english_term in self.medical_dict.items():
            # Usar expresiones regulares para palabras completas
            pattern = r'\b' + re.escape(spanish_term) + r'\b'
            processed_text = re.sub(pattern, english_term, processed_text, flags=re.IGNORECASE)
        
        return processed_text
    
    def translate_text(self, text):
        """Traduce texto del español al inglés"""
        try:
            # Preprocesar con diccionario médico
            preprocessed_text = self.preprocess_text_with_dictionary(text)
            
            # Traducir usando Google Translate
            if self.config.get('translation_engine') == 'google':
                result = self.translator.translate(
                    preprocessed_text,
                    src=self.config.get('source_language', 'es'),
                    dest=self.config.get('target_language', 'en')
                )
                return result.text
            else:
                # Traducción básica si no hay motor específico
                return preprocessed_text
                
        except Exception as e:
            raise Exception(f"Error en traducción: {str(e)}")
    
    def translate_pdf_data(self, pdf_data):
        """Traduce todos los bloques de texto de un PDF"""
        try:
            translated_data = []
            
            for page_data in pdf_data:
                translated_blocks = []
                
                for block in page_data['blocks']:
                    if block['text'].strip():
                        translated_text = self.translate_text(block['text'])
                        translated_blocks.append({
                            'text': translated_text,
                            'original_text': block['text'],
                            'x': block['x'],
                            'y': block['y'],
                            'width': block['width'],
                            'height': block['height'],
                            'confidence': block['confidence']
                        })
                    else:
                        # Mantener bloques vacíos
                        translated_blocks.append(block)
                
                translated_data.append({
                    'page': page_data['page'],
                    'blocks': translated_blocks
                })
            
            return translated_data
            
        except Exception as e:
            raise Exception(f"Error traduciendo PDF: {str(e)}")
