from flask import Flask, render_template, request, jsonify, redirect
import json
import pymysql
import sqlite3
from werkzeug.utils import secure_filename
import os
import magic
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import PyPDF2
from PyPDF2 import PdfFileReader
from tabulate import tabulate
import re
import pdfplumber
import pdf2image
import pytesseract
from pdf2image import convert_from_path
from pytesseract import image_to_string
import image
import io
from flask import url_for
from multilingual_pdf2text.pdf2text import PDF2Text
from multilingual_pdf2text.models.document_model.document import Document
import enchant
from nltk.tokenize import word_tokenize

app = Flask(__name__, static_url_path='/static')

score = 0
bloodpressure = 0
Cholestrol = 0
age = 0

# Creating a flask application.

@app.route("/", methods=['GET', 'POST'])
def index():
  if request.method == "POST":
    Gender = request.form['Yes_no_gender']
    age = request.form.get("age")
    tc = request.form.get("Cholestrol")
    systolic_bp = request.form.get("Systolic_blood_pressure")
    hdl = request.form.get("HDLCholestrol")
    diastolic_bp = request.form.get("Diastolic_blood_pressure")
    try:
      diabetes = request.form['Yes_no_D']
    except:
      diabetes = 'no'
    smoking = request.form['Yes_no_S']
    score = getPointstoRisk(Gender, age, tc, hdl, systolic_bp, diastolic_bp,
                            diabetes, smoking)
    comment = getRiskCategory(score)
    if (comment == "high risk"):
      color = "color:red;"
    elif (comment == "moderate risk"):
      color = "color:orange;"
    elif (comment == "low risk"):
      color = "color:lightgreen;"
    elif (comment == "very low risk"):
      color = "color:green;"
    suggestion = getSuggestion(comment)
    return render_template("index.html", var=1, score=score, comment=comment,
                           color=color, suggestion=suggestion)
  return render_template("index.html")


@app.route("/greek.html", methods=['GET', 'POST'])
def greek():
  if request.method == "POST":
    Gender = request.form['Yes_no_gender']
    print(Gender)
    age = request.form.get("age")
    print(age)
    tc = request.form.get("Cholestrol")
    print(tc)
    smoking = request.form['Yes_no_S']
    print(smoking)
    systolic_bp = request.form.get("Systolic_blood_pressure")
    print(systolic_bp)
    score = getGreekRisk(Gender, smoking, age, systolic_bp, tc)
    comment = getRiskCategory(score)
    if (comment == "high risk"):
      color = "color:red;"
    elif (comment == "moderate risk"):
      color = "color:orange;"
    elif (comment == "low risk"):
      color = "color:lightgreen;"
    elif (comment == "very low risk"):
      color = "color:green;"
    suggestion = getSuggestion(comment)
    return render_template("greek.html", var=1, score=score, comment=comment,
                           color=color, suggestion=suggestion)
  return render_template("greek.html")


app.config['SECRET_KEY'] = 'supersecretkey'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
     return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route('/pdf.html', methods=['GET',"POST"])
