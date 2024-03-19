
from flask_wtf import FlaskForm
from wtforms import FieldList, FileField, FormField, HiddenField, SubmitField, DecimalField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired, DataRequired
from energyData import customerData
from flask import Flask, render_template, request

application = Flask(__name__)
application.config['SECRET_KEY'] = '123'
application.config['UPLOAD_FOLDER'] = 'upload'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

class FlatRateUploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    rate = DecimalField("flatRate", validators=[InputRequired()])
    submit = SubmitField("Calculate Rate")

class VaryRateUploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    rate1 = DecimalField("VaryRate1", validators=[InputRequired()])
    rate2 = DecimalField("VaryRate2", validators=[InputRequired()])
    time1 = DecimalField("TimeRate1", validators=[InputRequired()])
    time2 = DecimalField("TimeRate2", validators=[InputRequired()])
    submit = SubmitField("Calculate Rate")

class FreeWeekendsRateUploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    rate = DecimalField("rate", validators=[InputRequired()])
    submit = SubmitField("Calculate Rate")

class compareUploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    rate1 = DecimalField("VaryRate1", validators=[InputRequired()])
    rate2 = DecimalField("VaryRate2", validators=[InputRequired()])
    time1 = DecimalField("TimeRate1", validators=[InputRequired()])
    time2 = DecimalField("TimeRate2", validators=[InputRequired()])
    flatRate = DecimalField("flatRate", validators=[InputRequired()])
    weekends = DecimalField("weekendsRate", validators=[InputRequired()])
    highestDays = DecimalField("highestDaysRate", validators=[InputRequired()])
    numDays = DecimalField("numDays", validators=[InputRequired()])
    submit = SubmitField("Calculate Rate")

class fileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    rate1 = DecimalField("VaryRate1", validators=[InputRequired()])
    rate2 = DecimalField("VaryRate2", validators=[InputRequired()])
    time1 = DecimalField("TimeRate1", validators=[InputRequired()])
    time2 = DecimalField("TimeRate2", validators=[InputRequired()])
    flatRate = DecimalField("flatRate", validators=[InputRequired()])
    weekends = DecimalField("weekendsRate", validators=[InputRequired()])
    highestDays = DecimalField("highestDaysRate", validators=[InputRequired()])
    numDays = DecimalField("numDays", validators=[InputRequired()])
    submit = SubmitField("Calculate Rate")
    checkboxList = HiddenField("checkboxList")

#class chooseRateFileForm(FlaskForm):



@application.route('/flat', methods=['GET','POST'])
def flat():
    form = FlatRateUploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), application.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        flatRate = form.rate.data
        i = customerData("Jonathan", "Procknow")
        i.energyDataInput(os.path.join(os.path.abspath(os.path.dirname(__file__)), application.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        calcRate = i.flatRateCalculation(float(flatRate))
        return "Your rate is " + str(calcRate)
    return render_template('flat.html', form=form)

@application.route('/vary', methods=['GET','POST'])
def vary():
    form = VaryRateUploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), application.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        rateUno = form.rate1.data
        rateDos = form.rate2.data
        timeUno = form.time1.data
        timeDos = form.time2.data
        i = customerData("Jonathan", "Procknow")
        i.energyDataInput(os.path.join(os.path.abspath(os.path.dirname(__file__)), application.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        calcRate = i.varyRate(float(rateUno), float(rateDos), int(timeUno), int(timeDos))
        return "Your rate is " + str(calcRate)
    return render_template('vary.html', form=form)

@application.route('/freeWeekends', methods=['GET','POST'])
def freeWeekends():
    form = FreeWeekendsRateUploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), application.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        rate = form.rate.data
        i = customerData("Jonathan", "Procknow")
        i.energyDataInput(os.path.join(os.path.abspath(os.path.dirname(__file__)), application.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        calcRate = i.freeWeekends(float(rate))
        return "Your rate is " + str(calcRate)
    return render_template('freeWeekends.html', form=form)

@application.route('/', methods=['GET','POST'])
def index():
    form = compareUploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), application.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        rateUno = form.rate1.data
        rateDos = form.rate2.data
        timeUno = form.time1.data
        timeDos = form.time2.data
        flatRate = form.flatRate.data
        weekend = form.weekends.data
        highestDays = form.highestDays.data
        numDays = form.numDays.data
        i = customerData("Jonathan", "Procknow")
        i.energyDataInput(os.path.join(os.path.abspath(os.path.dirname(__file__)), application.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        calcRate = i.compareRates(float(rateUno), float(rateDos), int(timeUno), int(timeDos), float(flatRate), float(weekend), float(highestDays), int(numDays))
        return render_template('results.html', content=calcRate)
    return render_template('index.html', form=form)

@application.route('/checkbox', methods=['GET','POST'])
def checkbox():
    print(request.method)
    if request.method == 'POST':
        print("Test2")
        print(request.form.getlist("myCheckbox"))
        checkboxList = request.form.getlist("myCheckbox")
        return render_template('displayCheckbox.html', checkboxList=checkboxList)
    return render_template('checkbox.html')

@application.route('/displayCheckbox', methods=['GET','POST'])
def displayCheckbox():
    form = fileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), application.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        rateUno = form.rate1.data
        rateDos = form.rate2.data
        timeUno = form.time1.data
        timeDos = form.time2.data
        flatRate = form.flatRate.data
        weekend = form.weekends.data
        highestDays = form.highestDays.data
        numDays = form.numDays.data
        checkboxList = form.checkboxList.data
        i = customerData("Jonathan", "Procknow")
        i.energyDataInput(os.path.join(os.path.abspath(os.path.dirname(__file__)), application.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        calcRate = i.variableCompareRates(float(rateUno), float(rateDos), int(timeUno), int(timeDos), float(flatRate), float(weekend), float(highestDays), int(numDays), checkboxList)
        return render_template('results.html',form=form, content=calcRate)
    return render_template('displayCheckbox.html', form=form)




#@application.route('compareRates', methods=['GET','POST'])
#def compareRates():
 #   form =
  #  if form.validate_on_submit():
   #     return render_template('results.html', content=calcRate)
    #return render_template('compareRates.html', form=form)

if(__name__ == "__main__"):
    application.run(debug=True)