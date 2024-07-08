import os
import sys
import csv
import posixpath
import uuid
from matching import PDF_names, best_matches, rename_files, sorted_table
import argparse

parser = argparse.ArgumentParser(
    prog='mailing',
    description='Mail PDF files to a list of people with names resemling the file names',
    epilog='Enjoy your teaching admin!')

parser.add_argument(
    '-l', '--list', help='CSV file with columns fullname;email', required=True)
parser.add_argument(
    '-f', '--folder', help="folder containing the PDF files called like 'Pepe Pérez, 3,5.pdf'", required=True)
parser.add_argument(
    '-u', '--url', help="base URL where the PDF files will be uploaded")
parser.add_argument('-v', '--verbose', action='store_true',
                    help='print matching list with scores')
parser.add_argument('-d', '--delimiter', help="CSV delimiter character (default: ,)", default=',')
parser.add_argument('-c', '--column', help="CSV number of column containing emails (first column is 0, last is -1, default: -1)", default='-1', type=int)
parser.add_argument('-r', '--reversed', help="PDF file names are FAMILY + GIVEN but first CSV columns are GIVEN, FAMILY or the other way around", action='store_true')
parser.add_argument('-n', '--names', help="given and family names in separate CSV columns (the first two ones)", action='store_true', required='--reversed' in sys.argv)

args = parser.parse_args()


def funcion():

    # CSV file with fullname;email
    data = args.list

    # folder with the PDF files, whose names should be more or less the previous full names
    path = args.folder

    if data is None:
        print("Error: no input CSV file")
    if path is None:
        print("Error: no input folder")
    if data is None or path is None:
        sys.exit(1)
    else:
        # base folder name for outputs
        base_folder = os.path.basename(os.path.abspath(
            os.path.normpath(path)))

        # get the list of PDF file names in path without extensions
        filenames = PDF_names(path)

        # from input CSV, dictionary fullname: email
        with open(data, newline='') as f:
            reader = csv.reader(f, delimiter=args.delimiter)
            if args.names: # if names are in separate columns
                if args.reversed:
                    fullname_email_dict = {datum[1] + " " + datum[0]: datum[args.column].replace(
                    " ", "").replace("\t", "") for datum in reader}
                else:
                    fullname_email_dict = {datum[0] + " " + datum[1]: datum[args.column].replace(
                    " ", "").replace("\t", "") for datum in reader}
            else:
                fullname_email_dict = {datum[0]: datum[args.column].replace(
                " ", "").replace("\t", "") for datum in reader}

        # create the list of fullnames
        fullnames = list(fullname_email_dict.keys())

        # get best matches list, whose elements are lists of the form [file name, full name, score]
        best_matches_list = best_matches(filenames, fullnames)[0]

        # print log if verbose mode is on ("-v" option) in decreasing failure likelihood order
        if args.verbose:
            sorted_table(best_matches_list, old_name="FILE name", new_name="MATCHED name")

        # create output CSV
        output = open(base_folder+'_mailing.csv', 'w')
        writer = csv.writer(output, delimiter=args.delimiter, quotechar='"', quoting=csv.QUOTE_ALL)

        # base URL to create links
        baseurl = args.url
        if baseurl is not None:
            # append UUID to elements in the previous list, which will look like [file name, full name, score, UUID]
            for item in best_matches_list:
                item.append(str(uuid.uuid4().hex))

            # CSV first row
            writer.writerow(['link']+['email'])
        else:
            # CSV first row
            writer.writerow(['file']+['email'])
        for item in best_matches_list:
            # CSV first column
            if baseurl is not None:
                # the URL is the baseurl argument + UUID (with PDF extension)
                first_column = [posixpath.join(baseurl, item[3]+'.pdf')]
            else:
                first_column = [item[0]+'.pdf']
            writer.writerow(first_column +
                            [fullname_email_dict[item[1]]])
        output.close()  # close csv file
        # Indicate output CSV file
        print('\nCSV file for mail merging:', output.name)

        if baseurl is not None:
            # create output subfolder if it doesn't already exist
            output_folder = base_folder+'_mailing'
            os.makedirs(output_folder, exist_ok=True)
            # reduce list to [file name, UUID]
            for item in best_matches_list:
                item.pop(2)
                item.pop(1)
            # copy renamed PDF files to output folder
            rename_files(path, output_folder, best_matches_list)

            # Indicate output folder
            print('\nrenamed PDF files copied to folder:', output_folder)
