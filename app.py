from flask import Flask, render_template, request
from algorithm import ID
import numpy as np
import csv
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('homepage.html')


@app.route('/homepage', methods=['GET','POST'])
def input_router():
    return render_template('input.html')

@app.route('/', methods=['GET','POST'])
def about_router():
    return render_template('about.html')

@app.route('/input', methods=['GET','POST'])
def home():
    PH = request.form['pH']
    EC=request.form['ec']
    ORGANIC_CARBON=request.form['organiccarbon']
    NITROGEN=request.form['nitrogen']
    PHOSPHOROUS=request.form['phosphorous']
    POTASSIUM=request.form['potassium']
    ZINC=request.form['zinc']
    BORON=request.form['boron']
    IRONS=request.form['iron']
    MANGANESE=request.form['manganese']
    COPPER=request.form['copper']
    SULPHUR=request.form['sulphur']
    array_file=np.array([['ph','ec','OC','N','P','K','Zn','B','Fe','Mn','Cu','S'],[PH,EC,ORGANIC_CARBON,NITROGEN,PHOSPHOROUS,POTASSIUM,ZINC,BORON,IRONS,MANGANESE,COPPER,SULPHUR]])
    output=ID(array_file)
    print(output)  
    return render_template('output.html',output=output)

@app.route('/output', methods=['GET','POST'])
def suggestion_router():
        n=0
        p=0
        k=0
        return render_template('npk_checker.html',nitrogen=n,phosphorous=p,potassium=k)



@app.route('/npk_checker', methods=['GET','POST'])
def suggestion_router_final():
    if request.form['Nitrogen']!='':
        if request.form['Phosphorus'] !='': 
            if request.form['Potassium'] !='':
                n=int(request.form['Nitrogen'])
                p=int(request.form['Phosphorus'])
                k=int(request.form['Potassium'])
                return render_template('npk_checker.html',nitrogen=n, phosphorous=p,potassium=k)
    return render_template('output.html')


if __name__ == "__main__":
    app.run(debug=True)















