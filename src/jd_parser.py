"""
Job Description Parser Module
Extracts requirements and key information from JD
"""

import re
from typing import Dict, List, Set
from pathlib import Path


class JDParser:
    """Parse and analyze Job Descriptions"""
    
    def __init__(self):
        # Common technical skills database
        self.tech_skills = {
            'languages': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 
                         'rust', 'php', 'ruby', 'swift', 'kotlin', 'scala', 'r', 'matlab'],
            'frameworks': ['react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'spring',
                          'node', 'express', 'nextjs', 'nuxt', 'svelte', 'laravel', 'rails'],
            'databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
                         'dynamodb', 'cassandra', 'oracle', 'sqlite'],
            'cloud': ['aws', 'azure', 'gcp', 'cloud', 'ec2', 's3', 'lambda', 'cloudformation',
                     'terraform', 'ansible'],
            'tools': ['git', 'docker', 'kubernetes', 'jenkins', 'jira', 'confluence',
                     'gitlab', 'circleci', 'travis', 'github actions'],
            'concepts': ['api', 'rest', 'graphql', 'microservices', 'ci/cd', 'devops',
                        'agile', 'scrum', 'tdd', 'machine learning', 'ai', 'data science']
        }
        
        # Experience level indicators
        self.experience_patterns = {
            'entry': ['entry', 'junior', '0-1 year', '0-2 year', 'fresher', 'graduate'],
            'mid': ['mid-level', '2-5 year', '3-6 year', 'intermediate'],
            'senior': ['senior', 'lead', '5+ year', '7+ year', 'expert', 'principal']
        }
    
    def parse_file(self, file_path: str) -> str:
        """
        Read JD from text file
        
        Args:
            file_path: Path to JD text file
            
        Returns:
            Job description text
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ Error reading JD file: {e}")
            return ""
    
    def extract_requirements(self, jd_text: str) -> Dict[str, List[str]]:
        """
        Extract specific requirements from JD
        
        Args:
            jd_text: Job description text
            
        Returns:
            Dict with categorized requirements
        """
        jd_lower = jd_text.lower()
        requirements = {
            'must_have': [],
            'nice_to_have': [],
            'responsibilities': []
        }
        
        # Find "Required" or "Must have" sections
        must_have_pattern = r'(?:required|must have|mandatory|essential)[\s:]+([^\n]+(?:\n(?!required|nice|responsibilities)[^\n]+)*)'
        must_matches = re.findall(must_have_pattern, jd_lower, re.IGNORECASE)
        requirements['must_have'] = [m.strip() for m in must_matches if m.strip()]
        
        # Find "Nice to have" or "Preferred" sections
        nice_pattern = r'(?:nice to have|preferred|bonus|plus)[\s:]+([^\n]+(?:\n(?!required|nice|responsibilities)[^\n]+)*)'
        nice_matches = re.findall(nice_pattern, jd_lower, re.IGNORECASE)
        requirements['nice_to_have'] = [m.strip() for m in nice_matches if m.strip()]
        
        # Find "Responsibilities" section
        resp_pattern = r'(?:responsibilities|duties|role)[\s:]+([^\n]+(?:\n(?!required|nice|qualifications)[^\n]+)*)'
        resp_matches = re.findall(resp_pattern, jd_lower, re.IGNORECASE)
        requirements['responsibilities'] = [m.strip() for m in resp_matches if m.strip()]
        
        return requirements
    
    def extract_skills(self, jd_text: str) -> Dict[str, Set[str]]:
        """
        Extract technical skills mentioned in JD
        
        Args:
            jd_text: Job description text
            
        Returns:
            Dict with categorized skills found in JD
        """
        jd_lower = jd_text.lower()
        found_skills = {category: set() for category in self.tech_skills.keys()}
        
        for category, skills in self.tech_skills.items():
            for skill in skills:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, jd_lower):
                    found_skills[category].add(skill)
        
        return found_skills
    
    def detect_experience_level(self, jd_text: str) -> str:
        """
        Detect required experience level
        
        Args:
            jd_text: Job description text
            
        Returns:
            Experience level: 'entry', 'mid', 'senior', or 'unknown'
        """
        jd_lower = jd_text.lower()
        
        for level, patterns in self.experience_patterns.items():
            for pattern in patterns:
                if pattern in jd_lower:
                    return level
        
        # Check for year patterns
        year_match = re.search(r'(\d+)[\s-]*(?:\+)?\s*(?:year|yr)', jd_lower)
        if year_match:
            years = int(year_match.group(1))
            if years <= 2:
                return 'entry'
            elif years <= 5:
                return 'mid'
            else:
                return 'senior'
        
        return 'unknown'
    
    def extract_qualifications(self, jd_text: str) -> List[str]:
        """
        Extract education and certification requirements
        
        Args:
            jd_text: Job description text
            
        Returns:
            List of qualification requirements
        """
        qualifications = []
        jd_lower = jd_text.lower()
        
        # Education patterns
        education_keywords = [
            'bachelor', 'master', 'phd', 'degree', 'diploma',
            'b.tech', 'm.tech', 'bsc', 'msc', 'mba', 'bca', 'mca'
        ]
        
        for keyword in education_keywords:
            if keyword in jd_lower:
                # Extract context
                pattern = rf'.{{0,50}}{keyword}.{{0,50}}'
                matches = re.findall(pattern, jd_lower)
                qualifications.extend(matches)
        
        # Certification patterns
        cert_keywords = ['certified', 'certification', 'certificate', 'license']
        for keyword in cert_keywords:
            if keyword in jd_lower:
                pattern = rf'.{{0,50}}{keyword}.{{0,50}}'
                matches = re.findall(pattern, jd_lower)
                qualifications.extend(matches)
        
        return list(set(qualifications))
    
    def parse(self, jd_text: str) -> Dict[str, any]:
        """
        Main parsing method - comprehensive JD analysis
        
        Args:
            jd_text: Job description text (or file path)
            
        Returns:
            Dict with complete JD analysis
        """
        # Check if input is a file path
        if Path(jd_text).exists():
            jd_text = self.parse_file(jd_text)
        
        if not jd_text.strip():
            return {
                'success': False,
                'error': 'Empty job description',
                'text': '',
                'skills': {},
                'requirements': {},
                'experience_level': 'unknown',
                'qualifications': []
            }
        
        # Extract all information
        skills = self.extract_skills(jd_text)
        requirements = self.extract_requirements(jd_text)
        experience_level = self.detect_experience_level(jd_text)
        qualifications = self.extract_qualifications(jd_text)
        
        # Count total skills
        total_skills = sum(len(skills_set) for skills_set in skills.values())
        
        return {
            'success': True,
            'text': jd_text,
            'skills': {k: list(v) for k, v in skills.items()},  # Convert sets to lists
            'total_skills_count': total_skills,
            'requirements': requirements,
            'experience_level': experience_level,
            'qualifications': qualifications,
            'word_count': len(jd_text.split())
        }


if __name__ == "__main__":
    # Test the parser
    jd_parser = JDParser()
    
    sample_jd = """
    Software Engineer - Python
    
    Required Skills:
    - 3+ years of Python development experience
    - Strong knowledge of Django or Flask
    - Experience with PostgreSQL and MongoDB
    - AWS cloud services
    
    Nice to have:
    - Docker and Kubernetes experience
    - CI/CD pipeline knowledge
    
    Qualifications:
    - Bachelor's degree in Computer Science or related field
    """
    
    result = jd_parser.parse(sample_jd)
    print("✅ JD Parser works!")
    print(f"📊 Found {result['total_skills_count']} skills")
    print(f"👔 Experience level: {result['experience_level']}")
