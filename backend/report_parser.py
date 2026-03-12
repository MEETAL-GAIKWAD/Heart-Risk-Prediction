import pdfplumber
import re
from typing import Dict, Optional
from schemas import PatientFeatures
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MedicalReportParser:
    """Parser for medical reports (PDF)"""
    
    def __init__(self):
        self.patterns = {
            'age': [
                r'age[:\s]+(\d+)',
                r'(\d+)\s*(?:years?|yrs?|y\.o\.)',
                r'patient.*?(\d+)\s*years?'
            ],
            'bp': [
                r'blood\s*pressure[:\s]+(\d+)[/\s]',
                r'bp[:\s]+(\d+)[/\s]',
                r'systolic[:\s]+(\d+)',
                r'(\d{2,3})\s*/\s*\d{2,3}\s*mmhg'
            ],
            'cholesterol': [
                r'cholesterol[:\s]+(\d+)',
                r'total\s*cholesterol[:\s]+(\d+)',
                r'chol[:\s]+(\d+)'
            ],
            'bmi': [
                r'bmi[:\s]+([\d.]+)',
                r'body\s*mass\s*index[:\s]+([\d.]+)'
            ],
            'diabetes': [
                r'diabetes[:\s]*(yes|no|positive|negative|present|absent)',
                r'diabetic[:\s]*(yes|no)',
                r'dm[:\s]*(yes|no|positive|negative)'
            ],
            'smoking': [
                r'smok(?:ing|er)[:\s]*(yes|no|positive|negative|current|former|never)',
                r'tobacco[:\s]*(yes|no|use|user)'
            ],
            'radiation_dose': [
                r'radiation\s*dose[:\s]+([\d.]+)',
                r'dose[:\s]+([\d.]+)\s*gy',
                r'total\s*dose[:\s]+([\d.]+)',
                r'([\d.]+)\s*gy'
            ],
            'treatment_site': [
                r'treatment\s*site[:\s]+(\w+)',
                r'site[:\s]+(\w+)',
                r'location[:\s]+(\w+)'
            ],
            'sessions': [
                r'sessions?[:\s]+(\d+)',
                r'fractions?[:\s]+(\d+)',
                r'treatments?[:\s]+(\d+)'
            ]
        }
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting PDF text: {str(e)}")
            raise
    
    def parse_value(self, text: str, field: str) -> Optional[any]:
        """Parse a specific field value from text"""
        text_lower = text.lower()
        
        if field not in self.patterns:
            return None
        
        for pattern in self.patterns[field]:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                value = match.group(1)
                
                # Convert based on field type
                if field in ['age', 'bp', 'sessions']:
                    try:
                        return int(value)
                    except:
                        continue
                
                elif field in ['bmi', 'radiation_dose']:
                    try:
                        return float(value)
                    except:
                        continue
                
                elif field in ['diabetes', 'smoking']:
                    # Convert yes/no to 1/0
                    value_lower = value.lower()
                    if value_lower in ['yes', 'positive', 'present', 'current', 'user', 'use']:
                        return 1
                    elif value_lower in ['no', 'negative', 'absent', 'never']:
                        return 0
                    elif value_lower == 'former':
                        return 0  # Former smoker treated as non-smoker
                
                elif field == 'treatment_site':
                    return value.lower().replace(' ', '_')
        
        return None
    
    def parse_report(self, pdf_path: str) -> Dict:
        """
        Parse medical report and extract patient features
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with extracted features and raw text
        """
        try:
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            logger.info(f"Extracted {len(text)} characters from PDF")
            
            # Parse each field
            extracted = {}
            for field in self.patterns.keys():
                value = self.parse_value(text, field)
                if value is not None:
                    extracted[field] = value
                    logger.info(f"Extracted {field}: {value}")
            
            # Fill in defaults for missing values
            defaults = {
                'age': 50,
                'bp': 120,
                'cholesterol': 200,
                'bmi': 25.0,
                'diabetes': 0,
                'smoking': 0,
                'radiation_dose': 0.0,
                'treatment_site': 'unknown',
                'sessions': 0
            }
            
            for field, default in defaults.items():
                if field not in extracted:
                    extracted[field] = default
                    logger.warning(f"Using default for {field}: {default}")
            
            return {
                'features': extracted,
                'raw_text': text[:1000]  # First 1000 chars for reference
            }
            
        except Exception as e:
            logger.error(f"Error parsing report: {str(e)}")
            raise
    
    def create_patient_features(self, extracted: Dict) -> PatientFeatures:
        """Convert extracted data to PatientFeatures object"""
        return PatientFeatures(
            age=extracted.get('age', 50),
            bp=extracted.get('bp', 120),
            cholesterol=extracted.get('cholesterol', 200),
            bmi=extracted.get('bmi', 25.0),
            diabetes=extracted.get('diabetes', 0),
            smoking=extracted.get('smoking', 0),
            radiation_dose=extracted.get('radiation_dose', 0.0),
            treatment_site=extracted.get('treatment_site', 'unknown'),
            sessions=extracted.get('sessions', 0)
        )


def parse_medical_report(pdf_path: str) -> tuple[PatientFeatures, str]:
    """
    Convenience function to parse medical report
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Tuple of (PatientFeatures, raw_text)
    """
    parser = MedicalReportParser()
    result = parser.parse_report(pdf_path)
    features = parser.create_patient_features(result['features'])
    return features, result['raw_text']