def upload_pdf():
  
  pytesseract.pytesseract.tesseract_cmd = r'C:\Users\manus\Desktop\Flask 2\tesseract-main\tessdata'
  os.environ['TESSDATA_PREFIX'] = r'C:\Users\manus\Desktop\Flask 2\tesseract-main\tessdata'
  os.environ['MAGIC_PATH'] = r'C:\python311\lib\site-packages\magic'
  if request.method == 'POST':
        
        
        file = request.files['file']
        file_content = file.read()
        image = pdf2image.convert_from_bytes(file_content)
        TEXT =[]
        for pagenumber, page in enumerate(image):
              pdf_document = Document(document_path= r"C:\Users\aksha\Downloads\female.pdf",language='ell')
              pdf2text = PDF2Text(document=pdf_document)
              content = pdf2text.extract()
              # detected_text = pytesseract.image_to_string(page, lang='ell')
              TEXT.append(content)
              result = ", ".join(str(v) for v in TEXT)
              result1 = result.lower()
              result2 = result1.replace(":", "")
              result2 = result2.replace(" ", "")

        ### This is one is for ENGLISH version pdf
        TEXT2 =[]
        for pagenumber, page in enumerate(image):
          detected_text = pytesseract.image_to_string(page)
          TEXT2.append(detected_text)
          result3 = ", ".join(TEXT2)
          result4 = result3.lower()
          result5 = result4.replace(" ", "")
          result5 = result5.replace(":", "")
          print(result5)


        #bloodpressure research box(free to add the any format in it)
        BPpatterns = ["(?<=συστολικἠαρτηριακἡπίεση)\d+", "(?<=συστολικἠαρτηριακἡπίεση.)\d+", "(?<=συστολικἠαρτηριακἡπίεση..)\d+", "(?<=συστολικἠαρτηριακἡπίεση..............)\d+"
        "(?<=συστολικἠαρτηριακἡπίεση...)\d+", "(?<=συστολικἠαρτηριακἡπίεση....)\d+", "(?<=συστολικἠαρτηριακἡπίεση.....)\d+", "(?<=συστολικἠαρτηριακἡπίεση......)\d+","(?<=συστολικἠαρτηριακἡπίεση..............)\d+",
        "(?<=συστολικἠαρτηριακἡπίεση.......)\d+", "(?<=συστολικἠαρτηριακἡπίεση........)\d+", "(?<=συστολικἠαρτηριακἡπίεση.........)\d+", "(?<=συστολικἠαρτηριακἡπίεση..........)\d+",
        "(?<=συστολικηαρτηριακηπιεση)\d+", "(?<=συστολικἠαρτηριακἡπίεση...........)\d+", "(?<=συστολικἠαρτηριακἡπίεση............)\d+", "(?<=συστολικἠαρτηριακἡπίεση.............)\d+", 
        "(?<=συστολικηαρτηριακηπιεση.)\d+", "(?<=συστολικηαρτηριακηπιεση..)\d+", "(?<=συστολικηαρτηριακηπιεση...)\d+", "(?<=συστολικηαρτηριακηπιεση....)\d+",
        "(?<=συστολικηαρτηριακηπιεση.....)\d+", "(?<=συστολικηαρτηριακηπιεση......)\d+", "(?<=συστολικηαρτηριακηπιεση.......)\d+", "(?<=συστολικηαρτηριακηπιεση.............)\d+", 
        "(?<=συστολικηαρτηριακηπιεση........)\d+", "(?<=συστολικηαρτηριακηπιεση.........)\d+", "(?<=συστολικηαρτηριακηπιεση..........)\d+", "(?<=συστολικηαρτηριακηπιεση..............)\d+", 
        "(?<=συστολικηαρτηριακηπιεση...........)\d+", "(?<=συστολικηαρτηριακηπιεση............)\d+"]

        ### This is one is for ENGLISH version pdf
        BPpatterns2 = ["(?<=systolicbloodpressure)\d+", "(?<=systolicbloodpressure.)\d+", "(?<=systolicbloodpressure..)\d+",
        "(?<=systolicbloodpressure...)\d+", "(?<=systolicbloodpressure....)\d+", "(?<=systolicbloodpressure.....)\d+", "(?<=systolicbloodpressure......)\d+",
        "(?<=systolicbloodpressure.......)\d+", "(?<=systolicbloodpressure........)\d+", "(?<=systolicbloodpressure.........)\d+", "(?<=systolicbloodpressure..........)\d+",
        "(?<=systolicbloodpressure...........)\d+", "(?<=systolicbloodpressure............)\d+", "(?<=systolicbloodpressure.............)\d+", "(?<=systolicbloodpressure..............)\d+",  
        "(?<=bloodpressure)\d+", "(?<=bloodpressure.)\d+", "(?<=bloodpressure..)\d+", "(?<=bloodpressure...)\d+", "(?<=bloodpressure....)\d+", "(?<=bloodpressure.....)\d+",
        "(?<=bloodpressure......)\d+", "(?<=bloodpressure.......)\d+", "(?<=bloodpressure........)\d+", "(?<=bloodpressure.........)\d+", "(?<=bloodpressure..........)\d+", 
        "(?<=bloodpressure...........)\d+", "(?<=bloodpressure............)\d+", "(?<=bloodpressure.............)\d+", "(?<=bloodpressure..............)\d+"]

        for BPpattern in BPpatterns:
          bloodpressure = re.findall(BPpattern, result2)
          if len(bloodpressure) != 0:
            break

        ### This is one is for ENGLISH version pdf
        for BPpattern2 in BPpatterns2:
          if len(bloodpressure) != 0:
            break
          else:
            bloodpressure = re.findall(BPpattern2, result5)
            if len(bloodpressure) != 0:
              break


        #cholesterol research box(free to add the any format in it)
        Cholesterolpatterns = ["(?<=χοληστερινη)\d+","(?<=XOAHETEPINH)\d+", "(?<=χοληστερινη.)\d+", "(?<=χοληστερινη..)\d+", "(?<=χοληστερινη...)\d+", "(?<=χοληστερινη....)\d+", "(?<=χοληστερινη.....)\d+",
        "(?<=χοληστερινη......)\d+", "(?<=χοληστερινη.......)\d+", "(?<=χοληστερινη........)\d+", "(?<=χοληστερινη.........)\d+", "(?<=χοληστερινη..........)\d+", "(?<=χοληστερινη...........)\d+",
        "(?<=χοληστερινη............)\d+", "(?<=χοληστερινη.............)\d+", "(?<=χοληστερινη..............)\d+", "(?<=χοληστερόλη)\d+", "(?<=χοληστερόλη.)\d+", "(?<=χοληστερόλη..)\d+" , "(?<=χοληστερόλη...)\d+",
        "(?<=χοληστερόλη....)\d+", "(?<=χοληστερόλη.....)\d+", "(?<=χοληστερόλη......)\d+", "(?<=χοληστερόλη.......)\d+", "(?<=χοληστερόλη........)\d+", "(?<=χοληστερόλη.........)\d+", "(?<=χοληστερόλη..........)\d+",
        "(?<=χοληστερόλη...........)\d+", "(?<=χοληστερόλη............)\d+", "(?<=χοληστερόλη.............)\d+", "(?<=χοληστερόλη..............)\d+", "(?<=χοληστερόλη...............)\d+", "(?<=χοληστερόλη................)\d+",
        "(?<=χοληστερόλη.................)\d+", "(?<=χοληστερόλη..................)\d+", "(?<=χοληστερόλη...................)\d+", "(?<=χοληστερόλη....................)\d+", "(?<=xoanotepoan......)\d+", "(?<=xoanotepoan.......)\d+",
        "(?<=xoanotepoan........)\d+", "(?<=xoanotepoan.........)\d+", "(?<=xoanotepoan..........)\d+", "(?<=xoanotepoan...........)\d+", "(?<=xoanotepoan............)\d+", "(?<=xoanotepoan.............)\d+",
        "(?<=xoanotepoan..............)\d+"]
        
        ### This is one is for ENGLISH version pdf
        Cholesterolpatterns2 =["(?<=cholesterol)\d+", "(?<=cholesterol.)\d+", "(?<=cholesterol..)\d+", "(?<=cholesterol...)\d+", "(?<=cholesterol....)\d+", "(?<=cholesterol.....)\d+", "(?<=cholesterol......)\d+",
        "(?<=cholesterol.......)\d+", "(?<=cholesterol........)\d+", "(?<=cholesterol.........)\d+", "(?<=cholesterol..........)\d+", "(?<=cholesterol...........)\d+", "(?<=cholesterol............)\d+",
        "(?<=cholesterol.............)\d+", "(?<=cholesterol..............)\d+"]

        Cholestrol2 = []
        for Cholesterolpattern in Cholesterolpatterns:
          Cholestrol = re.findall(Cholesterolpattern, result2)
          if len(Cholestrol) != 0 and int(Cholestrol[0]) > 149:
              for num in Cholestrol:
                if int(num) > 149:
                  Cholestrol2.append(num)
              break
          
        ### This is one is for ENGLISH version pdf  
        for Cholesterolpattern2 in Cholesterolpatterns2:
          if len(Cholestrol) != 0:
            break
          else:
            Cholestrol = re.findall(Cholesterolpattern2, result5)
            if len(Cholestrol) != 0 and int(Cholestrol[0]) > 149:
              for num in Cholestrol:
                if int(num) > 149:
                  Cholestrol2.append(num)
              break
         
        

        #Age research box(free to add the any format in it)
        Agepatterns = ["(?<=ετων)\d+", "(?<=ετων.)\d+", "(?<=ετων..)\d+", "(?<=ετων...)\d+", "(?<=ετων....)\d+", "(?<=ετων.....)\d+", "(?<=ετων......)\d+", "(?<=ετων.......)\d+", "(?<=ετων........)\d+",
        "(?<=ετων.........)\d+", "(?<=ετων..........)\d+", "(?<=ετων...........)\d+", "(?<=ετων............)\d+", "(?<=ετων.............)\d+", "(?<=ετων..............)\d+", "(?<=etan)\d+", "(?<=etan.)\d+", "(?<=etan...)\d+",
        "(?<=etan..)\d+", "(?<=etan....)\d+", "(?<=etan.....)\d+", "(?<=etan......)\d+", "(?<=etan.......)\d+", "(?<=etan........)\d+", "(?<=etan.........)\d+", "(?<=etan..........)\d+", "(?<=etan...........)\d+",
        "(?<=etan............)\d+", "(?<=etan.............)\d+", "(?<=etan..............)\d+"]

        ### This is one is for ENGLISH version pdf  
        Agepatterns2 = ["(?<=age)\d+", "(?<=age.)\d+", "(?<=age..)\d+", "(?<=age...)\d+", "(?<=age....)\d+", "(?<=age.....)\d+", "(?<=age......)\d+", "(?<=age.......)\d+", "(?<=age........)\d+", "(?<=age.........)\d+", "(?<=age..........)\d+",
        "(?<=age...........)\d+", "(?<=age............)\d+", "(?<=age.............)\d+", "(?<=age..............)\d+", "(?<=age...............)\d+"]
        # Search Age

        age2 = []
        for Agepattern in Agepatterns:
          age = re.findall(Agepattern, result2)
          if len(age) != 0:
             for num2 in age:
                if int(num2) > 40 and int(num2) < 79:
                  age2.append(num2)
             break
          
        ### This is one is for ENGLISH version pdf 
        for Agepattern2 in Agepatterns2:
          if len(age) != 0:
            break
          else:
             age = re.findall(Agepattern2, result5)
             if len(age) != 0:
               for num3 in age:
                if int(num3) > 40:
                  age2.append(num3)
             break

                
        #gender research box(free to add the any format in it)
        genderpatterns = ["(?<=φυλο)\w+","(?<=φυλο)\w+", "(?<=φυλο.)\w+", "(?<=φυλο..)\w+", "(?<=φυλο...)\w+", "(?<=φυλο....)\w+","(?<=YAO.)\w+", "(?<=φυλο.....)\w+", "(?<=φυλο......)\w+", "(?<=φυλο.......)\w+", "(?<=φυλο........)\w+", "(?<=φυλο.........)\w+", 
        "(?<=φυλο..........)\w+", "(?<=φυλο...........)\w+", "(?<=φυλο............)\w+", "(?<=φυλο.............)\w+", "(?<=φυλο..............)\w+", "(?<=ωητομ)\w+", "(?<=ωητομ.)\w+", "(?<=ωητομ..)\w+",
        "(?<=ωητομ...)\w+","(?<=ωητομ....)\w+", "(?<=ωητομ.....)\w+", "(?<=ωητομ......)\w+", "(?<=ωητομ.......)\w+", "(?<=ωητομ........)\w+", "(?<=ωητομ.........)\w+", "(?<=ωητομ..........)\w+", "(?<=ωητομ...........)\w+",
        "(?<=ωητομ............)\w+","(?<=ωητομ.............)\w+","(?<=ωητομ..............)\w+"]

        ### This is one is for ENGLISH version pdf 
        genderpatterns2 = ["(?<=gender)\w+", "(?<=gender.)\w+","(?<=gender..)\w+", "(?<=gender...)\w+", "(?<=gender....)\w+", "(?<=gender.....)\w+", "(?<=gender......)\w+", "(?<=gender.......)\w+",
        "(?<=gender........)\w+", "(?<=gender.........)\w+", "(?<=gender..........)\w+", "(?<=gender...........)\w+", "(?<=gender............)\w+", "(?<=gender.............)\w+", "(?<=gender..............)\w+"]

         # Search gender
        for genderpattern in genderpatterns:
          gender = re.findall(genderpattern, result2)
          if len(gender) != 0:
            break

         ### This is one is for ENGLISH version pdf 
        for genderpattern2 in genderpatterns2:
          if len(gender) != 0:
            break
          else:
            gender = re.findall(genderpattern2, result5)
            if len(gender) != 0:
              break
        
        if 'ἄντρας' in gender:
          gender[gender.index('ἄντρας')] = 'male'
        if 'αντρας' in gender:
          gender[gender.index('αντρας')] = 'male'
        if 'ϱϱϱϱϱϱ' in gender:
          gender[gender.index('ϱϱϱϱϱϱ')] = 'male'
        if 'γυναίκα' in gender:
          gender[gender.index('γυναίκα')] = 'female'
        if 'γυναικα' in gender:
          gender[gender.index('γυναικα')] = 'female'

        
        ## if 'male' not in gender or 'female' not in gender:
        ## gender = None

        #smoke research box(free to add the any format in it)
        somkingpatterns = ["(?<=καπνιστης)\w+", "(?<=καπνιστης.)\w+", "(?<=καπνιστης..)\w+", "(?<=καπνιστης...)\w+","(?<=KANINIETHE)\w+",
        "(?<=καπνιστης....)\w+", "(?<=καπνιστης.....)\w+", "(?<=καπνιστης......)\w+", "(?<=καπνιστης.......)\w+", "(?<=καπνιστης........)\w+","(?<=καπνιστης.........)\w+",
        "(?<=καπνιστης..........)\w+", "(?<=καπνιστης...........)\w+", "(?<=καπνιστης............)\w+", "(?<=καπνιστης.............)\w+", "(?<=καπνιστης..............)\w+",
        "(?<=καπνιστή)\w+", "(?<=καπνιστή.)\w+", "(?<=καπνιστή..)\w+", "(?<=καπνιστή...)\w+", "(?<=καπνιστή....)\w+", "(?<=καπνιστή.....)\w+", "(?<=καπνιστή......)\w+",
        "(?<=καπνιστή.......)\w+", "(?<=καπνιστή........)\w+", "(?<=καπνιστή.........)\w+", "(?<=καπνιστή..........)\w+", "(?<=καπνιστή...........)\w+", "(?<=καπνιστή............)\w+",
        "(?<=καπνιστή.............)\w+", "(?<=καπνιστή..............)\w+"]


        ### This is one is for ENGLISH version pdf
        somkingpatterns2 = ["(?<=smoker)\w+", "(?<=smoker.)\w+", "(?<=smoker..)\w+", "(?<=smoker...)\w+", "(?<=smoker....)\w+", "(?<=smoker.....)\w+", "(?<=smoker......)\w+",
        "(?<=smoker.......)\w+", "(?<=smoker........)\w+", "(?<=smoker.........)\w+", "(?<=smoker..........)\w+", "(?<=smoker...........)\w+", "(?<=smoker............)\w+",
        "(?<=smoker.............)\w+","(?<=smoker..............)\w+", "(?<=smoking)\w+", "(?<=smoking.)\w+", "(?<=smoking..)\w+", "(?<=smoking...)\w+", "(?<=smoking....)\w+", "(?<=smoking.....)\w+", "(?<=smoking......)\w+",
        "(?<=smoking.......)\w+", "(?<=smoking........)\w+", "(?<=smoking.........)\w+", "(?<=smoking..........)\w+", "(?<=smoking...........)\w+", "(?<=smoking............)\w+",
        "(?<=smoking.............)\w+","(?<=smoking..............)\w+"]


         # Search smoking
        for somkingpattern in somkingpatterns:
          smoking = re.findall(somkingpattern, result2)
          if len(smoking) != 0:
            break

        for somkingpattern2 in somkingpatterns2:
          if len(smoking) != 0:
            break
          else:
            smoking = re.findall(somkingpattern2, result5)
            if len(smoking) != 0:
              break



        if 'ναι' in smoking:
          smoking[smoking.index('ναι')] = 'yes'
        if 'ναϊ' in smoking:
          smoking[smoking.index('ναϊ')] = 'yes'
        if 'οχι' in smoking:
          smoking[smoking.index('οχι')] = 'no'
        if 'όχι' in smoking:
          smoking[smoking.index('όχι')] = 'no'

        ## if 'yes' not in smoking or 'no' not in smoking:
        ## smoking = None
        smoking = 'no'
        gender = 'female'
        
        return render_template("age.html", age = age2, Cholestrol = Cholestrol2, bloodpressure=bloodpressure, gender=gender, smoking = smoking)

        
  return render_template('pdf.html')

