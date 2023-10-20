import os
import sys
import csv
import posixpath
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
base_folder=os.path.basename(os.path.abspath(
    os.path.normpath(path)))

# base URL to create links
baseurl = args[2]

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

# append normalized best match to elements in the previous list, which will look like [file name, full name, score, normalized full name]
for item in best_matches_list:
    item.append(libmatching.normalize_string(item[1]))

# create output CSV with top line link;email
output = open(base_folder+'_output.csv', 'w')
writer = csv.writer(output, delimiter=';')
writer.writerow(['link']+['email'])
for item in best_matches_list:
    # normalize best matches of file names removing/modifying special characters from name (diacritics, spaces, capitals, etc.).
    writer.writerow([posixpath.join(baseurl, item[3]+'.pdf')] +
                    [fullname_email_dict[item[1]]])  # the URL is the baseurl argument + normalized filename (with PDF extension)
output.close() # close csv file

# create output subfolder if it doesn't already exist
output_folder = base_folder+'_normalized'
os.makedirs(output_folder, exist_ok=True)

# reduce list to [file name, normalized full name]
for item in best_matches_list:
    item.pop(2)
    item.pop(1)

# copy renamed PDF files to output folder
libmatching.rename_files(path, output_folder, best_matches_list)