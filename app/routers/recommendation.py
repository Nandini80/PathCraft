from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Itinerary
from app.schemas import ItinerariesResponse, ItineraryResponse
from sqlalchemy import func, desc
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"]
)

@router.get("/", response_model=ItinerariesResponse)
def get_recommendations(
    nights: int,
    region: Optional[str] = None,
    interests: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    MCP Server: Get recommended itineraries based on nights and optional filters.
    """
    try:
        query = db.query(Itinerary).filter(Itinerary.nights == nights)
        
        if region:
            query = query.filter(Itinerary.region == region)
        
        recommendations = query.all()
        
        if not recommendations:
            closest_query = db.query(Itinerary)
            
            if region:
                closest_query = closest_query.filter(Itinerary.region == region)
            
            closest_query = closest_query.order_by(
                func.abs(Itinerary.nights - nights)
            ).limit(3)
            
            recommendations = closest_query.all()
            
            if recommendations:
                return {
                    "success": True,
                    "count": len(recommendations),
                    "data": recommendations,
                    "message": "No exact match found. Showing closest alternatives."
                }
            
            return {
                "success": False,
                "count": 0,
                "data": [],
                "message": "No itineraries found for the given criteria."
            }
        
        if interests:
            interest_list = interests.split(',')
        
        return {
            "success": True,
            "count": len(recommendations),
            "data": recommendations
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch recommendations: {str(e)}"
        )

@router.get("/popular", response_model=ItinerariesResponse)
def get_popular_itineraries(db: Session = Depends(get_db)):
    """
    Get popular itineraries.
    """
    try:
        # In a real application, this would be based on user bookings or views
        # For now, we'll just return recommended itineraries
        popular = db.query(Itinerary).filter(Itinerary.is_recommended == True).limit(5).all()
        
        return {
            "success": True,
            "count": len(popular),
            "data": popular
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch popular itineraries: {str(e)}"
        )

@router.get("/stats")
def get_itinerary_stats(db: Session = Depends(get_db)):
    """
    Get itinerary statistics.
    """
    try:
        # Total counts
        total_itineraries = db.query(func.count(Itinerary.id)).scalar()
        
        # Count by region
        region_stats = db.query(
            Itinerary.region,
            func.count(Itinerary.id).label("count")
        ).group_by(Itinerary.region).all()
        
        # Count by duration
        duration_stats = db.query(
            Itinerary.nights,
            func.count(Itinerary.id).label("count")
        ).group_by(Itinerary.nights).order_by(Itinerary.nights).all()
        
        return {
            "success": True,
            "data": {
                "totalItineraries": total_itineraries,
                "byRegion": [{"region": r[0], "count": r[1]} for r in region_stats],
                "byDuration": [{"nights": d[0], "count": d[1]} for d in duration_stats]
            }
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch itinerary statistics: {str(e)}"
        )