@app.route('/age', methods=['POST'])
def age():
  age = request.form['age']
  bloodpressure = request.form['bloodpressure']
  Cholestrol = request.form["Cholestrol"]
  gender = request.form["gender"]
  smoking = request.form["smoking"]
  score = getGreekRisk(gender, smoking, age, bloodpressure, Cholestrol)
  comment = getRiskCategory(score)
  if (comment == "high risk"):
    color = "color:red;"
  elif (comment == "moderate risk"):
    color = "color:orange;"
  elif (comment == "low risk"):
    color = "color:lightgreen;"
  elif (comment == "very low risk"):
    color = "color:green;"
  suggestion = getSuggestion(comment)

  return render_template('pdf.html', age=age, bloodpressure=bloodpressure, Cholestrol=Cholestrol, gender ='female', smoking = 'no', var=1, score=score, comment=comment,
                           color=color, suggestion=suggestion)


@app.route("/heart_failure.html", methods=['GET', 'POST'])
def heart_failure():
  if request.method == "POST":

    BNP = request.form.get("BNP")
    NtProBNP = request.form.get("NtProBNP")

    BNP, NtProBNP = int(BNP), int(NtProBNP)

    results =  calculate_heart_failure(BNP, NtProBNP)  

    return render_template("heart_failure.html",  var=1, risk_level = results['liklihood_of_heart_failure'],
                           color = results['color'])

  return render_template("heart_failure.html")



