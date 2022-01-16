from flask import Flask, render_template,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField ,SelectField
from wtforms.validators import DataRequired,url,ValidationError
import csv
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


def _required(form, field):
    if not field.raw_data or not field.raw_data[0]:
        raise ValidationError('Field is required')


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired(message='important ,cannot be left empty')])
    location_url=StringField('location URL',validators=[url(require_tld=False,message='important cannot be left empty')])
    open_time=StringField('open time ',validators=[DataRequired(message='important cannot be left empty')])
    closing_time=StringField('closing time ',validators=[DataRequired(message='important cannot be left empty')])
    coffee_rating=SelectField('coffee rating',choices=[('☕'),('☕☕'),('☕☕☕'),('☕☕☕☕'),('☕☕☕☕☕')],validators=[DataRequired()])
    wifi_rating=SelectField('wifi rating',choices=[('💪'),('💪💪'),('💪💪💪'),('💪💪💪💪'),('💪💪💪💪💪')],validators=[DataRequired()])
    power_supply=SelectField('power supply',choices=[('🔌'),('🔌🔌'),('🔌🔌🔌'),('🔌🔌🔌🔌'),('🔌🔌🔌🔌🔌')],validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        print(form.cafe.data)
        print(form.submit.data)
        print(type(form.wifi_rating.data))
        print(form.power_supply.data)
        lister=[[form.cafe.data,form.location_url.data,form.open_time.data,form.closing_time.data,form.coffee_rating.data,form.wifi_rating.data,form.power_supply.data]]
        with open('cafe-data.csv','a',encoding='utf-8')as dater:
            maker=csv.writer(dater,lineterminator='\n')
            maker.writerows(lister)



    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes',methods=['GET', 'POST'])
def cafes():
    # with open('cafe-data.csv', newline='',encoding='utf-8') as csv_file:
    #     csv_data = csv.reader(csv_file, delimiter=',')
    #     list_of_rows = []
    #     for row in csv_data:
    #         list_of_rows.append(row)
    #     print(list_of_rows)
    #
    df=pd.read_csv('cafe-data.csv',header=0)
    df['indexed'] = [i for i in range(len(df))]
    fr = df.pop("indexed")
    df.insert(0, 'indexed', fr)
    pipe = list(df.values)





    return render_template('cafes.html', cafes=pipe)


if __name__ == '__main__':
    app.run(debug=True)
