from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            df = pd.read_csv(file)
            required_columns = ['ORDER ID', 'TRACKING ID', 'VALUE', 'CUSTOMER NAME', 'PRODUCT NAME']
            
            # Ensure all required columns are present, adding blank columns if necessary
            for column in required_columns:
                if column not in df.columns:
                    df[column] = ""

            # Process the 'ORDER ID' column to remove duplicate values within the same cell
            df['ORDER ID'] = df['ORDER ID'].apply(lambda x: ' '.join(sorted(set(x.split()), key=x.split().index)))

            # Rearrange columns to move 'ORDER ID' to the left side of 'TRACKING ID'
            df = df[required_columns]

            # Limit the DataFrame to the first 500 rows
            data = df.head(500)
            return render_template('index.html', tables=[data.to_html(classes='data')], titles=data.columns.values)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
