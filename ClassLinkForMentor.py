import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QTextEdit, QHBoxLayout, QWidget,QLabel
from PyQt5.QtGui import QPixmap
import colorama

import sys
import os
from multiprocessing import Process
import sqlite3
import time
import datetime
import random
import webbrowser
import threading
import cryptography.fernet
import pyAesCrypt
import mysql.connector
from flask import request as req
from flask import Flask, jsonify
import logging
from signal import SIGTERM

import flask
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QRadioButton,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QListWidget,
    QHBoxLayout,
    QAction,
    QMenuBar,
    QInputDialog,
    QFileDialog,
    QListView,
    QLineEdit,
    QMessageBox,
    QLabel,
    QGraphicsLineItem,
    QColorDialog,
    QTextEdit,
    QComboBox,
    QFormLayout
    )
from PyQt5.QtGui import QColor ,QPalette,QFont,QStandardItemModel,QStandardItem
from PyQt5.QtCore import QTimer ,QThread ,pyqtSignal,Qt
import json
import hashlib
import psycopg2
import base64
import signal
from cryptography.fernet import Fernet
from functools import partial
import cryptography
import socket

import QRGeneration
status = True

class ThemeCreator(QWidget):
    signal = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Выбор Цветов')
        self.setGeometry(100, 100, 300, 300)
        self.setStyleSheet(f'background-color : #202020; color : #FFFFFF')


        # Инициализация списка для хранения выбранных цветов
        self.colors = [QColor(255, 255, 255) for _ in range(3)]  # Начальные цвета (белый)

        # Создание вертикального layout
        layout = QVBoxLayout()
        
        # Создание кнопок и меток для каждого цвета
        self.color_labels = []

        h_layout = QHBoxLayout() 
        btn = QPushButton(f'Выбрать цвет для фона')
        btn.setStyleSheet('background-color: #303030;border-radius: 7px;')
        btn.clicked.connect(lambda checked, index=0: self.choose_color(index))
        h_layout.addWidget(btn)

        label = QLabel()
        label.setStyleSheet('background-color: #FFFFFF; border: 1px solid black;')
        label.setFixedSize(20, 20)
        h_layout.addWidget(label)
        self.color_labels.append(label)

        layout.addLayout(h_layout)

        h_layout = QHBoxLayout() 
        btn = QPushButton(f'Выбрать цвет для символв')
        btn.setStyleSheet('background-color: #303030;border-radius: 7px;')
        btn.clicked.connect(lambda checked, index=1: self.choose_color(index))
        h_layout.addWidget(btn)

        label = QLabel()
        label.setStyleSheet('background-color: #FFFFFF; border: 1px solid black;')
        label.setFixedSize(20, 20)
        h_layout.addWidget(label)
        self.color_labels.append(label)

        layout.addLayout(h_layout)

        h_layout = QHBoxLayout() 
        btn = QPushButton(f'Выбрать цвет для контуров')
        btn.setStyleSheet('background-color: #303030;border-radius: 7px;')
        btn.clicked.connect(lambda checked, index=2: self.choose_color(index))
        h_layout.addWidget(btn)

        label = QLabel()
        label.setStyleSheet('background-color: #FFFFFF; border: 1px solid black;')
        label.setFixedSize(20, 20)
        h_layout.addWidget(label)
        self.color_labels.append(label)
        
        layout.addLayout(h_layout)


        save_button = QPushButton('Сохранить')
        save_button.setStyleSheet('background-color: #303030;border-radius: 7px;')
        save_button.clicked.connect(self.sendColors)
        layout.addWidget(save_button)
        self.setLayout(layout)


    def choose_color(self, index):
        color = QColorDialog.getColor()
        if color.isValid():
            self.colors[index] = color
            self.color_labels[index].setStyleSheet(f'background-color: {color.name()}; border: 1px solid black;')
    def update_color_display(self):
        # Обновление текста метки с выбранными цветами
        self.colors_text = ', '.join([c if c else 'None' for c in self.colors])
    def sendColors(self):
        self.signal.emit([i.name() for i in self.colors])

        self.close()

