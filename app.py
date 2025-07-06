from flask import Flask, render_template, url_for, request
from src.main import calculator

app = Flask(__name__)

@app.route('/' ,methods= ['POST', 'GET'])
def index():
    if request.method == 'POST':
        return render_template('index.html', results = calculator(request.form.getlist('equation')))
    return render_template('index.html')
     
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')