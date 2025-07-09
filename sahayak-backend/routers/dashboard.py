from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import json
import os
from datetime import datetime

router = APIRouter()

class DashboardStats(BaseModel):
    storiesGenerated: int = 0
    worksheetsCreated: int = 0
    questionsAnswered: int = 0
    visualsGenerated: int = 0
    assessmentsCompleted: int = 0
    lessonPlans: int = 0
    lastUpdated: str

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    """
    Get dashboard statistics.
    Note: Currently returns default values as stats are managed client-side.
    In the future, this could be connected to a database for server-side tracking.
    """
    try:
        # For now, return default stats since data is stored client-side
        # In a production environment, these would come from a database
        stats = DashboardStats(
            storiesGenerated=0,
            worksheetsCreated=0,
            questionsAnswered=0,
            visualsGenerated=0,
            assessmentsCompleted=0,
            lessonPlans=0,
            lastUpdated=datetime.now().isoformat()
        )
        
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving dashboard stats: {str(e)}")

@router.get("/health")
async def dashboard_health():
    """Health check for dashboard service"""
    return {
        "status": "healthy",
        "service": "dashboard",
        "message": "Dashboard stats service is running",
        "storage": "client-side (localStorage)",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/info")
async def dashboard_info():
    """Get information about dashboard stats management"""
    return {
        "stats_location": "client-side",
        "storage_method": "localStorage",
        "real_time_updates": True,
        "features": [
            "Accurate counting from actual stored content",
            "Real-time updates when content is added/deleted",
            "Automatic refresh on navigation",
            "Zero values when no content exists"
        ],
        "localStorage_keys": {
            "content": "sahayak_past_content",
            "worksheets": "sahayak_past_worksheets", 
            "questions": "sahayak_past_questions",
            "visuals": "sahayak_past_visuals",
            "assessments": "sahayak_past_assessments",
            "lesson_plans": "sahayak_past_lesson_plans"
        }
    } 