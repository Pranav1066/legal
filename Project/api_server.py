"""
REST API Server for Legal Intelligence System
Built with FastAPI for programmatic access
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from utils.database import db
from utils.validators import validators
from agents.orchestrator import orchestrator

# Initialize FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    description="AI-powered Legal Intelligence System API"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Models
class LawyerCreate(BaseModel):
    name: str
    bar_number: str
    firm: Optional[str] = None
    practice_areas: str
    jurisdiction: str
    years_experience: Optional[int] = 0
    specializations: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class CaseCreate(BaseModel):
    case_number: str
    title: str
    case_type: str
    practice_area: str
    jurisdiction: str
    court: str
    filing_date: str
    status: str
    lawyer_id: int
    client_name: Optional[str] = None
    opposing_party: Optional[str] = None
    case_summary: Optional[str] = None
    key_issues: Optional[str] = None


class CaseLawResearchRequest(BaseModel):
    lawyer_id: int
    legal_issue: str
    jurisdiction: Optional[str] = None
    practice_area: Optional[str] = None
    current_facts: Optional[str] = None
    case_id: Optional[int] = None


class ContractAnalysisRequest(BaseModel):
    lawyer_id: int
    contract_name: str
    contract_type: str
    contract_text: str
    parties: str
    party_role: str
    jurisdiction: Optional[str] = None
    industry: Optional[str] = "General"


class ComplianceAssessmentRequest(BaseModel):
    lawyer_id: int
    organization: str
    industry: str
    jurisdictions: List[str]
    frameworks: List[str]
    scope: List[str]
    current_practices: Optional[str] = None


# Health Check
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": config.APP_NAME,
        "version": config.APP_VERSION,
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "environment": config.ENVIRONMENT}


# Lawyer Endpoints
@app.post("/lawyers", status_code=status.HTTP_201_CREATED)
async def create_lawyer(lawyer: LawyerCreate):
    """Create a new lawyer"""
    lawyer_data = lawyer.dict()

    # Validate
    errors = validators.validate_lawyer_data(lawyer_data)
    if errors:
        raise HTTPException(status_code=400, detail={"errors": errors})

    try:
        lawyer_id = db.add_lawyer(lawyer_data)
        return {"id": lawyer_id, "message": "Lawyer created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/lawyers")
async def get_lawyers():
    """Get all lawyers"""
    try:
        lawyers = db.get_all_lawyers()
        return {"lawyers": lawyers, "count": len(lawyers)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/lawyers/{lawyer_id}")
async def get_lawyer(lawyer_id: int):
    """Get lawyer by ID"""
    try:
        lawyer = db.get_lawyer_by_id(lawyer_id)
        if not lawyer:
            raise HTTPException(status_code=404, detail="Lawyer not found")
        return lawyer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/lawyers/{lawyer_id}/summary")
async def get_lawyer_summary(lawyer_id: int):
    """Get lawyer summary with statistics"""
    try:
        summary = orchestrator.get_lawyer_summary(lawyer_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Case Endpoints
@app.post("/cases", status_code=status.HTTP_201_CREATED)
async def create_case(case: CaseCreate):
    """Create a new case"""
    case_data = case.dict()

    # Validate
    errors = validators.validate_case_data(case_data)
    if errors:
        raise HTTPException(status_code=400, detail={"errors": errors})

    try:
        case_id = db.add_case(case_data)
        return {"id": case_id, "message": "Case created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cases/{case_id}")
async def get_case(case_id: int):
    """Get case by ID"""
    try:
        case = db.get_case_by_id(case_id)
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        return case
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/lawyers/{lawyer_id}/cases")
async def get_lawyer_cases(lawyer_id: int):
    """Get all cases for a lawyer"""
    try:
        cases = db.get_lawyer_cases(lawyer_id)
        return {"cases": cases, "count": len(cases)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# AI Agent Endpoints
@app.post("/research/case-law")
async def research_case_law(request: CaseLawResearchRequest):
    """Perform case law research"""
    try:
        result = orchestrator.research_case_law(
            request.lawyer_id,
            legal_issue=request.legal_issue,
            jurisdiction=request.jurisdiction,
            practice_area=request.practice_area,
            current_facts=request.current_facts,
            case_id=request.case_id
        )
        return {"analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/contract")
async def analyze_contract(request: ContractAnalysisRequest):
    """Analyze a contract"""
    try:
        result = orchestrator.analyze_contract(
            request.lawyer_id,
            contract_name=request.contract_name,
            contract_type=request.contract_type,
            contract_text=request.contract_text,
            parties=request.parties,
            party_role=request.party_role,
            jurisdiction=request.jurisdiction,
            industry=request.industry
        )
        return {"analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/assess/compliance")
async def assess_compliance(request: ComplianceAssessmentRequest):
    """Assess compliance"""
    try:
        result = orchestrator.assess_compliance(
            request.lawyer_id,
            organization=request.organization,
            industry=request.industry,
            jurisdictions=request.jurisdictions,
            frameworks=request.frameworks,
            scope=request.scope,
            current_practices=request.current_practices
        )
        return {"assessment": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/strategy/litigation/{case_id}")
async def develop_litigation_strategy(case_id: int, lawyer_id: int):
    """Develop litigation strategy for a case"""
    try:
        result = orchestrator.develop_litigation_strategy(lawyer_id, case_id)
        return {"strategy": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/comprehensive/{case_id}")
async def comprehensive_case_analysis(case_id: int, lawyer_id: int):
    """Perform comprehensive case analysis"""
    try:
        result = orchestrator.comprehensive_case_analysis(lawyer_id, case_id)
        return {"analyses": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Database Stats
@app.get("/stats/database")
async def get_database_stats():
    """Get database statistics"""
    try:
        stats = db.get_database_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Configuration
@app.get("/config")
async def get_config():
    """Get configuration summary"""
    try:
        config_summary = config.get_config_summary()
        return config_summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run_server():
    """Run the API server"""
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=config.API_PORT,
        log_level="info"
    )


if __name__ == "__main__":
    run_server()