class FormToDelete(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Удаление ученика")

        self.formLayout = QFormLayout()

        self.surname = QLineEdit(self)
        self.name = QLineEdit(self)
        self.pat = QLineEdit(self)
        self.klass = QLineEdit(self)
        self.klassName = QLineEdit(self)
        self.parent1In = QLineEdit(self)
        self.parent2In = QLineEdit(self)


        # Добавляем поля в форму
        self.formLayout.addRow(QLabel("Фамилия:"), self.surname)
        self.formLayout.addRow(QLabel("Имя:"), self.name)
        self.formLayout.addRow(QLabel("Отчество:"), self.pat)
        self.formLayout.addRow(QLabel("Класс:"), self.klass)
        self.formLayout.addRow(QLabel("Воспитатель:"), self.klassName)
        self.formLayout.addRow(QLabel("Первый родитель:"), self.parent1In)
        self.formLayout.addRow(QLabel("Второй родитель:"), self.parent2In)


        # Кнопка отправки
        self.submitButton = QPushButton("Удалить", self)
        self.submitButton.clicked.connect(self.handleSubmit)  

        layout = QVBoxLayout()
        layout.addLayout(self.formLayout)
        layout.addWidget(self.submitButton)

        self.setLayout(layout)
    connectdatasignal = pyqtSignal(list)
    def handleSubmit(self):
        self.sur = self.surname.text()
        self.name = self.name.text()
        self.pat = self.pat.text()
        self.klass = self.klass.text()
        self.klassname = self.klassName.text()
        self.parent1 = self.parent1In.text()
        self.parent2 = self.parent2In.text()

        self.connectdatasignal.emit([self.sur,self.name,self.pat,self.klass,self.klassname,self.parent1,self.parent2])
        self.close()

class FormToAdd(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавление данных")

        self.formLayout = QFormLayout()

        self.surname = QLineEdit(self)
        self.name = QLineEdit(self)
        self.pat = QLineEdit(self)
        self.klass = QLineEdit(self)
        self.klassName = QLineEdit(self)
        self.parent1In = QLineEdit(self)
        self.parent2In = QLineEdit(self)


        # Добавляем поля в форму
        self.formLayout.addRow(QLabel("Фамилия:"), self.surname)
        self.formLayout.addRow(QLabel("Имя:"), self.name)
        self.formLayout.addRow(QLabel("Отчество:"), self.pat)
        self.formLayout.addRow(QLabel("Класс:"), self.klass)
        self.formLayout.addRow(QLabel("Воспитатель:"), self.klassName)
        self.formLayout.addRow(QLabel("Первый родитель:"), self.parent1In)
        self.formLayout.addRow(QLabel("Второй родитель:"), self.parent2In)


        # Кнопка отправки
        self.submitButton = QPushButton("Добавить", self)
        self.submitButton.clicked.connect(self.handleSubmit)  

        layout = QVBoxLayout()
        layout.addLayout(self.formLayout)
        layout.addWidget(self.submitButton)

        self.setLayout(layout)
    connectdatasignal = pyqtSignal(list)
    def handleSubmit(self):
        self.sur = self.surname.text()
        self.name = self.name.text()
        self.pat = self.pat.text()
        self.klass = self.klass.text()
        self.klassname = self.klassName.text()
        self.parent1 = self.parent1In.text()
        self.parent2 = self.parent2In.text()

        self.connectdatasignal.emit([self.sur,self.name,self.pat,self.klass,self.klassname,self.parent1,self.parent2])
        self.close()

class ListOfAbsence(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ClassLink QR for mentors")
        font = app.font()
        font.setFamily('Consolas')
        font.setBold(True)
        font.setPointSize(14)
        self.setFixedSize(700,600)
        app.setFont(font)

        self.list = QTableWidget(self)
        layout = QHBoxLayout(self)

        self.load()

        layout.addWidget(self.list)
        self.setLayout(layout)
    def load(self):
        connection = sqlite3.connect('qrDatabase.db')
        cursor = connection.cursor()

        students = cursor.execute('SELECT Surname, Name, Pat, InInternat FROM internat ').fetchall()
        self.list.setColumnCount(4)
        self.list.setRowCount(len(students))
        self.list.setHorizontalHeaderLabels(['Фамилия','Имя','Отчество','В интернате'])
        for s ,idxs in enumerate(students):
            for i, idxi in enumerate(idxs):
                if idxi == 0:
                    idxi = 'Нет'
                elif idxi == 1:
                    idxi = 'Да'
                item = QTableWidgetItem(str(idxi))
                self.list.setItem(s,i,item)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            
class Main(QMainWindow):
    
    def __init__(self):
        super().__init__()
        name ,ok= QInputDialog.getText(self,'Подвердите личность','Введите имя: ')
        if name and ok:
            login ,ok= QInputDialog.getText(self,'Подвердите личность','Введите логин: ')
            if login and ok:
                password ,ok= QInputDialog.getText(self,'Подвердите личность','Введите пароль (он скрыт): ',echo=True)
                if password and ok:
                    data = [name,login,password]
                    if not self.auth(data):
                        status = False
                        self.closeEvent()
                        return
        self.setWindowTitle("ClassLink QR for mentors")
        font = app.font()
        font.setFamily('Consolas')
        font.setBold(True)
        font.setPointSize(14)
        app.setFont(font)

        
        self.menu_bar = self.menuBar()
        list_of_absence = self.menu_bar.addMenu("Посещении")
        func_menu = self.menu_bar.addMenu('Функции')
        theme_menu = self.menu_bar.addMenu('Тема')

        self.showListAbsence = QAction('Показать список посещения',self)

        self.showListAbsence.triggered.connect(self.showAbsence)

        list_of_absence.addAction(self.showListAbsence)

        self.addStudent = QAction('Добавить ученика',self)
        self.deleteStudent = QAction('Удалить ученика', self)

        self.addStudent.triggered.connect(self.addStudentFunc)
        self.deleteStudent.triggered.connect(self.deleteStudentFunc)

        func_menu.addAction(self.addStudent)
        func_menu.addAction(self.deleteStudent)

        self.selectColorW = ThemeCreator()
        self.selectColorW.signal.connect(self.selfTheme)

        light_theme = QAction("Светлая тема",self)
        dark_theme = QAction("Темная тема",self)
        self_theme = QAction("Своя тема" ,self)

        light_theme.triggered.connect(self.lightTheme)
        dark_theme.triggered.connect(self.darkTheme)
        self_theme.triggered.connect(self.selectColorW.show)

        theme_menu.addAction(light_theme)
        theme_menu.addAction(dark_theme)
        theme_menu.addAction(self_theme)


        self.studentList = QListWidget()
        self.student_info = QTextEdit()
        self.student_info.setReadOnly(True)  
        self.studentList.setFixedWidth(400)

        self.loadStudents()

        self.studentList.itemClicked.connect(self.display_student_info)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.studentList)
        self.layout.addWidget(self.student_info)

        self.file_update_timer = QTimer()
        self.file_update_timer.timeout.connect(self.loadStudents)
        self.file_update_timer.start(2000)

        container = QWidget()
        container.setLayout(self.layout)
        self.QR = QLabel()
        self.setCentralWidget(container)
        self.showMaximized()

        with open('settings.json' ,'r',encoding='utf-8') as f:
            data = json.load(f)
            back = data['back']
            fore = data['fore']
            border = data['border']
        self.backgroundColor = back
        self.foregroundColor = fore
        self.borderColor = border
        self.setStyleSheet(f'background-color : {self.backgroundColor}; color : {self.foregroundColor}')
        self.studentList.setStyleSheet(f"""
    QListWidget {{border-radius: 10px; padding: 5px;}}
    QListWidget::item {{padding: 5px; border-radius: 7px;}}
    QListView {{border: 1px solid {self.borderColor}}}
    QTableView {{border: 1px solid {self.borderColor}}}
    """)
        self.student_info.setStyleSheet((f"""
    QListWidget {{border-radius: 10px; padding: 5px;}}
    QListWidget::item {{padding: 5px; border-radius: 7px;}}
    QListView {{border: 1px solid {self.borderColor}}}
    {{border: 3px solid {self.borderColor}}}
    """))
        self.student_info.setStyleSheet(f"border-radius: 7px solid {self.borderColor}")

    def loadStudents(self):
        self.studentList.clear()
        connection = sqlite3.connect('qrDatabase.db')
        cursor = connection.cursor()

        students = cursor.execute('SELECT * FROM internat').fetchall()
        for s in students:
            surname = s[0]
            name = s[1]
            pat = s[2]

            data = surname + ' ' + name + ' ' + pat
            self.studentList.addItem(data)

    def display_student_info(self, current):
        if current:
            self.QR.clear()
            self.QR.hide()
            connection = sqlite3.connect('qrDatabase.db')
            cursor = connection.cursor()
            student_name = current.text().split()

            info = ''
            
            print(student_name)

            surname = student_name[0]
            name = student_name[1]
            pat = student_name[2]

            print(surname,name,pat)
            student_inf = cursor.execute(f'SELECT * FROM internat WHERE Surname = "{surname}" AND Name = "{name}" AND Pat = "{pat}"').fetchall()[0] 
            print(student_inf)
            klass = student_inf[3]
            klassName = student_inf[4]
            parent1 = student_inf[5]
            parent2 = student_inf[6]

            inSchool = student_inf[7]


            info += f'Фамилия: {surname}\nИмя: {name}\nОтчество: {pat}\nКласс: {klass}\nВоспитатель: {klassName}\nВ интернате: {'Да' if inSchool == 1 else 'Нет'}'
            
            self.QR = QLabel(self)


            self.qr = QPixmap(f'{surname}_{name}_{pat}_{klass}.png')
            self.QR.setPixmap(self.qr.scaled(300, 300, aspectRatioMode=True))

        
            layout = QHBoxLayout(self)
            layout.addWidget(self.QR)
            self.layout.addLayout(layout)
            self.student_info.setText(info)

    def showAbsence(self):
        self.winAb = ListOfAbsence()
        self.winAb.show()

    def addStudentFunc(self):
        self.addwin = FormToAdd()
        self.addwin.connectdatasignal.connect(self.adding)
        self.addwin.show()
    
    def adding(self,data):
        connection = sqlite3.connect('qrDatabase.db')
        cursor = connection.cursor()
        name = data[1]
        surname = data[0]
        pat = data[2]
        klass = data[3]
        klassName = data[4]
        parent = [data[5], data[6]]
        try:
            cursor.execute(f'INSERT INTO "internat" (Surname, Name, Pat, Class,ClassName,Parent1,Parent2,InInternat) VALUES ("{data[0]}","{data[1]}","{data[2]}","{data[3]}","{data[4]}","{data[5]}","{data[6]}",0)')
        except Exception as error:
            QMessageBox.critical(self, 'Ошибка',f'Ошибка: {error}')
        else:
            QMessageBox.information(self,'Добавлено','Ученик добавлен!')
            QRGeneration.QRGeneration(surname=surname,
                                      name=name,
                                      patronymic=pat,
                                      klass=klass,
                                      klassName=klassName,
                                      parents=parent).generateQR()
            cursor.close()
            connection.commit()
            connection.close()

    def deleteStudentFunc(self):
        self.delwin = FormToDelete()
        self.delwin.connectdatasignal.connect(self.deleting)
        self.delwin.show()

    def deleting(self,data):
        connection = sqlite3.connect('qrDatabase.db')
        cursor = connection.cursor()
        try:
            r = QMessageBox.question(self,'Удаление','Вы точно хотите удалить ученика?',QMessageBox.Yes | QMessageBox.No)
            if r == QMessageBox.Yes:
                cursor.execute(f'DELETE FROM internat WHERE Surname = "{data[0]}" AND Name = "{data[1]}" AND Pat = "{data[2]}" AND Class = "{data[3]}" AND ClassName = "{data[4]}" AND Parent1 = "{data[5]}" AND Parent2 = "{data[6]}"')
            else:
                return
        except Exception as error:
            QMessageBox.critical(self, 'Ошибка',f'Ошибка: {error}')
        else:

            QMessageBox.information(self,'Удалено','Ученик удален!')
            cursor.close()
            connection.commit()
            connection.close()

    def auth(self,data):
        try:
            connection = sqlite3.connect('qrDatabase.db')
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM nursery WHERE Name = "{data[0]}" AND Login = "{data[1]}" AND Password = "{data[2]}"')
            if cursor == []:
                QMessageBox.critical(self, 'Ошибка',f'Ошибка: Неправильные данные или пароль')
                return False
    
            
        except Exception as error:
            QMessageBox.critical(self, 'Ошибка',f'Ошибка:True {error}')
            return False
        
        else:
            return True

    def lightTheme(self):
        self.backgroundColor = '#FFFFFF'
        self.foregroundColor = '#000000'
        self.borderColor = '#000000'
        self.setStyleSheet(f'background-color : {self.backgroundColor}; color : {self.foregroundColor}')
        self.studentList.setStyleSheet(f"""
    QListWidget {{border-radius: 10px; padding: 5px;}}
    QListWidget::item {{padding: 5px; border-radius: 7px;}}
    QListView {{border: 1px solid {self.borderColor}}}
    QTableView {{border: 3px solid {self.borderColor}}}
    """)
        self.student_info.setStyleSheet((f"""
    QListWidget {{border-radius: 10px; padding: 5px;}}
    QListWidget::item {{padding: 5px; border-radius: 7px;}}
    QListView {{border: 1px solid {self.borderColor}}}
    QTableView {{border: 3px solid {self.borderColor}}}
    """))
        self.student_info.setStyleSheet(f"border-radius: 7px solid {self.borderColor}")
        with open('settings.json','r',encoding='utf-8') as f:
            data = json.load(f)

        data['back'] = self.backgroundColor
        data['fore'] = self.foregroundColor
        data['border'] = self.borderColor
        with open('settings.json','w',encoding='utf-8') as f:
            json.dump(data,f)
    
    def darkTheme(self):
        self.backgroundColor = '#202020'
        self.foregroundColor = '#FFFFFF'
        self.borderColor = '#404040'

        self.setStyleSheet(f'background-color : {self.backgroundColor}; color : {self.foregroundColor}')

        self.studentList.setStyleSheet(f"""
    QListWidget {{border-radius: 10px; padding: 5px;}}
    QListWidget::item {{padding: 5px; border-radius: 7px;}}
    QListView {{border: 1px solid {self.borderColor}}}
    QTableView {{border: 1px solid {self.borderColor}}}
    """)
        self.student_info.setStyleSheet((f"""
    QListWidget {{border-radius: 10px; padding: 5px;}}
    QListWidget::item {{padding: 5px; border-radius: 7px;}}
    QListView {{border: 1px solid {self.borderColor}}}
    QTableView {{border: 1px solid {self.borderColor}}}
    """))
        self.student_info.setStyleSheet(f"border-radius: 7px solid {self.borderColor}")
        with open('settings.json','r',encoding='utf-8') as f:
            data = json.load(f)

        data['back'] = self.backgroundColor
        data['fore'] = self.foregroundColor
        data['border'] = self.borderColor
        with open('settings.json','w',encoding='utf-8') as f:
            json.dump(data,f)
    
    def selfTheme(self,color):
        self.backgroundColor ,self.foregroundColor,self.borderColor = color[0],color[1],color[2]
        self.setStyleSheet(f'background-color : {self.backgroundColor}; color : {self.foregroundColor}')
        self.studentList.setStyleSheet(f"""
    QListWidget {{border-radius: 10px; padding: 5px;}}
    QListWidget::item {{padding: 5px; border-radius: 7px;}}
    QListView {{border: 1px solid {self.borderColor}}}
    QTableView {{border: 1px solid {self.borderColor}}}
    """)
        self.student_info.setStyleSheet((f"""
    QListWidget {{border-radius: 10px; padding: 5px;}}
    QListWidget::item {{padding: 5px; border-radius: 7px;}}
    QListView {{border: 1px solid {self.borderColor}}}
    QLabel {{border: 1px solid {self.borderColor}}}
    """))
        self.student_info.setStyleSheet(f"border-radius: 7px solid {self.borderColor}")
        with open('settings.json','r',encoding='utf-8') as f:
            data = json.load(f)

        data['back'] = self.backgroundColor
        data['fore'] = self.foregroundColor
        data['border'] = self.borderColor
        with open('settings.json','w',encoding='utf-8') as f:
            json.dump(data,f)


if status:
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = Main()
        window.show()
        sys.exit(app.exec_())