# Travel Itinerary Backend System

<div align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/fastapi-0.95+-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/sqlalchemy-2.0+-orange.svg" alt="SQLAlchemy">
</div>

<p align="center">A comprehensive backend system for managing travel itineraries built with FastAPI and SQLAlchemy.</p>

## ✨ Features

- **Database Architecture**: Comprehensive data model for travel itineraries including day-wise hotel accommodations, transfers, and activities
- **RESTful API**: Endpoints for creating, viewing, updating, and deleting itineraries
- **MCP Server**: Recommendation system that suggests itineraries based on duration and region
- **Data Seeding**: Realistic seed data for Phuket and Krabi regions in Thailand
- **Validation**: Input validation and error handling for all API endpoints
- **Documentation**: Comprehensive API documentation with sample request/response formats

## 🛠️ Technology Stack

- **Python 3.8+**: Core programming language
- **FastAPI**: Web framework for building APIs
- **SQLAlchemy**: ORM for database interactions
- **SQLite**: Database (can be replaced with PostgreSQL for production)
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for running the application

## 📁 Project Structure

```
travel_itinerary/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI application entry point
│   ├── database.py            # Database connection setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── itinerary.py      
│   │   ├── day.py            
│   │   ├── accommodation.py  
│   │   ├── transfer.py       
│   │   └── activity.py       
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── itinerary.py      
│   │   ├── day.py            
│   │   ├── accommodation.py  
│   │   ├── transfer.py       
│   │   └── activity.py       
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── itinerary.py      
│   │   └── recommendation.py 
│   └── services/
│       ├── __init__.py
│       └── recommendation.py 
├── scripts/
│   └── seed_data.py          
├── tests/
│   ├── __init__.py
│   ├── test_itinerary.py     
│   └── test_recommendation.py 
├── requirements.txt           
├── README.md                  
└── travel_itinerary.db        
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   git clone <repository-url>
   cd travel_itinerary
```

2. Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```


3. Install dependencies:

```shellscript
pip install -r requirements.txt
```


4. Run the application:

```shellscript
uvicorn app.main:app --reload
```


5. Seed the database with sample data:

```shellscript
python scripts/seed_data.py
```

## 🙏 Acknowledgements

- FastAPI for the excellent web framework
- SQLAlchemy for the powerful ORM
- Pydantic for the data validation
- The Python community for the amazing ecosystem