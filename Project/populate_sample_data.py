"""
Populate Sample Data for Legal Intelligence System
Run this script to add sample lawyers, cases, documents, and more
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.database import db
from config import config

print("=" * 70)
print("  Legal Intelligence System - Sample Data Population")
print("=" * 70)
print()


def add_sample_lawyers():
    """Add sample lawyers"""
    print("Adding sample lawyers...")

    lawyers = [
        {
            'name': 'Sarah Mitchell',
            'bar_number': 'CA234567',
            'firm': 'Mitchell & Associates LLP',
            'practice_areas': 'Corporate Law,Intellectual Property,Contract Law',
            'jurisdiction': 'Federal',
            'years_experience': 15,
            'specializations': 'Mergers & Acquisitions, Patent Litigation, Technology Transactions',
            'email': 'sarah.mitchell@mitchelllaw.com',
            'phone': '5551234567',
            'win_rate': 0.82,
            'total_cases': 127
        },
        {
            'name': 'Marcus Johnson',
            'bar_number': 'NY345678',
            'firm': 'Johnson Legal Group',
            'practice_areas': 'Criminal Law,Civil Litigation,Personal Injury',
            'jurisdiction': 'State',
            'years_experience': 22,
            'specializations': 'White Collar Defense, Class Actions, Medical Malpractice',
            'email': 'mjohnson@johnsonlegal.com',
            'phone': '5552345678',
            'win_rate': 0.78,
            'total_cases': 215
        },
        {
            'name': 'Dr. Emily Chen',
            'bar_number': 'TX456789',
            'firm': 'Chen & Partners',
            'practice_areas': 'Employment Law,Immigration Law,Family Law',
            'jurisdiction': 'State',
            'years_experience': 10,
            'specializations': 'Employment Discrimination, Visa Applications, Custody Disputes',
            'email': 'emily.chen@chenpartners.com',
            'phone': '5553456789',
            'win_rate': 0.85,
            'total_cases': 89
        },
        {
            'name': 'Robert Davis',
            'bar_number': 'FL567890',
            'firm': 'Davis Environmental Law',
            'practice_areas': 'Environmental Law,Real Estate,Regulatory Compliance',
            'jurisdiction': 'Federal',
            'years_experience': 18,
            'specializations': 'EPA Regulations, Land Use, Clean Water Act',
            'email': 'rdavis@davisenviro.com',
            'phone': '5554567890',
            'win_rate': 0.76,
            'total_cases': 142
        },
        {
            'name': 'Amanda Rodriguez',
            'bar_number': 'IL678901',
            'firm': 'Rodriguez Tax & Business Law',
            'practice_areas': 'Tax Law,Corporate Law,Securities',
            'jurisdiction': 'Federal',
            'years_experience': 12,
            'specializations': 'Tax Planning, SEC Compliance, Corporate Governance',
            'email': 'arodriguez@rtaxlaw.com',
            'phone': '5555678901',
            'win_rate': 0.88,
            'total_cases': 95
        }
    ]

    lawyer_ids = []
    for lawyer in lawyers:
        lawyer_id = db.add_lawyer(lawyer)
        lawyer_ids.append(lawyer_id)
        print(f"  ✓ Added: {lawyer['name']} (ID: {lawyer_id})")

    print(f"\n✓ {len(lawyers)} lawyers added successfully!\n")
    return lawyer_ids


def add_sample_cases(lawyer_ids):
    """Add sample cases"""
    print("Adding sample cases...")

    today = datetime.now()

    cases = [
        {
            'case_number': 'CV-2024-001234',
            'title': 'TechCorp Inc. v. Innovation Systems LLC',
            'case_type': 'Civil',
            'practice_area': 'Intellectual Property',
            'jurisdiction': 'Federal',
            'court': 'United States District Court, Northern District of California',
            'filing_date': (today - timedelta(days=180)).strftime('%Y-%m-%d'),
            'status': 'active',
            'lawyer_id': lawyer_ids[0],
            'client_name': 'TechCorp Inc.',
            'opposing_party': 'Innovation Systems LLC',
            'case_summary': 'Patent infringement lawsuit involving AI-powered software algorithms. Client alleges defendant copied proprietary machine learning technology without authorization.',
            'key_issues': 'Patent validity, infringement analysis, willfulness, damages calculation',
            'precedent_value': 'Could establish precedent for AI patent protection'
        },
        {
            'case_number': 'CR-2024-002345',
            'title': 'United States v. William Harper',
            'case_type': 'Criminal',
            'practice_area': 'Criminal Law',
            'jurisdiction': 'Federal',
            'court': 'United States District Court, Southern District of New York',
            'filing_date': (today - timedelta(days=90)).strftime('%Y-%m-%d'),
            'status': 'active',
            'lawyer_id': lawyer_ids[1],
            'client_name': 'William Harper',
            'opposing_party': 'United States Government',
            'case_summary': 'White collar criminal defense case involving allegations of securities fraud and insider trading. Defendant accused of material misstatements to investors.',
            'key_issues': 'Scienter, materiality, loss causation, sentencing guidelines',
            'precedent_value': 'Important for white collar defense strategy'
        },
        {
            'case_number': 'CV-2024-003456',
            'title': 'Martinez v. Global Manufacturing Corp.',
            'case_type': 'Civil',
            'practice_area': 'Employment Law',
            'jurisdiction': 'State',
            'court': 'Superior Court of Texas, Harris County',
            'filing_date': (today - timedelta(days=120)).strftime('%Y-%m-%d'),
            'status': 'active',
            'lawyer_id': lawyer_ids[2],
            'client_name': 'Maria Martinez',
            'opposing_party': 'Global Manufacturing Corp.',
            'case_summary': 'Employment discrimination case alleging gender-based pay disparity and hostile work environment. Plaintiff seeks back pay, damages, and injunctive relief.',
            'key_issues': 'Title VII violations, equal pay act, hostile work environment, punitive damages',
            'precedent_value': 'May impact employer pay equity practices'
        },
        {
            'case_number': 'CV-2024-004567',
            'title': 'Green Earth Alliance v. State Environmental Agency',
            'case_type': 'Administrative',
            'practice_area': 'Environmental Law',
            'jurisdiction': 'Federal',
            'court': 'United States Court of Appeals, Eleventh Circuit',
            'filing_date': (today - timedelta(days=210)).strftime('%Y-%m-%d'),
            'status': 'active',
            'lawyer_id': lawyer_ids[3],
            'client_name': 'Green Earth Alliance',
            'opposing_party': 'Florida Department of Environmental Protection',
            'case_summary': 'Challenge to state agency approval of industrial wastewater discharge permit. Environmental group alleges violation of Clean Water Act standards.',
            'key_issues': 'Administrative Procedure Act, Clean Water Act compliance, standing, ripeness',
            'precedent_value': 'Significant for environmental permitting process'
        },
        {
            'case_number': 'CV-2024-005678',
            'title': 'DataSystems Inc. Merger Acquisition',
            'case_type': 'Civil',
            'practice_area': 'Corporate Law',
            'jurisdiction': 'Federal',
            'court': 'Delaware Court of Chancery',
            'filing_date': (today - timedelta(days=60)).strftime('%Y-%m-%d'),
            'status': 'active',
            'lawyer_id': lawyer_ids[4],
            'client_name': 'DataSystems Inc.',
            'opposing_party': 'N/A - Transaction Matter',
            'case_summary': '$500M merger transaction with complex tax and regulatory issues. Involves cross-border considerations and SEC filing requirements.',
            'key_issues': 'M&A due diligence, securities regulations, tax structuring, antitrust clearance',
            'precedent_value': 'Standard corporate transaction'
        },
        {
            'case_number': 'CV-2023-006789',
            'title': 'Johnson v. MediCare Systems',
            'case_type': 'Civil',
            'practice_area': 'Personal Injury',
            'jurisdiction': 'State',
            'court': 'New York Supreme Court, New York County',
            'filing_date': (today - timedelta(days=365)).strftime('%Y-%m-%d'),
            'status': 'settled',
            'lawyer_id': lawyer_ids[1],
            'client_name': 'Robert Johnson',
            'opposing_party': 'MediCare Systems',
            'case_summary': 'Medical malpractice case involving surgical error. Plaintiff suffered permanent injury due to alleged negligence.',
            'outcome': 'settled',
            'outcome_date': (today - timedelta(days=30)).strftime('%Y-%m-%d'),
            'settlement_amount': 2500000.00,
            'key_issues': 'Medical standard of care, causation, damages',
            'precedent_value': 'Confidential settlement'
        },
        {
            'case_number': 'CV-2023-007890',
            'title': 'Smith Family Trust v. IRS',
            'case_type': 'Civil',
            'practice_area': 'Tax Law',
            'jurisdiction': 'Federal',
            'court': 'United States Tax Court',
            'filing_date': (today - timedelta(days=400)).strftime('%Y-%m-%d'),
            'status': 'closed',
            'lawyer_id': lawyer_ids[4],
            'client_name': 'Smith Family Trust',
            'opposing_party': 'Internal Revenue Service',
            'case_summary': 'Tax dispute over estate valuation and gift tax liability. Complex trust and estate planning issues.',
            'outcome': 'won',
            'outcome_date': (today - timedelta(days=45)).strftime('%Y-%m-%d'),
            'key_issues': 'Estate tax valuation, gift tax exemptions, trust administration',
            'precedent_value': 'Favorable precedent for family trust planning'
        }
    ]

    case_ids = []
    for case in cases:
        case_id = db.add_case(case)
        case_ids.append(case_id)
        print(f"  ✓ Added: {case['case_number']} - {case['title'][:50]}... (ID: {case_id})")

    print(f"\n✓ {len(cases)} cases added successfully!\n")
    return case_ids


def add_sample_documents(lawyer_ids, case_ids):
    """Add sample documents"""
    print("Adding sample documents...")

    today = datetime.now()

    documents = [
        {
            'document_type': 'contract',
            'title': 'Software License Agreement - TechCorp',
            'case_id': case_ids[0],
            'lawyer_id': lawyer_ids[0],
            'document_content': 'Sample software license agreement content...',
            'jurisdiction': 'Federal',
            'practice_area': 'Intellectual Property',
            'creation_date': (today - timedelta(days=150)).strftime('%Y-%m-%d'),
            'last_modified': (today - timedelta(days=100)).strftime('%Y-%m-%d'),
            'status': 'finalized',
            'risk_score': 0.35,
            'compliance_status': 'compliant',
            'review_notes': 'Reviewed and approved. All IP provisions properly drafted.'
        },
        {
            'document_type': 'motion',
            'title': 'Motion for Summary Judgment - Harper Case',
            'case_id': case_ids[1],
            'lawyer_id': lawyer_ids[1],
            'document_content': 'Motion for summary judgment content...',
            'jurisdiction': 'Federal',
            'practice_area': 'Criminal Law',
            'creation_date': (today - timedelta(days=60)).strftime('%Y-%m-%d'),
            'last_modified': (today - timedelta(days=55)).strftime('%Y-%m-%d'),
            'status': 'filed',
            'review_notes': 'Filed with court. Awaiting ruling.'
        },
        {
            'document_type': 'brief',
            'title': 'Memorandum in Support - Martinez Employment Case',
            'case_id': case_ids[2],
            'lawyer_id': lawyer_ids[2],
            'document_content': 'Legal brief supporting employment discrimination claims...',
            'jurisdiction': 'State',
            'practice_area': 'Employment Law',
            'creation_date': (today - timedelta(days=90)).strftime('%Y-%m-%d'),
            'last_modified': (today - timedelta(days=85)).strftime('%Y-%m-%d'),
            'status': 'filed'
        },
        {
            'document_type': 'contract',
            'title': 'Merger Agreement - DataSystems Transaction',
            'case_id': case_ids[4],
            'lawyer_id': lawyer_ids[4],
            'document_content': 'Merger and acquisition agreement...',
            'jurisdiction': 'Federal',
            'practice_area': 'Corporate Law',
            'creation_date': (today - timedelta(days=45)).strftime('%Y-%m-%d'),
            'last_modified': (today - timedelta(days=10)).strftime('%Y-%m-%d'),
            'status': 'draft',
            'risk_score': 0.42,
            'compliance_status': 'under_review',
            'review_notes': 'Under review for SEC compliance and tax implications.'
        },
        {
            'document_type': 'settlement_agreement',
            'title': 'Confidential Settlement Agreement - Johnson v. MediCare',
            'case_id': case_ids[5],
            'lawyer_id': lawyer_ids[1],
            'document_content': 'Confidential settlement agreement...',
            'jurisdiction': 'State',
            'practice_area': 'Personal Injury',
            'creation_date': (today - timedelta(days=35)).strftime('%Y-%m-%d'),
            'last_modified': (today - timedelta(days=30)).strftime('%Y-%m-%d'),
            'status': 'executed',
            'review_notes': 'Fully executed. Settlement funds distributed.'
        }
    ]

    doc_ids = []
    for doc in documents:
        doc_id = db.add_document(doc)
        doc_ids.append(doc_id)
        print(f"  ✓ Added: {doc['title'][:60]}... (ID: {doc_id})")

    print(f"\n✓ {len(documents)} documents added successfully!\n")
    return doc_ids


def add_sample_statutes():
    """Add sample statutes"""
    print("Adding sample statutes...")

    statutes = [
        {
            'statute_code': '35 USC 101',
            'title': 'Patentable Subject Matter',
            'jurisdiction': 'Federal',
            'category': 'Intellectual Property',
            'full_text': 'Whoever invents or discovers any new and useful process, machine, manufacture, or composition of matter, or any new and useful improvement thereof, may obtain a patent therefor, subject to the conditions and requirements of this title.',
            'summary': 'Defines what types of inventions are eligible for patent protection in the United States.',
            'effective_date': '1952-07-19',
            'last_amended': '2011-09-16',
            'status': 'active',
            'citation_count': 15234
        },
        {
            'statute_code': '42 USC 2000e-2',
            'title': 'Title VII - Unlawful Employment Practices',
            'jurisdiction': 'Federal',
            'category': 'Employment Law',
            'full_text': 'It shall be an unlawful employment practice for an employer to fail or refuse to hire or to discharge any individual, or otherwise to discriminate against any individual with respect to his compensation, terms, conditions, or privileges of employment, because of such individual\'s race, color, religion, sex, or national origin.',
            'summary': 'Prohibits employment discrimination based on protected characteristics.',
            'effective_date': '1964-07-02',
            'last_amended': '1991-11-21',
            'status': 'active',
            'citation_count': 28567
        },
        {
            'statute_code': '15 USC 78j(b)',
            'title': 'Securities Exchange Act - Manipulative and Deceptive Devices',
            'jurisdiction': 'Federal',
            'category': 'Securities Law',
            'full_text': 'It shall be unlawful for any person, directly or indirectly, by the use of any means or instrumentality of interstate commerce or of the mails, or of any facility of any national securities exchange to use or employ, in connection with the purchase or sale of any security registered on a national securities exchange or any security not so registered, or any securities-based swap agreement any manipulative or deceptive device or contrivance in contravention of such rules and regulations as the Commission may prescribe.',
            'summary': 'Prohibits securities fraud and market manipulation.',
            'effective_date': '1934-06-06',
            'last_amended': '2010-07-21',
            'status': 'active',
            'citation_count': 45123
        },
        {
            'statute_code': '33 USC 1311',
            'title': 'Clean Water Act - Effluent Limitations',
            'jurisdiction': 'Federal',
            'category': 'Environmental Law',
            'full_text': 'Except as in compliance with this section and sections 1312, 1316, 1317, 1328, 1342, and 1344 of this title, the discharge of any pollutant by any person shall be unlawful.',
            'summary': 'Establishes federal program to regulate discharge of pollutants into U.S. waters.',
            'effective_date': '1972-10-18',
            'last_amended': '2014-06-10',
            'status': 'active',
            'citation_count': 12456
        },
        {
            'statute_code': '26 USC 1',
            'title': 'Tax Rates for Individuals',
            'jurisdiction': 'Federal',
            'category': 'Tax Law',
            'full_text': 'There is hereby imposed on the taxable income of every individual who is a married individual and who files a separate return a tax determined in accordance with the following table...',
            'summary': 'Establishes federal income tax rates and brackets.',
            'effective_date': '1913-10-03',
            'last_amended': '2017-12-22',
            'status': 'active',
            'citation_count': 34567
        }
    ]

    statute_ids = []
    for statute in statutes:
        statute_id = db.add_statute(statute)
        statute_ids.append(statute_id)
        print(f"  ✓ Added: {statute['statute_code']} - {statute['title'][:50]}...")

    print(f"\n✓ {len(statutes)} statutes added successfully!\n")
    return statute_ids


def add_sample_precedents():
    """Add sample precedents"""
    print("Adding sample precedents...")

    precedents = [
        {
            'case_name': 'Alice Corp. v. CLS Bank International',
            'citation': '573 U.S. 208 (2014)',
            'court': 'Supreme Court of the United States',
            'jurisdiction': 'Federal',
            'decision_date': '2014-06-19',
            'practice_area': 'Intellectual Property',
            'legal_issue': 'Patent eligibility of computer-implemented inventions',
            'holding': 'Claims directed to abstract ideas are not patent eligible unless they contain an inventive concept sufficient to transform the claimed abstract idea into a patent-eligible application.',
            'reasoning': 'The Court established a two-step test for patent eligibility: (1) determine if claims are directed to patent-ineligible concept, and (2) if so, determine if additional elements transform the claim into patent-eligible application.',
            'importance_score': 0.98,
            'citation_count': 8234,
            'overruled': False,
            'keywords': 'patent eligibility, abstract ideas, software patents, Section 101'
        },
        {
            'case_name': 'McDonnell Douglas Corp. v. Green',
            'citation': '411 U.S. 792 (1973)',
            'court': 'Supreme Court of the United States',
            'jurisdiction': 'Federal',
            'decision_date': '1973-05-14',
            'practice_area': 'Employment Law',
            'legal_issue': 'Burden-shifting framework for employment discrimination cases',
            'holding': 'Established three-part burden-shifting test for proving employment discrimination under Title VII.',
            'reasoning': 'Plaintiff must establish prima facie case; burden then shifts to defendant to articulate legitimate non-discriminatory reason; burden shifts back to plaintiff to prove pretext.',
            'importance_score': 0.99,
            'citation_count': 12456,
            'overruled': False,
            'keywords': 'employment discrimination, burden shifting, Title VII, prima facie case'
        },
        {
            'case_name': 'Basic Inc. v. Levinson',
            'citation': '485 U.S. 224 (1988)',
            'court': 'Supreme Court of the United States',
            'jurisdiction': 'Federal',
            'decision_date': '1988-03-07',
            'practice_area': 'Securities Law',
            'legal_issue': 'Materiality standard and fraud-on-the-market theory in securities cases',
            'holding': 'Established that materiality depends on probability that disclosure would alter total mix of information. Endorsed fraud-on-the-market theory for reliance in securities fraud cases.',
            'reasoning': 'Information is material if there is substantial likelihood that reasonable investor would consider it important. Market efficiency allows presumption of reliance.',
            'importance_score': 0.97,
            'citation_count': 15678,
            'overruled': False,
            'keywords': 'securities fraud, materiality, fraud-on-the-market, reliance, Rule 10b-5'
        },
        {
            'case_name': 'Chevron U.S.A., Inc. v. Natural Resources Defense Council',
            'citation': '467 U.S. 837 (1984)',
            'court': 'Supreme Court of the United States',
            'jurisdiction': 'Federal',
            'decision_date': '1984-06-25',
            'practice_area': 'Environmental Law',
            'legal_issue': 'Judicial deference to agency interpretation of statutes',
            'holding': 'Established two-step framework for reviewing agency statutory interpretations. Courts must defer to reasonable agency interpretations of ambiguous statutes.',
            'reasoning': 'If Congress has not directly addressed the precise question at issue, court must defer to agency\'s interpretation if it is based on permissible construction of statute.',
            'importance_score': 0.99,
            'citation_count': 23456,
            'overruled': False,
            'keywords': 'Chevron deference, administrative law, statutory interpretation, agency discretion'
        },
        {
            'case_name': 'Commissioner v. Estate of Bosch',
            'citation': '387 U.S. 456 (1967)',
            'court': 'Supreme Court of the United States',
            'jurisdiction': 'Federal',
            'decision_date': '1967-06-05',
            'practice_area': 'Tax Law',
            'legal_issue': 'Federal courts\' treatment of state court decisions in federal tax cases',
            'holding': 'Federal courts should give proper regard to state court decisions on matters of state law, but are not bound by them in determining federal tax consequences.',
            'reasoning': 'State trial court decisions are not controlling on federal courts in determining federal tax liability when state law issues are involved.',
            'importance_score': 0.89,
            'citation_count': 5678,
            'overruled': False,
            'keywords': 'federal tax law, state law, Erie doctrine, estate planning'
        }
    ]

    precedent_ids = []
    for precedent in precedents:
        precedent_id = db.add_precedent(precedent)
        precedent_ids.append(precedent_id)
        print(f"  ✓ Added: {precedent['case_name']} ({precedent['citation']})")

    print(f"\n✓ {len(precedents)} precedents added successfully!\n")
    return precedent_ids


def add_sample_contracts(lawyer_ids, doc_ids):
    """Add sample contracts"""
    print("Adding sample contracts...")

    today = datetime.now()

    contracts = [
        {
            'contract_name': 'Master Services Agreement - Technology Consulting',
            'contract_type': 'Services Agreement',
            'parties': 'TechCorp Inc., Consulting Services Group LLC',
            'execution_date': (today - timedelta(days=120)).strftime('%Y-%m-%d'),
            'effective_date': (today - timedelta(days=120)).strftime('%Y-%m-%d'),
            'expiration_date': (today + timedelta(days=245)).strftime('%Y-%m-%d'),
            'jurisdiction': 'California',
            'governing_law': 'California',
            'contract_value': 500000.00,
            'status': 'active',
            'risk_level': 'medium',
            'risk_score': 0.42,
            'key_terms': 'Fixed fee $500K, 12-month term, IP ownership to client, confidentiality provisions',
            'obligations': 'Consulting services, deliverables per SOW, monthly reporting',
            'penalties': 'Late delivery penalties up to 10% of fees, termination for material breach',
            'termination_clauses': '30-day notice for convenience, immediate for cause',
            'document_id': doc_ids[0] if doc_ids else None,
            'lawyer_id': lawyer_ids[0]
        },
        {
            'contract_name': 'Commercial Lease Agreement - Office Space',
            'contract_type': 'Lease Agreement',
            'parties': 'Johnson Legal Group, Realty Management Corp.',
            'execution_date': (today - timedelta(days=730)).strftime('%Y-%m-%d'),
            'effective_date': (today - timedelta(days=730)).strftime('%Y-%m-%d'),
            'expiration_date': (today + timedelta(days=825)).strftime('%Y-%m-%d'),
            'jurisdiction': 'New York',
            'governing_law': 'New York',
            'contract_value': 360000.00,
            'status': 'active',
            'risk_level': 'low',
            'risk_score': 0.25,
            'key_terms': '$5000/month rent, 5-year term, 3% annual increase, renewal option',
            'obligations': 'Monthly rent payment, maintain premises, insurance requirements',
            'penalties': 'Late fees 5%, default interest, eviction for non-payment',
            'termination_clauses': 'No early termination except for default',
            'lawyer_id': lawyer_ids[1]
        },
        {
            'contract_name': 'Non-Disclosure Agreement - M&A Due Diligence',
            'contract_type': 'NDA',
            'parties': 'DataSystems Inc., Acquiring Company (confidential)',
            'execution_date': (today - timedelta(days=90)).strftime('%Y-%m-%d'),
            'effective_date': (today - timedelta(days=90)).strftime('%Y-%m-%d'),
            'expiration_date': (today + timedelta(days=1735)).strftime('%Y-%m-%d'),
            'jurisdiction': 'Delaware',
            'governing_law': 'Delaware',
            'status': 'active',
            'risk_level': 'high',
            'risk_score': 0.68,
            'key_terms': 'Mutual NDA, 5-year term, financial information disclosure, M&A purpose',
            'obligations': 'Maintain confidentiality, limit disclosure, return/destroy materials',
            'penalties': 'Injunctive relief, liquidated damages $1M, attorney fees',
            'termination_clauses': 'Mutual written consent, automatic after 5 years',
            'document_id': doc_ids[3] if len(doc_ids) > 3 else None,
            'lawyer_id': lawyer_ids[4]
        }
    ]

    contract_ids = []
    for contract in contracts:
        contract_id = db.add_contract(contract)
        contract_ids.append(contract_id)
        print(f"  ✓ Added: {contract['contract_name'][:60]}...")

    print(f"\n✓ {len(contracts)} contracts added successfully!\n")
    return contract_ids


def add_sample_compliance_requirements():
    """Add sample compliance requirements"""
    print("Adding sample compliance requirements...")

    requirements = [
        {
            'requirement_code': 'GDPR-ART-5',
            'framework': 'GDPR',
            'category': 'Data Privacy',
            'description': 'Personal data must be processed lawfully, fairly, and transparently; collected for specified, explicit and legitimate purposes; adequate, relevant and limited to what is necessary.',
            'jurisdiction': 'European Union',
            'industry': 'All',
            'mandatory': True,
            'penalty_description': 'Up to €20 million or 4% of annual global turnover, whichever is higher',
            'related_statutes': 'GDPR Articles 5, 6, 7',
            'implementation_notes': 'Requires privacy policy, consent mechanisms, data minimization practices, purpose limitation'
        },
        {
            'requirement_code': 'HIPAA-164.312',
            'framework': 'HIPAA',
            'category': 'Healthcare Data Security',
            'description': 'Technical safeguards for electronic protected health information including access controls, audit controls, integrity controls, transmission security.',
            'jurisdiction': 'United States',
            'industry': 'Healthcare',
            'mandatory': True,
            'penalty_description': 'Up to $1.5 million per violation type per year, criminal penalties possible',
            'related_statutes': '45 CFR 164.312, HITECH Act',
            'implementation_notes': 'Requires encryption, access logs, authentication, secure transmission protocols'
        },
        {
            'requirement_code': 'SOX-404',
            'framework': 'SOX',
            'category': 'Financial Controls',
            'description': 'Management must assess and report on effectiveness of internal controls over financial reporting. External auditors must attest to management\'s assessment.',
            'jurisdiction': 'United States',
            'industry': 'Public Companies',
            'mandatory': True,
            'penalty_description': 'Civil penalties, criminal prosecution for willful violations, delisting risk',
            'related_statutes': 'Sarbanes-Oxley Section 404, SEC Rules',
            'implementation_notes': 'Requires documented processes, control testing, management certification, auditor attestation'
        },
        {
            'requirement_code': 'PCI-DSS-3.2.1',
            'framework': 'PCI-DSS',
            'category': 'Payment Card Security',
            'description': 'Requirements for organizations handling credit card data including network security, access controls, encryption, monitoring.',
            'jurisdiction': 'Global',
            'industry': 'Payment Processing',
            'mandatory': True,
            'penalty_description': 'Fines up to $500K per incident, increased transaction fees, loss of card processing privileges',
            'related_statutes': 'Payment card industry standards',
            'implementation_notes': 'Requires firewall configuration, encryption, access controls, monitoring, testing'
        },
        {
            'requirement_code': 'CCPA-1798.100',
            'framework': 'CCPA',
            'category': 'Consumer Privacy Rights',
            'description': 'Consumers have right to know what personal information is collected, used, shared or sold. Businesses must disclose categories and specific pieces of personal information collected.',
            'jurisdiction': 'California',
            'industry': 'All',
            'mandatory': True,
            'penalty_description': 'Up to $7,500 per intentional violation, $2,500 per unintentional violation, plus private right of action for data breaches',
            'related_statutes': 'California Civil Code Section 1798.100-199',
            'implementation_notes': 'Requires privacy notice, consumer request process, data inventory, deletion capabilities'
        }
    ]

    compliance_ids = []
    for requirement in requirements:
        compliance_id = db.add_compliance_requirement(requirement)
        compliance_ids.append(compliance_id)
        print(f"  ✓ Added: {requirement['requirement_code']} - {requirement['description'][:50]}...")

    print(f"\n✓ {len(requirements)} compliance requirements added successfully!\n")
    return compliance_ids


def add_sample_deadlines(lawyer_ids, case_ids):
    """Add sample deadlines"""
    print("Adding sample deadlines...")

    today = datetime.now()

    deadlines = [
        {
            'case_id': case_ids[0],
            'lawyer_id': lawyer_ids[0],
            'deadline_type': 'Discovery',
            'description': 'Complete fact discovery - TechCorp patent case',
            'due_date': (today + timedelta(days=45)).strftime('%Y-%m-%d'),
            'priority': 'high',
            'status': 'pending',
            'reminder_sent': False,
            'notes': 'Coordinate with expert witnesses for technical documents'
        },
        {
            'case_id': case_ids[1],
            'lawyer_id': lawyer_ids[1],
            'deadline_type': 'Motion',
            'description': 'File motion for summary judgment - Harper criminal case',
            'due_date': (today + timedelta(days=15)).strftime('%Y-%m-%d'),
            'priority': 'critical',
            'status': 'pending',
            'reminder_sent': True,
            'notes': 'Draft complete, awaiting final review'
        },
        {
            'case_id': case_ids[2],
            'lawyer_id': lawyer_ids[2],
            'deadline_type': 'Response',
            'description': 'Respond to defendant\'s discovery requests - Martinez case',
            'due_date': (today + timedelta(days=8)).strftime('%Y-%m-%d'),
            'priority': 'high',
            'status': 'pending',
            'reminder_sent': True,
            'notes': 'Client interview scheduled for document production'
        },
        {
            'case_id': case_ids[3],
            'lawyer_id': lawyer_ids[3],
            'deadline_type': 'Brief',
            'description': 'File appellate brief - Environmental case',
            'due_date': (today + timedelta(days=60)).strftime('%Y-%m-%d'),
            'priority': 'medium',
            'status': 'pending',
            'reminder_sent': False,
            'notes': 'Research complete, begin drafting next week'
        },
        {
            'case_id': case_ids[4],
            'lawyer_id': lawyer_ids[4],
            'deadline_type': 'Transaction',
            'description': 'Close DataSystems merger transaction',
            'due_date': (today + timedelta(days=30)).strftime('%Y-%m-%d'),
            'priority': 'critical',
            'status': 'pending',
            'reminder_sent': True,
            'notes': 'SEC approval received, final documents in negotiation'
        },
        {
            'case_id': case_ids[0],
            'lawyer_id': lawyer_ids[0],
            'deadline_type': 'Hearing',
            'description': 'Claim construction hearing - TechCorp case',
            'due_date': (today + timedelta(days=90)).strftime('%Y-%m-%d'),
            'priority': 'high',
            'status': 'pending',
            'reminder_sent': False,
            'notes': 'Prepare claim construction briefing and presentation'
        }
    ]

    deadline_ids = []
    for deadline in deadlines:
        deadline_id = db.add_deadline(deadline)
        deadline_ids.append(deadline_id)
        print(f"  ✓ Added: {deadline['description'][:60]}... ({deadline['due_date']})")

    print(f"\n✓ {len(deadlines)} deadlines added successfully!\n")
    return deadline_ids


def main():
    """Main function to populate all sample data"""
    try:
        print("Starting data population...\n")

        # Add data in order of dependencies
        lawyer_ids = add_sample_lawyers()
        case_ids = add_sample_cases(lawyer_ids)
        doc_ids = add_sample_documents(lawyer_ids, case_ids)
        statute_ids = add_sample_statutes()
        precedent_ids = add_sample_precedents()
        contract_ids = add_sample_contracts(lawyer_ids, doc_ids)
        compliance_ids = add_sample_compliance_requirements()
        deadline_ids = add_sample_deadlines(lawyer_ids, case_ids)

        # Summary
        print("=" * 70)
        print("  DATA POPULATION COMPLETE")
        print("=" * 70)
        print()
        print(f"  ✓ {len(lawyer_ids)} Lawyers")
        print(f"  ✓ {len(case_ids)} Cases")
        print(f"  ✓ {len(doc_ids)} Documents")
        print(f"  ✓ {len(statute_ids)} Statutes")
        print(f"  ✓ {len(precedent_ids)} Precedents")
        print(f"  ✓ {len(contract_ids)} Contracts")
        print(f"  ✓ {len(compliance_ids)} Compliance Requirements")
        print(f"  ✓ {len(deadline_ids)} Deadlines")
        print()
        print("The Legal Intelligence System is now populated with sample data!")
        print("You can now launch the application and explore its features.")
        print()
        print("Quick Start: python start.py")
        print("=" * 70)

    except Exception as e:
        print(f"\n✗ Error during data population: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
