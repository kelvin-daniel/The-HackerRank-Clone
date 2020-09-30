from flask import render_template,request,redirect,url_for,abort
# from . import main

def index():
    '''
    view root page function that returns the index page and its data
    :return:
    '''
    myTitle='Home- Welcome to the best movie review site Online'
    return render_template('index.html', title=myTitle)