👗 Fashion Diva

Fashion Diva is a 2000s-themed web application that lets users upload clothing items, view them on an avatar, and interact with an AI fashion assistant.

👩‍💻 Contributors

Name	Role <br>
JJ - Backend Developer, AI, Integration <br>
Mariam - Frontend/Backend Developer, Design <br>
Stephen	- Frontend Developer, Design <br>
Elizabet	- Design <br>
Mariela	- AI Development <br>
Betul	- AI Development <br>

->  Setup & Run Instructions for Fashion Diva <br>

💻 Tech Stack <br>
Backend: Python, Flask <br>
Frontend: HTML/CSS/Jinja templates <br>
AI: YOLO model integration <br>
Database: SQLite (via schema.sql) <br>
Storage: Local file system <br>


-> How to Set Up & Run Locally <br>
Clone the repository <br>
git clone (https://github.com/CarmaClisthert/FashionDiva.git) <br>
cd fashion-diva <br>

-> Create a virtual environment <br>
python3 -m venv .venv <br>
source .venv/bin/activate <br>

-> Install dependencies <br>
pip install Flask <br>
pip install rembg <br>
pip install onnxruntime <br>

Set environment variable (Mac/Linux) <br>
export FLASK_APP=app.py <br>
export FLASK_ENV=development (On Windows use set instead of export) <br>

-> Initialize the database <br>
flask shell <br>
>>> from db import init_db <br>
>>> init_db() <br>
>>> exit() <br>

-> Run the application <br>
source .venv/bin/activate <br>
flask run <br>
Open your browser and go to: http://localhost:5000 <br>

📁 Project Structure <br>
├── app.py              # Main Flask app <br>
├── db.py               # DB connection and init <br>
├── schema.sql          # SQLite schema <br>
├── wardrobe.py         # Wardrobe image processing <br>
├── static/             # CSS, images <br>
├── templates/          # HTML (Jinja) templates <br>
├── instance/           # Database file lives here <br>
├── database/           <br> 
├── .gitignore <br>
├── README.md <br>


