from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
<<<<<<< HEAD
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
=======
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file:
        # Read the file into a DataFrame
        df = pd.read_csv(file)
        
        # Reorder columns: move 'id' to be the first column
        if 'id' in df.columns:
            cols = ['id'] + [col for col in df.columns if col != 'id']
            df = df[cols]
        
        # Remove 'numbers' column if it exists
        if 'numbers' in df.columns:
            df = df.drop(columns=['numbers'])
        
        # Convert DataFrame to HTML
        tables = [df.head(500).to_html(classes='data', header=True, index=False)]
        
        # Render the template with the table
        return render_template('data.html', tables=tables)
>>>>>>> 4f03da60319d9b81baa957012c4da79e1caa4c30

if __name__ == "__main__":
    app.run(debug=True)
