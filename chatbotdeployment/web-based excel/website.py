import pandas as pd
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Define the Excel file path
excel_file = 'hospital_data.xlsx'

# Load hospital data from Excel
def load_hospital_data():
    try:
        df = pd.read_excel(excel_file)
        return df
    except FileNotFoundError:
        print("Excel file not found. Creating a new one.")
        return pd.DataFrame()

# Add a new patient record
def add_patient_record(df, data):
    df = df.append(data, ignore_index=True, sort=False)
    return df

# Save data to Excel
def save_to_excel(df):
    df.to_excel(excel_file, index=False)

# Main route
@app.route('/')
def index():
    hospital_data = load_hospital_data()
    return render_template('index.html', hospital_data=hospital_data)

# Add Patient Record route
@app.route('/add_record', methods=['POST'])
def add_record():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        patient_disease = request.form['patient_disease']
        admission_date = request.form['admission_date']
        discharge_date = request.form['discharge_date']

        record = {
            'Patient ID': patient_id,
            'Patient Name': patient_name,
            'Doctor Name': doctor_name,
            'Patient Disease': patient_disease,
            'Admission Date': admission_date,
            'Discharge Date': discharge_date
        }

        hospital_data = load_hospital_data()
        hospital_data = add_patient_record(hospital_data, record)
        save_to_excel(hospital_data)
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
