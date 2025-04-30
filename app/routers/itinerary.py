from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Itinerary, Day, Accommodation, Transfer, Activity
from app.schemas import (
    ItineraryCreate, ItineraryResponse, ItinerariesResponse
)
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

router = APIRouter(
    prefix="/api/itineraries",
    tags=["Itineraries"]
)

@router.post("/", response_model=ItineraryResponse, status_code=status.HTTP_201_CREATED)
def create_itinerary(itinerary: ItineraryCreate, db: Session = Depends(get_db)):
    """
    Create a new itinerary with days, accommodations, transfers, and activities.
    """
    try:
        db_itinerary = Itinerary(
            name=itinerary.name,
            region=itinerary.region,
            nights=itinerary.nights,
            description=itinerary.description,
            highlights=itinerary.highlights,  
            price_estimate=itinerary.price_estimate,
            tags=itinerary.tags,
            is_recommended=itinerary.is_recommended
        )
        db.add(db_itinerary)
        db.flush()  # Flush to get the itinerary ID
        
        for day_data in itinerary.days:
            db_day = Day(
                day_number=day_data.day_number,
                date=day_data.date,
                itinerary_id=db_itinerary.id
            )
            db.add(db_day)
            db.flush()  
            
            # Create accommodations
            for acc_data in day_data.accommodations:
                db_accommodation = Accommodation(
                    hotel_name=acc_data.hotel_name,
                    check_in_time=acc_data.check_in_time,
                    check_out_time=acc_data.check_out_time,
                    day_id=db_day.id
                )
                db.add(db_accommodation)
            
            # Create transfers
            for transfer_data in day_data.transfers:
                db_transfer = Transfer(
                    from_location=transfer_data.from_location,
                    to_location=transfer_data.to_location,
                    departure_time=transfer_data.departure_time,
                    day_id=db_day.id
                )
                db.add(db_transfer)
            
            # Create activities
            for activity_data in day_data.activities:
                db_activity = Activity(
                    activity_name=activity_data.activity_name,
                    start_time=activity_data.start_time,
                    end_time=activity_data.end_time,
                    description=activity_data.description,
                    day_id=db_day.id
                )
                db.add(db_activity)
        
        db.commit()
        db.refresh(db_itinerary)
        
        return {
            "success": True,
            "data": db_itinerary,
            "message": "Itinerary created successfully"
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create itinerary: {str(e)}"
        )

@router.get("/", response_model=ItinerariesResponse)
def get_itineraries(
    region: Optional[str] = None,
    nights: Optional[int] = None,
    min_nights: Optional[int] = None,
    max_nights: Optional[int] = None,
    sort: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all itineraries with optional filtering and sorting.
    """
    try:
        query = db.query(Itinerary)
        
        if region:
            query = query.filter(Itinerary.region == region)
        
        if nights:
            query = query.filter(Itinerary.nights == nights)
        elif min_nights or max_nights:
            if min_nights:
                query = query.filter(Itinerary.nights >= min_nights)
            if max_nights:
                query = query.filter(Itinerary.nights <= max_nights)
        
        if sort == "nights_asc":
            query = query.order_by(Itinerary.nights.asc())
        elif sort == "nights_desc":
            query = query.order_by(Itinerary.nights.desc())
        elif sort == "name_asc":
            query = query.order_by(Itinerary.name.asc())
        else:
            query = query.order_by(Itinerary.created_at.desc())
        
        itineraries = query.all()
        
        return {
            "success": True,
            "count": len(itineraries),
            "data": itineraries
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch itineraries: {str(e)}"
        )

@router.get("/{itinerary_id}", response_model=ItineraryResponse)
def get_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
    """
    Get a specific itinerary by ID.
    """
    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    
    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Itinerary with ID {itinerary_id} not found"
        )
    
    return {
        "success": True,
        "data": itinerary
    }

@router.put("/{itinerary_id}", response_model=ItineraryResponse)
def update_itinerary(itinerary_id: int, itinerary_data: ItineraryCreate, db: Session = Depends(get_db)):
    """
    Update an existing itinerary.
    """
    db_itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    
    if not db_itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Itinerary with ID {itinerary_id} not found"
        )
    
    try:
        # Update details
        for key, value in itinerary_data.dict(exclude={"days"}).items():
            setattr(db_itinerary, key, value)
        
        # For simplicity, we're not updating nested entities here
        
        db.commit()
        db.refresh(db_itinerary)
        
        return {
            "success": True,
            "data": db_itinerary,
            "message": "Itinerary updated successfully"
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update itinerary: {str(e)}"
        )

@router.delete("/{itinerary_id}", response_model=ItineraryResponse)
def delete_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
    """
    Delete an itinerary.
    """
    db_itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    
    if not db_itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Itinerary with ID {itinerary_id} not found"
        )
    
    try:
        db.delete(db_itinerary)
        db.commit()
        
        return {
            "success": True,
            "message": "Itinerary deleted successfully"
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete itinerary: {str(e)}"
        )