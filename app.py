<<<<<<< HEAD
# app.py
from flask import Flask, request, send_file, render_template_string
import pandas as pd
import os

app = Flask(__name__)

# HTML for file upload form
html = """
<!doctype html>
<title>Upload CSV files</title>
<h1>Upload two CSV files</h1>
<form method="post" enctype="multipart/form-data">
    <input type="file" name="file1"><br><br>
    <input type="file" name="file2"><br><br>
    <input type="submit" value="Upload and Merge">
</form>
"""

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        # Get the uploaded files
        file1 = request.files['file1']
        file2 = request.files['file2']
        
        # Load both CSV files into DataFrames
        df1 = pd.read_csv(file1, delim_whitespace=True, header=None, names=['Product', 'Count'])
        df2 = pd.read_csv(file2, delim_whitespace=True, header=None, names=['Product', 'Count'])

        # Merge and sum the counts by product
        merged_df = pd.concat([df1, df2])
        total_df = merged_df.groupby('Product', as_index=False)['Count'].sum()

        # Save the result to a new CSV file
        output_path = 'total_count.csv'
        total_df.to_csv(output_path, index=False, sep=' ')

        # Return the merged file for download
        return send_file(output_path, as_attachment=True)
=======
from flask import Flask, request, send_file, render_template_string, flash
import pandas as pd
import os
from PyPDF2 import PdfReader
import tempfile

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages

# HTML form for uploading files
html = """
<!doctype html>
<title>Upload Files</title>
<h1>Upload CSV, Excel, or PDF Files</h1>
<p>You can upload multiple files of type CSV, XLSX, or PDF</p>
<form method="post" enctype="multipart/form-data">
    <input type="file" name="files" multiple><br><br>
    <input type="submit" value="Upload and Merge">
</form>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul>
    {% for message in messages %}
      <li>{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
"""

# Helper function to read data from a file based on its type
def read_file(file):
    filename = file.filename
    if filename.endswith('.csv'):
        # Read CSV file
        return pd.read_csv(file, delim_whitespace=True, header=None, names=['Product', 'Count'])
    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        # Read Excel file
        return pd.read_excel(file, header=None, names=['Product', 'Count'])
    elif filename.endswith('.pdf'):
        # Extract text from PDF and create DataFrame manually (assuming structure)
        text = ''
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()  # Extract text from each page

        # Split text by line, then parse each line
        lines = text.splitlines()
        data = []
        for line in lines:
            parts = line.split()  # Assuming space-separated format
            if len(parts) == 2:   # Only add if two items (Product, Count)
                data.append(parts)
        return pd.DataFrame(data, columns=['Product', 'Count']).astype({'Count': 'int'})
    else:
        flash(f"Unsupported file type: {filename}")
        return pd.DataFrame()  # Return empty DataFrame if unsupported

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        files = request.files.getlist("files")
        if not files or all(f.filename == '' for f in files):
            flash("No files selected!")
            return render_template_string(html)

        data_frames = []
        
        # Process each file individually
        for file in files:
            df = read_file(file)
            if not df.empty:
                data_frames.append(df)

        # If no valid data frames were added, return a message
        if not data_frames:
            flash("No valid files uploaded!")
            return render_template_string(html)

        # Merge and sum the counts by product
        merged_df = pd.concat(data_frames, ignore_index=True)
        total_df = merged_df.groupby('Product', as_index=False)['Count'].sum()

        # Save the result to a temporary CSV file
        output_path = tempfile.mktemp(suffix=".csv")
        total_df.to_csv(output_path, index=False, sep=' ')

        # Return the merged file for download
        return send_file(output_path, as_attachment=True, download_name="merged_file.csv")
>>>>>>> cd121bb (app updated with any types of files)

    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)