def getAgePoints(Gender, age, cur):
  if (age == None):
    return 0
  sql = """
    SELECT """ + Gender.title() + """ FROM Age_chart
    Where """ + str(age) + """ BETWEEN Age_low AND Age_high;
    """
  cur.execute(sql)
  age_pointer = cur.fetchall()
  if (age_pointer == []):
    return 0
  age_pointer = age_pointer[0][0]
  return age_pointer


def getSmokingPoints(Gender, smoking, cur):
  sql = """
    SELECT """ + Gender.title() + """ FROM Smoking_chart
    WHERE Smoking == """ + "\"" + smoking.title() + "\"" + """ ;
    """
  cur.execute(sql)
  smoking_pointer = cur.fetchall()
  smoking_pointer = smoking_pointer[0][0]
  return smoking_pointer


def getDiabetesPoints(Gender, diabetes, cur):
  sql = """
    SELECT """ + Gender.title() + """ FROM Diabetes_chart
    WHERE Diabetes == """ + "\"" + diabetes.title() + "\"" + """ ;
    """
  cur.execute(sql)
  diabetes_pointer = cur.fetchall()
  diabetes_pointer = diabetes_pointer[0][0]
  return diabetes_pointer


def getBPPoints(Gender, systolic_bp, diastolic_bp, cur):
  if (systolic_bp == None or diastolic_bp == None):
    return 0
  sql = """
    SELECT """ + Gender.title() + """ FROM BP_chart
    Where """ + str(systolic_bp) + """ BETWEEN Systolic_BP_low AND Systolic_BP_high
    AND """ + str(diastolic_bp) + """ BETWEEN Diastolic_BP_low AND Diastolic_BP_high;
    """
  cur.execute(sql)
  bp_pointer = cur.fetchall()
  if (bp_pointer == []):
    return 0
  bp_pointer = bp_pointer[0][0]
  return bp_pointer


