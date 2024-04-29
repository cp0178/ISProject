
from flask_wtf import FlaskForm
from wtforms import FieldList, FileField, FormField, HiddenField, SubmitField, DecimalField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired, DataRequired
from energyData import customerData
from flask import Flask, redirect, render_template, request, url_for, session
from flask_session import Session


application = Flask(__name__)
application.config['SECRET_KEY'] = '123'
application.config['UPLOAD_FOLDER'] = 'upload'
application.config["SESSION_PERMANENT"] = False
application.config["SESSION_TYPE"] = "filesystem"
Session(application)

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

class FlatRateUploadFileForm(FlaskForm):
    rate = DecimalField("flatRate", validators=[InputRequired()])
    submit = SubmitField("Calculate Rate")

class VaryRateUploadFileForm(FlaskForm):
    rate1 = DecimalField("VaryRate1", validators=[InputRequired()])
    rate2 = DecimalField("VaryRate2", validators=[InputRequired()])
    time1 = DecimalField("TimeRate1", validators=[InputRequired()])
    time2 = DecimalField("TimeRate2", validators=[InputRequired()])
    submit = SubmitField("Calculate Rate")

class FreeWeekendsRateUploadFileForm(FlaskForm):
    rate = DecimalField("rate", validators=[InputRequired()])
    submit = SubmitField("Calculate Rate")

class highestDaysRateUploadFileForm(FlaskForm):
    rate = DecimalField("rate", validators=[InputRequired()])
    daysOff = DecimalField("daysOff", validators=[InputRequired()])
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




@application.route('/flat', methods=['GET','POST'])
def flat():
    form = FlatRateUploadFileForm()
    if form.validate_on_submit():
        session["flatRateData"] = form.rate.data
        if session["freeWeekendsRate"] == "True":
            return redirect(url_for('freeWeekends'))
        elif session["highestDaysRate"] == "True":
            return redirect(url_for('highestDays'))
        else:
            return redirect(url_for('formSubmit'))
    return render_template('flat.html', form=form)

@application.route('/vary', methods=['GET','POST'])
def vary():
    form = VaryRateUploadFileForm()
    if form.validate_on_submit():
        session["rateUno"] = form.rate1.data
        session["rateDos"] = form.rate2.data
        session["timeUno"] = form.time1.data
        session["timeDos"] = form.time2.data
        if session["flatRate"] == "True":
            return redirect(url_for('flat'))
        elif session["freeWeekendsRate"] == "True":
            return redirect(url_for('freeWeekends'))
        elif session["highestDaysRate"] == "True":
            return redirect(url_for('highestDays'))
        else:
            return redirect(url_for('formSubmit'))
    return render_template('vary.html', form=form)

@application.route('/freeWeekends', methods=['GET','POST'])
def freeWeekends():
    form = FreeWeekendsRateUploadFileForm()
    if form.validate_on_submit():
        session["freeWeekendsRateData"] = form.rate.data
        if session["highestDaysRate"] == "True":
            return redirect(url_for('highestDays'))
        else:
            return redirect(url_for('formSubmit'))
    return render_template('freeWeekends.html', form=form)

@application.route('/highestDays', methods=['GET','POST'])
def highestDays():
    form = highestDaysRateUploadFileForm()
    if form.validate_on_submit():
        session["highestDaysRateData"] = form.rate.data
        session["daysOff"] = form.daysOff.data
        return redirect(url_for('formSubmit'))
    return render_template('highestDays.html', form=form)
    

