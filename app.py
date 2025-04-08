#app.py
#Created by W. Mariam Sanou on 4/7/25.
#cd fashiondiva --> source .venv/bin/activate --> python app.py 

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # data to return
        return f"Email: {email}, Password: {password}"
    return render_template("SignIn.html")


if __name__ == "__main__":
    app.run(debug=True)

