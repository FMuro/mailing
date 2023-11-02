import os
import sys
import csv
import posixpath
import uuid
import libmatching.libmatching as libmatching

# separate user-provided options and arguments (only expected argument "-d" for debug/test)
opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

# We now give names to default script arguments

# CSV file with fullname;email
data = args[0]

# folder with the PDF files, whose names should be more or less the previous full names
path = args[1]

# base folder name for outputs
base_folder = os.path.basename(os.path.abspath(
    os.path.normpath(path)))

# get the list of PDF file names in path without extensions
filenames = libmatching.PDF_names(path)

# from input CSV, dictionary fullname: email
with open(data, newline='') as f:
    reader = csv.reader(f, delimiter=';')
    fullname_email_dict = {datum[0]: datum[1].replace(
        " ", "").replace("\t", "") for datum in reader}

# create the list of fullnames
fullnames = list(fullname_email_dict.keys())

# get best matches list, whose elements are lists of the form [file name, full name, score]
best_matches_list = libmatching.best_matches(filenames, fullnames)[0]

# print log if debug mode is on ("-d" option) in decreasing failure likelihood order
if '-d' in opts:
    sorted_log_list = sorted(best_matches_list, key=lambda x: x[2])
    for match in sorted_log_list:
        print(*match, sep=' | ')

# create output CSV
output = open(base_folder+'_output.csv', 'w')
writer = csv.writer(output, delimiter=';')
if '-l' in opts:
    # append UUID to elements in the previous list, which will look like [file name, full name, score, UUID]
    for item in best_matches_list:
        item.append(str(uuid.uuid4().hex))
    # base URL to create links
    baseurl = args[2]
    # CSV first row
    writer.writerow(['link']+['email'])
else:
    # CSV first row
    writer.writerow(['file']+['email'])
for item in best_matches_list:
    # CSV first column
    if '-l' in opts:
        # the URL is the baseurl argument + UUID (with PDF extension)
        first_column = [posixpath.join(baseurl, item[3]+'.pdf')]
    else:
        first_column = [item[0]+'.pdf']
    writer.writerow(first_column +
                    [fullname_email_dict[item[1]]])
output.close()  # close csv file

if '-l' in opts:
    # create output subfolder if it doesn't already exist
    output_folder = base_folder+'_normalized'
    os.makedirs(output_folder, exist_ok=True)
    # reduce list to [file name, UUID]
    for item in best_matches_list:
        item.pop(2)
        item.pop(1)
    # copy renamed PDF files to output folder
    libmatching.rename_files(path, output_folder, best_matches_list)
