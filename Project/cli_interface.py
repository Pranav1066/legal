"""
Command Line Interface for Legal Intelligence System
"""
import click
import sys
from pathlib import Path
from tabulate import tabulate

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from utils.database import db
from agents.orchestrator import orchestrator


@click.group()
@click.version_option(config.APP_VERSION)
def cli():
    """Legal Intelligence System - AI-powered legal research and analysis"""
    pass


@cli.group()
def lawyer():
    """Manage lawyers"""
    pass


@lawyer.command('list')
def list_lawyers():
    """List all lawyers"""
    lawyers = db.get_all_lawyers()
    if lawyers:
        headers = ['ID', 'Name', 'Bar Number', 'Firm', 'Practice Areas']
        rows = [[l['id'], l['name'], l['bar_number'], l.get('firm', 'N/A'), l.get('practice_areas', 'N/A')]
                for l in lawyers]
        click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
    else:
        click.echo("No lawyers found.")


@lawyer.command('add')
@click.option('--name', prompt=True, help='Lawyer name')
@click.option('--bar-number', prompt=True, help='Bar number')
@click.option('--firm', prompt=True, help='Law firm')
@click.option('--practice-areas', prompt=True, help='Practice areas (comma-separated)')
@click.option('--jurisdiction', prompt=True, help='Jurisdiction')
def add_lawyer(name, bar_number, firm, practice_areas, jurisdiction):
    """Add a new lawyer"""
    lawyer_data = {
        'name': name,
        'bar_number': bar_number,
        'firm': firm,
        'practice_areas': practice_areas,
        'jurisdiction': jurisdiction
    }

    try:
        lawyer_id = db.add_lawyer(lawyer_data)
        click.echo(click.style(f'✓ Lawyer added successfully (ID: {lawyer_id})', fg='green'))
    except Exception as e:
        click.echo(click.style(f'✗ Error: {str(e)}', fg='red'))


@cli.group()
def case():
    """Manage cases"""
    pass


@case.command('list')
@click.option('--lawyer-id', type=int, help='Filter by lawyer ID')
def list_cases(lawyer_id):
    """List all cases"""
    if lawyer_id:
        cases = db.get_lawyer_cases(lawyer_id)
    else:
        cases = db.get_open_cases()

    if cases:
        headers = ['ID', 'Case Number', 'Title', 'Type', 'Status', 'Court']
        rows = [[c['id'], c['case_number'], c['title'][:30], c.get('case_type', 'N/A'),
                 c.get('status', 'N/A'), c.get('court', 'N/A')] for c in cases]
        click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
    else:
        click.echo("No cases found.")


@case.command('add')
@click.option('--case-number', prompt=True, help='Case number')
@click.option('--title', prompt=True, help='Case title')
@click.option('--lawyer-id', prompt=True, type=int, help='Lawyer ID')
@click.option('--case-type', prompt=True, help='Case type')
@click.option('--jurisdiction', prompt=True, help='Jurisdiction')
@click.option('--court', prompt=True, help='Court')
def add_case(case_number, title, lawyer_id, case_type, jurisdiction, court):
    """Add a new case"""
    case_data = {
        'case_number': case_number,
        'title': title,
        'lawyer_id': lawyer_id,
        'case_type': case_type,
        'jurisdiction': jurisdiction,
        'court': court,
        'status': 'active'
    }

    try:
        case_id = db.add_case(case_data)
        click.echo(click.style(f'✓ Case added successfully (ID: {case_id})', fg='green'))
    except Exception as e:
        click.echo(click.style(f'✗ Error: {str(e)}', fg='red'))


@cli.group()
def research():
    """Legal research commands"""
    pass


@research.command('case-law')
@click.option('--lawyer-id', prompt=True, type=int, help='Lawyer ID')
@click.option('--legal-issue', prompt=True, help='Legal issue to research')
@click.option('--jurisdiction', help='Jurisdiction')
@click.option('--practice-area', help='Practice area')
def research_case_law(lawyer_id, legal_issue, jurisdiction, practice_area):
    """Perform case law research"""
    click.echo("Researching case law...")

    try:
        result = orchestrator.research_case_law(
            lawyer_id,
            legal_issue=legal_issue,
            jurisdiction=jurisdiction,
            practice_area=practice_area
        )
        click.echo(click.style('✓ Research completed!', fg='green'))
        click.echo("\n" + result)
    except Exception as e:
        click.echo(click.style(f'✗ Error: {str(e)}', fg='red'))


@cli.group()
def analyze():
    """Analysis commands"""
    pass


@analyze.command('contract')
@click.option('--lawyer-id', prompt=True, type=int, help='Lawyer ID')
@click.option('--contract-file', type=click.Path(exists=True), help='Path to contract file')
def analyze_contract(lawyer_id, contract_file):
    """Analyze a contract"""
    if not contract_file:
        click.echo("Please provide a contract file.")
        return

    with open(contract_file, 'r') as f:
        contract_text = f.read()

    click.echo("Analyzing contract...")

    try:
        result = orchestrator.analyze_contract(
            lawyer_id,
            contract_name=Path(contract_file).name,
            contract_type="General",
            contract_text=contract_text,
            parties="TBD",
            party_role="Balanced"
        )
        click.echo(click.style('✓ Analysis completed!', fg='green'))
        click.echo("\n" + result)
    except Exception as e:
        click.echo(click.style(f'✗ Error: {str(e)}', fg='red'))


@cli.command()
def stats():
    """Show system statistics"""
    stats = db.get_database_stats()

    click.echo(click.style('\n📊 Legal Intelligence System Statistics\n', fg='cyan', bold=True))

    data = [
        ['Lawyers', stats.get('lawyers_count', 0)],
        ['Cases', stats.get('cases_count', 0)],
        ['Documents', stats.get('legal_documents_count', 0)],
        ['Statutes', stats.get('statutes_count', 0)],
        ['Precedents', stats.get('precedents_count', 0)],
        ['Contracts', stats.get('contracts_count', 0)],
        ['Research Sessions', stats.get('research_sessions_count', 0)]
    ]

    click.echo(tabulate(data, headers=['Metric', 'Count'], tablefmt='grid'))


@cli.command()
def config_info():
    """Show configuration information"""
    config_summary = config.get_config_summary()

    click.echo(click.style('\n⚙️ Configuration\n', fg='cyan', bold=True))
    click.echo(f"App Name: {config_summary['app_name']}")
    click.echo(f"Version: {config_summary['version']}")
    click.echo(f"Environment: {config_summary['environment']}")
    click.echo(f"Web Port: {config_summary['web_port']}")
    click.echo(f"API Port: {config_summary['api_port']}")
    click.echo(f"AI Model: {config_summary['ai_model']}")
    click.echo(f"Database: {config_summary['database_path']}")


if __name__ == '__main__':
    cli()
