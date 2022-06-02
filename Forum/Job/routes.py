from flask import Flask, Blueprint, abort,url_for, render_template, redirect, session
from Forum.models import Job
from Forum.Job.forms import JobForm
from Forum import db, bcrypt
from flask_login import current_user, login_required
from Forum.Utility.utils import page_permission 

job = Blueprint('Job', __name__)


@job.route('/jobs/add/', methods = ['POST', 'GET'])
@job.route('/jobs/add', methods = ['POST', 'GET'])
@login_required
@page_permission
def addJob():

    form = JobForm()
    if form.validate_on_submit():
        _job = Job(
            job_title = form.job_title.data,
            open_date = form.open_date.data,
            closing_date = form.closing_date.data,
            job_type = form.job_type.data,
            required_skills = form.requirements.data,
            job_description = form.job_description.data,
            sector = " ",
            duration = "  ", 
            job_link = form.job_link.data,
            city = form.city.data,
            province = form.province.data,
            company_id = current_user.id
        )

        db.session.add(_job)
        db.session.commit()
        return redirect(url_for('Organization.organization_profile', id=current_user.id))
    return render_template('Job/job_add.html', title = 'Post Job', form=form)


@job.route('/jobs', methods = ['POST', 'GET'])
@job.route('/jobs/', methods = ['POST', 'GET'])
@login_required
def show_Jobs():
    jobs = Job.query.all()

    return render_template('Job/jobs_show.html', title='Available Jobs', jobs = jobs)


@job.route('/job/<int:id>', methods = ['POST', 'GET'])
@job.route('/job/<int:id>/', methods = ['POST', 'GET'])
@login_required
def job_info(id):
    jobs = Job.query.get_or_404(id)

    return render_template('Job/job_info.html', title='Job Info', jobs = jobs)


