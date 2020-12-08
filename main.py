#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common

#Simple shortcut
def ws():
    """
    Just print our comma! Shortcut function!

    Returns
    -------
    None.

    """
    common.csvDataBase.write(str(","))

#Function to write patterns
def writeValues(text="", diff="0", c1="0", c2="1"):
    """
    Write data in the way we need to generate a correct database

    Parameters
    ----------
    text : TYPE, optional
        DESCRIPTION. The default is "".
    diff : TYPE, optional
        DESCRIPTION. The default is "0".
    c1 : TYPE, optional
        DESCRIPTION. The default is "0".
    c2 : TYPE, optional
        DESCRIPTION. The default is "1".

    Returns
    -------
    None.

    """
    common.csvDataBase.write(str(text))
    ws()
    common.csvDataBase.write(str(diff))
    ws()
    common.csvDataBase.write(str(c1))
    ws()
    common.csvDataBase.write(str(c2))
    common.csvDataBase.write("\n")
    


def main():
    """
    Main program function with loop

    Returns
    -------
    None.

    """
    
    succeed = False
    while succeed == False:
        fp = input("Entrez le chemin du fichiher: ")
        try:
            common.csvDataBase = open(fp, "w")
        except IOError:
                print("Failed to open the file!")
        else:
            print("Succeed to open the file!")
            succeed = True

main()

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    """
    Main page, used to enter the file you want to open

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return render_template('index.html')

@app.route('/form',methods = ['POST'])
def form():
    """
    WP that shows the text you want to add to the DB.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    result = request.form
    return render_template('form.html')

@app.route('/resultat', methods=['POST'])
def resultat():
    """
    Page that shows the entered word and all that goes with in a WP

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    result = request.form
    return render_template('resultat.html')

@app.route('/table', methods=['POST'])
def table():
    """
    Shows all the data we have in the DB as a WP.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return render_template('table.html')

app.run(debug=True)