def getHDLPoints(Gender, hdl, cur):
  if (hdl == None):
    return 0
  sql = """
    SELECT """ + Gender.title() + """ FROM HDLCholesterol_chart
    Where """ + str(hdl) + """ BETWEEN HDL_low AND HDL_high;
    """
  cur.execute(sql)
  hdl_pointer = cur.fetchall()
  if (hdl_pointer == []):
    return 0
  hdl_pointer = hdl_pointer[0][0]
  return hdl_pointer


def getTCPoints(Gender, tc, cur):
  sql = """
    SELECT """ + Gender.title() + """ FROM TC_chart
    Where """ + str(tc) + """ BETWEEN Cholesterol_low AND Cholesterol_high;
    """
  cur.execute(sql)
  tc_pointer = cur.fetchall()
  if (tc_pointer == []):
    return 0
  tc_pointer = tc_pointer[0][0]
  return tc_pointer


def getPointstoRisk(Gender, age, tc, hdl, systolic_bp, diastolic_bp, diabetes,
    smoking):
  conn = sqlite3.connect("main.db")
  cur = conn.cursor()
  try:
    total_score = getAgePoints(Gender, age, cur) \
                  + getTCPoints(Gender, tc, cur) \
                  + getHDLPoints(Gender, hdl, cur) \
                  + getBPPoints(Gender, systolic_bp, diastolic_bp, cur) \
                  + getDiabetesPoints(Gender, diabetes, cur) \
                  + getSmokingPoints(Gender, smoking, cur)
  except:
    total_score = 0
  sql = """
    SELECT """ + Gender.title() + """Risk FROM PointsToScore_chart
    Where TotalScore == """ + str(total_score) + """;
    """
  cur.execute(sql)
  pts_pointer = cur.fetchall()
  conn.close()
  pts_pointer = pts_pointer[0][0]
  return pts_pointer


