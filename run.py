#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common

common.fileOpened = False

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

from flask import Flask, render_template, request

common.flaskInstance = app = Flask(__name__)

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

@app.route('/form', methods = ['GET', 'POST'])#GET is used to handle add words for 2=<
def form():
    """
    WP that shows the text you want to add to the DB.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    if (common.fileOpened == False):
        fp = request.form.get("fp")
        try:
            common.csvDataBase = open(str(fp), "a+")
        except IOError:
            print("Failed to open the file!")
            return render_template('index.html', errorType="IOError: Erreur, fichier non ouvert.")
        else:
            print("Succeed to open the file!")
            common.fileOpened = True
            print("\n--- Opened file. ---")
            print("File name:", common.csvDataBase.name)
            return render_template('form.html')
    else:
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
    
    if (common.fileOpened == True):
        result=request.form
        writeValues(result.get("mot"), result.get("difficulte"), result.get("lettre1"), result.get("lettre2"))
        return render_template('resultat.html', mot=result.get("mot"), difficulte=result.get("difficulte"), lettre1=result.get("lettre1"), lettre2=result.get("lettre2"))
    else:
        return render_template('index.html', errorType="Erreur, fichier non ouvert.")

@app.route('/table', methods=['GET'])
def table():
    """
    Shows all the data we have in the DB as a WP.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    return render_template('table.html')

print("\n--- Server started. ---")
app.run(debug=True)
