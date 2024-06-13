from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
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

if __name__ == "__main__":
    app.run(debug=True)
