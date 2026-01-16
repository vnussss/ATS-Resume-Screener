"""
Resume Parser Module
Extracts text from PDF and DOCX resumes
"""

import PyPDF2
import pdfplumber
import docx
from pathlib import Path
from typing import Optional, Dict
import re


class ResumeParser:
    """Parse resumes from PDF and DOCX formats"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.doc']
    
    def parse_pdf(self, file_path: str) -> str:
        """
        Extract text from PDF using pdfplumber (better formatting)
        Falls back to PyPDF2 if needed
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        text = ""
        
        try:
            # Try pdfplumber first (better quality)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if text.strip():
                return text
        
        except Exception as e:
            print(f"⚠️  pdfplumber failed: {e}, trying PyPDF2...")
        
        # Fallback to PyPDF2
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        
        except Exception as e:
            print(f"❌ PyPDF2 also failed: {e}")
            return ""
        
        return text
    
    def parse_docx(self, file_path: str) -> str:
        """
        Extract text from DOCX file
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Extracted text
        """
        try:
            doc = docx.Document(file_path)
            text = []
            
            # Extract from paragraphs
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text.append(paragraph.text)
            
            # Extract from tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if cell.text.strip():
                            text.append(cell.text)
            
            return "\n".join(text)
        
        except Exception as e:
            print(f"❌ DOCX parsing failed: {e}")
            return ""
    
    def extract_contact_info(self, text: str) -> Dict[str, Optional[str]]:
        """
        Extract contact information from resume text
        
        Args:
            text: Resume text
            
        Returns:
            Dict with email, phone, linkedin
        """
        contact_info = {
            'email': None,
            'phone': None,
            'linkedin': None
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact_info['email'] = email_match.group(0)
        
        # Extract phone
        phone_pattern = r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact_info['phone'] = phone_match.group(0)
        
        # Extract LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, text.lower())
        if linkedin_match:
            contact_info['linkedin'] = linkedin_match.group(0)
        
        return contact_info
    
    def extract_education(self, text: str) -> list:
        """
        Extract education keywords
        
        Args:
            text: Resume text
            
        Returns:
            List of education-related terms
        """
        education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'mba', 'b.tech', 'm.tech',
            'b.e.', 'm.e.', 'bsc', 'msc', 'bca', 'mca', 'diploma',
            'university', 'college', 'institute', 'degree', 'cgpa', 'gpa'
        ]
        
        text_lower = text.lower()
        found_education = []
        
        for keyword in education_keywords:
            if keyword in text_lower:
                # Extract surrounding context (±30 chars)
                pattern = rf'.{{0,30}}{keyword}.{{0,30}}'
                matches = re.findall(pattern, text_lower)
                if matches:
                    found_education.extend(matches)
        
        return list(set(found_education))
    
    def parse(self, file_path: str) -> Dict[str, any]:
        """
        Main parsing method - detects format and extracts text
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Dict with extracted text and metadata
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {
                'success': False,
                'error': f"File not found: {file_path}",
                'text': '',
                'contact_info': {},
                'education': []
            }
        
        # Check file format
        file_ext = file_path.suffix.lower()
        
        if file_ext not in self.supported_formats:
            return {
                'success': False,
                'error': f"Unsupported format: {file_ext}. Supported: {self.supported_formats}",
                'text': '',
                'contact_info': {},
                'education': []
            }
        
        # Parse based on format
        if file_ext == '.pdf':
            text = self.parse_pdf(str(file_path))
        elif file_ext in ['.docx', '.doc']:
            text = self.parse_docx(str(file_path))
        else:
            text = ""
        
        if not text.strip():
            return {
                'success': False,
                'error': "No text could be extracted from the file",
                'text': '',
                'contact_info': {},
                'education': []
            }
        
        # Extract metadata
        contact_info = self.extract_contact_info(text)
        education = self.extract_education(text)
        
        return {
            'success': True,
            'text': text,
            'contact_info': contact_info,
            'education': education,
            'file_name': file_path.name,
            'file_size': file_path.stat().st_size,
            'word_count': len(text.split())
        }


if __name__ == "__main__":
    # Test the parser
    parser = ResumeParser()
    print("✅ Resume Parser initialized!")
    print(f"📁 Supported formats: {parser.supported_formats}")
