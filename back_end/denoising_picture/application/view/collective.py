from flask import Blueprint, request, jsonify, session, send_file
from application import db
from .. import model
import os

bp = Blueprint('collective', __name__, url_prefix='/user/<int:id>/collective')

