from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Real_Enter.html')

@app.route('/main')
def main():
    return render_template('KSC_Web_Main_Enter.html') 

if __name__ == '__main__':
    app.run(debug=True)