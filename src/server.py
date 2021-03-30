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
from flask_wtf import (
    FlaskForm
)

from wtforms import (
    Form,
    StringField,
    FloatField,
    validators,
    SubmitField,
)

app = Flask(__name__,
            template_folder='templates',
            static_folder='static'
            )
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'SUPER SECRETED'


class CountryData(FlaskForm):
    name = StringField('Name:', [validators.DataRequired()])
    economy = FloatField('Economy:', [validators.DataRequired()])
    family = FloatField('Family:', [validators.DataRequired()])
    health = FloatField('Health:', [validators.DataRequired()])
    freedom = FloatField('Freedom:', [validators.DataRequired()])
    trust = FloatField('Trust:', [validators.DataRequired()])
    generosity = FloatField('Generosity:', [validators.DataRequired()])
    dystopia = FloatField('Dystopia:', [validators.DataRequired()])
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
    x_test = np.array([0.20868, 0.13995, 0.28443,
                      0.36453, 0.10731, 0.16681, 1.56726])
    
    model = joblib.load('./models/best_model.pkl')
    prediction = model.predict(x_test.reshape(1, -1))
    return jsonify({'prediction': list(prediction)})


@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    
    model = joblib.load('./models/best_model.pkl')
    data_in = CountryData(request.form)

    context = {
        'data_in': data_in,
        'prediction': None,
    }

    if request.method == 'POST' and not data_in.validate_on_submit():
        country_data = {
            'economy': data_in.economy.data,
            'family': data_in.family.data,
            'health': data_in.health.data,
            'freedom': data_in.freedom.data,
            'trust':  data_in.trust.data,
            'generosity': data_in.generosity.data,
            'dystopia': data_in.dystopia.data,
        }

        context['country_name'] = request.form['name']

        x_test = np.array(list(country_data.values())).reshape(1, 7)
        context['prediction'] = model.predict(x_test)

    return render_template('country_data.html', **context)


if __name__ == "__main__":
    app.run()