@application.route('/formSubmit', methods=['GET','POST'])
def formSubmit():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), application.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        i = customerData("Jonathan", "Procknow")
        i.energyDataInput(os.path.join(os.path.abspath(os.path.dirname(__file__)), application.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        lowestVal = []
        selectedRates = []
        if session["varyRate"] == "True":
            rateUno = float(session["rateUno"])
            rateDos = float(session["rateDos"])
            timeUno = int(session["timeUno"])
            timeDos = int(session["timeDos"])
            vary = i.varyRate(rateUno, rateDos, timeUno, timeDos) 
            lowestVal.append(vary)
            selectedRates.append("vary")
        if session["flatRate"] == "True":
            flatRate = float(session["flatRateData"])
            flat = i.flatRateCalculation(flatRate)
            lowestVal.append(flat)
            selectedRates.append("flat")
        if session["freeWeekendsRate"] == "True":
            weekend = float(session["freeWeekendsRateData"])
            freeWeekend = i.freeWeekends(weekend)
            lowestVal.append(freeWeekend)
            selectedRates.append("freeWeekends")
        if session["highestDaysRate"] == "True":
            highestDays = float(session["highestDaysRateData"])
            numDays =  int(session["daysOff"])
            high = i.highestDay(highestDays, numDays)
            lowestVal.append(high)
            selectedRates.append("highestDays")
        lowestVal.sort()
        for a in selectedRates:
            if a == "vary":
                if vary == lowestVal[0]:
                    rateVals = "Vary Rate: "+ str(round(vary,2)) + "\n"
                    if len(selectedRates) > 1:
                        for b in selectedRates:
                            if b == "flat":
                                rateVals = rateVals + "Flat Rate: " + str(round(flat,2)) + "\n"
                            if b == "freeWeekends": 
                                rateVals = rateVals + "Free Weekends: " + str(round(freeWeekend,2)) + "\n"
                            if b == "highestDays":
                                rateVals = rateVals + "Highest Days Off: " + str(round(high,2)) + "\n"
                    return render_template('results.html', content="Vary rate is your best option", num=rateVals)
            if a == "flat":
                if flat == lowestVal[0]:
                    rateVals = "Flat Rate: "+ str(round(flat,2)) + "\n"
                    if len(selectedRates) > 1:
                        for b in selectedRates:
                            if b == "vary":
                                rateVals = rateVals + "Vary Rate: " + str(round(vary,2)) + "\n"
                            if b == "freeWeekends": 
                                rateVals = rateVals + "Free Weekends: " + str(round(freeWeekend,2)) + "\n"
                            if b == "highestDays":
                                rateVals = rateVals + "Highest Days Off: " + str(round(high,2)) + "\n"
                    return render_template('results.html', content="Flat rate is your best option", num=rateVals)
            if a == "freeWeekends":
                if freeWeekend == lowestVal[0]:
                    rateVals = "Free Weekends Rate: "+ str(round(freeWeekend,2)) + "\n"
                    if len(selectedRates) > 1:
                        for b in selectedRates:
                            if b == "vary":
                                rateVals = rateVals + "Vary Rate: " + str(round(vary,2)) + "\n"
                            if b == "flat": 
                                rateVals = rateVals + "Flat Rate: " + str(round(flat,2)) + "\n"
                            if b == "highestDays":
                                rateVals = rateVals + "Highest Days Off: " + str(round(high,2)) + "\n"
                    return render_template('results.html', content="Free weekends is your best option", num=rateVals)
            if a == "highestDays":
                if high == lowestVal[0]:
                    rateVals = "Free Weekends Rate: "+ str(round(freeWeekend,2)) + "\n"
                    if len(selectedRates) > 1:
                        for b in selectedRates:
                            if b == "vary":
                                rateVals = rateVals + "Vary Rate: " + str(round(vary,2)) + "\n"
                            if b == "flat": 
                                rateVals = rateVals + "Flat Rate: " + str(round(flat,2)) + "\n"
                            if b == "freeWeekends":
                                rateVals = rateVals + "Free Weekends: " + str(round(freeWeekend,2)) + "\n"
                    return render_template('results.html', content="Highest day off is your best option", num=rateVals)
    return render_template('formSubmit.html', form=form)

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
    varyRate = False
    flatRate = False
    freeWeekendsRate = False
    highestDaysRate = False
    print(request.method)
    if request.method == 'POST':
        print("Test2")
        print(request.form.getlist("myCheckbox"))
        checkboxList = request.form.getlist("myCheckbox")
        for i in checkboxList:
            if(i == "1"):
                print("varyrate")
                varyRate = True
            if (i== "2"):
                flatRate = True
            if(i == "3"):
                freeWeekendsRate = True
            if (i== "4"):
                highestDaysRate = True
        session["varyRate"] = str(varyRate)
        session["flatRate"] = str(flatRate)
        session["freeWeekendsRate"] = str(freeWeekendsRate)
        session["highestDaysRate"] = str(highestDaysRate)
        if session["varyRate"] == "True":
            return redirect(url_for('vary'))
        elif session["flatRate"] == "True":
            return redirect(url_for('flat'))
        elif session["freeWeekendsRate"] == "True":
            return redirect(url_for('freeWeekends'))
        else:
            return redirect(url_for('highestDays'))
        
    return render_template('checkbox.html')







if(__name__ == "__main__"):
    application.run(debug=True)