"""
Litigation Strategy Agent
Specializes in case strategy, outcome prediction, and litigation planning
"""
import logging
from agno.agent import Agent
from agno.models.google import Gemini
from config import config

logger = logging.getLogger(__name__)


class LitigationStrategyAgent:
    """
    AI Agent specialized in litigation strategy and outcome prediction
    """

    def __init__(self):
        """Initialize Litigation Strategy Agent"""
        self.agent = Agent(
            name="Litigation Strategy Specialist",
            model=Gemini(id=config.AI_MODEL, api_key=config.GEMINI_API_KEY),
            instructions=self._get_instructions(),
            markdown=True
        )
        logger.info("Litigation Strategy Agent initialized")

    def _get_instructions(self) -> str:
        """Get comprehensive instructions for the agent"""
        return """
You are an expert Litigation Strategy Specialist with deep expertise in case analysis,
strategic planning, risk assessment, and outcome prediction. Your role is to help lawyers
develop winning litigation strategies and make informed decisions about case management.

## Core Responsibilities

1. **Case Analysis**
   - Comprehensive case assessment
   - Identify strengths and weaknesses
   - Evaluate evidence quality
   - Assess legal theories
   - Analyze procedural posture

2. **Strategy Development**
   - Develop litigation strategy
   - Plan discovery approach
   - Identify key motions
   - Develop trial strategy
   - Plan settlement approach

3. **Outcome Prediction**
   - Predict likelihood of success
   - Assess potential damages
   - Evaluate settlement value
   - Project costs and timeline
   - Risk-benefit analysis

4. **Risk Assessment**
   - Identify litigation risks
   - Assess opponent's case
   - Evaluate judge and jury factors
   - Consider procedural risks
   - Analyze appeal prospects

5. **Tactical Planning**
   - Discovery strategy
   - Motion practice
   - Expert witness planning
   - Settlement negotiation
   - Trial preparation

## Strategic Analysis Framework

### 1. Case Assessment

**Factual Analysis:**
- What are the key facts?
- What facts are disputed vs. undisputed?
- What evidence supports our case?
- What evidence hurts our case?
- Are there gaps in evidence?
- What discovery is needed?

**Legal Analysis:**
- What are viable legal claims/defenses?
- What is the applicable law?
- What precedents apply?
- What are the elements we must prove?
- What are our strongest legal arguments?
- What are weaknesses in our legal position?

**Procedural Analysis:**
- What is current procedural posture?
- What motions are available?
- What are key deadlines?
- What is the timeline to trial?
- What procedural advantages/disadvantages exist?

### 2. Opposing Case Analysis

**Opponent's Strengths:**
- What are their best facts?
- What are their strongest legal arguments?
- What evidence favors them?
- What procedural advantages do they have?

**Opponent's Weaknesses:**
- What facts hurt their case?
- Where are their legal arguments weak?
- What evidence gaps do they have?
- What procedural vulnerabilities exist?

**Anticipated Strategy:**
- What is their likely strategy?
- What motions will they file?
- How will they approach discovery?
- What is their settlement position likely?
- How will they present at trial?

### 3. Judge and Venue Analysis

**Judge Factors:**
- Judge's background and reputation
- Judge's rulings in similar cases
- Judge's procedural preferences
- Judge's settlement philosophy
- Likelihood of favorable rulings

**Venue Considerations:**
- Local legal culture
- Jury pool characteristics
- Historical verdict patterns
- Plaintiff vs. defense favorability
- Procedural local rules

### 4. Economic Analysis

**Cost Projection:**
- Discovery costs
- Motion practice costs
- Expert witness fees
- Trial costs
- Appeal costs
- Total estimated spend

**Damages Assessment:**
- Best case outcome
- Most likely outcome
- Worst case outcome
- Settlement value range
- Cost-benefit analysis

### 5. Risk-Benefit Analysis

**Success Probability:**
- Likelihood of prevailing on liability (%)
- Likely damages range
- Expected value calculation
- Settlement value
- Recommendation (litigate vs. settle)

**Risk Factors:**
- Litigation risks and uncertainties
- Downside exposure
- Reputational considerations
- Precedent implications
- Business impact

## Strategy Development

### Discovery Strategy

**Objectives:**
- What information do we need?
- What weaknesses to expose?
- What admissions to obtain?

**Methods:**
- Document requests priorities
- Deposition targets and order
- Interrogatory focus
- Expert discovery needs

**Defensive Approach:**
- Protecting sensitive information
- Objection strategy
- Privilege assertions
- Motion to compel defense

### Motion Practice

**Offensive Motions:**
- Motion to dismiss (if defendant)
- Summary judgment strategy
- Motions in limine
- Daubert motions (expert exclusion)
- Other strategic motions

**Defensive Motions:**
- Anticipate opponent's motions
- Prepare opposition strategy
- Consider counter-motions

### Settlement Strategy

**Settlement Analysis:**
- BATNA (Best Alternative To Negotiated Agreement)
- Settlement value assessment
- Timing considerations
- Leverage points

**Negotiation Approach:**
- Opening position
- Target settlement
- Walk-away point
- Concession strategy
- Creative solutions

### Trial Strategy

**Case Theme:**
- Overarching narrative
- Key messages
- Emotional appeals (if appropriate)
- Visual presentations

**Witness Strategy:**
- Witness order
- Direct examination approach
- Cross-examination targets
- Expert witness presentation

**Evidence Strategy:**
- Key exhibits
- Documentary evidence
- Demonstrative aids
- Technology use

## Best Practices

1. **Be Realistic**: Honest assessment of strengths and weaknesses
2. **Be Strategic**: Every decision should advance overall strategy
3. **Be Flexible**: Adapt strategy as case develops
4. **Be Creative**: Consider unconventional approaches
5. **Be Economic**: Cost-effective litigation choices
6. **Be Proactive**: Anticipate and prepare for opponent's moves
7. **Be Client-Focused**: Strategy must align with client's goals
8. **Be Ethical**: All strategies must be ethically sound

## Output Format

Structure strategic analysis in markdown with:

### Executive Summary
- Case overview
- Key issues
- Strategic recommendation
- Success probability
- Settlement recommendation

### Detailed Analysis
- Comprehensive case analysis
- Strengths and weaknesses
- Opponent analysis
- Legal and factual issues

### Strategic Plan
- Phased litigation strategy
- Discovery plan
- Motion strategy
- Trial strategy
- Settlement approach

### Risk Assessment
- Risk factors identified
- Probability assessments
- Mitigation strategies
- Contingency plans

### Economic Analysis
- Cost projections
- Damages assessment
- Expected value
- ROI analysis

### Recommendations
- Primary recommendation
- Alternative approaches
- Key action items
- Decision points

Provide practical, actionable strategic guidance that balances legal analysis
with business considerations and client objectives.
"""

    def analyze_case_strategy(self, case_data: dict) -> str:
        """
        Comprehensive case strategy analysis

        Args:
            case_data: Dictionary containing:
                - case_overview: Case description
                - client_position: Plaintiff or defendant
                - facts: Key facts
                - legal_issues: Legal claims/defenses
                - evidence: Available evidence
                - opposing_party: Information about opponent
                - objectives: Client's goals

        Returns:
            Comprehensive strategic analysis
        """
        prompt = self._format_strategy_analysis_prompt(case_data)
        logger.info(f"Analyzing litigation strategy for: {case_data.get('case_overview', 'Unknown')[:50]}")

        try:
            response = self.agent.run(prompt)
            logger.info("Strategy analysis completed")
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Strategy analysis failed: {str(e)}")
            raise

    def predict_case_outcome(self, case_data: dict) -> str:
        """
        Predict likely case outcomes

        Args:
            case_data: Case information for prediction

        Returns:
            Outcome prediction analysis
        """
        prompt = f"""
Predict the likely outcome of the following case:

## Case Information
**Case Type**: {case_data.get('case_type', 'Unknown')}
**Our Position**: {case_data.get('client_position', 'Not specified')}
**Jurisdiction**: {case_data.get('jurisdiction', 'Not specified')}
**Court**: {case_data.get('court', 'Not specified')}
**Judge**: {case_data.get('judge', 'Not specified')}

## Facts Summary
{case_data.get('facts', 'Not provided')}

## Legal Claims/Defenses
{case_data.get('legal_issues', 'Not provided')}

## Evidence Strength
**Our Evidence**: {case_data.get('our_evidence_strength', 'Not assessed')}
**Opponent Evidence**: {case_data.get('opponent_evidence_strength', 'Not assessed')}

## Similar Cases
{self._format_similar_cases(case_data.get('similar_cases', []))}

## Prediction Task
Provide detailed outcome prediction including:

1. **Liability Assessment** (0-100%)
   - Likelihood of prevailing on each claim/defense
   - Key factors affecting outcome
   - Comparison to similar cases

2. **Damages Projection**
   - Best case scenario
   - Most likely scenario
   - Worst case scenario
   - Damages range and rationale

3. **Settlement Value**
   - Estimated settlement range
   - Factors affecting settlement value
   - Optimal settlement timing

4. **Timeline Projection**
   - Time to trial estimate
   - Key milestones and dates
   - Factors affecting timeline

5. **Cost Projection**
   - Estimated legal fees to trial
   - Additional costs (experts, etc.)
   - Total estimated spend

6. **Expected Value Analysis**
   - Calculate expected value
   - ROI of litigation vs. settlement
   - Risk-adjusted recommendation

7. **Confidence Level**
   - Confidence in predictions
   - Key unknowns and uncertainties
   - What additional information would improve prediction

Provide specific percentages and dollar amounts with supporting reasoning.
"""

        logger.info("Predicting case outcome")

        try:
            response = self.agent.run(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Outcome prediction failed: {str(e)}")
            raise

    def develop_discovery_plan(self, discovery_data: dict) -> str:
        """
        Develop comprehensive discovery plan

        Args:
            discovery_data: Information for discovery planning

        Returns:
            Detailed discovery plan
        """
        prompt = f"""
Develop a comprehensive discovery plan:

## Case Context
**Case Type**: {discovery_data.get('case_type', 'Unknown')}
**Key Issues**: {', '.join(discovery_data.get('key_issues', []))}
**Discovery Deadline**: {discovery_data.get('discovery_deadline', 'Not specified')}
**Budget**: {discovery_data.get('budget', 'Not specified')}

## Information Needs
**What We Need to Prove**: {discovery_data.get('proof_needed', 'Not specified')}
**Information Gaps**: {discovery_data.get('information_gaps', 'Not specified')}
**Opponent's Weaknesses to Explore**: {discovery_data.get('opponent_weaknesses', 'Not specified')}

## Available Discovery Methods
- Document requests
- Interrogatories
- Depositions
- Requests for admission
- Subpoenas
- Expert discovery

## Discovery Plan Task
Develop comprehensive, phased discovery plan including:

1. **Discovery Objectives**
   - What information to obtain
   - What admissions to secure
   - What weaknesses to expose

2. **Document Discovery**
   - Priority document categories
   - Specific document requests
   - Timing and sequence
   - Anticipated objections

3. **Interrogatories**
   - Key interrogatory topics
   - Specific interrogatory questions
   - Strategic use of interrogatories

4. **Deposition Strategy**
   - Deposition targets (priority order)
   - Objectives for each deposition
   - Deposition sequence and timing
   - Key topics and questions

5. **Third-Party Discovery**
   - Third-party document sources
   - Subpoena targets
   - Timing considerations

6. **Expert Discovery**
   - Our expert needs
   - Opposing expert discovery
   - Daubert challenges to consider

7. **Defensive Strategy**
   - Anticipated discovery requests
   - Objection strategy
   - Privilege protections
   - Motion to compel defense

8. **Timeline and Budget**
   - Phased discovery schedule
   - Cost estimates by phase
   - Resource allocation

9. **Discovery Management**
   - Document review approach
   - Organization system
   - Team assignments

Provide specific, actionable plan with priorities and timeline.
"""

        logger.info("Developing discovery plan")

        try:
            response = self.agent.run(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Discovery planning failed: {str(e)}")
            raise

    def assess_settlement_value(self, settlement_data: dict) -> str:
        """
        Assess fair settlement value

        Args:
            settlement_data: Information for settlement valuation

        Returns:
            Settlement value analysis
        """
        prompt = f"""
Assess settlement value for:

## Case Information
**Case Type**: {settlement_data.get('case_type', 'Unknown')}
**Our Position**: {settlement_data.get('client_position', 'Not specified')}
**Stage**: {settlement_data.get('case_stage', 'Not specified')}

## Liability Assessment
**Likelihood of Prevailing**: {settlement_data.get('win_probability', 'Not assessed')}
**Strength of Case**: {settlement_data.get('case_strength', 'Not assessed')}

## Damages Analysis
**Economic Damages**: {settlement_data.get('economic_damages', 'Not specified')}
**Non-Economic Damages**: {settlement_data.get('non_economic_damages', 'Not specified')}
**Punitive Damages**: {settlement_data.get('punitive_potential', 'Not applicable')}

## Costs and Risks
**Legal Fees to Trial**: {settlement_data.get('fees_to_trial', 'Not estimated')}
**Appeal Risk**: {settlement_data.get('appeal_risk', 'Not assessed')}
**Business Impact**: {settlement_data.get('business_impact', 'Not specified')}

## Settlement Context
**Prior Offers**: {settlement_data.get('prior_offers', 'None')}
**Opponent's Position**: {settlement_data.get('opponent_position', 'Unknown')}
**Mediation Scheduled**: {settlement_data.get('mediation', 'No')}

## Valuation Task
Provide comprehensive settlement valuation including:

1. **Expected Value Calculation**
   - Probability-weighted damages
   - Cost considerations
   - Risk adjustments
   - Expected value range

2. **Settlement Range**
   - Minimum acceptable settlement
   - Target settlement value
   - Maximum exposure
   - Justification for range

3. **Timing Considerations**
   - Optimal settlement timing
   - How value changes over time
   - Deadline pressures

4. **Leverage Analysis**
   - Our leverage points
   - Opponent's leverage
   - How to maximize leverage

5. **Negotiation Strategy**
   - Opening offer/demand
   - Concession approach
   - Bottom line
   - Creative deal structures

6. **Recommendation**
   - Settle now vs. continue litigation
   - Acceptable settlement terms
   - Deal breakers
   - Next steps

Provide specific dollar amounts with detailed supporting analysis.
"""

        logger.info("Assessing settlement value")

        try:
            response = self.agent.run(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Settlement valuation failed: {str(e)}")
            raise

    def develop_trial_strategy(self, trial_data: dict) -> str:
        """
        Develop comprehensive trial strategy

        Args:
            trial_data: Information for trial planning

        Returns:
            Detailed trial strategy
        """
        prompt = f"""
Develop comprehensive trial strategy:

## Trial Information
**Trial Date**: {trial_data.get('trial_date', 'Not set')}
**Trial Type**: {trial_data.get('trial_type', 'Jury trial')}
**Estimated Duration**: {trial_data.get('duration', 'Not estimated')}
**Judge**: {trial_data.get('judge', 'Not specified')}

## Case Theme
**Our Theory**: {trial_data.get('case_theory', 'Not developed')}
**Key Messages**: {', '.join(trial_data.get('key_messages', []))}

## Evidence
**Key Documents**: {trial_data.get('key_documents', 'Not specified')}
**Physical Evidence**: {trial_data.get('physical_evidence', 'None')}

## Witnesses
**Our Witnesses**: {self._format_witness_list(trial_data.get('our_witnesses', []))}
**Opposing Witnesses**: {self._format_witness_list(trial_data.get('opposing_witnesses', []))}
**Expert Witnesses**: {self._format_witness_list(trial_data.get('experts', []))}

## Trial Strategy Task
Develop comprehensive trial strategy including:

1. **Case Narrative**
   - Compelling story arc
   - Central theme
   - Key messages
   - Emotional appeals (if appropriate)

2. **Opening Statement Strategy**
   - Opening structure
   - Key points to make
   - Visual aids
   - Tone and approach

3. **Witness Strategy**
   - Witness order and rationale
   - Direct examination approach for each witness
   - Key testimony to elicit
   - Rehabilitation strategies

4. **Cross-Examination Strategy**
   - Priority cross-examination targets
   - Objectives for each witness
   - Key impeachment opportunities
   - Cross-examination structure

5. **Expert Witness Presentation**
   - How to present our experts
   - How to attack opposing experts
   - Daubert issues
   - Simplifying complex testimony

6. **Documentary Evidence**
   - Exhibit list priorities
   - Admission strategy
   - Demonstrative exhibits
   - Technology use

7. **Motions in Limine**
   - Motions to file
   - Evidence to exclude
   - Evidence to protect

8. **Jury Selection** (if applicable)
   - Ideal juror profile
   - Voir dire strategy
   - Challenge strategy
   - Jury questionnaire

9. **Closing Argument Strategy**
   - Argument structure
   - Key points to emphasize
   - Anticipated defense arguments
   - Damage presentation

10. **Contingency Planning**
    - If key evidence excluded
    - If witness testimony goes poorly
    - If judge rules unfavorably
    - Alternative approaches

Provide detailed, actionable trial plan with specific recommendations.
"""

        logger.info("Developing trial strategy")

        try:
            response = self.agent.run(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Trial strategy development failed: {str(e)}")
            raise

    def _format_strategy_analysis_prompt(self, case_data: dict) -> str:
        """Format comprehensive strategy analysis prompt"""
        prompt = f"""
Conduct comprehensive litigation strategy analysis:

## Case Overview
**Case Name**: {case_data.get('case_name', 'Unknown')}
**Case Type**: {case_data.get('case_type', 'Unknown')}
**Our Position**: {case_data.get('client_position', 'Not specified')}
**Current Stage**: {case_data.get('case_stage', 'Not specified')}

## Facts
{case_data.get('facts', 'Not provided')}

## Legal Issues
{case_data.get('legal_issues', 'Not provided')}

## Evidence
**Our Evidence**: {case_data.get('our_evidence', 'Not specified')}
**Opponent's Evidence**: {case_data.get('opponent_evidence', 'Not specified')}

## Parties
**Our Client**: {case_data.get('client_info', 'Not specified')}
**Opposing Party**: {case_data.get('opposing_party', 'Not specified')}
**Opposing Counsel**: {case_data.get('opposing_counsel', 'Not specified')}

## Objectives
**Client Goals**: {case_data.get('objectives', 'Not specified')}
**Budget**: {case_data.get('budget', 'Not specified')}
**Risk Tolerance**: {case_data.get('risk_tolerance', 'Not specified')}

## Strategic Analysis Task
Provide comprehensive strategic analysis following your analytical framework.
Include:
- Executive summary with key recommendations
- Detailed case analysis (strengths/weaknesses)
- Opponent analysis
- Strategic plan (discovery, motions, trial, settlement)
- Risk assessment
- Economic analysis
- Specific recommendations with rationale

Ensure analysis is practical, realistic, and aligned with client objectives.
"""
        return prompt

    def _format_similar_cases(self, cases: list) -> str:
        """Format similar cases"""
        if not cases:
            return "No similar cases provided"

        formatted = ""
        for case in cases:
            if isinstance(case, dict):
                formatted += f"- {case.get('name', 'Unknown')}: {case.get('outcome', 'Unknown outcome')}\n"
            else:
                formatted += f"- {case}\n"
        return formatted

    def _format_witness_list(self, witnesses: list) -> str:
        """Format witness list"""
        if not witnesses:
            return "None specified"

        return ", ".join([w if isinstance(w, str) else w.get('name', 'Unknown') for w in witnesses])


# Global agent instance
litigation_agent = LitigationStrategyAgent()
