"""
Scoring Engine Module
Calculate similarity between resume and JD using TF-IDF + Cosine Similarity
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple
import re


class ResumeScorer:
    """Score and match resumes against job descriptions"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 2),  # Unigrams and bigrams
            min_df=1,
            stop_words='english'
        )
    
    def calculate_cosine_similarity(self, resume_text: str, jd_text: str) -> float:
        """
        Calculate cosine similarity between resume and JD
        
        Args:
            resume_text: Processed resume text
            jd_text: Processed job description text
            
        Returns:
            Similarity score (0-100)
        """
        try:
            # Create TF-IDF vectors
            documents = [jd_text, resume_text]
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Convert to percentage
            return round(similarity * 100, 2)
        
        except Exception as e:
            print(f"⚠️  Similarity calculation error: {e}")
            return 0.0
    
    def calculate_keyword_match(self, resume_skills: List[str], 
                                jd_skills: Dict[str, List[str]]) -> Dict[str, any]:
        """
        Calculate keyword/skill matching score
        
        Args:
            resume_skills: Skills extracted from resume
            jd_skills: Skills extracted from JD (categorized)
            
        Returns:
            Dict with match statistics
        """
        # Flatten JD skills
        all_jd_skills = []
        for category, skills in jd_skills.items():
            all_jd_skills.extend(skills)
        
        if not all_jd_skills:
            return {
                'match_score': 0,
                'matched_skills': [],
                'missing_skills': [],
                'match_percentage': 0
            }
        
        # Convert to lowercase sets for comparison
        resume_skills_set = set(skill.lower() for skill in resume_skills)
        jd_skills_set = set(skill.lower() for skill in all_jd_skills)
        
        # Find matches and misses
        matched_skills = list(resume_skills_set.intersection(jd_skills_set))
        missing_skills = list(jd_skills_set - resume_skills_set)
        
        # Calculate percentage
        match_percentage = (len(matched_skills) / len(jd_skills_set) * 100) if jd_skills_set else 0
        
        return {
            'match_score': round(match_percentage, 2),
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'total_jd_skills': len(jd_skills_set),
            'matched_count': len(matched_skills),
            'missing_count': len(missing_skills)
        }
    
    def calculate_experience_match(self, resume_text: str, required_level: str) -> Dict[str, any]:
        """
        Match experience level mentioned in resume with JD requirement
        
        Args:
            resume_text: Resume text
            required_level: Required experience level from JD
            
        Returns:
            Dict with experience match details
        """
        resume_lower = resume_text.lower()
        
        # Extract years of experience from resume
        year_patterns = [
            r'(\d+)[\s-]*(?:\+)?\s*(?:years?|yrs?)\s+(?:of\s+)?experience',
            r'experience[:\s]+(\d+)[\s-]*(?:\+)?\s*(?:years?|yrs?)',
        ]
        
        years_found = []
        for pattern in year_patterns:
            matches = re.findall(pattern, resume_lower)
            years_found.extend([int(m) for m in matches])
        
        max_years = max(years_found) if years_found else 0
        
        # Determine resume experience level
        if max_years <= 2:
            resume_level = 'entry'
        elif max_years <= 5:
            resume_level = 'mid'
        else:
            resume_level = 'senior'
        
        # Calculate match
        level_scores = {
            'entry': 1,
            'mid': 2,
            'senior': 3,
            'unknown': 0
        }
        
        required_score = level_scores.get(required_level, 0)
        resume_score = level_scores.get(resume_level, 0)
        
        # Score logic: 
        # - Exact match = 100
        # - Over-qualified = 80
        # - Under-qualified = score based on gap
        if required_score == 0:
            match_score = 100  # Unknown requirement, give benefit of doubt
        elif resume_score == required_score:
            match_score = 100
        elif resume_score > required_score:
            match_score = 80  # Over-qualified
        else:
            # Under-qualified: reduce score based on gap
            gap = required_score - resume_score
            match_score = max(0, 100 - (gap * 30))
        
        return {
            'experience_match_score': match_score,
            'resume_experience_years': max_years,
            'resume_experience_level': resume_level,
            'required_level': required_level,
            'is_match': match_score >= 70
        }
    
    def calculate_education_match(self, resume_education: List[str], 
                                   jd_qualifications: List[str]) -> Dict[str, any]:
        """
        Match education qualifications
        
        Args:
            resume_education: Education info from resume
            jd_qualifications: Required qualifications from JD
            
        Returns:
            Dict with education match details
        """
        if not jd_qualifications:
            return {
                'education_match_score': 100,
                'is_match': True,
                'notes': 'No specific education requirement in JD'
            }
        
        # Convert to lowercase for comparison
        resume_edu_text = ' '.join(resume_education).lower()
        jd_qual_text = ' '.join(jd_qualifications).lower()
        
        # Common degree keywords
        degree_keywords = {
            'bachelor': ['bachelor', 'b.tech', 'b.e.', 'bsc', 'bca', 'ba', 'bcom'],
            'master': ['master', 'm.tech', 'm.e.', 'msc', 'mca', 'mba', 'ma', 'mcom'],
            'phd': ['phd', 'doctorate', 'ph.d']
        }
        
        # Find required degree level
        required_level = 'bachelor'  # Default
        for level, keywords in degree_keywords.items():
            if any(keyword in jd_qual_text for keyword in keywords):
                required_level = level
                break
        
        # Check if resume has required level
        has_required = False
        for keyword in degree_keywords.get(required_level, []):
            if keyword in resume_edu_text:
                has_required = True
                break
        
        # Check for higher qualifications
        if required_level == 'bachelor':
            for level in ['master', 'phd']:
                for keyword in degree_keywords.get(level, []):
                    if keyword in resume_edu_text:
                        has_required = True
                        break
        
        match_score = 100 if has_required else 50
        
        return {
            'education_match_score': match_score,
            'required_level': required_level,
            'is_match': has_required,
            'notes': 'Education requirement met' if has_required else f'{required_level.title()} degree may be required'
        }
    
    def calculate_overall_score(self, resume_data: Dict, jd_data: Dict) -> Dict[str, any]:
        """
        Calculate comprehensive ATS score
        
        Args:
            resume_data: Parsed and processed resume data
            jd_data: Parsed and processed JD data
            
        Returns:
            Dict with complete scoring breakdown
        """
        # 1. Cosine Similarity (40% weight)
        cosine_score = self.calculate_cosine_similarity(
            resume_data.get('processed_text', ''),
            jd_data.get('processed_text', '')
        )
        
        # 2. Keyword Match (30% weight)
        keyword_match = self.calculate_keyword_match(
            resume_data.get('skills', []),
            jd_data.get('skills', {})
        )
        
        # 3. Experience Match (20% weight)
        experience_match = self.calculate_experience_match(
            resume_data.get('text', ''),
            jd_data.get('experience_level', 'unknown')
        )
        
        # 4. Education Match (10% weight)
        education_match = self.calculate_education_match(
            resume_data.get('education', []),
            jd_data.get('qualifications', [])
        )
        
        # Calculate weighted overall score
        overall_score = (
            cosine_score * 0.40 +
            keyword_match['match_score'] * 0.30 +
            experience_match['experience_match_score'] * 0.20 +
            education_match['education_match_score'] * 0.10
        )
        
        # Determine recommendation
        if overall_score >= 75:
            recommendation = 'Strong Match - Interview'
            status = 'selected'
        elif overall_score >= 60:
            recommendation = 'Potential Match - Review'
            status = 'review'
        else:
            recommendation = 'Not a Strong Match'
            status = 'rejected'
        
        return {
            'overall_score': round(overall_score, 2),
            'recommendation': recommendation,
            'status': status,
            'breakdown': {
                'cosine_similarity': cosine_score,
                'keyword_match': keyword_match,
                'experience_match': experience_match,
                'education_match': education_match
            }
        }


if __name__ == "__main__":
    # Test the scorer
    scorer = ResumeScorer()
    
    sample_resume = "python developer with 3 years experience django flask aws docker"
    sample_jd = "looking for python developer with django experience and aws knowledge"
    
    score = scorer.calculate_cosine_similarity(sample_resume, sample_jd)
    print(f"✅ Scorer works! Similarity: {score}%")
