"""
Interactive Web Interface for Legal Intelligence System
Built with Streamlit for user-friendly interaction
"""
import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from utils.database import db
from utils.validators import validators
from agents.orchestrator import orchestrator
from human_intervention.approval_manager import approval_manager
from human_intervention.feedback_handler import feedback_handler
import logging

logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title=config.APP_NAME,
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main application entry point"""

    # Sidebar
    st.sidebar.title("⚖️ Legal Intelligence")
    st.sidebar.markdown(f"**Version:** {config.APP_VERSION}")

    # Main navigation
    page = st.sidebar.selectbox(
        "Navigation",
        [
            "Dashboard",
            "Case Law Research",
            "Contract Analysis",
            "Compliance Assessment",
            "Legal Drafting",
            "Litigation Strategy",
            "Case Management",
            "Document Library",
            "Research Sessions",
            "System Status"
        ]
    )

    # Lawyer selection
    st.sidebar.markdown("---")
    lawyers = db.get_all_lawyers()
    if lawyers:
        lawyer_options = {f"{l['name']} ({l['bar_number']})": l['id'] for l in lawyers}
        selected_lawyer = st.sidebar.selectbox("Select Lawyer", list(lawyer_options.keys()))
        lawyer_id = lawyer_options[selected_lawyer]
    else:
        st.sidebar.warning("No lawyers in database. Please add a lawyer first.")
        lawyer_id = None

    # Route to appropriate page
    if page == "Dashboard":
        show_dashboard(lawyer_id)
    elif page == "Case Law Research":
        show_case_law_research(lawyer_id)
    elif page == "Contract Analysis":
        show_contract_analysis(lawyer_id)
    elif page == "Compliance Assessment":
        show_compliance_assessment(lawyer_id)
    elif page == "Legal Drafting":
        show_legal_drafting(lawyer_id)
    elif page == "Litigation Strategy":
        show_litigation_strategy(lawyer_id)
    elif page == "Case Management":
        show_case_management(lawyer_id)
    elif page == "Document Library":
        show_document_library(lawyer_id)
    elif page == "Research Sessions":
        show_research_sessions(lawyer_id)
    elif page == "System Status":
        show_system_status()


def show_dashboard(lawyer_id):
    """Show main dashboard"""
    st.title("📊 Legal Intelligence Dashboard")

    if not lawyer_id:
        st.warning("Please add a lawyer to the system to view dashboard.")
        show_add_lawyer_form()
        return

    # Get lawyer summary
    summary = orchestrator.get_lawyer_summary(lawyer_id)
    lawyer = summary['lawyer']

    # Header
    st.markdown(f"## Welcome, {lawyer['name']}")
    st.markdown(f"**Firm:** {lawyer.get('firm', 'N/A')} | **Bar Number:** {lawyer['bar_number']} | **Experience:** {lawyer.get('years_experience', 'N/A')} years")

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Cases", summary['total_cases'])
    with col2:
        st.metric("Active Cases", summary['active_cases'])
    with col3:
        st.metric("Win Rate", f"{summary['win_rate']:.1f}%")
    with col4:
        st.metric("Research Sessions", summary['research_sessions'])

    # Recent Cases
    st.markdown("---")
    st.subheader("📁 Recent Cases")

    if summary['recent_cases']:
        for case in summary['recent_cases']:
            with st.expander(f"{case['case_number']} - {case['title']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Type:** {case.get('case_type', 'N/A')}")
                    st.markdown(f"**Status:** {case.get('status', 'N/A')}")
                    st.markdown(f"**Court:** {case.get('court', 'N/A')}")
                with col2:
                    st.markdown(f"**Filed:** {case.get('filing_date', 'N/A')}")
                    st.markdown(f"**Practice Area:** {case.get('practice_area', 'N/A')}")
                    st.markdown(f"**Jurisdiction:** {case.get('jurisdiction', 'N/A')}")
    else:
        st.info("No cases found. Add a case to get started.")

    # Quick Actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔍 Research Case Law", use_container_width=True):
            st.session_state.page = "Case Law Research"
            st.rerun()

    with col2:
        if st.button("📄 Draft Document", use_container_width=True):
            st.session_state.page = "Legal Drafting"
            st.rerun()

    with col3:
        if st.button("⚖️ Analyze Contract", use_container_width=True):
            st.session_state.page = "Contract Analysis"
            st.rerun()


def show_case_law_research(lawyer_id):
    """Show case law research interface"""
    st.title("🔍 Case Law Research")

    if not lawyer_id:
        st.warning("Please select a lawyer to perform research.")
        return

    st.markdown("Research relevant case law and precedents using AI-powered analysis.")

    # Research form
    with st.form("case_law_research_form"):
        st.subheader("Research Parameters")

        legal_issue = st.text_area(
            "Legal Issue",
            placeholder="Describe the legal issue you're researching...",
            height=100
        )

        col1, col2 = st.columns(2)
        with col1:
            jurisdiction = st.selectbox("Jurisdiction", ["Federal", "State", "Local", "International"])
            practice_area = st.selectbox("Practice Area", config.DEFAULT_PRACTICE_AREAS)

        with col2:
            case_id = st.selectbox(
                "Related Case (Optional)",
                ["None"] + [f"{c['case_number']} - {c['title']}" for c in db.get_lawyer_cases(lawyer_id)]
            )

        current_facts = st.text_area(
            "Current Facts (Optional)",
            placeholder="Provide facts of your current case for context...",
            height=100
        )

        submit = st.form_submit_button("🔍 Research Precedents", use_container_width=True)

    if submit:
        if not legal_issue:
            st.error("Please provide a legal issue to research.")
        else:
            with st.spinner("Researching case law... This may take a moment."):
                try:
                    # Get case ID if selected
                    selected_case_id = None
                    if case_id != "None":
                        case_number = case_id.split(" - ")[0]
                        cases = db.get_lawyer_cases(lawyer_id)
                        for c in cases:
                            if c['case_number'] == case_number:
                                selected_case_id = c['id']
                                break

                    # Perform research
                    result = orchestrator.research_case_law(
                        lawyer_id,
                        legal_issue=legal_issue,
                        jurisdiction=jurisdiction,
                        practice_area=practice_area,
                        current_facts=current_facts if current_facts else None,
                        case_id=selected_case_id
                    )

                    st.success("✅ Research completed!")
                    st.markdown("---")
                    st.markdown(result)

                    # Feedback
                    st.markdown("---")
                    with st.expander("📝 Provide Feedback"):
                        rating = st.slider("Rate this analysis", 1, 5, 3)
                        comments = st.text_area("Comments (Optional)")
                        if st.button("Submit Feedback"):
                            feedback_handler.submit_feedback(
                                content_id=f"research_{lawyer_id}_{legal_issue[:20]}",
                                content_type="case_law_research",
                                user_id=lawyer_id,
                                rating=rating,
                                comments=comments
                            )
                            st.success("Thank you for your feedback!")

                except Exception as e:
                    st.error(f"Research failed: {str(e)}")


def show_contract_analysis(lawyer_id):
    """Show contract analysis interface"""
    st.title("📄 Contract Analysis")

    if not lawyer_id:
        st.warning("Please select a lawyer to analyze contracts.")
        return

    st.markdown("Analyze contracts for risks, compliance, and favorable terms using AI.")

    # Analysis type
    analysis_type = st.radio(
        "Analysis Type",
        ["Analyze New Contract", "Review Existing Contract"]
    )

    if analysis_type == "Analyze New Contract":
        with st.form("contract_analysis_form"):
            st.subheader("Contract Details")

            contract_name = st.text_input("Contract Name")
            contract_type = st.selectbox(
                "Contract Type",
                ["Services Agreement", "Sale Agreement", "License Agreement", "NDA", "Employment Agreement", "Other"]
            )

            col1, col2 = st.columns(2)
            with col1:
                party_role = st.selectbox("Our Role", ["Buyer", "Seller", "Licensor", "Licensee", "Employer", "Employee"])
                jurisdiction = st.text_input("Jurisdiction", "Federal")

            with col2:
                industry = st.text_input("Industry", "General")
                parties = st.text_input("Contracting Parties", "Party A, Party B")

            contract_text = st.text_area(
                "Contract Text",
                placeholder="Paste the full contract text here...",
                height=300
            )

            submit = st.form_submit_button("🔍 Analyze Contract", use_container_width=True)

        if submit:
            if not contract_text or not contract_name:
                st.error("Please provide contract name and text.")
            else:
                with st.spinner("Analyzing contract... This may take a moment."):
                    try:
                        result = orchestrator.analyze_contract(
                            lawyer_id,
                            contract_name=contract_name,
                            contract_type=contract_type,
                            contract_text=contract_text,
                            parties=parties,
                            party_role=party_role,
                            jurisdiction=jurisdiction,
                            industry=industry
                        )

                        st.success("✅ Analysis completed!")
                        st.markdown("---")
                        st.markdown(result)

                        # Feedback
                        st.markdown("---")
                        with st.expander("📝 Provide Feedback"):
                            rating = st.slider("Rate this analysis", 1, 5, 3)
                            comments = st.text_area("Comments (Optional)")
                            if st.button("Submit Feedback"):
                                feedback_handler.submit_feedback(
                                    content_id=f"contract_{contract_name}",
                                    content_type="contract_analysis",
                                    user_id=lawyer_id,
                                    rating=rating,
                                    comments=comments
                                )
                                st.success("Thank you for your feedback!")

                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")

    else:  # Review Existing Contract
        documents = db.get_all_lawyers()  # Get documents for lawyer
        if documents:
            doc_options = [f"{d['title']} (ID: {d['id']})" for d in documents if d.get('document_type') in ['contract', 'agreement']]
            if doc_options:
                selected_doc = st.selectbox("Select Contract", doc_options)

                if st.button("🔍 Analyze Selected Contract"):
                    doc_id = int(selected_doc.split("ID: ")[1].rstrip(")"))
                    with st.spinner("Analyzing contract..."):
                        try:
                            result = orchestrator.analyze_contract(lawyer_id, contract_id=doc_id)
                            st.success("✅ Analysis completed!")
                            st.markdown("---")
                            st.markdown(result)
                        except Exception as e:
                            st.error(f"Analysis failed: {str(e)}")
            else:
                st.info("No contracts found in document library.")
        else:
            st.info("No documents found. Upload or create a contract first.")


def show_compliance_assessment(lawyer_id):
    """Show compliance assessment interface"""
    st.title("✅ Compliance Assessment")

    if not lawyer_id:
        st.warning("Please select a lawyer to perform compliance assessment.")
        return

    st.markdown("Assess regulatory compliance and identify compliance gaps.")

    with st.form("compliance_form"):
        st.subheader("Compliance Parameters")

        organization = st.text_input("Organization Name")
        industry = st.selectbox(
            "Industry",
            ["Healthcare", "Financial Services", "Technology", "Manufacturing", "Retail", "Other"]
        )

        col1, col2 = st.columns(2)
        with col1:
            jurisdictions = st.multiselect("Jurisdictions", ["Federal", "State", "Local", "International"])
        with col2:
            frameworks = st.multiselect("Compliance Frameworks", config.COMPLIANCE_FRAMEWORKS)

        scope = st.multiselect(
            "Assessment Scope",
            ["Data Privacy", "Financial Compliance", "Employment Law", "Environmental", "Industry-Specific"]
        )

        current_practices = st.text_area(
            "Current Compliance Practices",
            placeholder="Describe your current compliance program and practices...",
            height=150
        )

        submit = st.form_submit_button("🔍 Assess Compliance", use_container_width=True)

    if submit:
        if not organization:
            st.error("Please provide organization name.")
        else:
            with st.spinner("Assessing compliance... This may take a moment."):
                try:
                    result = orchestrator.assess_compliance(
                        lawyer_id,
                        organization=organization,
                        industry=industry,
                        jurisdictions=jurisdictions,
                        frameworks=frameworks,
                        scope=scope,
                        current_practices=current_practices
                    )

                    st.success("✅ Assessment completed!")
                    st.markdown("---")
                    st.markdown(result)

                    # Feedback
                    st.markdown("---")
                    with st.expander("📝 Provide Feedback"):
                        rating = st.slider("Rate this assessment", 1, 5, 3)
                        comments = st.text_area("Comments (Optional)")
                        if st.button("Submit Feedback"):
                            feedback_handler.submit_feedback(
                                content_id=f"compliance_{organization}",
                                content_type="compliance_assessment",
                                user_id=lawyer_id,
                                rating=rating,
                                comments=comments
                            )
                            st.success("Thank you for your feedback!")

                except Exception as e:
                    st.error(f"Assessment failed: {str(e)}")


def show_legal_drafting(lawyer_id):
    """Show legal drafting interface"""
    st.title("✍️ Legal Drafting")

    if not lawyer_id:
        st.warning("Please select a lawyer to draft documents.")
        return

    st.markdown("Draft legal documents using AI assistance.")

    document_type = st.selectbox(
        "Document Type",
        ["Legal Memorandum", "Motion", "Demand Letter", "Contract Clause"]
    )

    if document_type == "Legal Memorandum":
        show_memo_drafting(lawyer_id)
    elif document_type == "Motion":
        show_motion_drafting(lawyer_id)
    elif document_type == "Demand Letter":
        show_demand_letter_drafting(lawyer_id)
    elif document_type == "Contract Clause":
        show_clause_drafting(lawyer_id)


def show_memo_drafting(lawyer_id):
    """Show memo drafting form"""
    with st.form("memo_form"):
        st.subheader("Legal Memorandum Details")

        col1, col2 = st.columns(2)
        with col1:
            recipient = st.text_input("To", "Senior Partner")
            author = st.text_input("From", "Associate")
        with col2:
            subject = st.text_input("Re", "Legal Research Memorandum")
            date = st.date_input("Date")

        question = st.text_area("Question Presented", height=100)
        facts = st.text_area("Facts", height=150)

        col1, col2 = st.columns(2)
        with col1:
            jurisdiction = st.text_input("Jurisdiction")
        with col2:
            statutes = st.text_input("Applicable Statutes (comma-separated)")

        submit = st.form_submit_button("✍️ Draft Memorandum", use_container_width=True)

    if submit:
        if not question or not facts:
            st.error("Please provide question and facts.")
        else:
            with st.spinner("Drafting memorandum..."):
                try:
                    result = orchestrator.draft_legal_document(
                        lawyer_id,
                        'memo',
                        recipient=recipient,
                        author=author,
                        subject=subject,
                        date=str(date),
                        question=question,
                        facts=facts,
                        jurisdiction=jurisdiction,
                        statutes=statutes.split(',') if statutes else []
                    )

                    st.success("✅ Memorandum drafted!")
                    st.markdown("---")
                    st.markdown(result)

                except Exception as e:
                    st.error(f"Drafting failed: {str(e)}")


def show_motion_drafting(lawyer_id):
    """Show motion drafting form"""
    with st.form("motion_form"):
        st.subheader("Motion Details")

        col1, col2 = st.columns(2)
        with col1:
            court = st.text_input("Court")
            case_number = st.text_input("Case Number")
        with col2:
            case_caption = st.text_input("Case Caption")
            motion_type = st.text_input("Motion Type", "Motion for Summary Judgment")

        relief_sought = st.text_area("Relief Sought", height=100)
        facts = st.text_area("Factual Background", height=150)
        arguments = st.text_area("Key Arguments (one per line)", height=100)

        submit = st.form_submit_button("✍️ Draft Motion", use_container_width=True)

    if submit:
        if not motion_type or not relief_sought:
            st.error("Please provide motion type and relief sought.")
        else:
            with st.spinner("Drafting motion..."):
                try:
                    result = orchestrator.draft_legal_document(
                        lawyer_id,
                        'motion',
                        court=court,
                        case_number=case_number,
                        case_caption=case_caption,
                        motion_type=motion_type,
                        relief_sought=relief_sought,
                        facts=facts,
                        arguments=arguments.split('\n') if arguments else []
                    )

                    st.success("✅ Motion drafted!")
                    st.markdown("---")
                    st.markdown(result)

                except Exception as e:
                    st.error(f"Drafting failed: {str(e)}")


def show_demand_letter_drafting(lawyer_id):
    """Show demand letter drafting form"""
    with st.form("demand_letter_form"):
        st.subheader("Demand Letter Details")

        col1, col2 = st.columns(2)
        with col1:
            client_name = st.text_input("Client Name")
            recipient_name = st.text_input("Recipient Name")
        with col2:
            recipient_address = st.text_input("Recipient Address")
            subject = st.text_input("Subject")

        facts = st.text_area("Facts", height=150)
        legal_basis = st.text_area("Legal Basis", height=100)
        demand = st.text_input("Demand")
        deadline = st.date_input("Response Deadline")

        submit = st.form_submit_button("✍️ Draft Demand Letter", use_container_width=True)

    if submit:
        if not recipient_name or not demand:
            st.error("Please provide recipient and demand.")
        else:
            with st.spinner("Drafting demand letter..."):
                try:
                    result = orchestrator.draft_legal_document(
                        lawyer_id,
                        'demand_letter',
                        client_name=client_name,
                        recipient_name=recipient_name,
                        recipient_address=recipient_address,
                        subject=subject,
                        facts=facts,
                        legal_basis=legal_basis,
                        demand=demand,
                        deadline=str(deadline)
                    )

                    st.success("✅ Demand letter drafted!")
                    st.markdown("---")
                    st.markdown(result)

                except Exception as e:
                    st.error(f"Drafting failed: {str(e)}")


def show_clause_drafting(lawyer_id):
    """Show contract clause drafting form"""
    with st.form("clause_form"):
        st.subheader("Contract Clause Details")

        clause_type = st.selectbox(
            "Clause Type",
            ["Indemnification", "Limitation of Liability", "Termination", "Payment Terms",
             "Intellectual Property", "Confidentiality", "Force Majeure", "Dispute Resolution"]
        )

        purpose = st.text_area("Purpose of Clause", height=100)

        col1, col2 = st.columns(2)
        with col1:
            contract_type = st.text_input("Contract Type", "General")
            party_favored = st.selectbox("Party Favored", ["Balanced", "Our Client", "Counterparty"])
        with col2:
            jurisdiction = st.text_input("Jurisdiction")
            industry = st.text_input("Industry")

        requirements = st.text_area("Specific Requirements", height=100)

        submit = st.form_submit_button("✍️ Draft Clause", use_container_width=True)

    if submit:
        if not purpose:
            st.error("Please provide the purpose of the clause.")
        else:
            with st.spinner("Drafting clause..."):
                try:
                    result = orchestrator.draft_legal_document(
                        lawyer_id,
                        'contract_clause',
                        clause_type=clause_type,
                        purpose=purpose,
                        contract_type=contract_type,
                        party_favored=party_favored,
                        jurisdiction=jurisdiction,
                        industry=industry,
                        requirements=requirements
                    )

                    st.success("✅ Clause drafted!")
                    st.markdown("---")
                    st.markdown(result)

                except Exception as e:
                    st.error(f"Drafting failed: {str(e)}")


def show_litigation_strategy(lawyer_id):
    """Show litigation strategy interface"""
    st.title("⚖️ Litigation Strategy")

    if not lawyer_id:
        st.warning("Please select a lawyer.")
        return

    st.markdown("Develop comprehensive litigation strategy using AI analysis.")

    # Select case
    cases = db.get_lawyer_cases(lawyer_id)
    if not cases:
        st.info("No cases found. Please add a case first.")
        return

    case_options = {f"{c['case_number']} - {c['title']}": c['id'] for c in cases}
    selected_case = st.selectbox("Select Case", list(case_options.keys()))
    case_id = case_options[selected_case]

    strategy_type = st.radio(
        "Strategy Type",
        ["Comprehensive Strategy", "Outcome Prediction", "Settlement Valuation"]
    )

    if st.button("🔍 Generate Strategy", use_container_width=True):
        with st.spinner("Developing strategy... This may take a moment."):
            try:
                result = orchestrator.develop_litigation_strategy(lawyer_id, case_id)

                st.success("✅ Strategy developed!")
                st.markdown("---")
                st.markdown(result)

                # Feedback
                st.markdown("---")
                with st.expander("📝 Provide Feedback"):
                    rating = st.slider("Rate this strategy", 1, 5, 3)
                    comments = st.text_area("Comments (Optional)")
                    if st.button("Submit Feedback"):
                        feedback_handler.submit_feedback(
                            content_id=f"strategy_{case_id}",
                            content_type="litigation_strategy",
                            user_id=lawyer_id,
                            rating=rating,
                            comments=comments
                        )
                        st.success("Thank you for your feedback!")

            except Exception as e:
                st.error(f"Strategy development failed: {str(e)}")


def show_case_management(lawyer_id):
    """Show case management interface"""
    st.title("📁 Case Management")

    if not lawyer_id:
        st.warning("Please select a lawyer.")
        return

    tab1, tab2, tab3 = st.tabs(["View Cases", "Add Case", "Case Details"])

    with tab1:
        cases = db.get_lawyer_cases(lawyer_id)
        if cases:
            for case in cases:
                with st.expander(f"{case['case_number']} - {case['title']}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**Type:** {case.get('case_type', 'N/A')}")
                        st.markdown(f"**Status:** {case.get('status', 'N/A')}")
                    with col2:
                        st.markdown(f"**Court:** {case.get('court', 'N/A')}")
                        st.markdown(f"**Filed:** {case.get('filing_date', 'N/A')}")
                    with col3:
                        st.markdown(f"**Practice Area:** {case.get('practice_area', 'N/A')}")
                        st.markdown(f"**Jurisdiction:** {case.get('jurisdiction', 'N/A')}")
        else:
            st.info("No cases found.")

    with tab2:
        show_add_case_form(lawyer_id)

    with tab3:
        if cases:
            case_options = {f"{c['case_number']} - {c['title']}": c['id'] for c in cases}
            selected = st.selectbox("Select Case", list(case_options.keys()))
            case_id = case_options[selected]

            case = db.get_case_by_id(case_id)
            if case:
                st.json(case)


def show_document_library(lawyer_id):
    """Show document library"""
    st.title("📚 Document Library")

    if not lawyer_id:
        st.warning("Please select a lawyer.")
        return

    st.info("Document library functionality - lists all legal documents.")


def show_research_sessions(lawyer_id):
    """Show research sessions"""
    st.title("🔬 Research Sessions")

    if not lawyer_id:
        st.warning("Please select a lawyer.")
        return

    sessions = db.get_lawyer_research_sessions(lawyer_id)

    if sessions:
        for session in sessions:
            with st.expander(f"{session['session_name']} - {session['session_date']}"):
                st.markdown(f"**Practice Area:** {session.get('practice_area', 'N/A')}")
                st.markdown(f"**Jurisdiction:** {session.get('jurisdiction', 'N/A')}")
                st.markdown(f"**Query:** {session.get('research_query', 'N/A')}")
                st.markdown(f"**Findings:** {session.get('findings', 'N/A')[:200]}...")
    else:
        st.info("No research sessions found.")


def show_system_status():
    """Show system status"""
    st.title("⚙️ System Status")

    # Database stats
    st.subheader("📊 Database Statistics")
    stats = db.get_database_stats()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Lawyers", stats.get('lawyers_count', 0))
        st.metric("Cases", stats.get('cases_count', 0))
    with col2:
        st.metric("Documents", stats.get('legal_documents_count', 0))
        st.metric("Statutes", stats.get('statutes_count', 0))
    with col3:
        st.metric("Precedents", stats.get('precedents_count', 0))
        st.metric("Contracts", stats.get('contracts_count', 0))
    with col4:
        st.metric("Deadlines", stats.get('deadlines_count', 0))
        st.metric("Research Sessions", stats.get('research_sessions_count', 0))

    # Configuration
    st.markdown("---")
    st.subheader("⚙️ Configuration")
    config_summary = config.get_config_summary()
    st.json(config_summary)

    # Validation
    st.markdown("---")
    st.subheader("✅ Configuration Validation")
    issues = config.validate_config()
    if issues:
        st.warning("Configuration Issues:")
        for issue in issues:
            st.markdown(f"- {issue}")
    else:
        st.success("✅ Configuration is valid")


def show_add_lawyer_form():
    """Show form to add a lawyer"""
    with st.form("add_lawyer_form"):
        st.subheader("Add New Lawyer")

        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name *")
            bar_number = st.text_input("Bar Number *")
            firm = st.text_input("Firm")
        with col2:
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            years_exp = st.number_input("Years of Experience", min_value=0, max_value=70, value=0)

        practice_areas = st.multiselect("Practice Areas *", config.DEFAULT_PRACTICE_AREAS)
        jurisdiction = st.selectbox("Primary Jurisdiction *", ["Federal", "State", "Local", "International"])
        specializations = st.text_input("Specializations (comma-separated)")

        submit = st.form_submit_button("Add Lawyer")

    if submit:
        lawyer_data = {
            'name': name,
            'bar_number': bar_number,
            'firm': firm,
            'practice_areas': ','.join(practice_areas),
            'jurisdiction': jurisdiction,
            'years_experience': years_exp,
            'specializations': specializations,
            'email': email,
            'phone': phone
        }

        errors = validators.validate_lawyer_data(lawyer_data)
        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                lawyer_id = db.add_lawyer(lawyer_data)
                st.success(f"✅ Lawyer added successfully! (ID: {lawyer_id})")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to add lawyer: {str(e)}")


def show_add_case_form(lawyer_id):
    """Show form to add a case"""
    with st.form("add_case_form"):
        st.subheader("Add New Case")

        col1, col2 = st.columns(2)
        with col1:
            case_number = st.text_input("Case Number *", placeholder="CV-2024-001234")
            title = st.text_input("Title *")
            case_type = st.selectbox("Case Type *", ["Civil", "Criminal", "Administrative", "Family", "Bankruptcy"])
        with col2:
            practice_area = st.selectbox("Practice Area *", config.DEFAULT_PRACTICE_AREAS)
            jurisdiction = st.selectbox("Jurisdiction *", ["Federal", "State", "Local"])
            court = st.text_input("Court *")

        col1, col2 = st.columns(2)
        with col1:
            filing_date = st.date_input("Filing Date")
            status = st.selectbox("Status", ["active", "pending", "closed", "settled"])
        with col2:
            client_name = st.text_input("Client Name")
            opposing_party = st.text_input("Opposing Party")

        case_summary = st.text_area("Case Summary", height=150)
        key_issues = st.text_area("Key Issues")

        submit = st.form_submit_button("Add Case")

    if submit:
        case_data = {
            'case_number': case_number,
            'title': title,
            'case_type': case_type,
            'practice_area': practice_area,
            'jurisdiction': jurisdiction,
            'court': court,
            'filing_date': str(filing_date),
            'status': status,
            'lawyer_id': lawyer_id,
            'client_name': client_name,
            'opposing_party': opposing_party,
            'case_summary': case_summary,
            'key_issues': key_issues
        }

        errors = validators.validate_case_data(case_data)
        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                case_id = db.add_case(case_data)
                st.success(f"✅ Case added successfully! (ID: {case_id})")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to add case: {str(e)}")


if __name__ == "__main__":
    main()
