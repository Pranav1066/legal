"""
Case Law Research Agent
Specializes in researching case law, finding precedents, and analyzing legal decisions
"""
import logging
from agno.agent import Agent
from agno.models.google import Gemini
from config import config

logger = logging.getLogger(__name__)


class CaseLawResearchAgent:
    """
    AI Agent specialized in case law research and precedent analysis
    """

    def __init__(self):
        """Initialize Case Law Research Agent"""
        self.agent = Agent(
            name="Case Law Research Specialist",
            model=Gemini(id=config.AI_MODEL, api_key=config.GEMINI_API_KEY),
            instructions=self._get_instructions(),
            markdown=True
        )
        logger.info("Case Law Research Agent initialized")

    def _get_instructions(self) -> str:
        """Get comprehensive instructions for the agent"""
        return """
You are an expert Case Law Research Specialist with deep expertise in legal precedents,
judicial reasoning, and case analysis. Your role is to help lawyers research relevant
case law, analyze judicial decisions, and identify applicable precedents.

## Core Responsibilities

1. **Case Law Research**
   - Search and identify relevant precedents
   - Analyze judicial decisions and reasoning
   - Track case law developments and trends
   - Identify overruling and distinguishing cases

2. **Precedent Analysis**
   - Evaluate precedential value and binding authority
   - Analyze factual similarities and differences
   - Assess applicability to current cases
   - Identify key holdings and dicta

3. **Citation Network Analysis**
   - Map citation relationships between cases
   - Identify seminal and frequently cited cases
   - Track judicial influence and authority
   - Recognize citation patterns and trends

4. **Legal Issue Identification**
   - Extract key legal issues from cases
   - Categorize issues by legal domain
   - Identify recurring legal questions
   - Recognize novel legal issues

5. **Judicial Reasoning Analysis**
   - Analyze judicial logic and argumentation
   - Identify persuasive vs. mandatory authority
   - Evaluate dissenting and concurring opinions
   - Assess strength of reasoning

## Analysis Framework

When conducting case law research, structure your analysis as follows:

### 1. Case Overview
- Case name and citation
- Court and jurisdiction
- Decision date
- Judge(s) and panel composition
- Case type and procedural posture

### 2. Facts Summary
- Key facts relevant to legal issues
- Procedural history
- Lower court decisions
- Parties and their positions

### 3. Legal Issues
- Primary legal questions presented
- Secondary and related issues
- Jurisdictional questions
- Constitutional issues (if any)

### 4. Holdings
- Court's decision on each issue
- Ratio decidendi (binding reasoning)
- Disposition (affirmed, reversed, remanded, etc.)
- Vote breakdown (if applicable)

### 5. Reasoning Analysis
- Legal principles applied
- Statutory interpretation methods
- Precedents cited and their significance
- Policy considerations
- Logical structure of opinion

### 6. Precedential Value
- Binding authority level
- Jurisdictional scope
- Subject matter scope
- Strength as precedent (weak, moderate, strong)
- Likelihood of being followed

### 7. Distinguishing Factors
- How this case differs from others
- Unique factual circumstances
- Novel legal interpretations
- Jurisdictional peculiarities

### 8. Related Cases
- Cases cited in opinion
- Cases citing this opinion
- Overruled or modified cases
- Conflicting decisions

### 9. Practical Implications
- Impact on current case
- Litigation strategy considerations
- Arguments that can be made
- Potential weaknesses or distinguishing factors

### 10. Research Recommendations
- Additional cases to review
- Related legal issues to research
- Statute or regulation research needed
- Secondary sources to consult

## Best Practices

1. **Be Thorough**: Consider all relevant precedents, not just those supporting one position
2. **Be Critical**: Evaluate strength of precedents and reasoning objectively
3. **Be Current**: Check if cases have been overruled, distinguished, or criticized
4. **Be Precise**: Accurately cite cases and quote holdings
5. **Be Analytical**: Don't just summarize - analyze applicability and significance
6. **Be Practical**: Focus on how precedents can be used in current case
7. **Be Comprehensive**: Consider majority, concurring, and dissenting opinions
8. **Be Contextual**: Understand jurisdictional and temporal context

## Output Format

Structure your case law research in markdown with:
- Clear headings and subheadings
- Proper case citations
- Bullet points for key information
- Tables for comparing multiple cases
- Block quotes for important holdings or reasoning

When analyzing applicability to a current case:
- Explicitly state factual similarities and differences
- Assess strength of analogies
- Identify potential counterarguments
- Provide strategic recommendations

Always ground your analysis in the actual case law provided, citing specific cases,
holdings, and reasoning. Distinguish between binding authority, persuasive authority,
and dicta.
"""

    def research_precedents(self, research_data: dict) -> str:
        """
        Research relevant case law precedents

        Args:
            research_data: Dictionary containing:
                - legal_issue: Primary legal issue
                - jurisdiction: Relevant jurisdiction
                - practice_area: Area of law
                - current_facts: Facts of current case
                - precedents: List of potentially relevant cases

        Returns:
            Comprehensive precedent research analysis
        """
        prompt = self._format_precedent_research_prompt(research_data)
        logger.info(f"Researching precedents for: {research_data.get('legal_issue', 'Unknown')[:50]}")

        try:
            response = self.agent.run(prompt)
            logger.info("Precedent research completed")
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Precedent research failed: {str(e)}")
            raise

    def analyze_case_applicability(self, case_data: dict) -> str:
        """
        Analyze how a specific case applies to current situation

        Args:
            case_data: Dictionary containing case info and current situation

        Returns:
            Analysis of case applicability
        """
        prompt = f"""
Analyze the applicability of the following precedent to the current case:

## Precedent Case
**Case Name**: {case_data.get('case_name', 'Unknown')}
**Citation**: {case_data.get('citation', 'N/A')}
**Court**: {case_data.get('court', 'Unknown')}
**Decision Date**: {case_data.get('decision_date', 'N/A')}

**Facts**: {case_data.get('facts', 'Not provided')}
**Legal Issue**: {case_data.get('legal_issue', 'Not specified')}
**Holding**: {case_data.get('holding', 'Not provided')}
**Reasoning**: {case_data.get('reasoning', 'Not provided')}

## Current Case
**Facts**: {case_data.get('current_facts', 'Not provided')}
**Legal Issue**: {case_data.get('current_issue', 'Not specified')}
**Jurisdiction**: {case_data.get('current_jurisdiction', 'Not specified')}

## Task
Provide a detailed analysis including:
1. **Factual Comparison**: Similarities and differences between cases
2. **Legal Issue Alignment**: How closely the legal issues match
3. **Precedential Authority**: Binding vs. persuasive authority level
4. **Applicability Assessment**: Strong, moderate, or weak applicability
5. **Distinguishing Factors**: Ways opposing counsel might distinguish this case
6. **Strategic Use**: How to best use this precedent in arguments
7. **Risk Assessment**: Potential weaknesses in relying on this precedent
8. **Recommendation**: Whether to cite prominently, use as support, or avoid

Be specific and provide actionable guidance for litigation strategy.
"""

        try:
            response = self.agent.run(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Case applicability analysis failed: {str(e)}")
            raise

    def compare_cases(self, cases_data: dict) -> str:
        """
        Compare multiple cases to identify patterns and differences

        Args:
            cases_data: Dictionary with list of cases to compare

        Returns:
            Comparative case analysis
        """
        prompt = f"""
Compare and analyze the following cases:

{self._format_multiple_cases(cases_data.get('cases', []))}

## Comparison Criteria
- Factual patterns
- Legal issues addressed
- Holdings and outcomes
- Judicial reasoning approaches
- Precedential value
- Jurisdictional considerations

## Task
Provide a comprehensive comparison including:
1. **Common Threads**: Shared facts, issues, or reasoning
2. **Key Differences**: How cases diverge
3. **Trend Analysis**: Evolution of law across cases
4. **Conflicting Holdings**: Any contradictions or tensions
5. **Strongest Precedents**: Which cases have most authority
6. **Strategic Implications**: How to use these cases together

Present findings in clear, organized format with tables where appropriate.
"""

        try:
            response = self.agent.run(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Case comparison failed: {str(e)}")
            raise

    def extract_legal_principles(self, case_data: dict) -> str:
        """
        Extract legal principles and rules from case law

        Args:
            case_data: Case information

        Returns:
            Extracted legal principles
        """
        prompt = f"""
Extract and articulate the legal principles from the following case:

**Case**: {case_data.get('case_name', 'Unknown')}
**Citation**: {case_data.get('citation', 'N/A')}

**Holding**: {case_data.get('holding', 'Not provided')}
**Reasoning**: {case_data.get('reasoning', 'Not provided')}
**Full Opinion**: {case_data.get('full_text', 'Not available')}

## Task
Extract and clearly articulate:
1. **Black Letter Law**: The specific legal rules established
2. **Tests/Standards**: Any tests or standards articulated by the court
3. **Elements**: Required elements for claims or defenses
4. **Factors**: Factors courts should consider
5. **Legal Principles**: Broader principles underlying the decision
6. **Exceptions**: Any exceptions or limitations noted
7. **Application Guidance**: How to apply these principles to new facts

Present principles in clear, quotable form that can be used in legal arguments.
"""

        try:
            response = self.agent.run(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Legal principle extraction failed: {str(e)}")
            raise

    def _format_precedent_research_prompt(self, research_data: dict) -> str:
        """Format comprehensive precedent research prompt"""
        precedents = research_data.get('precedents', [])

        prompt = f"""
Conduct comprehensive case law research for the following matter:

## Research Parameters
**Legal Issue**: {research_data.get('legal_issue', 'Not specified')}
**Jurisdiction**: {research_data.get('jurisdiction', 'Not specified')}
**Practice Area**: {research_data.get('practice_area', 'Not specified')}

**Current Case Facts**: {research_data.get('current_facts', 'Not provided')}

## Available Precedents ({len(precedents)} cases)

{self._format_precedents_detailed(precedents)}

## Task
Provide comprehensive case law research analysis following your analytical framework.
Focus on identifying the most relevant and applicable precedents for the legal issue.
Provide strategic recommendations for how to use these precedents effectively.
"""
        return prompt

    def _format_precedents_detailed(self, precedents: list) -> str:
        """Format precedents with full details"""
        if not precedents:
            return "**No precedents provided**"

        formatted = ""
        for i, case in enumerate(precedents, 1):
            formatted += f"\n### Case {i}: {case.get('case_name', 'Unknown')}\n"
            formatted += f"**Citation**: {case.get('citation', 'N/A')}\n"
            formatted += f"**Court**: {case.get('court', 'Unknown')} ({case.get('jurisdiction', 'Unknown')})\n"
            formatted += f"**Date**: {case.get('decision_date', 'N/A')}\n"
            formatted += f"**Legal Issue**: {case.get('legal_issue', 'Not specified')}\n"
            formatted += f"**Holding**: {case.get('holding', 'Not provided')}\n"
            formatted += f"**Importance Score**: {case.get('importance_score', 'N/A')}\n"
            formatted += f"**Citations**: {case.get('citation_count', 0)}\n"
            if case.get('reasoning'):
                formatted += f"**Reasoning**: {case.get('reasoning')[:300]}...\n"
            formatted += "\n"

        return formatted

    def _format_multiple_cases(self, cases: list) -> str:
        """Format multiple cases for comparison"""
        if not cases:
            return "**No cases provided**"

        formatted = ""
        for i, case in enumerate(cases, 1):
            formatted += f"\n## Case {i}: {case.get('case_name', 'Unknown')}\n"
            formatted += f"- **Citation**: {case.get('citation', 'N/A')}\n"
            formatted += f"- **Court**: {case.get('court', 'Unknown')}\n"
            formatted += f"- **Date**: {case.get('decision_date', 'N/A')}\n"
            formatted += f"- **Facts**: {case.get('facts', 'Not provided')[:200]}...\n"
            formatted += f"- **Issue**: {case.get('legal_issue', 'Not specified')}\n"
            formatted += f"- **Holding**: {case.get('holding', 'Not provided')}\n\n"

        return formatted


# Global agent instance
case_law_agent = CaseLawResearchAgent()
