The goal of this `python` script is to send PDF files to a list of people via links uploaded somewhere.

We must have the following things:

- A CSV file `mycontacts.csv` with two columns containing the recipients's information: **fullname;email**.
- A folder `myfolder` with all PDF files. Their names should resemble the recipients's full names. It is important that words (names and surnames) are always in the same order.

Optionally, with option `-l`:

- A site `www.baseurl.com/myspace` where the output PDF files can be uploaded.

Install the requirements and run the script as follows:

```
$ python mailing.py path/to/mycontacts.csv path/to/myfolder 'www.baseurl.com/myspace'
```

The normal output is: 

- A CSV file called `myfolder_output.csv` which contains **file;email** (including this header line).

With option `-l` the output is:

- A CSV file called `myfolder_output.csv` which contains **link;email** (including this header line).
- A folder `myfolder_normalized` within the current location containing the PDF files, renamed with a UUID for anonimity.

Now, you must:

- Merge mail `myfolder_output.csv` sending each **file** to the corresponding **email**.

With option `-l`, you should instead:

- Upload the contents of `myfolder_normalized` to `www.baseurl.com/myspace`.
- Merge mail `myfolder_output.csv` sending each **link** to the corresponding **email**.

The option `-d` prints a list of the form `file name | macthed name | score` in decreasing failure likelihood order for you to check if there are errors.

You can test this script as follows. Assuming you're at this project's root:

```
$ cd test
$ python3 ../mailing.py -d mycontacts.csv myfolder 'www.baseurl.com/myspace'
$ cat myfolder_output.csv
$ python3 ../mailing.py -d -l mycontacts.csv myfolder 'www.baseurl.com/myspace'
$ cat myfolder_output.csv
$ ls myfolder_normalized
```

The `zsh` script `splitpdf.sh` just wraps the [`pdfcpu`](https://github.com/pdfcpu/pdfcpu) command to split a PDF file (1st argument) into a folder (2nd argument) based on the PDF's table of contents. You can alternatively used my pure `python` solution [PDFSplitter](https://github.com/FMuro/PDFSplitter).