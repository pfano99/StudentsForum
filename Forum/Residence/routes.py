from flask import Flask, Blueprint, abort,url_for, render_template, redirect, session
from Forum.models import Residence
from Forum.Residence.forms import ResidenceForm
from Forum import db, bcrypt
from flask_login import current_user, login_required


residence = Blueprint('Residence', __name__)

@residence.route('/residence')
@residence.route('/residence/')
def showResidence():
    res = Residence.query.all()

    return render_template('Residence/residence_show.html',accomodation=res, title='Accomodation')


@residence.route('/residence/<int:id>', methods=['POST', 'GET'])
@residence.route('/residence/<int:id>/', methods=['POST', 'GET'])
def residenceInfo(id):
    res = Residence.query.get_or_404(id)
    return render_template('Residence/residence_info.html',accomodation=res, title='Accomodation details')


@residence.route('/residence/add', methods=['POST', 'GET'])
@residence.route('/residence/add/', methods=['POST', 'GET'])
def addResidence():
    form = ResidenceForm()
    if form.validate_on_submit():
        res = Residence(
            name = form.name.data,
            description = form.description.data,
            location = form.location.data,
            room_type = form.room_type.data,
            price = form.price.data,
            rules = form.rules.data,
            entertainment = form.entertainment.data,
            safety_and_sec = form.safety_and_sec.data,
            company_id = current_user.id
        )
        db.session.add(res)
        db.session.commit()
        return redirect(url_for('Organization.organization_profile', id=current_user.id))
    return render_template('Residence/residence_add.html',form=form, title='Add Accomodation')
