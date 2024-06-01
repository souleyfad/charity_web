from flask import render_template, Blueprint, request, redirect, url_for, flash, jsonify
#from charity.data import projets
from charity import web_charity_bp
from charity.models.projet import Projet
from charity.models.don import Don
import requests
from extensions import db

@web_charity_bp.route("/")
def index():
    projets = Projet.query.all()
    return render_template('index.html', projets = projets)

@web_charity_bp.route("/projet/<int:projet_id>")
def show(projet_id):
    projet = Projet.query.get_or_404(projet_id)
    total_dons = calculer_total_dons(projet_id)
    return render_template('show.html', projet=projet, total_dons=total_dons)

def calculer_total_dons(projet_id):
    projet = Projet.query.get_or_404(projet_id)
    dons = projet.dons
    total_dons = 0
    for don in dons:
        total_dons += don.montant

    return total_dons


@web_charity_bp.route("/don", methods=['POST'])
def don():
    try:
        identifiant = request.form['identifiant']
        montant = request.form['montant']
        telephone = request.form['telephone']
        modePayement = request.form['modePayement']
        projet_id = request.form['projet_id']

        don = Don(identifiant=identifiant,
                montant=montant,
                telephone=telephone,
                modePayement=modePayement,
                projet_id=projet_id)
        
        paygate_url ="https://paygateglobal.com/api/v1/pay"
        response = requests.post(paygate_url,
                                json={
                                    'auth_token': '5b2a5ed8-7764-4f51-a0fc-f3f49980d54e',
                                    'phone_number': telephone,
                                    'amount': montant,
                                    'identifiant': identifiant,
                                    'network': modePayement
                                })
        response_data = response.json()
        print('reponse', response_data)

        db.session.add(don)
        db.session.commit()

        total_dons = calculer_total_dons(projet_id)
        #flash('Merci pour votre don.', 'success')
        #return redirect(url_for('charity_web.show', projet_id=projet_id))

        return jsonify({'success': True, 'total_dons': total_dons})
    except Exception as e:
        print(e)
        #flash('Votre don a échoué .', 'error')
        #return redirect(url_for('charity_web.show', projet_id=projet_id))
        return jsonify({'success': False})

