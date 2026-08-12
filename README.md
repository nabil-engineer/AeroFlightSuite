# ✈️ AeroFlight Suite

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python) ![Git](https://img.shields.io/badge/Git-Version_Control-orange?logo=git) ![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github) ![License](https://img.shields.io/badge/License-MIT-green)

> 🚀 This project is part of my Software Engineering & AI portfolio.

### Professional Flight Management System developed with Python

AeroFlight Suite is a professional Python-based flight management system designed to simulate and manage flight operations through a clean, modular, and maintainable architecture.

The system integrates flight management, airport and aircraft databases, route calculation, fuel analysis, weather intelligence, flight search, filtering, sorting, statistics, and SQLite persistence.

The application enables users to:

- Create and manage flight records.
- Select aircraft from an integrated aircraft database.
- Select departure and arrival airports.
- Calculate automatic route distance using the Haversine formula.
- Calculate flight duration.
- Estimate fuel consumption.
- Calculate fuel costs.
- Analyze weather conditions and their impact on flights.
- Calculate weather severity and weather factors.
- Store flight records in a SQLite database.
- Search and filter stored flights.
- Perform advanced flight searches.
- Sort flight records.
- Manage flight statuses.
- Update flight weather, cost, and distance information.
- Delete flight records.
- View flight history.
- Display flight statistics.
- Generate professional flight reports.
- Search aircraft by manufacturer or model.
- Search airports by IATA code or city.
- Create safe SQLite database backups.

---

## 📷 Screenshots

### Main Menu

![Main Menu](screenshots/main-menu.png)

---

### New Flight

![New Flight](screenshots/new-flight.png)

---

### Flight History

![Flight History](screenshots/history.png)

---

### Statistics

![Statistics](screenshots/statistics.png)

---

## ✨ Features

✈️ Flight Management

- ✔ Flight Creation
- ✔ Flight History
- ✔ Flight Statistics
- ✔ Flight Search
- ✔ Advanced Flight Search
- ✔ Flight Filtering
- ✔ Flight Sorting
- ✔ Flight Status Management
- ✔ Flight Deletion
- ✔ Flight Updates
- ✔ Professional Flight Reports

🛫 Aircraft & Airport Database

- ✔ Aircraft Database
- ✔ Aircraft Search
- ✔ Airport Database
- ✔ Airport Search
- ✔ Search by IATA Code
- ✔ Search by City
- ✔ Manufacturer & Aircraft Model Information

🗺️ Route & Flight Calculations

- ✔ Automatic Route Distance Calculation
- ✔ Haversine Distance Calculation
- ✔ Flight Duration Calculation
- ✔ Aircraft Speed Integration
- ✔ Fuel Consumption Calculation
- ✔ Fuel Cost Calculation
- ✔ Fuel Price Management

🌦️ Weather Intelligence

- ✔ Weather Data Integration
- ✔ Weather Condition Analysis
- ✔ Weather Severity Analysis
- ✔ Weather Impact on Fuel Consumption
- ✔ Weather Factor Calculation
- ✔ Wind Speed & Direction
- ✔ Temperature
- ✔ Pressure
- ✔ Humidity
- ✔ Visibility

🗄️ Database & Data Management

- ✔ SQLite Database
- ✔ Centralized Database Connection Management
- ✔ Database Schema Migration
- ✔ Database Indexing
- ✔ CRUD Operations
- ✔ Safe SQLite Database Backups
- ✔ Absolute Database Paths
- ✔ Absolute Backup Paths

🔎 Search & Filtering

- ✔ Standard Flight Search
- ✔ Advanced Flight Search
- ✔ Departure Filtering
- ✔ Arrival Filtering
- ✔ Aircraft Filtering
- ✔ Distance Filtering
- ✔ Weather Factor Filtering
- ✔ Flight Sorting

🛡️ Reliability

- ✔ Input Validation
- ✔ Centralized Error Handling
- ✔ Database Error Handling
- ✔ Modular Architecture
- ✔ Python Compilation Checks
- ✔ Testing Infrastructure

---

## 🛠 Technologies

- Python 3
- SQLite3
- Python Standard Library
- Object-Oriented Programming (OOP)
- Modular Architecture
- Layered Database Architecture
- SQLite Online Backup API
- Haversine Formula
- Git
- GitHub

---

## 📂 Project Structure

AeroFlightSuite/
│
├── config/
│   └── config.py
│
├── core/
│   ├── catalog.py
│   ├── flight.py
│   ├── history.py
│   ├── menu.py
│   └── statistics.py
│
├── database/
│   ├── __init__.py
│   ├── backup_manager.py
│   ├── common.py
│   ├── create_queries.py
│   ├── delete_queries.py
│   ├── read_queries.py
│   ├── update_queries.py
│   └── database_manager.py
│
├── data/
│   ├── aircraft_data.py
│   └── airport_data.py
│
├── managers/
│   ├── delete_manager.py
│   ├── file_manager.py
│   ├── flight_manager.py
│   ├── flight_repository.py
│   ├── search_manager.py
│   └── status_manager.py
│
├── models/
│   └── flight_model.py
│
├── services/
│   └── flight_service.py
│
├── utils/
│   ├── calculator.py
│   ├── display.py
│   ├── logger.py
│   ├── route_calculator.py
│   └── validation.py
│
├── screenshots/
│   ├── aircraft-database.png
│   ├── airport-database.png
│   ├── history.png
│   ├── main-menu.png
│   ├── new-flight.png
│   └── statistics.png
│
├── database/
│   └── aeroflight.db
│
├── backups/
│
├── tests/
│
├── main.py
├── README.md
├── LICENSE
├── requirements.txt
└── .gitignore


## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/nabil-engineer/AeroFlightSuite.git
```

Go to the project folder:

```bash
cd AeroFlightSuite
```

Create a virtual environment (optional):

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ How to Run

Run the application from the project directory:

```bash
python main.py
```

---

## 🚀 Future Improvements

- Export Flight Reports to PDF
- Export Flight Data to Excel
- Professional Graphical User Interface (Tkinter)
- Interactive Dashboard
- Charts & Analytics
- Web Version (Flask)
- User Authentication & Login System
- REST API
- Weather API Integration
- Interactive Airport Maps
- Docker Deployment
- AI Flight Assistant
- Fuel Consumption Prediction
- Intelligent Route Optimization
- Advanced Flight Data Analysis
- Machine Learning Integration

---

## 🗺️ Project Roadmap

### ✅ Version 1.0 — Flight Management System

- Aircraft Database
- Flight Creation
- Flight History
- Flight Statistics
- Fuel Consumption Calculator
- Fuel Cost Calculation
- CSV Storage (Legacy)

---

### ✅ Version 2.0 — Flight Planner

- Airport Database
- Automatic Route Distance Calculation
- Flight Number & Flight Date
- Flight Status Management
- Flight Search
- Flight Deletion
- Aircraft Search
- Airport Search
- Modular Project Architecture

---

### ✅ Version 3.0 — Professional Database System

- SQLite Database Integration
- Complete CRUD System (Create, Read, Update, Delete)
- Advanced Flight Search
- Flight Filtering
- Flight Sorting
- Database Backup 
- Data Validation Improvements

---

### ✅ Version 4.0 — Weather Intelligence & Professional Flight Management

- Weather Model
- Weather Severity Analysis
- Weather Impact on Fuel Consumption
- Weather Factor Calculation
- Wind Speed & Direction Analysis
- Temperature, Pressure & Humidity Data
- Visibility Analysis
- Professional Flight Reports
- Advanced Flight Search
- Flight Filtering & Sorting
- Aircraft & Airport Search
- Flight Status Management
- Flight Update Operations
- Database Schema Migration
- Database Indexing
- Centralized Database Connection
- Absolute Database & Backup Paths
- SQLite Native Backup API
- Improved Modular Architecture
- Legacy Data Compatibility

---

### 🔄 Version 5.0 — Runway Performance + Professional Desktop GUI

#### Runway Performance
- Required Takeoff Distance
- Landing Distance
- Airport Elevation
- Runway Length

#### Professional Desktop GUI
- Tkinter User Interface
- Dashboard
- Icons & Images
- Charts & Analytics
- Improved User Experience

---

### 🔄 Version 6.0 — Aircraft Maintenance + Web Application

#### Aircraft Maintenance
- Aircraft Maintenance Records
- Maintenance Schedule
- Engine Hours
- Maintenance Alerts
- Maintenance History

#### Web Application
- Flask Web Application
- Responsive Interface
- User Authentication
- REST API

---

### 🔄 Version 7.0 — Airport Management + Aviation Services

#### Airport Management
- Gates
- Flights
- Aircraft Parking
- Runways
- Airport Operations

#### Aviation Services
- Weather API Integration
- Interactive Airport Maps
- PDF Flight Reports
- Excel Export

---

### 🔄 Version 8.0 — Flight Analytics

- Flight Analytics
- Charts & Statistics
- Fuel Analysis
- Monthly Reports
- Performance Analysis
- Dashboard Analytics

---

### 🔄 Version 9.0 — Advanced Web Application

- Advanced Flask Architecture
- Advanced REST API
- User & Role Management
- Advanced Flight Management
- Web-based Analytics
- Real-time Flight Data

---

### 🔄 Version 10.0 — Artificial Intelligence

- AI Flight Assistant
- Fuel Consumption Prediction
- Intelligent Route Optimization
- Flight Data Analysis
- Predictive Maintenance
- Flight Performance Prediction

---

## 👨‍💻 Author

**Nabil Elouizi**

Software Engineering Student

Python Developer

AI & Aerospace Enthusiast

🌐 Portfolio:
<https://nabil-engineer.github.io/nabil-portfolio/>

💻 GitHub:
<https://github.com/nabil-engineer>

---

## 📄 License

This project is licensed under the MIT License.