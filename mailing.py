from thefuzz import fuzz
from thefuzz import process
from unidecode import unidecode
import os
import sys
import shutil
import csv
import posixpath

# script arguments
data = sys.argv[1]  # CSV file with fullname;email
# folder with the PDF files, whose names should be more or less the previous full names
path = sys.argv[2]
baseurl = sys.argv[3]  # base URL to create links

# get the PDF file names in path without extensions
files = [os.path.splitext(filename)[0] for filename in os.listdir(
    path) if filename.endswith('.pdf')]

# from input CSV, dictionary fullname: email
with open(data, newline='') as f:
    reader = csv.reader(f, delimiter=';')
    fullname_email = {datum[0]: datum[1].replace(
        " ", "") for datum in reader}

# create output CSV with top line link;email
output = open('output.csv', 'w')
writer = csv.writer(output, delimiter=';')
writer.writerow(['link']+['email'])

# for each fullname, choose best filename match, copy PDF file with normalize filename to normalized subfolder, and add link;email to output CSV
for file in files:
    best_match = process.extractOne(file, fullname_email.keys())[0]
    normalized_filename = unidecode(file).strip().replace(
        " ", "").replace(",", "").lower()  # normalize file names removing/modifying special characters from name (diacritics, spaces, capitals, etc.).
    writer.writerow([posixpath.join(baseurl, normalized_filename+'.pdf')] +
                    [fullname_email[best_match]])  # the URL is the baseurl argument + normalized filename (with PDF extension)
    # create subfolder called 'normalized'
    os.makedirs(os.path.join(path, 'normalized'), exist_ok=True)
    shutil.copy(os.path.join(path, file.strip()+'.pdf'), os.path.join(path, 'normalized',
                normalized_filename+'.pdf'))  # copy PDFs with normalized filenames to subfolder
