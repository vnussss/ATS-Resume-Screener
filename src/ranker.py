"""
Ranker Module
Rank multiple resumes and generate explanations
"""

import pandas as pd
from typing import List, Dict
from datetime import datetime


class ResumeRanker:
    """Rank and explain resume selections"""
    
    def __init__(self):
        self.ranking_criteria = {
            'overall_score': 0.5,
            'keyword_match': 0.3,
            'experience_match': 0.2
        }
    
    def rank_resumes(self, scored_resumes: List[Dict]) -> List[Dict]:
        """
        Rank resumes by overall score
        
        Args:
            scored_resumes: List of resume dicts with scores
            
        Returns:
            Sorted list of resumes with ranks
        """
        # Sort by overall score (descending)
        sorted_resumes = sorted(
            scored_resumes,
            key=lambda x: x.get('overall_score', 0),
            reverse=True
        )
        
        # Add rank numbers
        for idx, resume in enumerate(sorted_resumes, 1):
            resume['rank'] = idx
        
        return sorted_resumes
    
    def generate_explanation(self, resume_data: Dict, score_data: Dict) -> str:
        """
        Generate human-readable explanation for resume decision
        
        Args:
            resume_data: Resume information
            score_data: Scoring breakdown
            
        Returns:
            Explanation text
        """
        candidate_name = resume_data.get('file_name', 'Candidate')
        overall_score = score_data.get('overall_score', 0)
        status = score_data.get('status', 'unknown')
        breakdown = score_data.get('breakdown', {})
        
        # Start explanation
        explanation_parts = []
        
        # Overall verdict
        if status == 'selected':
            explanation_parts.append(
                f"✅ **{candidate_name}** is a **Strong Match** (Score: {overall_score}/100)"
            )
        elif status == 'review':
            explanation_parts.append(
                f"⚠️  **{candidate_name}** is a **Potential Match** (Score: {overall_score}/100) - Needs Manual Review"
            )
        else:
            explanation_parts.append(
                f"❌ **{candidate_name}** is **Not a Strong Match** (Score: {overall_score}/100)"
            )
        
        explanation_parts.append("\n**Why?**\n")
        
        # Cosine similarity analysis
        cosine = breakdown.get('cosine_similarity', 0)
        if cosine >= 70:
            explanation_parts.append(f"• 🎯 **Strong content alignment** ({cosine}% similarity with JD)")
        elif cosine >= 50:
            explanation_parts.append(f"• 📊 **Moderate content alignment** ({cosine}% similarity with JD)")
        else:
            explanation_parts.append(f"• ⚠️  **Limited content alignment** ({cosine}% similarity with JD)")
        
        # Keyword match analysis
        keyword_data = breakdown.get('keyword_match', {})
        match_score = keyword_data.get('match_score', 0)
        matched_count = keyword_data.get('matched_count', 0)
        missing_count = keyword_data.get('missing_count', 0)
        matched_skills = keyword_data.get('matched_skills', [])
        missing_skills = keyword_data.get('missing_skills', [])
        
        if match_score >= 70:
            explanation_parts.append(
                f"• 💼 **Strong skill match** ({matched_count} out of {matched_count + missing_count} key skills found)"
            )
        elif match_score >= 40:
            explanation_parts.append(
                f"• 📝 **Partial skill match** ({matched_count} out of {matched_count + missing_count} key skills found)"
            )
        else:
            explanation_parts.append(
                f"• ⚠️  **Limited skill match** ({matched_count} out of {matched_count + missing_count} key skills found)"
            )
        
        # Show matched skills
        if matched_skills:
            top_matched = matched_skills[:8]  # Show top 8
            explanation_parts.append(f"  - ✅ Found: {', '.join(top_matched)}")
        
        # Show missing skills
        if missing_skills and status != 'selected':
            top_missing = missing_skills[:8]  # Show top 8
            explanation_parts.append(f"  - ❌ Missing: {', '.join(top_missing)}")
        
        # Experience analysis
        exp_data = breakdown.get('experience_match', {})
        exp_score = exp_data.get('experience_match_score', 0)
        resume_years = exp_data.get('resume_experience_years', 0)
        required_level = exp_data.get('required_level', 'unknown')
        
        if exp_score >= 90:
            explanation_parts.append(
                f"• 👔 **Experience requirement met** ({resume_years} years, {required_level} level)"
            )
        elif exp_score >= 70:
            explanation_parts.append(
                f"• 📈 **Close experience match** ({resume_years} years, {required_level} level required)"
            )
        else:
            explanation_parts.append(
                f"• ⚠️  **Experience gap** ({resume_years} years found, {required_level} level required)"
            )
        
        # Education analysis
        edu_data = breakdown.get('education_match', {})
        edu_score = edu_data.get('education_match_score', 0)
        edu_notes = edu_data.get('notes', '')
        
        if edu_score >= 80:
            explanation_parts.append(f"• 🎓 **Education requirement met** ({edu_notes})")
        else:
            explanation_parts.append(f"• 📚 **Education review needed** ({edu_notes})")
        
        # Final recommendation
        explanation_parts.append(f"\n**Recommendation:** {score_data.get('recommendation', 'Review required')}")
        
        return '\n'.join(explanation_parts)
    
    def generate_summary_report(self, ranked_resumes: List[Dict]) -> str:
        """
        Generate summary report for all candidates
        
        Args:
            ranked_resumes: List of ranked resumes with scores
            
        Returns:
            Summary report text
        """
        total_candidates = len(ranked_resumes)
        selected = sum(1 for r in ranked_resumes if r.get('status') == 'selected')
        review = sum(1 for r in ranked_resumes if r.get('status') == 'review')
        rejected = sum(1 for r in ranked_resumes if r.get('status') == 'rejected')
        
        avg_score = sum(r.get('overall_score', 0) for r in ranked_resumes) / total_candidates if total_candidates > 0 else 0
        
        report_parts = [
            "# 📊 ATS Screening Report\n",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"**Total Candidates Screened:** {total_candidates}",
            f"**Average Score:** {avg_score:.2f}/100\n",
            "## 📈 Screening Results\n",
            f"• ✅ **Strong Matches (Interview):** {selected}",
            f"• ⚠️  **Potential Matches (Review):** {review}",
            f"• ❌ **Not Strong Matches:** {rejected}\n",
            "## 🏆 Top Candidates\n"
        ]
        
        # Show top 5 candidates
        top_candidates = ranked_resumes[:5]
        for candidate in top_candidates:
            name = candidate.get('file_name', 'Unknown')
            score = candidate.get('overall_score', 0)
            rank = candidate.get('rank', '-')
            status_emoji = {
                'selected': '✅',
                'review': '⚠️',
                'rejected': '❌'
            }.get(candidate.get('status'), '•')
            
            report_parts.append(f"{rank}. {status_emoji} **{name}** - {score:.1f}/100")
        
        return '\n'.join(report_parts)
    
    def export_to_csv(self, ranked_resumes: List[Dict], output_path: str) -> bool:
        """
        Export results to CSV
        
        Args:
            ranked_resumes: List of ranked resumes
            output_path: Path to save CSV
            
        Returns:
            Success status
        """
        try:
            # Prepare data for DataFrame
            export_data = []
            
            for resume in ranked_resumes:
                breakdown = resume.get('breakdown', {})
                keyword_data = breakdown.get('keyword_match', {})
                exp_data = breakdown.get('experience_match', {})
                
                export_data.append({
                    'Rank': resume.get('rank', '-'),
                    'Candidate': resume.get('file_name', 'Unknown'),
                    'Overall Score': resume.get('overall_score', 0),
                    'Status': resume.get('status', 'unknown'),
                    'Recommendation': resume.get('recommendation', ''),
                    'Similarity Score': breakdown.get('cosine_similarity', 0),
                    'Keyword Match': keyword_data.get('match_score', 0),
                    'Skills Matched': keyword_data.get('matched_count', 0),
                    'Skills Missing': keyword_data.get('missing_count', 0),
                    'Experience Score': exp_data.get('experience_match_score', 0),
                    'Experience (Years)': exp_data.get('resume_experience_years', 0)
                })
            
            # Create DataFrame and export
            df = pd.DataFrame(export_data)
            df.to_csv(output_path, index=False)
            
            return True
        
        except Exception as e:
            print(f"❌ CSV export failed: {e}")
            return False


if __name__ == "__main__":
    # Test the ranker
    ranker = ResumeRanker()
    print("✅ Ranker initialized!")
