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
output = open(os.path.basename(os.path.abspath(
    os.path.normpath(path)))+'_output.csv', 'w')
writer = csv.writer(output, delimiter=';')
writer.writerow(['link']+['email'])

# create subfolder called 'normalized' if it doesn't already exist
os.makedirs(os.path.join(path, 'normalized'), exist_ok=True)

log_list = []

for i in range(len(file_name_positions)):
    # normalize best macthes of file names removing/modifying special characters from name (diacritics, spaces, capitals, etc.).
    normalized_fullname = unidecode(fullnames[full_name_positions[i]]).strip().replace(
        " ", "").replace(",", "").lower()
    log_list.append([M[file_name_positions[i],full_name_positions[i]],normalized_fullname,filenames[file_name_positions[i]]])
    writer.writerow([posixpath.join(baseurl, normalized_fullname+'.pdf')] +
                    [fullname_email_dict[fullnames[full_name_positions[i]]]])  # the URL is the baseurl argument + normalized filename (with PDF extension)
    shutil.copy(os.path.join(path, filenames[file_name_positions[i]]+'.pdf'), os.path.join(path, 'normalized',
                                                                                                   normalized_fullname+'.pdf'))  # copy PDFs with normalized filenames to subfolder
sorted_log_list=sorted(log_list, key=lambda x:x[0])
with open(os.path.basename(os.path.abspath(os.path.normpath(path)))+'.log', 'w') as log:
    for item in sorted_log_list:
        log.write("---\n"+"SCORE: "+str(item[0])+"\n"+"OLD: "+item[2]+".pdf\n"+"NEW: "+item[1]+".pdf\n")