def getRiskCategory(pts_pointer):
  conn = sqlite3.connect("main.db")
  cur = conn.cursor()

  sql = """
    SELECT Category FROM RiskCategory_chart
    Where """ + str(pts_pointer) + """ BETWEEN Risk_low AND Risk_high;
    """
  cur.execute(sql)
  rc_pointer = cur.fetchall()
  conn.close()
  rc_pointer = rc_pointer[0][0]
  return rc_pointer


def getGreekRisk(Gender, smoking, age, systolic_bp, tc_greek):
  conn = sqlite3.connect("main.db")
  cur = conn.cursor()
  sql = """
    SELECT Risk FROM GreekDataSet_chart
    Where Gender == """ + "\"" + Gender.lower() + "\"" + """
    AND Smoking == """ + "\"" + smoking.title() + "\"" + """
    AND """ + str(age) + """ BETWEEN Age_low AND Age_high
    AND """ + str(systolic_bp) + """ BETWEEN Systolic_BP_low AND Systolic_BP_high
    AND """ + str(tc_greek) + """ BETWEEN TC_low AND TC_high;
    """
  cur.execute(sql)
  gr_pointer = cur.fetchall()
  conn.close()
  gr_pointer = gr_pointer[0][0]
  return gr_pointer

def convert_pdf_to_img(pdf_file):
    """
    @desc: this function converts a PDF into Image
    
    @params:
        - pdf_file: the file to be converted
    
    @returns:
        - an interable containing image format of all the pages of the PDF
    """
    return convert_from_path(pdf_file)


