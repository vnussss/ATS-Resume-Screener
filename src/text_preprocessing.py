"""
Text Preprocessing Module
Cleans and normalizes resume & JD text using NLP
"""

import re
import spacy
from typing import List, Set
import nltk
from nltk.corpus import stopwords

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("⚠️  Downloading spaCy model... (one-time setup)")
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


class TextPreprocessor:
    """Clean and normalize text for ATS processing"""
    
    def __init__(self):
        self.stop_words: Set[str] = set(stopwords.words('english'))
        # Keep important job-related words
        self.keep_words = {'python', 'java', 'c++', 'react', 'node', 'sql', 
                          'aws', 'azure', 'docker', 'kubernetes', 'api'}
        self.stop_words -= self.keep_words
    
    def clean_text(self, text: str) -> str:
        """
        Clean raw text: remove noise, normalize
        
        Args:
            text: Raw text from resume/JD
            
        Returns:
            Cleaned text string
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s#+.-]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract technical skills and key terms
        
        Args:
            text: Cleaned text
            
        Returns:
            List of extracted skills/keywords
        """
        doc = nlp(text)
        
        # Extract noun chunks and entities
        skills = []
        
        # Get named entities (technologies, orgs, etc.)
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'GPE']:
                skills.append(ent.text.lower())
        
        # Get noun phrases (technical terms)
        for chunk in doc.noun_chunks:
            # Filter out common phrases
            if len(chunk.text.split()) <= 3 and chunk.text.lower() not in self.stop_words:
                skills.append(chunk.text.lower())
        
        # Get important single tokens
        for token in doc:
            if (token.pos_ in ['NOUN', 'PROPN'] and 
                token.text.lower() not in self.stop_words and
                len(token.text) > 2):
                skills.append(token.text.lower())
        
        # Deduplicate while preserving order
        seen = set()
        unique_skills = []
        for skill in skills:
            if skill not in seen:
                seen.add(skill)
                unique_skills.append(skill)
        
        return unique_skills
    
    def lemmatize(self, text: str) -> str:
        """
        Lemmatize text (reduce words to base form)
        
        Args:
            text: Text to lemmatize
            
        Returns:
            Lemmatized text
        """
        doc = nlp(text)
        lemmatized = []
        
        for token in doc:
            # Skip stopwords unless in keep_words
            if token.text.lower() in self.stop_words:
                continue
            
            # Keep meaningful words
            if not token.is_punct and not token.is_space:
                lemmatized.append(token.lemma_)
        
        return ' '.join(lemmatized)
    
    def preprocess(self, text: str, extract_skills_flag: bool = True) -> dict:
        """
        Full preprocessing pipeline
        
        Args:
            text: Raw text to process
            extract_skills_flag: Whether to extract skills
            
        Returns:
            Dict with cleaned text, lemmatized text, and skills
        """
        # Step 1: Clean
        cleaned = self.clean_text(text)
        
        # Step 2: Lemmatize
        lemmatized = self.lemmatize(cleaned)
        
        # Step 3: Extract skills (optional)
        skills = []
        if extract_skills_flag:
            skills = self.extract_skills(cleaned)
        
        return {
            'cleaned': cleaned,
            'lemmatized': lemmatized,
            'skills': skills,
            'word_count': len(cleaned.split())
        }


# Utility function for quick preprocessing
def quick_preprocess(text: str) -> str:
    """Quick preprocessing for simple use cases"""
    preprocessor = TextPreprocessor()
    return preprocessor.preprocess(text)['lemmatized']


if __name__ == "__main__":
    # Test the preprocessor
    sample_text = """
    I am a Software Engineer with 3+ years of experience in Python, JavaScript, and React.
    Worked at Google and Microsoft on cloud infrastructure. 
    Email: john@example.com | www.linkedin.com/in/johndoe
    """
    
    preprocessor = TextPreprocessor()
    result = preprocessor.preprocess(sample_text)
    
    print("🧹 Cleaned:", result['cleaned'][:100])
    print("📝 Lemmatized:", result['lemmatized'][:100])
    print("💼 Skills:", result['skills'][:10])
    print("✅ Preprocessing works!")
