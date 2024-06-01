from charity.models.categorie import Categorie
from flask import jsonify, request
from extensions import db

class CategorieController:

    def __init__(self):
        self.categorie_model = Categorie

    def create(self):
        try:
            data = request.get_json()
            nouvelle_categorie = self.categorie_model(libelle=data['libelle'])
            db.session.add(nouvelle_categorie)
            db.session.commit()
            return jsonify({'message': 'Nouvelle catégorie créée avec succès'}), 201
        except KeyError:
            return jsonify({'message': 'Données manquantes'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': e}), 500
        
    def all(self):
        try:
            categories = self.categorie_model.query.all()
            result = [{'id': categorie.id, 'libelle': categorie.libelle} for categorie in categories]
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'message': e}), 500