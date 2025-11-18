"""
Feedback Handler
Collects and manages user feedback on AI-generated content
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class FeedbackHandler:
    """Handles user feedback collection and management"""

    def __init__(self):
        """Initialize feedback handler"""
        self.feedback_store = {}
        self.feedback_counter = 0
        logger.info("Feedback Handler initialized")

    def submit_feedback(
        self,
        content_id: str,
        content_type: str,
        user_id: int,
        rating: int,
        comments: Optional[str] = None,
        specific_issues: Optional[List[str]] = None
    ) -> str:
        """
        Submit feedback on AI-generated content

        Args:
            content_id: ID of content being rated
            content_type: Type of content (analysis, document, strategy, etc.)
            user_id: ID of user providing feedback
            rating: Rating (1-5 scale)
            comments: Optional feedback comments
            specific_issues: Optional list of specific issues

        Returns:
            Feedback ID
        """
        self.feedback_counter += 1
        feedback_id = f"feedback_{self.feedback_counter}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        feedback = {
            'id': feedback_id,
            'content_id': content_id,
            'content_type': content_type,
            'user_id': user_id,
            'rating': rating,
            'comments': comments,
            'specific_issues': specific_issues or [],
            'submitted_at': datetime.now(),
            'addressed': False,
            'follow_up': None
        }

        self.feedback_store[feedback_id] = feedback
        logger.info(f"Feedback submitted: {feedback_id} (Rating: {rating}/5)")

        return feedback_id

    def get_feedback(self, feedback_id: str) -> Optional[Dict[str, Any]]:
        """
        Get specific feedback record

        Args:
            feedback_id: Feedback ID

        Returns:
            Feedback record or None
        """
        return self.feedback_store.get(feedback_id)

    def get_content_feedback(self, content_id: str) -> List[Dict[str, Any]]:
        """
        Get all feedback for specific content

        Args:
            content_id: Content ID

        Returns:
            List of feedback records
        """
        feedback_list = [
            f for f in self.feedback_store.values()
            if f['content_id'] == content_id
        ]

        return sorted(feedback_list, key=lambda x: x['submitted_at'], reverse=True)

    def get_user_feedback(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get all feedback from a user

        Args:
            user_id: User ID

        Returns:
            List of feedback records
        """
        feedback_list = [
            f for f in self.feedback_store.values()
            if f['user_id'] == user_id
        ]

        return sorted(feedback_list, key=lambda x: x['submitted_at'], reverse=True)

    def get_feedback_by_type(self, content_type: str) -> List[Dict[str, Any]]:
        """
        Get all feedback for content type

        Args:
            content_type: Content type

        Returns:
            List of feedback records
        """
        feedback_list = [
            f for f in self.feedback_store.values()
            if f['content_type'] == content_type
        ]

        return sorted(feedback_list, key=lambda x: x['submitted_at'], reverse=True)

    def get_low_rated_content(self, threshold: int = 3) -> List[Dict[str, Any]]:
        """
        Get content with low ratings

        Args:
            threshold: Rating threshold (content rated below this)

        Returns:
            List of feedback records with low ratings
        """
        low_rated = [
            f for f in self.feedback_store.values()
            if f['rating'] < threshold
        ]

        return sorted(low_rated, key=lambda x: x['rating'])

    def get_feedback_summary(self, content_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get summary statistics for feedback

        Args:
            content_type: Optional filter by content type

        Returns:
            Summary statistics
        """
        feedback_list = list(self.feedback_store.values())

        if content_type:
            feedback_list = [f for f in feedback_list if f['content_type'] == content_type]

        if not feedback_list:
            return {
                'total_feedback': 0,
                'average_rating': 0,
                'rating_distribution': {},
                'most_common_issues': []
            }

        ratings = [f['rating'] for f in feedback_list]
        rating_dist = {i: ratings.count(i) for i in range(1, 6)}

        # Count issues
        all_issues = []
        for f in feedback_list:
            all_issues.extend(f.get('specific_issues', []))

        issue_counts = {}
        for issue in all_issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1

        most_common = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        summary = {
            'total_feedback': len(feedback_list),
            'average_rating': sum(ratings) / len(ratings),
            'rating_distribution': rating_dist,
            'most_common_issues': most_common,
            'percentage_positive': (len([r for r in ratings if r >= 4]) / len(ratings) * 100) if ratings else 0
        }

        return summary

    def mark_addressed(self, feedback_id: str, follow_up: str) -> bool:
        """
        Mark feedback as addressed

        Args:
            feedback_id: Feedback ID
            follow_up: Follow-up notes

        Returns:
            Success status
        """
        if feedback_id not in self.feedback_store:
            return False

        self.feedback_store[feedback_id]['addressed'] = True
        self.feedback_store[feedback_id]['follow_up'] = follow_up
        self.feedback_store[feedback_id]['addressed_at'] = datetime.now()

        logger.info(f"Feedback marked as addressed: {feedback_id}")
        return True

    def identify_improvement_areas(self) -> Dict[str, List[str]]:
        """
        Identify areas needing improvement based on feedback

        Returns:
            Dictionary of content types and their improvement areas
        """
        improvement_areas = {}

        for content_type in set(f['content_type'] for f in self.feedback_store.values()):
            type_feedback = self.get_feedback_by_type(content_type)
            low_rated = [f for f in type_feedback if f['rating'] <= 2]

            if low_rated:
                issues = []
                for f in low_rated:
                    issues.extend(f.get('specific_issues', []))
                    if f.get('comments'):
                        issues.append(f['comments'])

                improvement_areas[content_type] = list(set(issues))[:5]

        return improvement_areas


# Global feedback handler instance
feedback_handler = FeedbackHandler()