def convert_image_to_text(file):
    """
    @desc: this function extracts text from image
    
    @params:
        - file: the image file to extract the content
    
    @returns:
        - the textual content of single image
    """
    
    text = image_to_string(file)
    return text


def get_text_from_any_pdf(pdf_file):
    """
    @desc: this function is our final system combining the previous functions
    
    @params:
        - file: the original PDF File
    
    @returns:
        - the textual content of ALL the pages
    """
    images = convert_pdf_to_img(pdf_file)
    final_text = ""
    for pg, img in enumerate(images):
        
        final_text += convert_image_to_text(img)
        #print("Page n°{}".format(pg))
        #print(convert_image_to_text(img))
    
    return final_text

def getSuggestion(riskCategory):
  conn = sqlite3.connect("main.db")
  cur = conn.cursor()

  sql = """
  SELECT suggestion FROM Suggestion_chart
  Where category == """+"\""+riskCategory.lower()+"\""+""";
  """
  cur.execute(sql)
  rc_pointer = cur.fetchall()
  conn.close()
  rc_pointer = rc_pointer[0][0]
  return rc_pointer


def calculate_heart_failure(BNP, NtProBNP):
    liklihood_of_heart_failure = 'low'
    color = 'color:green'

    if BNP >= 100 and BNP < 400:
        liklihood_of_heart_failure = 'Medium'
        color = 'color:orange'

    if NtProBNP >= 300 and NtProBNP < 1800:
        liklihood_of_heart_failure = 'Medium'
        color = 'color:orange'

    if BNP > 500:
        liklihood_of_heart_failure = 'high'
        color = 'color:red'

    if NtProBNP > 1800:
        liklihood_of_heart_failure = 'high'
        color = 'color:red'

    return {"liklihood_of_heart_failure": liklihood_of_heart_failure, "color": color}

if __name__ == "__main__":
  app.run(debug = True)
