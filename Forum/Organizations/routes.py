from flask import  Blueprint, session, url_for, render_template, redirect, abort
from Forum.Organizations.forms import OrgRegistrationForm, OrgLoginForm
from Forum.models import Organization, Job, Bursary, Residence
from Forum import db, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from Forum.Utility.utils import format_email, SaveDocuments, page_permission

organization = Blueprint('Organization', __name__)


@organization.route('/organization')
def organization_home():
    return render_template('Organization/organization_home.html', title='Companies')



#                        Registration Section                       #

@organization.route('/organization/register', methods = ['POST', 'GET'])
def organization_registeration():
    form = OrgRegistrationForm()
    if form.validate_on_submit():
        image = 'default'
        if form.image.data:
            photo = SaveDocuments()
            image = photo.save_organization_picture(form.image.data)
        name = form.name.data
        email = format_email(form.email.data)
        telephone  = form.telephone.data
        website = form.website.data
        location = form.location.data
        password = bcrypt.generate_password_hash(form.password.data)
        organization_info = Organization(name=name, email=email, telephone=telephone, website=website, location=location, password=password, image=image)
        
        db.session.add(organization_info)
        db.session.commit()
        return redirect(url_for('Organization.organization_login'))
    return render_template('Organization/organization_register.html', form = form, title='Organization Registration')



#                               LOGIN                                   #


@organization.route('/organization/login', methods=['POST', 'GET'])
def organization_login():

    if 'account_type' in session:
        if  session['account_type'] == 'Normal':
            return abort(401)


    form = OrgLoginForm()
    if form.validate_on_submit():
        session['account_type'] = 'Organization'
        user = Organization.query.filter_by(email = format_email(form.email.data)).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return  redirect(url_for('Organization.organization_profile', id=user.id))
    return render_template('Organization/organization_login.html',form=form, title='Login Organization')


#                           LOGOUT 

@organization.route('/organization/logout')
@login_required
def organization_logout():
    logout_user()
    session.pop('account_type', None)
    return redirect(url_for('main.index'))


#                           Organization Profile                        # 

@organization.route('/organization/profile/<int:id>', methods=['POST', 'GET'])
@login_required
def organization_profile(id):
    user = Organization.query.get_or_404(id)
    bursaries = Bursary.query.filter_by(company_id = id)
    residences = Residence.query.filter_by(company_id = id)
    jobs = Job.query.filter_by(company_id = id)

    return render_template('Organization/organization_profile.html', title='Organization Profile', 
                        user=user, bursaries = bursaries, jobs = jobs, residences=residences)



@organization.route('/organization/account/<int:id>', methods=['POST', 'GET'])
@login_required
@page_permission
def organization_account(id):
    user = Organization.query.get_or_404(id)
    return render_template('Organization/organization_account.html', title='Organization Account', user=user)




