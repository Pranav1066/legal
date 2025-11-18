"""
Legal Drafting Agent
Specializes in drafting legal documents, motions, briefs, and correspondence
"""
import logging
from agno.agent import Agent
from agno.models.google import Gemini
from config import config

logger = logging.getLogger(__name__)


class LegalDraftingAgent:
    """
    AI Agent specialized in legal document drafting
    """

    def __init__(self):
        """Initialize Legal Drafting Agent"""
        self.agent = Agent(
            name="Legal Drafting Specialist",
            model=Gemini(id=config.AI_MODEL, api_key=config.GEMINI_API_KEY),
            instructions=self._get_instructions(),
            markdown=True
        )
        logger.info("Legal Drafting Agent initialized")

    def _get_instructions(self) -> str:
        """Get comprehensive instructions for the agent"""
        return """
You are an expert Legal Drafting Specialist with mastery in legal writing,
document preparation, and persuasive advocacy. Your role is to help lawyers
draft clear, effective, and professionally formatted legal documents.

## Core Responsibilities

1. **Document Drafting**
   - Draft pleadings, motions, and briefs
   - Prepare contracts and agreements
   - Create legal memoranda
   - Draft correspondence

2. **Legal Writing Excellence**
   - Clear, precise legal writing
   - Proper legal citations
   - Logical argumentation
   - Persuasive advocacy

3. **Document Review and Editing**
   - Review and improve drafts
   - Ensure proper formatting
   - Check citations and authorities
   - Refine arguments

4. **Template Creation**
   - Develop document templates
   - Create standard clauses
   - Design form documents
   - Build document libraries

## Document Types

### Litigation Documents
- Complaints and answers
- Motions (to dismiss, for summary judgment, etc.)
- Briefs (appellate, trial, etc.)
- Discovery requests and responses
- Affidavits and declarations
- Proposed orders
- Settlement agreements

### Transactional Documents
- Contracts and agreements
- Purchase agreements
- Licensing agreements
- NDAs and confidentiality agreements
- Employment agreements
- Operating agreements
- Terms of service

### Advisory Documents
- Legal memoranda
- Opinion letters
- Client advisories
- Demand letters
- Cease and desist letters
- Response letters

### Corporate Documents
- Articles of incorporation
- Bylaws
- Board resolutions
- Stock certificates
- Minutes of meetings
- Shareholder agreements

## Legal Writing Principles

### 1. Clarity
- Use plain English where possible
- Define technical terms
- Avoid unnecessary jargon
- Use short sentences and paragraphs
- Organize logically

### 2. Precision
- Be specific, not vague
- Use defined terms consistently
- Avoid ambiguity
- Include necessary qualifications
- Specify dates, amounts, parties

### 3. Conciseness
- Eliminate redundancy
- Cut unnecessary words
- Use active voice
- Avoid throat-clearing
- Get to the point

### 4. Formality
- Professional tone
- Appropriate level of formality
- Respectful language
- Objective presentation (where appropriate)
- Advocacy where appropriate

### 5. Organization
- Logical structure
- Clear headings and subheadings
- Numbered paragraphs where appropriate
- Effective use of white space
- Table of contents for long documents

### 6. Citations
- Proper Bluebook or local citation format
- Accurate case names and citations
- Pin cites for specific propositions
- Signal usage (see, see also, cf., but see, etc.)
- Short form citations

### 7. Persuasion (for advocacy documents)
- Lead with strong arguments
- Address counterarguments
- Use persuasive but ethical rhetoric
- Cite favorable authority prominently
- Distinguish unfavorable authority
- Tell compelling story with facts

## Drafting Framework

### For Motions and Briefs:

**I. Caption/Header**
- Court name
- Case caption
- Case number
- Document title

**II. Introduction**
- State what you're seeking
- Briefly explain why
- Preview strongest arguments

**III. Statement of Facts**
- Chronological narrative
- Include only relevant facts
- Cite to record
- Present favorably but accurately

**IV. Argument**
- Organize by issues
- CREAC/IRAC structure
  - Conclusion/Issue
  - Rule
  - Explanation
  - Application
  - Conclusion
- Use headings as thesis statements
- Lead with strongest argument

**V. Conclusion**
- State relief requested
- Be specific about what court should do
- Include signature block

### For Contracts:

**Structure:**
1. Title
2. Preamble (parties and recitals)
3. Definitions
4. Operative provisions
5. Representations and warranties
6. Covenants
7. Conditions
8. Remedies and dispute resolution
9. General provisions
10. Signature blocks

**Drafting Tips:**
- Use "shall" for obligations
- Use "will" for future events
- Use "may" for discretion
- Use defined terms consistently
- Number and title sections
- Use cross-references carefully
- Include integration clause

### For Legal Memoranda:

**Structure:**
1. Heading (To, From, Date, Re)
2. Question Presented
3. Brief Answer
4. Facts
5. Discussion/Analysis
6. Conclusion

**Analysis:**
- Objective tone
- Analyze all sides
- Identify weaknesses
- Apply law to facts
- Provide realistic assessment

## Best Practices

1. **Know Your Audience**: Adjust sophistication and tone for judges, clients, opposing counsel
2. **Understand Purpose**: Advocate vs. advise, inform vs. persuade
3. **Follow Local Rules**: Court rules, formatting requirements, page limits
4. **Be Accurate**: Check facts, law, and citations carefully
5. **Be Ethical**: Honest representation, disclose adverse authority
6. **Be Professional**: Avoid personal attacks, maintain civility
7. **Proofread**: Grammar, spelling, formatting, citation errors damage credibility
8. **Use Templates Wisely**: Start with templates but customize thoroughly

## Output Format

When drafting documents:

1. **Use proper legal formatting**
   - Appropriate headers and footers
   - Page numbers
   - Line numbering (if required)
   - Proper spacing

2. **Include necessary components**
   - Caption/title
   - Signature blocks
   - Certificate of service
   - Exhibits references
   - Table of contents/authorities (if needed)

3. **Provide clean, ready-to-file documents**
   - Professional appearance
   - Proper citations
   - Consistent formatting
   - No placeholder text

4. **Include drafting notes**
   - Explain key choices
   - Flag items needing verification
   - Suggest alternatives where applicable
   - Note local rule considerations

Produce documents that are professional, persuasive, and ready for filing or execution
with minimal editing required.
"""

    def draft_legal_memo(self, memo_data: dict) -> str:
        """
        Draft a legal memorandum

        Args:
            memo_data: Dictionary containing:
                - question: Legal question to address
                - facts: Relevant facts
                - jurisdiction: Applicable jurisdiction
                - applicable_law: Relevant statutes, cases
                - purpose: Purpose of memo (research, client advice, etc.)

        Returns:
            Drafted legal memorandum
        """
        prompt = f"""
Draft a legal memorandum addressing the following:

## Memo Parameters
**To**: {memo_data.get('recipient', 'Senior Partner')}
**From**: {memo_data.get('author', 'Associate')}
**Re**: {memo_data.get('subject', 'Legal Research Memorandum')}
**Date**: {memo_data.get('date', 'Today')}

## Question Presented
{memo_data.get('question', 'Not specified')}

## Facts
{memo_data.get('facts', 'Not provided')}

## Applicable Law
**Jurisdiction**: {memo_data.get('jurisdiction', 'Not specified')}
**Statutes**: {', '.join(memo_data.get('statutes', []))}
**Relevant Cases**:
{self._format_cases_list(memo_data.get('cases', []))}

## Analysis Required
Draft a complete legal memorandum following standard format:
1. Question Presented (reframed if needed for clarity)
2. Brief Answer (2-3 sentences)
3. Facts (organized and relevant)
4. Discussion (thorough legal analysis with CREAC structure)
5. Conclusion

Use objective tone, analyze both favorable and unfavorable authorities,
provide realistic assessment. Cite cases and statutes properly.
"""

        logger.info(f"Drafting legal memo: {memo_data.get('subject', 'Unknown')[:50]}")

        try:
            response = self.agent.run(prompt)
            logger.info("Legal memo drafting completed")
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Legal memo drafting failed: {str(e)}")
            raise

    def draft_motion(self, motion_data: dict) -> str:
        """
        Draft a legal motion

        Args:
            motion_data: Information about motion to draft

        Returns:
            Drafted motion
        """
        prompt = f"""
Draft a motion for filing in court:

## Court Information
**Court**: {motion_data.get('court', 'Not specified')}
**Case Number**: {motion_data.get('case_number', 'XX-XXXX-XXXXXX')}
**Case Caption**: {motion_data.get('case_caption', 'Plaintiff v. Defendant')}

## Motion Type
{motion_data.get('motion_type', 'Not specified')}

## Relief Sought
{motion_data.get('relief_sought', 'Not specified')}

## Factual Background
{motion_data.get('facts', 'Not provided')}

## Legal Basis
**Applicable Rules**: {', '.join(motion_data.get('rules', []))}
**Supporting Cases**:
{self._format_cases_list(motion_data.get('cases', []))}
**Statutes**: {', '.join(motion_data.get('statutes', []))}

## Arguments
{self._format_arguments(motion_data.get('arguments', []))}

## Draft Requirements
Create a complete motion including:
1. Caption
2. Title
3. Introduction (what you're asking for and why)
4. Statement of Facts (relevant background)
5. Argument (organized by issue with legal analysis)
6. Conclusion (specific relief requested)
7. Signature block
8. Certificate of service

Use persuasive but professional tone. Cite authorities properly.
Organize arguments logically with strongest first.
"""

        logger.info(f"Drafting motion: {motion_data.get('motion_type', 'Unknown')}")

        try:
            response = self.agent.run(prompt)
            logger.info("Motion drafting completed")
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Motion drafting failed: {str(e)}")
            raise

    def draft_demand_letter(self, demand_data: dict) -> str:
        """
        Draft a demand letter

        Args:
            demand_data: Information for demand letter

        Returns:
            Drafted demand letter
        """
        prompt = f"""
Draft a demand letter:

## Client Information
**Client**: {demand_data.get('client_name', 'Our Client')}
**Client Position**: {demand_data.get('client_position', 'Not specified')}

## Recipient Information
**Recipient**: {demand_data.get('recipient_name', 'Recipient')}
**Recipient Address**: {demand_data.get('recipient_address', '[Address]')}

## Matter
**Subject**: {demand_data.get('subject', 'Legal Matter')}
**Facts**: {demand_data.get('facts', 'Not provided')}

## Legal Basis
{demand_data.get('legal_basis', 'Not provided')}

## Damages/Relief
{demand_data.get('damages', 'Not specified')}

## Demand
**Amount/Action Demanded**: {demand_data.get('demand', 'Not specified')}
**Deadline**: {demand_data.get('deadline', 'Not specified')}

## Tone
{demand_data.get('tone', 'Firm but professional')}

## Draft Requirements
Create a professional demand letter that:
1. Identifies your client and role
2. States the facts clearly and persuasively
3. Explains legal basis for demand
4. Specifies damages or harm
5. Makes clear demand with deadline
6. States consequences of non-compliance
7. Maintains professional but firm tone
8. Includes proper closing and signature

Letter should be persuasive but professional, firm but not inflammatory.
"""

        logger.info(f"Drafting demand letter: {demand_data.get('subject', 'Unknown')[:50]}")

        try:
            response = self.agent.run(prompt)
            logger.info("Demand letter drafting completed")
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Demand letter drafting failed: {str(e)}")
            raise

    def draft_contract_clause(self, clause_data: dict) -> str:
        """
        Draft a specific contract clause

        Args:
            clause_data: Information about clause to draft

        Returns:
            Drafted contract clause
        """
        prompt = f"""
Draft a contract clause:

## Clause Type
{clause_data.get('clause_type', 'Not specified')}

## Purpose
{clause_data.get('purpose', 'Not specified')}

## Context
**Contract Type**: {clause_data.get('contract_type', 'General')}
**Party Favored**: {clause_data.get('party_favored', 'Balanced')}
**Jurisdiction**: {clause_data.get('jurisdiction', 'Not specified')}
**Industry**: {clause_data.get('industry', 'General')}

## Requirements
{clause_data.get('requirements', 'Not provided')}

## Additional Considerations
{clause_data.get('considerations', 'None specified')}

## Drafting Task
Draft a complete, professional contract clause that:
1. Clearly expresses the intended rights and obligations
2. Uses proper contract drafting language
3. Anticipates potential issues or disputes
4. Includes appropriate qualifications or exceptions
5. Integrates well with standard contract structure
6. Protects client's interests appropriately

Provide:
- Primary version (main recommendation)
- Alternative version (if different approach possible)
- Drafting notes explaining key choices

Use proper contract language: "shall" for obligations, "may" for discretion,
defined terms, clear structure.
"""

        logger.info(f"Drafting contract clause: {clause_data.get('clause_type', 'Unknown')}")

        try:
            response = self.agent.run(prompt)
            logger.info("Contract clause drafting completed")
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Contract clause drafting failed: {str(e)}")
            raise

    def improve_legal_writing(self, writing_data: dict) -> str:
        """
        Review and improve legal writing

        Args:
            writing_data: Text to review and suggestions

        Returns:
            Improved version with explanations
        """
        prompt = f"""
Review and improve the following legal writing:

## Document Type
{writing_data.get('document_type', 'Legal document')}

## Original Text
{writing_data.get('original_text', 'Not provided')}

## Improvement Focus
{', '.join(writing_data.get('focus_areas', ['Clarity', 'Conciseness', 'Persuasiveness']))}

## Context
**Audience**: {writing_data.get('audience', 'Not specified')}
**Purpose**: {writing_data.get('purpose', 'Not specified')}

## Review Task
Provide:
1. **Overall Assessment**: Strengths and weaknesses
2. **Specific Issues**: Identify problems with examples
3. **Improved Version**: Complete rewrite with improvements
4. **Explanation**: Key changes and why they improve the text
5. **Additional Suggestions**: Further recommendations

Focus on:
- Clarity and precision
- Conciseness (eliminating wordiness)
- Organization and flow
- Persuasiveness (if advocacy document)
- Professional tone
- Grammar and usage
- Citation format

Provide side-by-side comparison for key passages showing before and after.
"""

        logger.info("Reviewing and improving legal writing")

        try:
            response = self.agent.run(prompt)
            logger.info("Legal writing improvement completed")
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Legal writing improvement failed: {str(e)}")
            raise

    def _format_cases_list(self, cases: list) -> str:
        """Format list of cases"""
        if not cases:
            return "No cases provided"

        formatted = ""
        for case in cases:
            if isinstance(case, dict):
                formatted += f"- {case.get('name', 'Unknown')}, {case.get('citation', 'No citation')}\n"
            else:
                formatted += f"- {case}\n"
        return formatted

    def _format_arguments(self, arguments: list) -> str:
        """Format list of arguments"""
        if not arguments:
            return "No specific arguments provided"

        formatted = ""
        for i, arg in enumerate(arguments, 1):
            formatted += f"{i}. {arg}\n"
        return formatted


# Global agent instance
drafting_agent = LegalDraftingAgent()
