"""
Compliance Advisory Agent
Specializes in regulatory compliance, risk management, and policy development
"""
import logging
from agno.agent import Agent
from agno.models.google import Gemini
from config import config

logger = logging.getLogger(__name__)


class ComplianceAdvisoryAgent:
    """
    AI Agent specialized in compliance advisory and regulatory analysis
    """

    def __init__(self):
        """Initialize Compliance Advisory Agent"""
        self.agent = Agent(
            name="Compliance Advisory Specialist",
            model=Gemini(id=config.AI_MODEL, api_key=config.GEMINI_API_KEY),
            instructions=self._get_instructions(),
            markdown=True
        )
        logger.info("Compliance Advisory Agent initialized")

    def _get_instructions(self) -> str:
        """Get comprehensive instructions for the agent"""
        return """
You are an expert Compliance Advisory Specialist with deep expertise in regulatory
compliance, risk management, corporate governance, and policy development. Your role
is to help organizations navigate complex regulatory requirements and maintain compliance.

## Core Responsibilities

1. **Regulatory Compliance Assessment**
   - Identify applicable laws and regulations
   - Assess current compliance status
   - Identify compliance gaps and risks
   - Provide remediation recommendations

2. **Risk Management**
   - Identify compliance risks
   - Assess risk severity and likelihood
   - Develop risk mitigation strategies
   - Monitor ongoing compliance risks

3. **Policy Development**
   - Draft compliance policies and procedures
   - Review and update existing policies
   - Ensure policies meet regulatory requirements
   - Align policies with best practices

4. **Regulatory Research**
   - Research applicable regulations
   - Track regulatory changes and updates
   - Interpret regulatory requirements
   - Analyze regulatory impact

5. **Compliance Program Design**
   - Design comprehensive compliance programs
   - Develop compliance frameworks
   - Create monitoring and auditing procedures
   - Establish reporting mechanisms

## Key Compliance Areas

### 1. Data Privacy and Security
- GDPR compliance
- CCPA/CPRA compliance
- HIPAA privacy and security
- Data breach notification requirements
- Cross-border data transfers
- Privacy policy requirements
- Consent management
- Data retention and deletion

### 2. Financial Compliance
- SOX (Sarbanes-Oxley) compliance
- Anti-money laundering (AML)
- Know Your Customer (KYC)
- Securities regulations
- Financial reporting requirements
- Internal controls
- Audit requirements

### 3. Employment Compliance
- Labor law compliance
- Workplace safety (OSHA)
- Anti-discrimination laws
- Wage and hour requirements
- Benefits compliance (ERISA)
- Immigration compliance (I-9)
- Harassment prevention
- Employee privacy

### 4. Industry-Specific Compliance
- Healthcare (HIPAA, FDA)
- Financial services (SEC, FINRA)
- Payment card industry (PCI-DSS)
- Telecommunications (FCC)
- Environmental (EPA)
- Food safety (FDA, USDA)
- Pharmaceuticals (FDA, DEA)

### 5. International Compliance
- Foreign Corrupt Practices Act (FCPA)
- UK Bribery Act
- Export controls (ITAR, EAR)
- International sanctions
- Anti-boycott regulations
- Transfer pricing
- Tax compliance

### 6. Corporate Governance
- Board responsibilities
- Fiduciary duties
- Shareholder rights
- Executive compensation
- Related party transactions
- Conflicts of interest
- Whistleblower protections

## Compliance Assessment Framework

When assessing compliance, structure analysis as follows:

### 1. Regulatory Inventory
- List all applicable regulations
- Identify jurisdictional requirements
- Note industry-specific rules
- Track regulatory changes

### 2. Requirements Analysis
- Break down specific requirements
- Identify mandatory vs. recommended practices
- Note deadlines and timelines
- Document evidence requirements

### 3. Gap Analysis
- Current state assessment
- Required state identification
- Gap identification
- Priority ranking

### 4. Risk Assessment
- Identify compliance risks
- Rate risk severity (Critical/High/Medium/Low)
- Assess likelihood of violation
- Calculate potential penalties
- Consider reputational impact

### 5. Remediation Planning
- Prioritize remediation actions
- Develop implementation timeline
- Assign responsibilities
- Estimate resource requirements
- Set measurable milestones

### 6. Ongoing Monitoring
- Establish compliance metrics
- Design monitoring procedures
- Create reporting mechanisms
- Schedule regular reviews
- Plan for regulatory updates

## Best Practices

1. **Be Comprehensive**: Consider all applicable regulations across jurisdictions
2. **Be Current**: Stay updated on regulatory changes and interpretations
3. **Be Practical**: Provide implementable solutions, not just theoretical compliance
4. **Be Risk-Based**: Prioritize high-risk areas and violations with severe penalties
5. **Be Documented**: Emphasize documentation for audit and enforcement defense
6. **Be Proactive**: Anticipate regulatory changes and emerging compliance issues
7. **Be Business-Focused**: Balance compliance requirements with operational needs
8. **Be Clear**: Explain complex regulations in understandable terms

## Output Format

Structure compliance analysis in markdown with:

### Executive Summary
- Overall compliance status
- Critical issues requiring immediate attention
- High-priority recommendations
- Resource requirements

### Regulatory Landscape
- Applicable laws and regulations
- Jurisdictional requirements
- Recent or upcoming regulatory changes
- Enforcement trends

### Compliance Assessment
- Area-by-area compliance status
- Specific requirements and current state
- Identified gaps and deficiencies
- Risk rating for each gap

### Risk Analysis
**Risk Matrix** showing:
- Risk description
- Severity (Critical/High/Medium/Low)
- Likelihood (High/Medium/Low)
- Potential penalties
- Impact (financial, operational, reputational)
- Priority for remediation

### Remediation Recommendations
- Specific actions required
- Implementation timeline
- Responsible parties
- Resource needs
- Success metrics
- Expected outcomes

### Policy Recommendations
- Policies that need creation or revision
- Key policy provisions
- Implementation guidance
- Training requirements

### Monitoring and Auditing
- Ongoing compliance monitoring procedures
- Audit schedules and scope
- Reporting requirements
- Update mechanisms

Provide specific, actionable guidance with clear implementation steps. Reference
specific regulatory provisions and include citations where applicable. Consider
both legal requirements and industry best practices.
"""

    def assess_compliance(self, compliance_data: dict) -> str:
        """
        Assess compliance with applicable regulations

        Args:
            compliance_data: Dictionary containing:
                - organization: Organization information
                - industry: Industry sector
                - jurisdiction: Relevant jurisdictions
                - frameworks: Compliance frameworks (GDPR, HIPAA, etc.)
                - current_practices: Current compliance practices
                - scope: Areas to assess

        Returns:
            Comprehensive compliance assessment
        """
        prompt = self._format_compliance_assessment_prompt(compliance_data)
        logger.info(f"Assessing compliance for: {compliance_data.get('organization', 'Unknown')}")

        try:
            response = self.agent.run(prompt)
            logger.info("Compliance assessment completed")
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Compliance assessment failed: {str(e)}")
            raise

    def analyze_regulatory_requirement(self, requirement_data: dict) -> str:
        """
        Analyze specific regulatory requirement

        Args:
            requirement_data: Information about regulation

        Returns:
            Detailed requirement analysis
        """
        prompt = f"""
Analyze the following regulatory requirement:

## Regulation Details
**Framework**: {requirement_data.get('framework', 'Unknown')}
**Regulation**: {requirement_data.get('regulation_name', 'Unknown')}
**Jurisdiction**: {requirement_data.get('jurisdiction', 'Unknown')}
**Effective Date**: {requirement_data.get('effective_date', 'Unknown')}

## Requirement Text
{requirement_data.get('requirement_text', 'Not provided')}

## Organization Context
**Industry**: {requirement_data.get('industry', 'Not specified')}
**Size**: {requirement_data.get('organization_size', 'Not specified')}
**Current Practices**: {requirement_data.get('current_practices', 'Not specified')}

## Analysis Required
1. **Interpretation**: What does this requirement actually mandate?
2. **Applicability**: Does this apply to our organization? Under what circumstances?
3. **Compliance Steps**: Specific actions needed to comply
4. **Evidence Requirements**: What documentation/proof is needed?
5. **Penalties**: Consequences of non-compliance
6. **Timeline**: Deadlines and implementation schedule
7. **Resources**: Personnel, technology, budget needed
8. **Best Practices**: Industry standards beyond minimum compliance
9. **Monitoring**: How to demonstrate ongoing compliance
10. **Implementation Guidance**: Step-by-step compliance roadmap

Provide practical, actionable guidance for achieving and maintaining compliance.
"""

        try:
            response = self.agent.run(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Regulatory requirement analysis failed: {str(e)}")
            raise

    def develop_compliance_policy(self, policy_data: dict) -> str:
        """
        Develop compliance policy document

        Args:
            policy_data: Information about policy requirements

        Returns:
            Draft policy document
        """
        prompt = f"""
Develop a compliance policy for:

## Policy Information
**Policy Name**: {policy_data.get('policy_name', 'Unknown')}
**Policy Type**: {policy_data.get('policy_type', 'Unknown')}
**Applicable Regulations**: {', '.join(policy_data.get('regulations', []))}
**Target Audience**: {policy_data.get('target_audience', 'All employees')}

## Organization Context
**Industry**: {policy_data.get('industry', 'Not specified')}
**Size**: {policy_data.get('organization_size', 'Not specified')}
**Risk Profile**: {policy_data.get('risk_profile', 'Not specified')}

## Policy Requirements
{policy_data.get('requirements', 'Not provided')}

## Task
Draft a comprehensive compliance policy including:

1. **Purpose and Scope**
   - Policy objectives
   - Who it applies to
   - What it covers

2. **Definitions**
   - Key terms defined clearly

3. **Policy Statements**
   - Clear, enforceable rules
   - Specific prohibited and required behaviors
   - Standards and procedures

4. **Roles and Responsibilities**
   - Who is responsible for what
   - Accountability structure

5. **Procedures**
   - Step-by-step compliance procedures
   - Required actions and timelines
   - Reporting requirements

6. **Monitoring and Enforcement**
   - Compliance monitoring methods
   - Violation consequences
   - Disciplinary procedures

7. **Training and Communication**
   - Training requirements
   - Communication plan
   - Acknowledgment process

8. **Policy Maintenance**
   - Review schedule
   - Update procedures
   - Version control

9. **Related Policies and References**
   - Related documents
   - Regulatory citations
   - Additional resources

10. **Approval and Effective Date**
    - Approval authority
    - Effective date
    - Review date

Draft policy should be clear, enforceable, and compliant with all applicable regulations.
Use professional policy language and formatting.
"""

        try:
            response = self.agent.run(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Policy development failed: {str(e)}")
            raise

    def create_compliance_checklist(self, checklist_data: dict) -> str:
        """
        Create compliance checklist for specific regulation

        Args:
            checklist_data: Information about compliance requirements

        Returns:
            Detailed compliance checklist
        """
        prompt = f"""
Create a comprehensive compliance checklist for:

## Compliance Framework
**Framework**: {checklist_data.get('framework', 'Unknown')}
**Jurisdiction**: {checklist_data.get('jurisdiction', 'Unknown')}
**Industry**: {checklist_data.get('industry', 'Not specified')}

## Scope
{checklist_data.get('scope', 'General compliance')}

## Task
Create a detailed, actionable compliance checklist organized by:

1. **Categories**: Group requirements by logical categories
2. **Requirements**: Specific compliance requirements
3. **Actions**: Concrete actions needed for each requirement
4. **Evidence**: Documentation or proof required
5. **Responsible Party**: Who should complete each action
6. **Deadline**: When it must be completed
7. **Status**: Checkbox for tracking completion
8. **Notes**: Additional guidance or considerations

Format as a practical checklist that can be used for:
- Initial compliance assessment
- Implementation tracking
- Ongoing compliance monitoring
- Audit preparation

Make checklist comprehensive but manageable. Prioritize requirements by importance
and risk. Include guidance on how to use the checklist effectively.
"""

        try:
            response = self.agent.run(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Checklist creation failed: {str(e)}")
            raise

    def assess_data_breach_response(self, breach_data: dict) -> str:
        """
        Assess data breach and provide response guidance

        Args:
            breach_data: Information about data breach

        Returns:
            Breach response recommendations
        """
        prompt = f"""
Provide data breach response guidance for:

## Breach Details
**Type of Data**: {breach_data.get('data_type', 'Unknown')}
**Number of Records**: {breach_data.get('record_count', 'Unknown')}
**Discovery Date**: {breach_data.get('discovery_date', 'Unknown')}
**Breach Cause**: {breach_data.get('cause', 'Under investigation')}
**Geographic Scope**: {breach_data.get('geographic_scope', 'Unknown')}

## Organization Context
**Industry**: {breach_data.get('industry', 'Not specified')}
**Jurisdiction**: {breach_data.get('jurisdiction', 'Not specified')}
**Applicable Laws**: {', '.join(breach_data.get('applicable_laws', ['GDPR', 'CCPA', 'State breach notification laws']))}

## Response Guidance Needed
Provide comprehensive breach response plan including:

1. **Immediate Actions** (First 24-48 hours)
   - Containment steps
   - Evidence preservation
   - Team assembly
   - Initial assessment

2. **Investigation Requirements**
   - Scope determination
   - Root cause analysis
   - Impact assessment
   - Documentation requirements

3. **Legal Notification Obligations**
   - Regulatory notification requirements
   - Timing requirements (e.g., 72-hour GDPR rule)
   - What information must be included
   - Which authorities to notify

4. **Individual Notification**
   - Who must be notified
   - Timing requirements
   - Content requirements
   - Method of notification

5. **Public Relations and Communications**
   - Communication strategy
   - Key messaging
   - FAQ development
   - Media handling

6. **Remediation**
   - Security improvements
   - Prevention measures
   - Credit monitoring/identity theft services
   - Compensation considerations

7. **Legal Risks and Exposure**
   - Potential penalties
   - Litigation risk
   - Regulatory enforcement likelihood
   - Insurance considerations

8. **Documentation**
   - Required records
   - Evidence chain of custody
   - Timeline documentation
   - Decision-making records

Prioritize actions by urgency and regulatory requirement. Provide specific guidance
on notification timing and content to ensure compliance with applicable laws.
"""

        try:
            response = self.agent.run(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Data breach response assessment failed: {str(e)}")
            raise

    def _format_compliance_assessment_prompt(self, compliance_data: dict) -> str:
        """Format comprehensive compliance assessment prompt"""
        prompt = f"""
Conduct a comprehensive compliance assessment for:

## Organization Profile
**Name**: {compliance_data.get('organization', 'Unknown')}
**Industry**: {compliance_data.get('industry', 'Not specified')}
**Jurisdiction(s)**: {', '.join(compliance_data.get('jurisdictions', ['Not specified']))}
**Size**: {compliance_data.get('size', 'Not specified')}
**Business Model**: {compliance_data.get('business_model', 'Not specified')}

## Compliance Scope
**Frameworks**: {', '.join(compliance_data.get('frameworks', config.COMPLIANCE_FRAMEWORKS))}
**Focus Areas**: {', '.join(compliance_data.get('scope', ['General compliance']))}

## Current State
**Existing Compliance Program**: {compliance_data.get('existing_program', 'Not specified')}
**Known Issues**: {', '.join(compliance_data.get('known_issues', ['None identified']))}
**Recent Audits**: {compliance_data.get('recent_audits', 'None')}

## Current Practices
{compliance_data.get('current_practices', 'Not provided')}

## Assessment Task
Provide comprehensive compliance assessment following your analytical framework.
Focus on:
- Identifying all applicable regulations
- Assessing current compliance status
- Identifying gaps and risks
- Providing prioritized remediation recommendations
- Developing implementation roadmap

Ensure recommendations are practical, prioritized, and include resource estimates.
"""
        return prompt


# Global agent instance
compliance_agent = ComplianceAdvisoryAgent()
