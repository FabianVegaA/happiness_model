import joblib
import numpy as np

from flask import (
    Flask,
    jsonify, 
    render_template,
    request,
    flash,
    make_response,
    redirect,
)
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

from wtforms import (
    Form, 
    StringField, 
    FloatField,
    validators, 
    SubmitField, 
)

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'SUPER SECRETED'

class CountryData(FlaskForm):
    name = StringField('Name', [validators.Length(min=1, max=50), validators.DataRequired()])
    economy = FloatField('Economy', [validators.NumberRange(min=0, max=100), validators.DataRequired()])
    family = FloatField('Family', [validators.NumberRange(min=0, max=100), validators.DataRequired()])
    health = FloatField('Health', [validators.NumberRange(min=0, max=100), validators.DataRequired()])
    freedom = FloatField('Freedom', [validators.NumberRange(min=0, max=100), validators.DataRequired()])
    trust = FloatField('Trust', [validators.NumberRange(min=0, max=100), validators.DataRequired()])
    generosity = FloatField('Generosity', [validators.NumberRange(min=0, max=100), validators.DataRequired()])
    dystopia = FloatField('Dystopia', [validators.NumberRange(min=0, max=100), validators.DataRequired()])
    submit = SubmitField('Send')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.route('/', methods=['GET', 'POST'])
def index():
    response = make_response(redirect('/calculate'))
    return response

@app.route('/predict', methods=['GET'])
def predict():
    X_test = np.array([0.20868,0.13995,0.28443,0.36453,0.10731,0.16681,1.56726])
    prediction = model.predict(X_test.reshape(1, -1))
    return jsonify({'prediction': list(prediction)})

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    model = joblib.load('./models/best_model.pkl')
    
    data_in = CountryData()

    context = {
        'data_in': data_in,
    }
       
    
    if not data_in.validate_on_submit():
        country_data = {
            'economy' : data_in.economy.data,
            'family' : data_in.family.data,
            'health' : data_in.health.data,
            'freedom' : data_in.freedom.data,
            'trust' : data_in.trust.data,
            'generosity': data_in.generosity.data,
            'dystopia' : data_in.dystopia.data,
        }
        
        context['country_name'] = data_in.name.data
        
        x_test = np.array(list(country_data.values())).reshape(1, 7)
        context['prediction'] = model.predict(x_test)
    
    return render_template('country_data.html', **context)    


if __name__ == "__main__":
    model = joblib.load('./models/best_model.pkl')
    app.run(port=8080, debug=True)
