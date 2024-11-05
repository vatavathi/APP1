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

    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)

