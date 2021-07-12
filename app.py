from flask import Flask, render_template, request
import os
from random import *

app = Flask(__name__)
ch = "ABCDEF"


@app.route('/')
def documents():
    return '''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Home</title>
            <style>
                    h2{
                       text-align: center;
                    }
                     h1{
                       text-align: center;
                    }
                    a{
                        max-width: max-content;
                        margin: auto;
                    }
                    form{
                        max-width: max-content;
                        margin: auto;
                    }
                   
                </style>
        </head>
        <body  style="background: linear-gradient(to bottom, #ffb84d 11%, #ffff 100%);object-fit: cover;background-repeat: no-repeat;">
            <h1>Click to generate 10 Document file</h1>
            <form action = "http://127.0.0.1:5000/Created">
                <br>
                <input type="submit" value="generate">
                <br>
            </form>
            <br>
            <h2><a href="http://127.0.0.1:5000/Statistical_Model">Statistical Model</a></h2>
        </body>
    </html>
    '''


@app.route('/Created')
def creat():
    creat_files()
    return '''
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>generated</title>
                <style>
                 h2{
                       text-align: center;
                    }
                    p{
                        max-width: max-content;
                        margin: auto;
                    }
                    h1{
                        max-width: max-content;
                        margin: auto;
                    }
                </style>
            </head>
            <body  style="background: linear-gradient(to bottom, #ffb84d 11%, #ffff 100%);object-fit: cover;background-repeat: no-repeat;">
                <h1>The generation was successful</h1>
                <br>
                <h2><a href="http://127.0.0.1:5000/Statistical_Model">Statistical Model</a></h2>
                <h2><a href="http://127.0.0.1:5000">Home</a></h2>
            </body>
        </html>
        '''


@app.route('/Statistical_Model')
def statistical():
    return render_template('Statistical Model.html')


@app.route('/Statistical Model Result', methods=["POST"])
def statistical_result():
    directory = os.path.dirname(os.path.abspath("app.py"))
    text_files = files(directory)
    string = request.form['query']
    matrix = count()
    query = Query(string)
    sim(matrix, query)
    matrix = sorted(matrix, reverse=True, key=lambda doc: matrix[doc]["score"])
    return render_template('Result.html', matrix=matrix, num=len(text_files))


def creat_files():
    directory = os.path.dirname(os.path.abspath("app.py"))
    text_files = files(directory)
    for file in text_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)

    for i in range(10):
        f = open(f"D{i + 1}.txt", "w")
        txt = ""
        for j in range(randint(5, 15)):
            txt += choice(ch) + " "
        f.write(txt[:len(txt) - 1])


def files(directory):
    files_in_directory = os.listdir(directory)
    text_files = [file for file in files_in_directory if file.endswith(".txt")]
    return text_files


def count():
    matrix = {}
    directory = os.path.dirname(os.path.abspath("app.py"))
    text_files = files(directory)
    for i in range(len(text_files)):
        file_name = f"D{i + 1}"
        counter = {}
        file = open(f"{file_name}.txt", "r")
        text = file.read()
        for char in ch:
            counter[char] = text.count(char)
        matrix[file_name] = counter
        file.close()
    return matrix


def Query(string):
    query = {}
    start = 1
    for char in ch:
        if char in string:
            end = string.index(';', start) if start < string.rindex(';') else string.index('>')
            query[char] = float(string[start + 2:end])
            start = string.index(';', start) + 1 if start < string.rindex(';') else start
        else:
            query[char] = 0
    return query


def sim(matrix, query):
    directory = os.path.dirname(os.path.abspath("app.py"))
    text_files = files(directory)
    for i in range(len(text_files)):
        inner = 0
        for char in ch:
            inner += (matrix[f"D{i + 1}"][char]/sum(matrix[f"D{i + 1}"].values()))*query[char]
        matrix[f"D{i + 1}"]["score"] = inner


if __name__ == '__main__':
    app.run(debug=True)
