from flask import Blueprint, jsonify
from charity.data import projets
from charity import api_charity_bp
from charity.controllers.CategorieController import CategorieController
from charity.controllers.ProjetController import ProjetController

categorie_controller = CategorieController()
projet_controller = ProjetController()

@api_charity_bp.route("")
def api_list():
    return jsonify(projets)

@api_charity_bp.route("/categories", methods=['POST'])
def add_category():
    return categorie_controller.create()

@api_charity_bp.route("/categories", methods=['GET'])
def list_categories():
    return categorie_controller.all()

@api_charity_bp.route("/projets", methods=['POST'])
def add_projet():
    return projet_controller.create()

@api_charity_bp.route("/projets", methods=['GET'])
def list_projet():
    return projet_controller.all()