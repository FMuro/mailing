from thefuzz import process
from scipy import optimize
from scipy.sparse import csr_matrix
from unidecode import unidecode
import numpy as np
import os
import sys
import shutil
import csv
import posixpath
import collections

# separate user-provided options and arguments (only expected argument "-d" for debug/test)
opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

# We now give names to default script arguments

# CSV file with fullname;email
data = args[0]

# folder with the PDF files, whose names should be more or less the previous full names
path = args[1]

# base folder name for outputs
base_folder=os.path.basename(os.path.abspath(
    os.path.normpath(path)))

# base URL to create links
baseurl = args[2]

# get the list of PDF file names in path without extensions
filenames = [os.path.splitext(filename)[0] for filename in os.listdir(
    path) if filename.endswith('.pdf')]

# from input CSV, dictionary fullname: email
with open(data, newline='') as f:
    reader = csv.reader(f, delimiter=';')
    fullname_email_dict = {datum[0]: datum[1].replace(
        " ", "").replace("\t", "") for datum in reader}

# create the list of fullnames
fullnames = list(fullname_email_dict.keys())

# list of answers accepted as YES
yes_list = ['1', 'y', 'Y', 'yes', 'Yes', 'YES', 'ye', 'Ye', 'YE']

# get the score matrix (filenames, fullnames)
rows_list = []
columns_list = []
scores_list = []
for file, count in collections.Counter(filenames).items():
    matches = process.extract(file, fullnames)
    for match in matches:
        rows_list.append(filenames.index(file))
        columns_list.append(fullnames.index(match[0]))
        scores_list.append(match[1])
rows = np.array(rows_list)
columns = np.array(columns_list)
scores = np.array(scores_list)
M = csr_matrix((scores, (rows, columns)), shape=(
    len(filenames), len(fullnames))).toarray()

# solve the linear sum assignment problem
[file_name_positions, full_name_positions] = optimize.linear_sum_assignment(
    M, maximize=True)
total_score = M[file_name_positions, full_name_positions].sum()

# create output CSV with top line link;email
output = open(base_folder+'_output.csv', 'w')
writer = csv.writer(output, delimiter=';')
writer.writerow(['link']+['email'])

# create output subfolder if it doesn't already exist
output_folder = base_folder+'_normalized'
os.makedirs(output_folder, exist_ok=True)

for i in range(len(file_name_positions)):
    # normalize best macthes of file names removing/modifying special characters from name (diacritics, spaces, capitals, etc.).
    normalized_fullname = unidecode(fullnames[full_name_positions[i]]).strip().replace(
        " ", "").replace(",", "").lower()
    if "-v" in opts:
        print('---')
        print('OLD: '+filenames[file_name_positions[i]] + '.pdf')
        print('NEW: '+normalized_fullname+'.pdf')
    writer.writerow([posixpath.join(baseurl, normalized_fullname+'.pdf')] +
                    [fullname_email_dict[fullnames[full_name_positions[i]]]])  # the URL is the baseurl argument + normalized filename (with PDF extension)
    shutil.copy(os.path.join(path, filenames[file_name_positions[i]].strip()+'.pdf'), os.path.join(output_folder,
                                                                                                   normalized_fullname+'.pdf'))  # copy PDFs with normalized filenames to subfolder

if "-v" in opts:
    print('---')
    print('')
    print('TOTAL SCORE: '+str(total_score))
    print('')
