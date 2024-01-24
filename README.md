# What does this do?

The goal of this `python` package is to send PDF files to a list of people, either as attachments or via links uploaded somewhere.

We must have the following things:

- A CSV file `mycontacts.csv` with two columns containing the recipients's information: **fullname;email**.
- A folder `myfolder` with all PDF files. Their names should resemble the recipients's full names. It is important that words (names and surnames) are always in the same order.

Optionally, with option `-u`:

- A site `www.baseurl.com/myspace` where the output PDF files can be uploaded.

# Install

Run the following command in terminal:

```
pip install --upgrade git+https://github.com/FMuro/mailing.git#egg=mailing
```

Use this command to update the package too. 

# How to use

Run the following command:

```
$ mailing -l path/to/mycontacts.csv -f path/to/myfolder -u 'www.baseurl.com/myspace'
```

The normal output is: 

- A CSV file called `myfolder_mailing.csv` which contains **file;email** (including this header line).

With option `-u` the output is:

- A CSV file called `myfolder_mailing.csv` which contains **link;email** (including this header line).
- A folder `myfolder_mailing` within the current location containing the PDF files, renamed with a UUID for anonimity.

Now, you must:

- Merge mail `myfolder_mailing.csv` sending each **file** to the corresponding **email**.

With option `-u`, you should instead:

- Upload the contents of `myfolder_mailing` to `www.baseurl.com/myspace`.
- Merge mail `myfolder_mailing.csv` sending each **link** to the corresponding **email**.

The option `-v` prints a list of the form `OLD file name | NEW file name | score` in decreasing failure likelihood order for you to check if there are errors.

You can get help by running:

```
$ mailing -h
```

# Testing

You can test this package as follows. Assuming you're at this project's root:

```
$ cd test
$ mailing -v -l mycontacts.csv -f myfolder
$ cat myfolder_mailing.csv
$ rm myfolder_mailing.csv
$ mailing -v -l mycontacts.csv -f myfolder -u 'www.baseurl.com/myspace'
$ cat myfolder_mailing.csv
$ ls myfolder_mailing
$ rm -r myfolder_mailing.csv myfolder_mailing/

```

The `zsh` package `splitpdf.sh` just wraps the [`pdfcpu`](https://github.com/pdfcpu/pdfcpu) command to split a PDF file (1st argument) into a folder (2nd argument) based on the PDF's table of contents. You can alternatively used my pure `python` solution [PDFSplitter](https://github.com/FMuro/PDFSplitter).