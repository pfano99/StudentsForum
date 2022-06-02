import os
import secrets
from flask import session, abort

from Forum import app
            
class SaveDocuments:
    def _save_in_directory(self, form_picture, sub_folder):
        random_name = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fullname = random_name + f_ext
        picture_path = os.path.join(app.root_path, 'static/{}'.format(sub_folder), picture_fullname)
        form_picture.save(picture_path)
        return picture_fullname

    def save_profile_picture(self, form_picture):
        picture_fullname = self._save_in_directory(form_picture, 'profile_pictures')
        return picture_fullname

    def save_post_picture(self, form_picture):
        picture_fullname = self._save_in_directory(form_picture, 'post_pictures')
        return picture_fullname


    def save_product_picture(self, form_picture):
        picture_fullname = self._save_in_directory(form_picture, 'product_pictures')
        return picture_fullname


    def save_organization_picture(self, form_picture):
        picture_fullname = self._save_in_directory(form_picture, 'organization_pictures')
        return picture_fullname

    def save_bursary_document(self, form_document):

        picture_fullname = self._save_in_directory(form_document, 'bursary_documents')
        return picture_fullname



def format_email(email):
    email = email.lower()
    email = email.lstrip()
    email = email.rstrip()
    return email


def page_permission(func):
    def wrapper(*args, **kwargs):
        if 'account_type' in session:
            if  session['account_type'] == 'Normal':
                return abort(401)
        else:
            f = func(*args, **kwargs)
            return f
    return wrapper
