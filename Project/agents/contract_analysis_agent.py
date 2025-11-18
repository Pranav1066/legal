"""
Contract Analysis Agent
Specializes in contract review, risk assessment, and clause analysis
"""
import logging
from agno.agent import Agent
from agno.models.google import Gemini
from config import config

logger = logging.getLogger(__name__)


class ContractAnalysisAgent:
    """
    AI Agent specialized in contract analysis and risk assessment
    """

    def __init__(self):
        """Initialize Contract Analysis Agent"""
        self.agent = Agent(
            name="Contract Analysis Specialist",
            model=Gemini(id=config.AI_MODEL, api_key=config.GEMINI_API_KEY),
            instructions=self._get_instructions(),
            markdown=True
        )
        logger.info("Contract Analysis Agent initialized")

    def _get_instructions(self) -> str:
        """Get comprehensive instructions for the agent"""
        return """
You are an expert Contract Analysis Specialist with deep expertise in contract law,
risk assessment, and commercial transactions. Your role is to help lawyers and
businesses analyze contracts, identify risks, and ensure favorable terms.

## Core Responsibilities

1. **Contract Review**
   - Comprehensive clause-by-clause analysis
   - Identify missing or problematic provisions
   - Assess overall contract structure and coherence
   - Check for internal inconsistencies

2. **Risk Assessment**
   - Identify liability exposures
   - Assess termination risks
   - Evaluate payment and performance risks
   - Analyze indemnification obligations
   - Review limitation of liability clauses
   - Assess insurance requirements

3. **Clause Analysis**
   - Analyze specific contract provisions
   - Identify favorable vs. unfavorable terms
   - Suggest alternative language
   - Compare to market standards

4. **Compliance Verification**
   - Check regulatory compliance
   - Verify required legal provisions
   - Ensure proper execution requirements
   - Validate jurisdictional requirements

5. **Negotiation Support**
   - Identify negotiable terms
   - Suggest leverage points
   - Recommend fallback positions
   - Prioritize issues by importance

## Key Contract Areas to Analyze

### 1. Parties and Recitals
- Correct legal entity names
- Proper identification of parties
- Background and purpose clarity

### 2. Scope of Work / Services
- Clear definition of obligations
- Deliverables and specifications
- Performance standards
- Acceptance criteria

### 3. Payment Terms
- Payment amounts and structure
- Payment schedule and milestones
- Late payment provisions
- Expense reimbursement
- Price adjustment mechanisms

### 4. Term and Termination
- Contract duration
- Renewal provisions
- Termination rights and grounds
- Notice requirements
- Post-termination obligations
- Survival provisions

### 5. Intellectual Property
- Ownership of work product
- License grants and restrictions
- Pre-existing IP treatment
- Protection of confidential information
- Non-compete and non-solicitation

### 6. Representations and Warranties
- Scope and accuracy
- Materiality qualifications
- Disclosure schedules
- Survival period
- Warranty disclaimers

### 7. Indemnification
- Scope of indemnification obligations
- Carve-outs and limitations
- Defense obligations
- Notice requirements
- Mutual vs. one-sided indemnities

### 8. Limitation of Liability
- Caps on damages
- Excluded damages types
- Carve-outs from limitations
- Reasonableness of caps

### 9. Insurance
- Required coverage types
- Coverage amounts
- Additional insured requirements
- Certificates of insurance
- Waiver of subrogation

### 10. Dispute Resolution
- Governing law
- Venue and jurisdiction
- Arbitration vs. litigation
- Fee shifting provisions
- Mandatory mediation

### 11. General Provisions
- Assignment restrictions
- Amendment procedures
- Notice provisions
- Force majeure
- Severability
- Entire agreement
- Counterparts

## Risk Assessment Framework

Categorize risks as:
- **CRITICAL**: Must be addressed before signing
- **HIGH**: Should be addressed or explicitly accepted
- **MEDIUM**: Worth negotiating if leverage exists
- **LOW**: Monitor but may accept as-is

For each risk:
1. Describe the risk clearly
2. Explain potential consequences
3. Assess likelihood of occurrence
4. Suggest mitigation strategies
5. Provide recommended contract language

## Best Practices

1. **Be Thorough**: Review entire contract, including exhibits and schedules
2. **Be Practical**: Balance legal perfection with business reality
3. **Be Clear**: Explain risks in business terms, not just legalese
4. **Be Specific**: Provide exact language suggestions
5. **Be Strategic**: Prioritize issues by importance and negotiability
6. **Be Proactive**: Identify issues that might arise during performance
7. **Be Comparative**: Reference market standards where applicable
8. **Be Constructive**: Suggest solutions, not just problems

## Output Format

Structure contract analysis in markdown with:

### Executive Summary
- Overall assessment
- Key risks (3-5 most important)
- Critical action items
- Recommendation (sign, negotiate, reject)

### Detailed Analysis
- Section-by-section review
- Risk identification and rating
- Specific concerns with clause references
- Suggested revisions

### Risk Matrix
- Table summarizing all identified risks
- Risk level, description, likelihood, impact
- Recommended action for each

### Recommended Changes
- Numbered list of suggested revisions
- Current language vs. proposed language
- Justification for each change
- Priority level (must-have, should-have, nice-to-have)

### Negotiation Strategy
- Key leverage points
- Likely counterparty concerns
- Compromise positions
- Walk-away issues

Always provide specific clause references, quote problematic language, and suggest
concrete alternative wording. Balance legal protection with commercial feasibility.
"""

    def analyze_contract(self, contract_data: dict) -> str:
        """
        Perform comprehensive contract analysis

        Args:
            contract_data: Dictionary containing:
                - contract_name: Name/title of contract
                - contract_type: Type (e.g., services, sale, license)
                - contract_text: Full contract text
                - parties: Contracting parties
                - party_role: Client's role (buyer, seller, etc.)
                - jurisdiction: Applicable jurisdiction
                - industry: Industry context

        Returns:
            Comprehensive contract analysis
        """
        prompt = self._format_contract_analysis_prompt(contract_data)
        logger.info(f"Analyzing contract: {contract_data.get('contract_name', 'Unknown')[:50]}")

        try:
            response = self.agent.run(prompt)
            logger.info("Contract analysis completed")
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Contract analysis failed: {str(e)}")
            raise

    def assess_contract_risk(self, contract_data: dict) -> str:
        """
        Focused risk assessment of contract

        Args:
            contract_data: Contract information

        Returns:
            Detailed risk assessment
        """
        prompt = f"""
Perform a comprehensive risk assessment for the following contract:

## Contract Information
**Contract Name**: {contract_data.get('contract_name', 'Unknown')}
**Contract Type**: {contract_data.get('contract_type', 'Unknown')}
**Our Role**: {contract_data.get('party_role', 'Not specified')}
**Contract Value**: {contract_data.get('contract_value', 'Not specified')}
**Term**: {contract_data.get('term', 'Not specified')}

## Contract Text
{contract_data.get('contract_text', 'Not provided')[:5000]}

## Risk Categories to Assess
{', '.join(config.CONTRACT_RISK_CATEGORIES)}

## Task
Provide detailed risk assessment including:
1. **Risk Identification**: All significant risks organized by category
2. **Risk Scoring**: Rate each risk (Critical/High/Medium/Low)
3. **Likelihood Assessment**: Probability of risk materializing
4. **Impact Analysis**: Potential consequences if risk occurs
5. **Risk Mitigation**: Strategies to reduce or eliminate each risk
6. **Contract Modifications**: Specific language changes to address risks
7. **Risk Acceptance**: Risks that may need to be accepted with management approval
8. **Overall Risk Profile**: Summary risk level for entire contract

Present findings in clear risk matrix format with actionable recommendations.
"""

        try:
            response = self.agent.run(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Contract risk assessment failed: {str(e)}")
            raise

    def review_specific_clause(self, clause_data: dict) -> str:
        """
        Analyze a specific contract clause

        Args:
            clause_data: Information about specific clause

        Returns:
            Clause analysis and recommendations
        """
        prompt = f"""
Review and analyze the following contract clause:

## Clause Details
**Clause Type**: {clause_data.get('clause_type', 'Unknown')}
**Section Reference**: {clause_data.get('section_reference', 'Not specified')}

**Current Language**:
{clause_data.get('clause_text', 'Not provided')}

## Context
**Contract Type**: {clause_data.get('contract_type', 'Not specified')}
**Our Position**: {clause_data.get('party_role', 'Not specified')}
**Jurisdiction**: {clause_data.get('jurisdiction', 'Not specified')}

## Analysis Required
1. **Interpretation**: What does this clause actually mean and require?
2. **Favorability**: Is this favorable, neutral, or unfavorable to our client?
3. **Risks**: What risks does this clause create?
4. **Market Standard**: How does this compare to market standard language?
5. **Enforceability**: Are there any enforceability concerns?
6. **Improvements**: How can this clause be improved?
7. **Alternative Language**: Provide 2-3 alternative versions (aggressive, moderate, minimal changes)

Be specific and provide ready-to-use alternative language.
"""

        try:
            response = self.agent.run(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Clause review failed: {str(e)}")
            raise

    def compare_contracts(self, comparison_data: dict) -> str:
        """
        Compare multiple contract versions or similar contracts

        Args:
            comparison_data: Data for contract comparison

        Returns:
            Comparative analysis
        """
        prompt = f"""
Compare the following contracts:

## Contract A
**Name**: {comparison_data.get('contract_a_name', 'Version A')}
{comparison_data.get('contract_a_text', 'Not provided')[:3000]}

## Contract B
**Name**: {comparison_data.get('contract_b_name', 'Version B')}
{comparison_data.get('contract_b_text', 'Not provided')[:3000]}

## Comparison Task
1. **Key Differences**: Identify material differences between contracts
2. **Risk Comparison**: Which contract has better risk allocation?
3. **Terms Comparison**: Compare key commercial terms
4. **Favorability**: Which contract is more favorable to which party?
5. **Improvements**: Suggest taking best provisions from each
6. **Recommendation**: Which contract to use as base, or hybrid approach?

Present findings in side-by-side comparison format where helpful.
"""

        try:
            response = self.agent.run(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Contract comparison failed: {str(e)}")
            raise

    def generate_negotiation_strategy(self, contract_data: dict) -> str:
        """
        Generate negotiation strategy for contract

        Args:
            contract_data: Contract information and business context

        Returns:
            Negotiation strategy and talking points
        """
        prompt = f"""
Develop a negotiation strategy for the following contract:

## Contract Details
**Contract**: {contract_data.get('contract_name', 'Unknown')}
**Type**: {contract_data.get('contract_type', 'Unknown')}
**Value**: {contract_data.get('contract_value', 'Unknown')}
**Our Position**: {contract_data.get('party_role', 'Unknown')}

## Business Context
**Our Leverage**: {contract_data.get('our_leverage', 'Not specified')}
**Relationship Importance**: {contract_data.get('relationship_importance', 'Not specified')}
**Alternatives**: {contract_data.get('alternatives', 'Not specified')}
**Time Pressure**: {contract_data.get('time_pressure', 'Not specified')}

## Key Issues Identified
{self._format_issues(contract_data.get('key_issues', []))}

## Strategy Development
Provide:
1. **Negotiation Priorities**: Rank issues (must-win, should-win, nice-to-win)
2. **Opening Position**: Initial demands for key issues
3. **Target Position**: Realistic goals for each issue
4. **Fallback Position**: Acceptable compromise positions
5. **Walk-Away Points**: Issues that are non-negotiable
6. **Leverage Points**: Where we have negotiating power
7. **Anticipated Objections**: Likely counterparty pushback
8. **Response Strategies**: How to address objections
9. **Concession Strategy**: What to give up and in what order
10. **Talking Points**: Key arguments for priority issues

Frame strategy around achieving business objectives while managing legal risk.
"""

        try:
            response = self.agent.run(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Negotiation strategy generation failed: {str(e)}")
            raise

    def _format_contract_analysis_prompt(self, contract_data: dict) -> str:
        """Format comprehensive contract analysis prompt"""
        prompt = f"""
Perform a comprehensive analysis of the following contract:

## Contract Information
**Contract Name**: {contract_data.get('contract_name', 'Unknown')}
**Contract Type**: {contract_data.get('contract_type', 'Unknown')}
**Parties**: {contract_data.get('parties', 'Not specified')}
**Our Role**: {contract_data.get('party_role', 'Not specified')}
**Jurisdiction**: {contract_data.get('jurisdiction', 'Not specified')}
**Industry**: {contract_data.get('industry', 'General')}

## Full Contract Text
{contract_data.get('contract_text', 'Not provided')}

## Analysis Requirements
Provide comprehensive analysis following your analytical framework. Focus on:
- Executive summary with key findings
- Detailed section-by-section review
- Risk assessment with specific risk ratings
- Recommended changes with specific language
- Negotiation strategy and priorities

Ensure analysis is practical, specific, and actionable for business decision-making.
"""
        return prompt

    def _format_issues(self, issues: list) -> str:
        """Format list of issues"""
        if not issues:
            return "No specific issues provided"

        formatted = ""
        for i, issue in enumerate(issues, 1):
            formatted += f"{i}. {issue}\n"
        return formatted


# Global agent instance
contract_agent = ContractAnalysisAgent()
