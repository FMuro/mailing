#!/bin/zsh

# Splits $1 PDF file as per table of contents into $2 folder
pdfcpu split -m bookmark $1 $2