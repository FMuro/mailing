# What does this do?

The goal of this `python` package is to send PDF files to a list of people, either as attachments or via links uploaded somewhere.

We must have the following things:

- A CSV file `mycontacts.csv` delimited with `,` (configurable through options) with at least two columns containing the recipients's information:

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

# How to use (email files)

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
file,email
Santiago Ramírez Péres, .pdf,sramirezperez@example.com
...,...
```

Now, you must:

- Merge mail `myfolder_mailing.csv` sending each **file** to the corresponding **email**.

You can get help by running:

```
mailing -h
```

# Email links instead of files

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
file,email
www.baseurl.com/myspace/d66cd867db5a4953b7a7763667f1dc90.pdf;sramirezperez@example.com
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

With `--delimiter DELIMITER` you can choose the CSV delimiter character. **Default is `,`** and other common options are `;` and `|`, and of course tabs, but you'd have to insert a real tab in the terminal (the way of doing that depends on the terminal).

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

# Remove

```
pip uninstall mailing
```