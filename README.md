👗 Fashion Diva

Fashion Diva is a 2000s-themed web application that lets users upload clothing items, view them on an avatar, and interact with an AI fashion assistant.

👩‍💻 Contributors

Name	Role
JJ - Backend Developer, AI, Integration
Mariam - Frontend/Backend Developer, Design
Stephen	- Frontend Developer, Design
Elizabet	- Design
Mariela	- AI Development
Betul	- AI Development

->  Setup & Run Instructions for Fashion Diva

💻 Tech Stack
Backend: Python, Flask
Frontend: HTML/CSS/Jinja templates
AI: YOLO model integration
Database: SQLite (via schema.sql)
Storage: Local file system


-> How to Set Up & Run Locally
Clone the repository
git clone (https://github.com/CarmaClisthert/FashionDiva.git)
cd fashion-diva

-> Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

-> Install dependencies
pip install Flask opencv-python torch pillow
Set environment variable (Mac/Linux)
export FLASK_APP=app.py
export FLASK_ENV=development (On Windows use set instead of export)

-> Initialize the database
flask shell
>>> from db import init_db
>>> init_db()
>>> exit()

-> Run the application
source .venv/bin/activate
flask run
Open your browser and go to: http://localhost:5000 

📁 Project Structure
├── app.py              # Main Flask app
├── db.py               # DB connection and init
├── schema.sql          # SQLite schema
├── wardrobe.py         # Wardrobe image processing
├── static/             # CSS, images
├── templates/          # HTML (Jinja) templates
├── instance/           # Database file lives here
├── database/           
├── .gitignore
├── README.md


