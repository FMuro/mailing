from thefuzz import fuzz
from thefuzz import process
from unidecode import unidecode
import os
import sys
import shutil
import csv
import posixpath

# separate options and arguments
opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

# placeholder in case there are problems
problems = False

# script arguments
data = args[0]  # CSV file with fullname;email
# folder with the PDF files, whose names should be more or less the previous full names
path = args[1]
baseurl = args[2]  # base URL to create links
# get the PDF file names in path without extensions
files = [os.path.splitext(filename)[0] for filename in os.listdir(
    path) if filename.endswith('.pdf')]
# from input CSV, dictionary fullname: email
with open(data, newline='') as f:
    reader = csv.reader(f, delimiter=';')
    fullname_email = {datum[0]: datum[1].replace(
        " ", "").replace("\t", "") for datum in reader}
if "-d" not in opts:  # normal mode
    # create output CSV with top line link;email
    output = open(os.path.basename(os.path.abspath(
        os.path.normpath(path)))+'_output.csv', 'w')
    writer = csv.writer(output, delimiter=';')
    writer.writerow(['link']+['email'])
else:
    print('---')

# for each fullname, choose best filename match, copy PDF file with normalize filename to normalized subfolder, and add link;email to output CSV
for file in files:
    [best_match, quality] = process.extractOne(file, fullname_email.keys())
    normalized_filename = unidecode(best_match).strip().replace(
        " ", "").replace(",", "").lower()  # normalize best macthes of file names removing/modifying special characters from name (diacritics, spaces, capitals, etc.).
    if "-d" in opts:  # debug/test mode
        # debug/test mode
        print('file name='+file)
        print('best match='+best_match)
        print('quality percentage='+str(quality))
        print('link='+posixpath.join(baseurl, normalized_filename+'.pdf'))
        print('email='+fullname_email[best_match])
        print('---')
    else:  # normal mode
        # create subfolder called 'normalized' if it doesn't already exist
        os.makedirs(os.path.join(path, 'normalized'), exist_ok=True)
        # check poor quality
        if quality < 75:
            # query if accept anyway
            accept = input('WARNING: '+file+' matching ' +
                           best_match+' is poor! ('+str(quality)+'% quality). Do you accept it anyway? (y/n): ')
            if accept not in ['y', 'yes', 'Y', 'Yes', 'YES']:
                # set problems placeholder True
                problems = True
                # create subfolder called 'problematic_files' if it doesn't already exist
                os.makedirs(os.path.join(
                    path, 'problematic_files'), exist_ok=True)
                shutil.copy(os.path.join(path, file.strip()+'.pdf'), os.path.join(path, 'problematic_files',
                                                                                  file.strip()+'.pdf'))  # copy PDFs with normalized filenames to subfolder
            else:
                writer.writerow([posixpath.join(baseurl, normalized_filename+'.pdf')] +
                                [fullname_email[best_match]])  # the URL is the baseurl argument + normalized filename (with PDF extension)
                shutil.copy(os.path.join(path, file.strip()+'.pdf'), os.path.join(path, 'normalized',
                                                                                  normalized_filename+'.pdf'))  # copy PDFs with normalized filenames to subfolder
        else:
            writer.writerow([posixpath.join(baseurl, normalized_filename+'.pdf')] +
                            [fullname_email[best_match]])  # the URL is the baseurl argument + normalized filename (with PDF extension)
            shutil.copy(os.path.join(path, file.strip()+'.pdf'), os.path.join(path, 'normalized',
                                                                              normalized_filename+'.pdf'))  # copy PDFs with normalized filenames to subfolder
if problems:
    print('THERE WERE SOME PROBLEMS! Disregarded files are in the problematic_files subfolder. Deal with them separately.')
