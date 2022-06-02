from flask import Blueprint, render_template, request, redirect, url_for
from Forum.Bursary.forms import BursaryForm
from flask_login import login_required, current_user
from Forum.models import Bursary
from Forum import db
from Forum.Utility.utils import SaveDocuments, page_permission

 
bursary = Blueprint('Bursary', __name__)


@bursary.route('/bursaries/add', methods = ['POST', 'GET'])
@login_required
@page_permission
def addBursary():
    form = BursaryForm()

    if form.validate_on_submit():
        doc = None
        if form.document.data:
            doc_obj = SaveDocuments()
            doc = doc_obj.save_bursary_document(form.document.data)


        _bursary = Bursary(
            bursary_name = form.bursary_name.data,
            web_link = form.web_link.data,
            open_date = form.opening_date.data,
            closing_date = form.closing_date.data,
            requirement_to_apply = form.requirements.data,
            how_to_apply = doc,
            document = form.document.data,
            company_id = current_user.id
        )
        db.session.add(_bursary)
        db.session.commit()
        return redirect(url_for('Organization.organization_profile', id = current_user.id))

    return render_template('Bursary/bursary_add.html',form = form, title = 'Add Bursary')


@bursary.route('/bursaries')
@bursary.route('/bursaries/')
@login_required
def showBursary():
    bursaries = Bursary.query.all()
    return render_template('Bursary/bursaries_show.html', title='Bursaries', bursaries = bursaries)

@bursary.route('/bursaries/<int:id>')
@bursary.route('/bursaries/<int:id>/')
@login_required
def infoBursary(id):
    return render_template('comming_soon.html')





