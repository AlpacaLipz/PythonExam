from flask import Flask, render_template, request, redirect
app = Flask(__name__)
app.secret_key = 'not a password'

DATABASE = "exam_db"