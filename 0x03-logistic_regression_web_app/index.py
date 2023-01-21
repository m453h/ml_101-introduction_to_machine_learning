from flask import Flask
from flask import request
from flask import render_template
from model import DiabetesPredictor
from datetime import datetime

config = {
    "DEBUG": True  # run app in debug mode
}


app = Flask(__name__)

# Flask to use the above defined config
app.config.from_mapping(config)


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model = DiabetesPredictor()

        if request.form['pregnancies_no'] == ''\
            or request.form['glucose'] == '' \
            or request.form['blood_pressure'] == '' \
            or request.form['skin_thickness'] == '' \
            or request.form['insulin'] == '' \
            or request.form['bmi'] == '' \
            or request.form['diabetes_pedigree_fn'] == '' \
            or request.form['age'] == '':

            return render_template('base.html', display_results = False , message='Please provide\
                all the information on the form below')
 
        outcome = model.make_prediction(request.form['pregnancies_no'], 
        request.form['glucose'], 
        request.form['blood_pressure'], 
        request.form['skin_thickness'],
        request.form['insulin'],
        request.form['bmi'],
        request.form['diabetes_pedigree_fn'],
        request.form['age'])

        return render_template('base.html', display_results = True, predicted = outcome)


    return render_template('base.html', display_results = False, message = None)

if __name__ == "__main__":
    app.run()