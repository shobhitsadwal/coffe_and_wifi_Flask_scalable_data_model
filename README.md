# coffe_and_wifi_Flask_scalable_data_model
this is a website made by me to gather the data of the people who love to work in cafes but need pretty reliable wifi connections and also a good power supply for their laptops to carry their tasks without any power issues .

![fico](https://media.vlpt.us/images/daylee/post/ea7e3bdf-dc67-4b03-9136-4043606ee8f4/image.png)

# files to refer 
  - ```requirements.txt``` for all the requirments 
  - ```main.py``` for the flask application operations and the main execution application file 
  - ```static/``` for the css styling
  - ```templates/``` tempelates with bootsrapping modifications
  - ```cafe-data.csv``` the comma seperated values containing the records inputs 
  - ```cafe-data-scalable.txt``` this is the scalable code containing the use of Databases 
  
 # Aims and objective 
  to build a website that contains the information by the working professionals in any place of the country thay are living in to notify and help others which cafe is the best to chose from by refering 
  to these four variables 
  
       opened time 
       closed time
       coffee taste
       power supply for charging laptops 
       wifi for internet access and to work from cafes 
       
# project preparation 
  the project was built entirely with the help of **flask** , **flask-wtforms** and **flask-bootstrap**,
  for reading more about flask bootstrap and go to a little documentaion of combining the responsiveness to a website design go here https://pythonhosted.org/Flask-Bootstrap/ ,
  for reading how wtforms work please go here https://wtforms.readthedocs.io/en/2.3.x/validators/ ,
  for boostrap documentation please go here https://getbootstrap.com/
  
# front-end 
The base is the index.html which is the home or the base adress which is referred as ```/``` or ```127:1.11.01:500``` . The base index or the home page have a welcome template along with a show me button.
The show me buttons connnect with the ```cafe-data.csv``` file which displays the table that contains the column *cafe-name,location,open,close,coffee,wifi and power*.

The page that displays the table comes under the ```/cafes``` in the address box in the search bar of the browser . We have actually not made a button  for the adding operations but we can access it using ```/add``` to
add the data . The ```/add``` redirects us to a page in which there is a flask bootstrap form with built in validators waiting for our input . 

After filling out the required form it redirects us to the ```/cafes``` and we can see our tables being displayed as they are stored in CSV .

![tin](https://media.vlpt.us/images/daylee/post/b0b5e1a2-7a37-4991-b9aa-872c63e2869e/image.png)

![bin](https://media.vlpt.us/images/daylee/post/2ece378e-6eee-425b-aa82-9a963b5618a0/image.png)

# Backend with flask 

now as we have seen how everything is working in the frontend we should know how code flow is running in the backend , the ```main.py``` is the core part of this whole project as it has the route and the methods that are
connected with the front-end oparate within the flow of the framework. 

## the main.py contains the following code
```python
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
```

- from flask.wtforms we have imported Flaskforms. We have to use the Flaskform class for the inheritance of the forms and validation data from the same .The use of flaskform is emphasized here because it 
is more versatile and has better warnings rather than the own designed. After making the class from the inherited flaskforms we can initiate the form back to the page and use the forms in the *add.html* template .

- ```@app.route``` is set as decorator which is completing the frameworks fucntionality . We have set some of the methods with ```methods=['GET','POST']``` because of both posting and retrieving the data from the flask forms 
- the use of ```forms.validate_on_submit()``` is used here because the forms are being validated while running on the web , if their is no validation , the form quality will suffer which will result in insignificant data .
- the last method which is pointing to the cafes.html template is reading from the csv file . We used pandas here because it is simple to make a dataframe that is optimsed for table structures and further reduving complexity


# using extends in bootsrap 

the booststrap boiler plate is a very basic but has some world class css modificatons inside it , we can see the code below for the usage of inline blocking and extends 

```html
{% extends 'bootstrap/base.html' %}

{% block title %}Add A New Cafe{% endblock %}
{% block styles %}
    {{super()}}
    <link rel="stylesheet"
          href="{{url_for('.static', filename='./css/styles.css')}}">
{% endblock %}

{% block content %}
<div class="container">
  <div class="row">
    <div class="col-sm-12 col-md-8">

      <h1>Add a new cafe into the database</h1>

      <!-- This is where your WTForm will go -->
        <form action="{{url_for('add_cafe')}}" method="post" >

            {{form.csrf_token}}
       <p>
          {% include "bootstrap/base.html"%}
          {{ form.csrf_token }}
          {{ form.cafe.label }}<br>{{ form.cafe(size=30) }}<br>
          {%for errors in form.cafe.errors%}
          <span style="color:red">{{(errors)}}</span>
          {%endfor%}
       </p>
        <p>
          {% include "bootstrap/base.html"%}
          {{ form.csrf_token }}
          {{ form.location_url.label }}<br>{{ form.location_url(size=30) }}<br>
          {%for errors in form.location_url.errors%}
          <span style="color:red">{{flash(errors)}}</span>
          {%endfor%}
        </p>
        <p>
            {% include "bootstrap/base.html"%}
            {{ form.csrf_token }}
            {{ form.open_time.label }}<br>{{ form.open_time(size=30) }}<br>
            {%for errors in form.open_time.errors%}
            <span style="color:red">{{errors}}</span>
            {%endfor%}
        </p>
        <p>
            {% include "bootstrap/base.html"%}
            {{ form.csrf_token }}
            {{ form.closing_time.label }}<br>{{ form.closing_time(size=30) }}<br>
            {%for errors in form.closing_time.errors%}
            <span style="color:red">{{errors}}</span>
            {%endfor%}
        </p>
        <p>
            {% include "bootstrap/base.html"%}
            {{ form.csrf_token }}
            {{ form.coffee_rating.label }}<br>{{ form.coffee_rating() }}<br>
            {%for errors in form.coffee_rating.errors%}
            <span style="color:red">{{errors}}</span>
            {%endfor%}
        </p>
        <p>
            {% include "bootstrap/base.html"%}
            {{ form.csrf_token }}
            {{ form.wifi_rating.label }}<br>{{ form.wifi_rating()}}<br>
            {%for errors in form.wifi_rating.errors%}
            <span style="color:red">{{errors}}</span>
            {%endfor%}
        </p>
        <p>
            {% include "bootstrap/base.html"%}
            {{ form.csrf_token }}
            {{ form.power_supply.label }}<br>{{ form.power_supply() }}<br>
            {%for errors in form.power_supply.errors%}
            <span style="color:red">{{errors}}</span>
            {%endfor%}
        </p>

        <p>
        {% include "bootstrap/base.html"%}
        {{ form.submit }}
        </p>

        </form>

	    <p class="space-above"><a href="/cafes">See all cafes</a></p>


    </div>
  </div>
</div>

{% endblock %}

```

# Jinja templating in Flask 

Flask uses Jinja templating to insert the values given by python to iterate or insert the codeblocks from the program to the html page. Jinja is the main component inside the flask ,
```{{}}``` and ```{}``` are the Jinja temp extension blocks for linking the html pages to the decorator with the adress value that the user gives.


# Further improvements and scalablity of the model 

if we open **cafe-data-scalable.txt** , we will see that there is a slight modification to the code , the new code contains and links to the database that has been configured by **sql-alchemy**

```python
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    location_url=db.Column(db.String(300), unique=True, nullable=False)
    opentime=db.Column(db.String(80), unique=True, nullable=False)
    closingtime=db.Column(db.String(80), unique=True, nullable=False)
    coffe_rating=db.Column(db.String(80), unique=True, nullable=False)
    wifi_rating=db.Column(db.String(80), unique=True, nullable=False)
    power_supply=db.Column(db.String(80), unique=True, nullable=False)
    
class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired(message='important ,cannot be left empty')])
    location_url=StringField('location URL',validators=[url(require_tld=False,message='important cannot be left empty')])
    open_time=StringField('open time ',validators=[DataRequired(message='important cannot be left empty')])
    closing_time=StringField('closing time ',validators=[DataRequired(message='important cannot be left empty')])
    coffee_rating=SelectField('coffee rating',choices=[('☕'),('☕☕'),('☕☕☕'),('☕☕☕☕'),('☕☕☕☕☕')],validators=[DataRequired()])
    wifi_rating=SelectField('wifi rating',choices=[('💪'),('💪💪'),('💪💪💪'),('💪💪💪💪'),('💪💪💪💪💪')],validators=[DataRequired()])
    power_supply=SelectField('power supply',choices=[('🔌'),('🔌🔌'),('🔌🔌🔌'),('🔌🔌🔌🔌'),('🔌🔌🔌🔌🔌')],validators=[DataRequired()])
    submit = SubmitField('Submit')

```

the new block of code is very important in creating a database that can be very useful in storing a huge amount of data if the code has to be deployed online. The csv files are not a good choice 
to store the data as there are always risk and chances of missing files and code unreachablity .

Further the site can also be improved by adding some of the more functionality like booking the place in advance by making a form and an api of the same . The next idea also revolves around creating 
a website that monitors the cafe situation in a particular area and provides inforamtion to the owners analysing data according to the information we collect throgh this website .



 

   
    
  



