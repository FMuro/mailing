The goal of this `python` script is to send PDF files to a list of people via links uploaded somewhere.

We must have the following things:

- A CSV file `mycontacts.csv` with two columns containing the recipients's information: **fullname;email**.
- A folder `myfolder` with all PDF files. Their names should resemble the recipient full names.
- A site `www.baseurl.com/myspace` where the output PDF files can be uploaded.

Install the requirements and run the script as follows:

```
$ python mailing.py path/to/mycontacts.csv path/to/myfolder 'www.baseurl.com/myspace'
```

The output is: 

- A CSV file called `myfolder_output.csv` which contains **link;email** (including this header line).
- A folder `myfolder/normalized` containing the PDF files with normalized file names.

Now, you must:

- Upload the contents of `myfolder/normalized` to `www.baseurl.com/myspace`.
- Merge mail `myfolder_output.csv` sending each **link** to the corresponding **email**.

You can test this script as follows. Assuming you're at this project's root:

```
$ cd test
$ python mailing.py mycontacts.csv myfolder 'www.baseurl.com/myspace'
$ cat myfolder_output.csv
```
