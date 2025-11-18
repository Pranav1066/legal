"""
Legal Intelligence Orchestrator
Coordinates all legal agents and manages comprehensive legal analyses
"""
import logging
from typing import Dict, Any
from datetime import datetime

from agents.case_law_research_agent import case_law_agent
from agents.contract_analysis_agent import contract_agent
from agents.compliance_advisory_agent import compliance_agent
from agents.legal_drafting_agent import drafting_agent
from agents.litigation_strategy_agent import litigation_agent
from utils.database import db

logger = logging.getLogger(__name__)


class LegalOrchestrator:
    """
    Central orchestrator for Legal Intelligence System
    Coordinates all specialized agents and manages comprehensive analyses
    """

    def __init__(self):
        """Initialize the orchestrator"""
        self.case_law_agent = case_law_agent
        self.contract_agent = contract_agent
        self.compliance_agent = compliance_agent
        self.drafting_agent = drafting_agent
        self.litigation_agent = litigation_agent
        logger.info("Legal Orchestrator initialized")

    def research_case_law(self, lawyer_id: int, **kwargs) -> str:
        """
        Conduct case law research

        Args:
            lawyer_id: Lawyer ID
            **kwargs: Research parameters

        Returns:
            Case law research analysis
        """
        logger.info(f"Starting case law research for lawyer {lawyer_id}")

        try:
            lawyer = db.get_lawyer_by_id(lawyer_id)
            if not lawyer:
                raise ValueError(f"Lawyer with ID {lawyer_id} not found")

            research_data = {
                'legal_issue': kwargs.get('legal_issue'),
                'jurisdiction': kwargs.get('jurisdiction', lawyer.get('jurisdiction', 'Not specified')),
                'practice_area': kwargs.get('practice_area', lawyer.get('practice_areas', 'General')),
                'current_facts': kwargs.get('current_facts'),
                'precedents': kwargs.get('precedents', [])
            }

            if 'case_id' in kwargs and kwargs['case_id']:
                case = db.get_case_by_id(kwargs['case_id'])
                if case:
                    research_data['current_facts'] = case.get('case_summary')

            result = self.case_law_agent.research_precedents(research_data)

            # Save research session
            db.add_research_session({
                'session_name': f"Case Law Research - {research_data.get('legal_issue', 'Unknown')[:50]}",
                'lawyer_id': lawyer_id,
                'case_id': kwargs.get('case_id'),
                'research_query': research_data.get('legal_issue'),
                'practice_area': research_data.get('practice_area'),
                'jurisdiction': research_data.get('jurisdiction'),
                'findings': result[:1000]  # Store summary
            })

            logger.info("Case law research completed successfully")
            return result

        except Exception as e:
            logger.error(f"Case law research failed: {str(e)}")
            raise

    def analyze_contract(self, lawyer_id: int, contract_id: int = None, **kwargs) -> str:
        """
        Analyze contract

        Args:
            lawyer_id: Lawyer ID
            contract_id: Contract ID (if analyzing existing contract)
            **kwargs: Additional parameters

        Returns:
            Contract analysis
        """
        logger.info(f"Analyzing contract for lawyer {lawyer_id}")

        try:
            contract_data = kwargs.copy()

            if contract_id:
                contract = db.get_document_by_id(contract_id)
                contract_data.update({
                    'contract_name': contract.get('title'),
                    'contract_text': contract.get('document_content'),
                    'contract_type': contract.get('document_type')
                })

            result = self.contract_agent.analyze_contract(contract_data)

            # Save analysis
            db.save_analysis_result({
                'analysis_type': 'contract_analysis',
                'entity_type': 'contract',
                'entity_id': contract_id or 0,
                'lawyer_id': lawyer_id,
                'result_summary': result[:500],
                'detailed_analysis': result
            })

            logger.info("Contract analysis completed successfully")
            return result

        except Exception as e:
            logger.error(f"Contract analysis failed: {str(e)}")
            raise

    def assess_compliance(self, lawyer_id: int, **kwargs) -> str:
        """
        Assess compliance

        Args:
            lawyer_id: Lawyer ID
            **kwargs: Compliance parameters

        Returns:
            Compliance assessment
        """
        logger.info(f"Assessing compliance for lawyer {lawyer_id}")

        try:
            lawyer = db.get_lawyer_by_id(lawyer_id)
            if not lawyer:
                raise ValueError(f"Lawyer with ID {lawyer_id} not found")

            compliance_data = {
                'organization': kwargs.get('organization', lawyer.get('firm', 'Not specified')),
                'industry': kwargs.get('industry'),
                'jurisdictions': kwargs.get('jurisdictions', [lawyer.get('jurisdiction', 'Not specified')]),
                'frameworks': kwargs.get('frameworks', []),
                'current_practices': kwargs.get('current_practices'),
                'scope': kwargs.get('scope', [])
            }

            result = self.compliance_agent.assess_compliance(compliance_data)

            # Save analysis
            db.save_analysis_result({
                'analysis_type': 'compliance_assessment',
                'entity_type': 'organization',
                'entity_id': 0,
                'lawyer_id': lawyer_id,
                'result_summary': result[:500],
                'detailed_analysis': result
            })

            logger.info("Compliance assessment completed successfully")
            return result

        except Exception as e:
            logger.error(f"Compliance assessment failed: {str(e)}")
            raise

    def draft_legal_document(self, lawyer_id: int, document_type: str, **kwargs) -> str:
        """
        Draft legal document

        Args:
            lawyer_id: Lawyer ID
            document_type: Type of document (memo, motion, letter, etc.)
            **kwargs: Document parameters

        Returns:
            Drafted document
        """
        logger.info(f"Drafting {document_type} for lawyer {lawyer_id}")

        try:
            if document_type == 'memo':
                result = self.drafting_agent.draft_legal_memo(kwargs)
            elif document_type == 'motion':
                result = self.drafting_agent.draft_motion(kwargs)
            elif document_type == 'demand_letter':
                result = self.drafting_agent.draft_demand_letter(kwargs)
            elif document_type == 'contract_clause':
                result = self.drafting_agent.draft_contract_clause(kwargs)
            else:
                raise ValueError(f"Unsupported document type: {document_type}")

            # Save document
            doc_id = db.add_document({
                'document_type': document_type,
                'title': kwargs.get('title', f"{document_type.title()} Draft"),
                'case_id': kwargs.get('case_id'),
                'lawyer_id': lawyer_id,
                'document_content': result,
                'status': 'draft',
                'creation_date': datetime.now().strftime('%Y-%m-%d')
            })

            logger.info(f"Document drafting completed successfully (ID: {doc_id})")
            return result

        except Exception as e:
            logger.error(f"Document drafting failed: {str(e)}")
            raise

    def develop_litigation_strategy(self, lawyer_id: int, case_id: int, **kwargs) -> str:
        """
        Develop litigation strategy

        Args:
            lawyer_id: Lawyer ID
            case_id: Case ID
            **kwargs: Additional parameters

        Returns:
            Litigation strategy
        """
        logger.info(f"Developing litigation strategy for case {case_id}")

        try:
            case = db.get_case_by_id(case_id)
            if not case:
                raise ValueError(f"Case with ID {case_id} not found")

            lawyer = db.get_lawyer_by_id(lawyer_id)
            if not lawyer:
                raise ValueError(f"Lawyer with ID {lawyer_id} not found")

            case_data = {
                'case_name': case.get('title', 'Unknown'),
                'case_type': case.get('case_type', 'Civil'),
                'client_position': kwargs.get('client_position', 'plaintiff'),
                'case_stage': case.get('status', 'active'),
                'facts': case.get('case_summary', 'Not provided'),
                'legal_issues': case.get('key_issues', 'Not specified'),
                'client_info': kwargs.get('client_info', case.get('client_name', 'Client')),
                'objectives': kwargs.get('objectives'),
                **kwargs
            }

            result = self.litigation_agent.analyze_case_strategy(case_data)

            # Save analysis
            db.save_analysis_result({
                'analysis_type': 'litigation_strategy',
                'entity_type': 'case',
                'entity_id': case_id,
                'lawyer_id': lawyer_id,
                'result_summary': result[:500],
                'detailed_analysis': result
            })

            logger.info("Litigation strategy completed successfully")
            return result

        except Exception as e:
            logger.error(f"Litigation strategy development failed: {str(e)}")
            raise

    def comprehensive_case_analysis(self, lawyer_id: int, case_id: int) -> Dict[str, str]:
        """
        Perform comprehensive analysis across all dimensions

        Args:
            lawyer_id: Lawyer ID
            case_id: Case ID

        Returns:
            Dictionary with all analysis results
        """
        logger.info(f"Starting comprehensive analysis for case {case_id}")

        results = {}

        try:
            case = db.get_case_by_id(case_id)

            # Case Law Research
            logger.info("Running case law research...")
            results['case_law_research'] = self.research_case_law(
                lawyer_id,
                case_id=case_id,
                legal_issue=case.get('key_issues'),
                practice_area=case.get('practice_area')
            )

            # Litigation Strategy
            logger.info("Developing litigation strategy...")
            results['litigation_strategy'] = self.develop_litigation_strategy(
                lawyer_id,
                case_id
            )

            # Get case documents for contract analysis if applicable
            documents = db.get_case_documents(case_id)
            if documents:
                logger.info("Analyzing case documents...")
                results['document_analyses'] = []
                for doc in documents[:3]:  # Limit to first 3 documents
                    if doc.get('document_type') in ['contract', 'agreement']:
                        analysis = self.analyze_contract(
                            lawyer_id,
                            contract_id=doc.get('id')
                        )
                        results['document_analyses'].append(analysis)

            logger.info("Comprehensive analysis completed successfully")
            return results

        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {str(e)}")
            raise

    def get_lawyer_summary(self, lawyer_id: int) -> Dict[str, Any]:
        """
        Get summary statistics for a lawyer

        Args:
            lawyer_id: Lawyer ID

        Returns:
            Summary dictionary
        """
        try:
            lawyer = db.get_lawyer_by_id(lawyer_id)
            cases = db.get_lawyer_cases(lawyer_id)
            research_sessions = db.get_lawyer_research_sessions(lawyer_id)

            closed_cases = [c for c in cases if c.get('status') in ['closed', 'settled', 'dismissed']]
            won_cases = [c for c in closed_cases if c.get('outcome') in ['won', 'favorable', 'settled']]

            summary = {
                'lawyer': lawyer,
                'total_cases': len(cases),
                'active_cases': len([c for c in cases if c.get('status') == 'active']),
                'closed_cases': len(closed_cases),
                'win_rate': (len(won_cases) / len(closed_cases) * 100) if closed_cases else 0,
                'research_sessions': len(research_sessions),
                'years_experience': lawyer.get('years_experience', 0),
                'specializations': lawyer.get('specializations', ''),
                'recent_cases': cases[:5] if cases else []
            }

            return summary

        except Exception as e:
            logger.error(f"Failed to get lawyer summary: {str(e)}")
            raise


# Global orchestrator instance
orchestrator = LegalOrchestrator()
