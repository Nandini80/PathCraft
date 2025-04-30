import sys
import os
from datetime import date, time
from decimal import Decimal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models import Itinerary, Day, Accommodation, Transfer, Activity

def seed_database():
    """
    Seed the database with realistic data for Phuket and Krabi regions.
    """
    print("Starting database seeding...")
    
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        db.query(Activity).delete()
        db.query(Transfer).delete()
        db.query(Accommodation).delete()
        db.query(Day).delete()
        db.query(Itinerary).delete()
        
        print("Existing data cleared. Creating new seed data...")
        
        durations = [2, 3, 4, 5, 6, 7, 8]
        regions = ["Phuket", "Krabi"]
        
        # Phuket activities
        phuket_activities = [
            {"name": "Phi Phi Islands Tour", "description": "Full-day speedboat tour to Phi Phi Islands with snorkeling and lunch"},
            {"name": "Phuket Old Town Tour", "description": "Explore the historic streets and architecture of Phuket Old Town"},
            {"name": "Big Buddha Visit", "description": "Visit the iconic 45-meter tall Big Buddha statue with panoramic views"},
            {"name": "Patong Beach Day", "description": "Relax at Phuket's most famous beach with water activities"},
            {"name": "Fantasea Show", "description": "Evening cultural show showcasing Thai heritage and elephants"},
            {"name": "James Bond Island Tour", "description": "Visit the famous island featured in 'The Man with the Golden Gun'"},
            {"name": "Thai Cooking Class", "description": "Learn to cook authentic Thai dishes with a local chef"},
            {"name": "Similan Islands Snorkeling", "description": "Day trip to the pristine Similan Islands for snorkeling"},
            {"name": "Bangla Road Nightlife", "description": "Experience Phuket's vibrant nightlife scene"},
            {"name": "Elephant Sanctuary Visit", "description": "Ethical elephant experience at a local sanctuary"}
        ]
        
        krabi_activities = [
            {"name": "Four Islands Tour", "description": "Visit Chicken Island, Tup Island, Poda Island, and Phra Nang Cave Beach"},
            {"name": "Railay Beach Day", "description": "Explore the stunning limestone cliffs and beaches of Railay"},
            {"name": "Emerald Pool & Hot Springs", "description": "Swim in the natural Emerald Pool and relax in the hot springs"},
            {"name": "Tiger Cave Temple", "description": "Climb 1,237 steps to the summit for panoramic views of Krabi"},
            {"name": "Kayaking in Ao Thalane", "description": "Paddle through stunning mangrove forests and limestone karsts"},
            {"name": "Hong Islands Tour", "description": "Visit the beautiful Hong Islands with their lagoons and beaches"},
            {"name": "Rock Climbing", "description": "Try rock climbing on Railay's world-famous limestone cliffs"},
            {"name": "Krabi Night Market", "description": "Experience local food and culture at the Krabi Town night market"},
            {"name": "Thung Teao Forest Natural Park", "description": "Hike through pristine rainforest to the Crystal Lagoon"},
            {"name": "Island Hopping Tour", "description": "Explore multiple islands in the Andaman Sea in one day"}
        ]
        
        for region in regions:
            activities = phuket_activities if region == "Phuket" else krabi_activities
            
            for nights in durations:
                if nights <= 3:
                    itinerary_type = "Quick Getaway"
                elif nights >= 7:
                    itinerary_type = "Extended Vacation"
                else:
                    itinerary_type = "Adventure"
                
                itinerary_name = f"{region} {nights}-Night {itinerary_type}"
                
                itinerary = Itinerary(
                    name=itinerary_name,
                    region=region,
                    nights=nights,
                    description=f"Experience the best of {region} in {nights} nights",
                    highlights=[a["name"] for a in activities[:3]],  
                    price_estimate=Decimal(800 + (nights * 150)),
                    tags=["beach", "culture", "nightlife" if region == "Phuket" else "nature"], 
                    is_recommended=True
                )
                db.add(itinerary)
                db.flush() 
                
                # Create days for this itinerary
                for day_num in range(1, nights + 2):  
                    day_date = date(2023, 6, day_num)  
                    
                    day = Day(
                        day_number=day_num,
                        date=day_date,
                        itinerary_id=itinerary.id
                    )
                    db.add(day)
                    db.flush() 
                    
                    # Add accommodation for each day
                    hotel_name = f"{region} {'Beach' if region == 'Phuket' else 'Cliff'} Resort"
                    
                    accommodation = Accommodation(
                        hotel_name=hotel_name,
                        check_in_time=time(14, 0) if day_num == 1 else None,
                        check_out_time=time(11, 0) if day_num == nights + 1 else None,
                        day_id=day.id
                    )
                    db.add(accommodation)
                    
                    # Add transfers for first and last day
                    if day_num == 1:
                        transfer = Transfer(
                            from_location=f"{region} Airport",
                            to_location=hotel_name,
                            departure_time=time(12, 0),
                            day_id=day.id
                        )
                        db.add(transfer)
                    elif day_num == nights + 1:
                        transfer = Transfer(
                            from_location=hotel_name,
                            to_location=f"{region} Airport",
                            departure_time=time(13, 0),
                            day_id=day.id
                        )
                        db.add(transfer)
                    
                    # Add activities (except for departure day)
                    if day_num <= nights:
                        # Choose activities based on day number (to ensure variety)
                        activity_index = (day_num - 1) % len(activities)
                        activity_data = activities[activity_index]
                        
                        activity = Activity(
                            activity_name=activity_data["name"],
                            start_time=time(9, 0),
                            end_time=time(16, 0),
                            description=activity_data["description"],
                            day_id=day.id
                        )
                        db.add(activity)
                        
                        # Add evening activity every other day
                        if day_num % 2 == 0:
                            evening_activity_index = (day_num + 3) % len(activities)
                            evening_activity_data = activities[evening_activity_index]
                            
                            evening_activity = Activity(
                                activity_name=f"Evening: {evening_activity_data['name']}",
                                start_time=time(18, 0),
                                end_time=time(21, 0),
                                description=evening_activity_data["description"],
                                day_id=day.id
                            )
                            db.add(evening_activity)
        
        db.commit()
        print("Database seeding completed successfully!")
        return {"success": True, "message": "Database seeded successfully"}
    
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {str(e)}")
        return {"success": False, "error": str(e)}
    
    finally:
        db.close()

if __name__ == "__main__":
    result = seed_database()
    print(result["message"])
    if not result["success"]:
        sys.exit(1)