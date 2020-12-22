#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import flask
from flask import Flask, render_template, request

common.flaskInstance = app = Flask(__name__)
common.fileOpened = False

#Function to write patterns
def writeValues(text="", diff="0", c1="0", c2="1"):
    """
    Write data in the way we need to generate a correct CSV database, updated in the file at end of func.

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
    
    common.csvDataBase.write(str(text)+","+str(diff)+","+str(c1)+","+str(c2)+",\n")
    common.csvDataBase.flush()

def htmlifiedTable(txt):
    sources = txt.split("\n")
    i = 0
    output = ""
    
    while i<len(sources):
        #Use two-times parsing for simplification and better HTML
        if (sources[i] != ""):
            l1 = -1
            l2 = -1
            d = -1
            t = ""
            values = sources[i].split(",")
            length = len(values)
            #First parsing
            if (length >= 0):
                t = values[0]
            if (length >= 1):
                if (values[1].isnumeric()):
                    d = int(values[1])
            if (length >= 2):
                if (values[2].isnumeric()):
                    l1 = int(values[2])
            if (length >= 3):
                if (values[3].isnumeric()):
                    l2 = int(values[3])
            
            #Second parsing, HTML embedding
            output += "<tr>"
            output += "<td>"
            if t != "":
                output += t
            else:
                output += "inconnu"
            output += "</td>"
            output += "<td>"
            if d != -1:
                output += str(d)
            else:
                output += "inconnu"
            output += "</td>"
            output += "<td>"
            if l1 != -1:
                output += str(l1)
            else:
                output += "inconnu"
            output += "</td>"
            output += "<td>"
            if l2 != -1:
                output += str(l2)
            else:
                output += "inconnu"
            output += "</td>"
            output += "</tr>"
        i+=1
    return output

@app.errorhandler(Exception)
def server_error(err):
    """
    Default error handler to retrieve proper error WP with right redirections.
    By using <path>§<description>, the redirection will not be history backward but redirection to <path>, and the error string <description>
    If "§" isn't used, all the error is displayed as the error string.

    Parameters
    ----------
    err : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.
    int
        DESCRIPTION.

    """
    app.logger.exception(err)
    replace = "window.location.href = &quot;"
    if ("§" in str(err)):
        val = str(err).split("§")[0]
        if (val == "go_back"):
            replace = "window.history.go(-1); return false;"
        else:
            replace += val+"&quot;"
        err = str(err).split("§")[1]
    else:
        replace += "/&quot;"
    return render_template("errors.html", error_string=str(err), redirection=replace), 500

@app.route('/')
def index():
    """
    Main page, used to enter the file you want to open. If something fails with the files, redirections should be made to here, and let user choose a new file or try again.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return render_template('index.html')

@app.route('/form', methods = ['GET', 'POST'])#GET is used to handle add words for 2=<
def form():
    """
    WP that shows the form used to add words to the DB.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    if ("common.csvDataBase" in globals()):
        if (common.fileOpened == False or common.csvDataBase.closed == True):
            fp = request.form.get("fp")
            try:
                common.csvDataBase = open(str(fp), "a+")
            except IOError:
                    flask.abort(603, description=("/§Impossible to open file as write only: "+str(fp)))
            else:
                common.fileOpened = True
                return render_template('form.html')
        else:
            return render_template('form.html')
    else:
        flask.abort(600, description="/§File not opened.")
    

@app.route('/resultat', methods=['POST'])
def resultat():
    """
    Page that shows the entered word and all that goes with in a WP

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if ("common.csvDataBase" in globals()):
        if (common.fileOpened == True and common.csvDataBase.closed == False):
            result=request.form
            writeValues(result.get("mot"), result.get("difficulte"), result.get("lettre1"), result.get("lettre2"))
            return render_template('resultat.html', mot=result.get("mot"), difficulte=result.get("difficulte"), lettre1=result.get("lettre1"), lettre2=result.get("lettre2"))
        else:
            flask.abort(601, description=("/§File closed unexpectedly: "+str(common.csvDataBase.name)))
    else:
        flask.abort(600, description="/§File not opened.")

@app.route('/table', methods=['GET'])
def table():
    """
    Shows all the data we have in the DB as a WP by using an HTML table

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    file = ""
    if ("common.csvDataBase" in globals()):
        try:
            file = open(common.csvDataBase.name, 'r')
        except IOError:
            flask.abort(602, description=("/§Impossible to open file as read only: "+str(common.csvDataBase.name)))
        else:
            data = file.read();
            file.close()
            return render_template('table.html', data=htmlifiedTable(data))
    else:
        flask.abort(600, description="/§File not opened.")

print("\n--- Server started. ---")
app.run(debug=True)
