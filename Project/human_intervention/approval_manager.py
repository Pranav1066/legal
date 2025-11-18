"""
Approval Manager
Handles human approval workflows for critical legal decisions
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ApprovalManager:
    """Manages approval workflows for AI-generated content"""

    def __init__(self):
        """Initialize approval manager"""
        self.pending_approvals = {}
        logger.info("Approval Manager initialized")

    def request_approval(
        self,
        approval_type: str,
        content: str,
        metadata: Dict[str, Any],
        requester_id: int
    ) -> str:
        """
        Request approval for AI-generated content

        Args:
            approval_type: Type of approval (document, strategy, analysis, etc.)
            content: Content requiring approval
            metadata: Additional metadata
            requester_id: ID of requester

        Returns:
            Approval request ID
        """
        approval_id = f"{approval_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{requester_id}"

        approval_request = {
            'id': approval_id,
            'type': approval_type,
            'content': content,
            'metadata': metadata,
            'requester_id': requester_id,
            'status': 'pending',
            'created_at': datetime.now(),
            'approved_by': None,
            'approved_at': None,
            'comments': None
        }

        self.pending_approvals[approval_id] = approval_request
        logger.info(f"Approval requested: {approval_id}")

        return approval_id

    def approve(
        self,
        approval_id: str,
        approver_id: int,
        comments: Optional[str] = None,
        modifications: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Approve a request

        Args:
            approval_id: Approval request ID
            approver_id: ID of approver
            comments: Optional approval comments
            modifications: Optional modifications to content

        Returns:
            Updated approval record
        """
        if approval_id not in self.pending_approvals:
            raise ValueError(f"Approval request {approval_id} not found")

        approval = self.pending_approvals[approval_id]
        approval['status'] = 'approved'
        approval['approved_by'] = approver_id
        approval['approved_at'] = datetime.now()
        approval['comments'] = comments

        if modifications:
            approval['modified_content'] = modifications
            approval['content_modified'] = True
        else:
            approval['content_modified'] = False

        logger.info(f"Approval granted: {approval_id} by user {approver_id}")

        return approval

    def reject(
        self,
        approval_id: str,
        approver_id: int,
        reason: str
    ) -> Dict[str, Any]:
        """
        Reject a request

        Args:
            approval_id: Approval request ID
            approver_id: ID of approver
            reason: Rejection reason

        Returns:
            Updated approval record
        """
        if approval_id not in self.pending_approvals:
            raise ValueError(f"Approval request {approval_id} not found")

        approval = self.pending_approvals[approval_id]
        approval['status'] = 'rejected'
        approval['approved_by'] = approver_id
        approval['approved_at'] = datetime.now()
        approval['rejection_reason'] = reason

        logger.info(f"Approval rejected: {approval_id} by user {approver_id}")

        return approval

    def get_pending_approvals(self, requester_id: Optional[int] = None) -> list:
        """
        Get pending approval requests

        Args:
            requester_id: Optional filter by requester

        Returns:
            List of pending approvals
        """
        pending = [
            a for a in self.pending_approvals.values()
            if a['status'] == 'pending'
        ]

        if requester_id:
            pending = [a for a in pending if a['requester_id'] == requester_id]

        return pending

    def get_approval_status(self, approval_id: str) -> str:
        """
        Get status of approval request

        Args:
            approval_id: Approval request ID

        Returns:
            Status string
        """
        if approval_id not in self.pending_approvals:
            return 'not_found'

        return self.pending_approvals[approval_id]['status']

    def get_approval_history(self, requester_id: int) -> list:
        """
        Get approval history for a user

        Args:
            requester_id: User ID

        Returns:
            List of all approval requests
        """
        history = [
            a for a in self.pending_approvals.values()
            if a['requester_id'] == requester_id
        ]

        return sorted(history, key=lambda x: x['created_at'], reverse=True)


# Global approval manager instance
approval_manager = ApprovalManager()
