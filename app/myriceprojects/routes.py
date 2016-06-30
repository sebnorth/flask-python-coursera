# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request
from . import myriceprojects
from .. import db
from ..models import Project, Project2, Project3
from .dane import pobierz_dane, pobierz_opisy, pobierz_short


@myriceprojects.route('/')
def index():
    return render_template('myriceprojects/index.html')



@myriceprojects.route('/user/<username>')
def user(username):
    return render_template('myriceprojects/user.html', username=username)
    

@myriceprojects.route('/rice1')
def rice1():
    titleList = pobierz_dane('tytuly.csv')
    descriptionList =  pobierz_opisy('opisy.csv')
    titleshortList = pobierz_short('short.csv')
    db.create_all()
    Project.query.delete()
    for title, description, titleshort in zip(titleList, descriptionList, titleshortList):
        db.session.add(Project(title = title[0], description = description, titleshort = titleshort[0]))
    db.session.commit()
    objectList = Project.query.all()    
    titleList = [item.title for item in objectList]
    descriptionList = [item.description for item in objectList]
    titleshortList = [item.titleshort for item in objectList]
    dictRiceList1 = zip(titleList, descriptionList, titleshortList)
    #print(dictRiceList1)
    return render_template('myriceprojects/rice1.html',  dictRiceList1 = dictRiceList1)  
    
@myriceprojects.route('/rice2')
def rice2():
    titleList = pobierz_dane('tytuly2.csv')
    descriptionList =  pobierz_opisy('opisy2.csv')
    titleshortList = pobierz_short('short2.csv')
    db.create_all()
    Project2.query.delete()
    for title, description, titleshort in zip(titleList, descriptionList, titleshortList):
        db.session.add(Project2(title = title[0], description = description, titleshort = titleshort[0]))
    db.session.commit()
    objectList = Project2.query.all()   
    titleList = [item.title for item in objectList]
    descriptionList = [item.description for item in objectList]
    titleshortList = [item.titleshort for item in objectList]
    dictRiceList2 = zip(titleList, descriptionList, titleshortList)
    #print(descriptionList)
    return render_template('myriceprojects/rice2.html',  dictRiceList2 = dictRiceList2)    

@myriceprojects.route('/rice3')
def rice3():
    titleList = pobierz_dane('tytuly3.csv')
    descriptionList =  pobierz_opisy('opisy3.csv', 10)
    titleshortList = pobierz_short('short3.csv')
    db.create_all()
    Project3.query.delete()
    for title, description, titleshort in zip(titleList, descriptionList, titleshortList):
        db.session.add(Project3(title = title[0], description = description, titleshort = titleshort[0]))
    db.session.commit()
    objectList = Project3.query.all()   
    titleList = [item.title for item in objectList]
    descriptionList = [item.description for item in objectList]
    titleshortList = [item.titleshort for item in objectList]
    dictRiceList3 = zip(titleList, descriptionList, titleshortList)
    #print titleshortList
    return render_template('myriceprojects/rice3.html',  dictRiceList3 = dictRiceList3)         
    
#http://stackoverflow.com/questions/14428564/flask-wtf-uses-input-submit-instead-of-button-type-submit

