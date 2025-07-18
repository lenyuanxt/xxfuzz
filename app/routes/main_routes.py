# app/routes/main_routes.py
from flask import Blueprint, render_template, request, jsonify
import requests, os, json

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html', message="Welcome to IoT Web Fuzz Platform")

@bp.route('/template/manage')
def template_manage():
    return render_template('template_manage.html')

@bp.route('/fuzz')
def fuzz_view():
    return render_template('fuzz.html')