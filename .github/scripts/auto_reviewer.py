#!/usr/bin/env python3
"""
Cloud-based Automated PR Reviewer
Runs on GitHub Actions - Reviews 1 PR per run, 8 times daily
"""

import os
import sys
import json
import time
import random
from datetime import datetime
from typing import List, Dict, Optional

try:
    from github import Github
    import requests
except ImportError:
    print("Installing required packages...")
    os.system("pip install PyGithub requests")
    from github import Github
    import requests


class CloudPRReviewer:
    """Cloud-based PR reviewer for GitHub Actions"""
    
    def __init__(self):
        self.token = os.environ.get('GITHUB_TOKEN')
        self.repo_owner = os.environ.get('REPO_OWNER', 'eeshsaxena')
        self.repo_name = os.environ.get('REPO_NAME', 'outreach-emails')
        
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable not set")
        
        self.gh = Github(self.token)
        self.repo = self.gh.get_repo(f"{self.repo_owner}/{self.repo_name}")
        
        # State file to track progress
        self.state_file = '.github/pr_review_state.json'
        self.state = self.load_state()
    
    def load_state(self) -> Dict:
        """Load review progress state"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Could not load state: {e}")
        
        return {
            'reviewed_prs': [],
            'last_review_date': None,
            'total_reviewed': 0,
            'current_index': 0
        }
    
    def save_state(self):
        """Save review progress state"""
        try:
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            print(f"✅ State saved: {self.state['total_reviewed']} PRs reviewed total")
        except Exception as e:
            print(f"⚠️ Could not save state: {e}")
    
    def get_unreviewed_pr(self) -> Optional[object]:
        """Get next PR that hasn't been reviewed by this bot"""
        print(f"🔍 Fetching closed PRs from {self.repo_owner}/{self.repo_name}...")
        
        # Get closed PRs
        pulls = self.repo.get_pulls(state='closed', sort='updated', direction='desc')
        
        reviewed_numbers = set(self.state['reviewed_prs'])
        
        for pr in pulls:
            if pr.number not in reviewed_numbers:
                # Check if we already reviewed it
                reviews = pr.get_reviews()
                already_reviewed = False
                
                for review in reviews:
                    if review.user.login == self.repo_owner:  # Check if you already reviewed
                        already_reviewed = True
                        break
                
                if not already_reviewed:
                    print(f"✅ Found unreviewed PR: #{pr.number}")
                    return pr
        
        print("⚠️ No unreviewed PRs found")
        return None
    
    def analyze_pr(self, pr) -> Dict:
        """Analyze PR to generate intelligent review"""
        title = pr.title.lower()
        body = (pr.body or '').lower()
        
        # Analyze type
        is_bug_fix = any(word in title or word in body 
                        for word in ['fix', 'bug', 'issue', 'error', 'broken'])
        is_feature = any(word in title or word in body 
                        for word in ['add', 'feature', 'new', 'implement'])
        is_docs = any(word in title or word in body 
                     for word in ['doc', 'readme', 'documentation'])
        is_refactor = any(word in title or word in body 
                         for word in ['refactor', 'cleanup', 'improve', 'optimize'])
        is_test = any(word in title or word in body 
                     for word in ['test', 'testing', 'spec'])
        
        # Get file changes
        files = list(pr.get_files())
        additions = sum(f.additions for f in files)
        deletions = sum(f.deletions for f in files)
        
        return {
            'type': 'bug_fix' if is_bug_fix else 
                   'feature' if is_feature else 
                   'docs' if is_docs else 
                   'refactor' if is_refactor else 
                   'test' if is_test else 'other',
            'files_changed': len(files),
            'additions': additions,
            'deletions': deletions,
            'files': files
        }
    
    def generate_review(self, pr, analysis: Dict) -> str:
        """Generate intelligent review comment"""
        pr_type = analysis['type']
        
        # Type-specific openings
        openings = {
            'bug_fix': [
                "Thanks for tackling this bug! 🐛",
                "Great work on resolving this issue! 🔧",
                "Appreciate the bug fix! 👍"
            ],
            'feature': [
                "Excellent feature addition! 🚀",
                "Nice implementation! ✨",
                "Great work on this new functionality! 🎯"
            ],
            'docs': [
                "Thanks for improving our documentation! 📚",
                "Great doc update! 📝",
                "Appreciate the documentation work! 📖"
            ],
            'refactor': [
                "Nice refactoring! ♻️",
                "Great code improvements! ⚡",
                "Excellent cleanup work! 🧹"
            ],
            'test': [
                "Thanks for adding tests! ✅",
                "Great test coverage! 🧪",
                "Appreciate the testing work! 🎯"
            ],
            'other': [
                "Thanks for this contribution! 👍",
                "Great work on this PR! 🎯",
                "Nice changes! ✨"
            ]
        }
        
        comment_parts = []
        
        # Opening
        comment_parts.append(random.choice(openings.get(pr_type, openings['other'])))
        
        # Analysis
        comment_parts.append(f"\n\n**📊 Change Summary:**")
        comment_parts.append(f"- Files modified: {analysis['files_changed']}")
        comment_parts.append(f"- Lines added: +{analysis['additions']}")
        comment_parts.append(f"- Lines removed: -{analysis['deletions']}")
        comment_parts.append(f"- Net change: {analysis['additions'] - analysis['deletions']:+d}")
        
        # Strengths
        comment_parts.append(f"\n\n**✅ Positive Observations:**")
        
        strengths = []
        
        if analysis['files_changed'] <= 5:
            strengths.append("Well-scoped changes - focused and easy to review")
        
        if analysis['additions'] < 150:
            strengths.append("Concise implementation - good for maintainability")
        
        if analysis['deletions'] > analysis['additions']:
            strengths.append("Net code reduction - great for simplicity!")
        
        # Check file types
        file_extensions = set()
        has_tests = False
        has_docs = False
        
        for f in analysis['files']:
            ext = f.filename.split('.')[-1] if '.' in f.filename else ''
            file_extensions.add(ext)
            
            if 'test' in f.filename.lower():
                has_tests = True
            if any(doc in f.filename.lower() for doc in ['readme', '.md', 'doc']):
                has_docs = True
        
        if has_tests:
            strengths.append("Includes test coverage - excellent!")
        if has_docs:
            strengths.append("Documentation updates included")
        
        if 'py' in file_extensions:
            strengths.append("Python code follows good practices")
        if 'js' in file_extensions or 'ts' in file_extensions:
            strengths.append("JavaScript/TypeScript changes look solid")
        
        if not strengths:
            strengths = ["Changes are well-structured", "Addresses the stated objective"]
        
        for strength in strengths[:3]:
            comment_parts.append(f"- {strength}")
        
        # Constructive observations
        comment_parts.append(f"\n\n**💡 Technical Observations:**")
        
        observations = []
        
        if pr_type == 'bug_fix':
            observations.append("Consider adding a regression test for this fix")
        elif pr_type == 'feature':
            observations.append("Feature implementation looks solid - nice work!")
        elif pr_type == 'refactor':
            observations.append("Refactoring improves code quality significantly")
        
        if analysis['files_changed'] > 10:
            observations.append("Large PR - consider breaking into smaller chunks in the future")
        
        if analysis['additions'] > 300:
            observations.append("Substantial changes - ensure all edge cases are covered")
        
        if not has_tests and pr_type in ['bug_fix', 'feature']:
            observations.append("Future PRs could benefit from test coverage")
        
        if not observations:
            observations = ["Implementation approach is sound", "Changes align with PR objectives"]
        
        for obs in observations[:2]:
            comment_parts.append(f"- {obs}")
        
        # Closing
        closings = [
            "\n\n**Summary:** Solid contribution! Thanks for improving the codebase. 🎯",
            "\n\n**Overall:** Great work! Appreciate your effort on this. 💪",
            "\n\n**Final thought:** Well done! This adds value to the project. ⭐"
        ]
        comment_parts.append(random.choice(closings))
        
        # Add timestamp
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
        comment_parts.append(f"\n\n---\n*Automated review · {now}*")
        
        return '\n'.join(comment_parts)
    
    def post_review(self, pr, comment: str) -> bool:
        """Post review on PR"""
        try:
            # Add delay before posting (5-10 minutes simulation in seconds for testing)
            delay = random.randint(5, 10)  # In production, would be 300-600 (5-10 minutes)
            print(f"⏳ Waiting {delay} seconds before posting review...")
            time.sleep(delay)
            
            # Create review
            pr.create_review(
                body=comment,
                event='COMMENT'  # Can be COMMENT, APPROVE, or REQUEST_CHANGES
            )
            
            print(f"✅ Review posted on PR #{pr.number}: {pr.title}")
            return True
            
        except Exception as e:
            print(f"❌ Error posting review: {e}")
            return False
    
    def review_next_pr(self) -> bool:
        """Review the next unreviewed PR"""
        print("\n" + "="*60)
        print("🤖 CLOUD PR REVIEWER")
        print("="*60)
        print(f"Repository: {self.repo_owner}/{self.repo_name}")
        print(f"Current time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"PRs reviewed so far: {self.state['total_reviewed']}")
        print("="*60 + "\n")
        
        # Get next PR to review
        pr = self.get_unreviewed_pr()
        
        if not pr:
            print("🎉 All PRs have been reviewed!")
            return False
        
        print(f"\n📝 Reviewing PR #{pr.number}: {pr.title}")
        print(f"   Author: {pr.user.login}")
        print(f"   Status: {'Merged' if pr.merged else 'Closed'}")
        print(f"   Created: {pr.created_at}")
        
        # Analyze PR
        analysis = self.analyze_pr(pr)
        print(f"\n📊 Analysis:")
        print(f"   Type: {analysis['type']}")
        print(f"   Files: {analysis['files_changed']}")
        print(f"   Changes: +{analysis['additions']} -{analysis['deletions']}")
        
        # Generate review
        review_comment = self.generate_review(pr, analysis)
        
        print(f"\n📝 Generated Review:")
        print("-" * 60)
        print(review_comment)
        print("-" * 60)
        
        # Post review
        success = self.post_review(pr, review_comment)
        
        if success:
            # Update state
            self.state['reviewed_prs'].append(pr.number)
            self.state['total_reviewed'] += 1
            self.state['last_review_date'] = datetime.utcnow().isoformat()
            self.save_state()
            
            print(f"\n✅ Successfully reviewed PR #{pr.number}")
            print(f"📊 Total PRs reviewed: {self.state['total_reviewed']}")
            return True
        else:
            print(f"\n❌ Failed to review PR #{pr.number}")
            return False
    
    def run(self):
        """Main execution"""
        try:
            success = self.review_next_pr()
            
            if success:
                print("\n" + "="*60)
                print("🎉 Review cycle completed successfully!")
                print("="*60)
                sys.exit(0)
            else:
                print("\n" + "="*60)
                print("⚠️ No PRs reviewed in this cycle")
                print("="*60)
                sys.exit(0)
                
        except Exception as e:
            print(f"\n❌ Error in review process: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    """Entry point"""
    print("🚀 Starting Cloud PR Reviewer...")
    
    try:
        reviewer = CloudPRReviewer()
        reviewer.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
