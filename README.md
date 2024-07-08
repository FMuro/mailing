# What does this do?

The goal of this `python` package is to send PDF files to a list of people, either as attachments or via links uploaded somewhere.

We must have the following things:

- A CSV file `mycontacts.csv` delimited with `,` (configurable through options) with at least two columns containing the recipients's information (separate columns for given and family names allowed through options):

| name                   | email                     |
| ---------------------- | ------------------------- |
| Santiago Ramírez Pérez | sramirezperez@example.com |
| ...                    | ...                       |

```
name,email
Santiago Ramírez Pérez,sramirezperez@example.com
...,...
```

- A folder `myfolder` with all PDF files. Their names should resemble the recipients's names.

Optionally, with option `--url`:

- A site `www.baseurl.com/myspace` where the output PDF files can be uploaded.

# Install

Run the following command in terminal:

```
pip install --upgrade git+https://github.com/FMuro/mailing.git#egg=mailing
```

Use this command to update the package too. 

# How to use (send files)

Run the following command:

```
mailing -l path/to/mycontacts.csv -f path/to/myfolder
```

The output is: 

- A CSV file `myfolder_mailing.csv` which looks like:
  
| file                         | email                     |
| ---------------------------- | ------------------------- |
| Santiago Ramírez Péres, .pdf | sramirezperez@example.com |
| ...                          | ...                       |
  
```
"file","email"
"Santiago Ramírez Péres, .pdf","sramirezperez@example.com"
...,...
```

Now, you must:

- Merge mail `myfolder_mailing.csv` sending each **file** to the corresponding **email**.

You can get help by running:

```
mailing -h
```

# Send links instead of files

Use option `--url`. 

```
mailing -l path/to/mycontacts.csv -f path/to/myfolder -u 'www.baseurl.com/myspace'
```

The output is:

- A CSV file `myfolder_mailing.csv` which looks like:
- 
| file                                                         | email                     |
| ------------------------------------------------------------ | ------------------------- |
| www.baseurl.com/myspace/d66cd867db5a4953b7a7763667f1dc90.pdf | sramirezperez@example.com |
| ...                                                          | ...                       |
  
```
"file","email"
"www.baseurl.com/myspace/d66cd867db5a4953b7a7763667f1dc90.pdf","sramirezperez@example.com"
...,...
```

- A folder `myfolder_mailing` within the current location containing the PDF files, renamed with a UUID for anonymity.

Now, you must:

- Upload the contents of `myfolder_mailing` to `www.baseurl.com/myspace`.
- Merge mail `myfolder_mailing.csv` sending each **link** to the corresponding **email**.

# Other options

`--verbose` prints a list of the following form in decreasing failure likelihood order for you to check if there are errors

| FILE name               | MATCHED name           | SCORE |
| ----------------------- | ---------------------- | ----- |
| Santiago Ramírez Péres, | Santiago Ramírez Pérez | 95    |
| ...                     | ...                    | ...   |

`--column COLUMN` number of column containing emails. It **deafults to the last one**. First column is `0`, last is `-1`, etc.

`--delimiter DELIMITER` choose the CSV delimiter character. **Default is `,`** and other common options are `;` and `|`, and of course tabs, but you'd have to insert a real tab in the terminal (the way of doing that depends on the terminal).

`--names` when given and family names are in separate CSV columns, i.e. it looks in either of the following two ways

| GIVEN name | FAMILY name   | email                     |
| ---------- | ------------- | ------------------------- |
| Santiago   | Ramírez Péres | sramirezperez@example.com |
| ...        | ...           | ...                       |

```
GIVEN name,FAMILY name,email
Santiago,Ramírez Péres,
...,...,
```

| FAMILY name   | GIVEN name | email                     |
| ------------- | ---------- | ------------------------- |
| Ramírez Péres | Santiago   | sramirezperez@example.com |
| ...           | ...        | ...                       |

```
FAMILY name,GIVEN name,email
Ramírez Péres,Santiago,
...,...,
```

`--reversed` if `--names` is passed and file names look like `Ramírez Péres, Santiago, 3,5.pdf` while CSV colums look like `GIVEN name,FAMILY name,email`, or the other way around, i.e. file names look like `Santiago Ramírez Péres, 3,5.pdf` and CSV colums look like `FAMILY name,GIVEN name,email`

# Testing

You can test this package as follows. Assuming you're at this project's root:

```
cd test
mailing -v -l mycontacts.csv -f myfolder
cat myfolder_mailing.csv
rm -rf myfolder_mailing
mailing -v -l mycontacts.csv -f myfolder -u 'www.baseurl.com/myspace'
cat myfolder_mailing.csv
ls myfolder_mailing
```

# Warning

If your files are called like `Pérez, Pepe, .pdf` and your CSV file has a single names column which look like `Pepe Pérez` this script won't match names reliably. The same if files look like `Pepe Pérez, .pdf` and the CSV names column looks like `Pérez, Pepe`. Something like this can only be solved when family and given names are in separate columns and you use the options `--names --reversed`.

# Remove

```
pip uninstall mailing
```