# ✈️ AeroFlight Suite

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python) ![Git](https://img.shields.io/badge/Git-Version_Control-orange?logo=git) ![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github) ![License](https://img.shields.io/badge/License-MIT-green)

> 🚀 This project is part of my Software Engineering & AI portfolio.

### Professional Flight Management System developed with Python

AeroFlight Suite is a Python-based application designed to simulate and manage flight operations through a clean and modular architecture.

The application enables users to:

- Create and manage flight records.
- Select aircraft from an integrated database.
- Calculate flight duration.
- Estimate fuel consumption.
- Calculate fuel costs.
- Store flight records in SQLite database.
- Create SQLite database backups.
- View flight history.
- Display flight statistics.
- Search aircraft by manufacturer or model.

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

- ✔ Flight Creation
- ✔ Flight History
- ✔ Flight Statistics
- ✔ Flight Search
- ✔ Advanced Flight Search
- ✔ Flight Filtering
- ✔ Flight Sorting
- ✔ Flight Status Management
- ✔ Flight Deletion
- ✔ Professional Flight Report

- ✔ Aircraft Database
- ✔ Aircraft Search

- ✔ Airport Database
- ✔ Airport Search

- ✔ Automatic Route Distance Calculation
- ✔ Automatic Distance Calculation using Haversine Formula
- ✔ Fuel Consumption Calculator
- ✔ Fuel Cost Calculator

- ✔ SQLite Database
- ✔ SQLite Backup

- ✔ Input Validation

---

## 🛠 Technologies

- Python 3
- SQLite3
- Python Standard Library
- Object-Oriented Programming (OOP)
- Modular Programming
- Git
- GitHub

---

## 📂 Project Structure

```text
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
│   ├── airport_data.py
│   └── flights.db
│
├── managers/
│   ├── delete_manager.py
│   ├── file_manager.py
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
├── backup/
│
├── main.py
├── README.md
├── LICENSE
├── requirements.txt
└── .gitignore
```


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

Run the application:

```bash
python main.py
```

---

## 🚀 Future Improvements

- Export Flight Reports (PDF & Excel)
- Professional Graphical User Interface (Tkinter)
- Web Version (Flask)
- User Authentication & Login System
- Weather API Integration
- Interactive Airport Maps
- Dashboard with Charts & Analytics
- REST API
- Docker Deployment
- AI Flight Assistant
- Fuel Consumption Prediction
- Intelligent Route Optimization
- Flight Data Analysis

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

### 🔄 Version 4.0 — Professional Desktop GUI

- Tkinter User Interface
- Dashboard
- Icons & Images
- Charts & Analytics
- Improved User Experience

---

### 🔄 Version 5.0 — Web Application

- Flask Web Application
- Responsive Interface
- User Authentication
- REST API

---

### 🔄 Version 6.0 — Aviation Services

- Weather API Integration
- Interactive Airport Maps
- PDF Flight Reports
- Excel Export

---

### 🔄 Version 7.0 — Artificial Intelligence

- AI Flight Assistant
- Fuel Consumption Prediction
- Intelligent Route Optimization
- Flight Data Analysis

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