from Forum import db, loginmanager
from datetime import datetime
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask import abort, session

@loginmanager.user_loader
def load_user(user_id):
    if session['account_type'] == 'Normal':
        return User.query.get(user_id)
    elif session['account_type'] == 'Organization':
        return Organization.query.get(user_id)


class Follow(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    date = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)



class User(db.Model, UserMixin):
    __searchable__ = ['first_name', 'last_name', 'email', 'location', 'school']
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100), nullable = False)
    last_name = db.Column(db.String(100), nullable = True)
    email = db.Column(db.String(120), nullable = False, unique = True)
    about_me = db.Column(db.Text, nullable = True)
    joindate = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    school = db.Column(db.String(60), nullable = True)
    course = db.Column(db.String(60), nullable = True)
    password = db.Column(db.String(60), nullable = False)
    profile_picture = db.Column(db.String(60), nullable = False, default = 'default.jpeg')
    location = db.Column(db.String(60), nullable = True)
    is_admin = db.Column(db.Boolean, nullable = False, default=False)
    gender = db.Column(db.String(6), nullable = False) 

    post = db.relationship('Post', backref='author', lazy=True)
    comment = db.relationship('Comment', backref = 'author', lazy=True)

    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                            backref = db.backref('follower', lazy = 'joined'), lazy='dynamic', cascade = 'all, delete-orphan')
                        
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id],
                            backref = db.backref('followed', lazy = 'joined'), lazy='dynamic', cascade = 'all, delete-orphan')
                        


    product = db.relationship('Product', backref='seller', lazy = True)
    product_comment = db.relationship('ProductComment', backref='author', lazy = True)


    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower = self, followed = user)
            db.session.add(f)

    def unfollow(self, user):
        if self.is_following(user):
            f = self.followed.filter_by(followed_id=user.id).first()
            if f:
                db.session.delete(f)


    #this will return True if the given user is being followed by the current logged in user
    def is_following(self, user):
        return self.followed.filter_by(followed_id = user.id).first() is not None

    def followed_user_posts(self):
        #this will return the post of all the users being followed by the current logged in users
        #Combing current user's post with the people they're following posts
        #This will allow users to be able to see their own posts in the timeline
        return Post.query.join(Follow, Follow.followed_id == Post.user_id).filter(Follow.follower_id == self.id)

    def get_followed_friends(self,):
        pass

    def __repr__(self,):
        return "Name: {}, email:{}".format(self.first_name, self.email)


class Post(db.Model):
    __searchable__ = ['title', 'content']
    post_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), nullable = False)
    content = db.Column(db.Text, nullable = True)
    picture = db.Column(db.String(60), nullable = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    comment = db.relationship('Comment', backref="post", lazy = True)

    def __repr__(self,):
        return "{}: {}".format(self.title, self.content)


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable = False)

    def __repr__(self,):
        return "comment id: {}, content: {}".format(self.comment_id, self.content)


class Product(db.Model):
    __searchable__ = ['product_name', 'description']
    id = db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String(100), nullable = False)
    condition = db.Column(db.String(10), nullable = False)
    description = db.Column(db.Text, nullable = False)
    price = db.Column(db.Integer, nullable = False)
    category = db.Column(db.String(20), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    image = db.Column(db.String(60), nullable = True) ######## String must be 120 characters
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self,):
        return "Name: {}, Category: {}".format(self.product_name, self.category)


class ProductComment(db.Model):
    comment_id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(100), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable = False)

    def __repr__(self,):
        return "comment id: {}, content: {}".format(self.comment_id, self.content)

class Organization(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(150), nullable = False, unique=True)
    telephone = db.Column(db.String(10), nullable = False)
    website = db.Column(db.String(250), nullable = False)
    location = db.Column(db.String(300), nullable = False)
    password = db.Column(db.String(60), nullable = False)
    date_joined = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    about = db.Column(db.Text, nullable = True)
    image = db.Column(db.String(60), nullable = True)

    offer_jobs = db.Column(db.Boolean, nullable = False, default=1)
    offer_bursary = db.Column(db.Boolean, nullable = False, default=1)
    offer_residence = db.Column(db.Boolean, nullable = False, default=1)

    bursaries = db.relationship('Bursary', backref='organization', lazy=True)
    jobs = db.relationship('Job', backref='organization', lazy=True)
    residence = db.relationship('Residence', backref='organization', lazy=True)
    

    def __repr__(self,):
        return "Name: {}, Category: {}, Telephone: {}".format(self.name, self.email, self.telephone)


    def total_jobs_count(self,):
        if self.offer_jobs != 0:
            return Job.query.filter_by(company_id = self.id).count()
        else:
            return None

    def total_bursaries_count(self,):
        if self.offer_bursary != 0:
            return Bursary.query.filter_by(company_id = self.id).count()
        else:
            return None

    def total_residences_count(self,):
        if self.offer_residence != 0:
            return Residence.query.filter_by(company_id = self.id).count()
        else:
            return None
            
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(60), nullable = False) 
    open_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    closing_date = db.Column(db.DateTime, nullable = False)
    
    date_posted = db.Column(db.DateTime, nullable = True, default = datetime.utcnow)
    job_type = db.Column(db.String(60), nullable = False) #apprenticeship, full-time-job, learnership
    required_skills = db.Column(db.Text, nullable = False)
    job_description = db.Column(db.Text, nullable = True)
    sector = db.Column(db.String(60), nullable = False) # information technology, busniness etc..
    duration = db.Column(db.String(60), nullable=True) #How long (Permanet, Months, Years) ##### must nullable = False

    job_link = db.Column(db.String(60), nullable=True)
    province = db.Column(db.String(60), nullable = False) # province
    city = db.Column(db.String(60), nullable=True)

    company_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable = False)

    def __repr__(self,):
        return "Job title: {}, job type: {}, province: {}, Sector: {}".format(self.job_title, self.job_type, self.province, self.sector)
    
class Bursary(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    bursary_name = db.Column(db.String(120), nullable = True)
    web_link = db.Column(db.String(250), nullable = False)    
    open_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    closing_date = db.Column(db.DateTime, nullable = False)
    # fields_of_study = db.Column(db.Text, nullable = True)
    requirement_to_apply = db.Column(db.Text, nullable = False)
    how_to_apply = db.Column(db.Text, nullable = False)
    document = db.Column(db.String(60), nullable = True)
    #contact information
    date_posted = db.Column(db.DateTime, nullable = True, default = datetime.utcnow)

    company_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable = False) 

    def __repr__(self,):
        return "Name: {}, Organization: {}".format(self.bursary_name, self.organization.name)
    
class Residence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable = False)
    description = db.Column(db.Text, nullable = True)
    location = db.Column(db.String(250), nullable = False)
    room_type = db.Column(db.String(60), nullable = False)
    price = db.Column(db.Integer, nullable=True)
    rules = db.Column(db.Text, nullable=True)
    entertainment = db.Column(db.Text, nullable = True)
    safety_and_sec = db.Column(db.Text, nullable=True)
    # contact information # emial, cellphone
    
    date_posted = db.Column(db.DateTime, nullable = True, default = datetime.utcnow)
    
    company_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable = False)


    # company link
    # reviews link
    # images link

    def __repr__(self,):
        return "{} found at: {}".format(self.name, self.location)

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(60), nullable=False)


########### WISH TABLE | CART 



#Authorization and Authentication for flask-admin
class AdminModelView(ModelView):
    def is_accessible(self):
        if 'account_type' in session and session['account_type'] == 'Normal':
            if current_user.is_authenticated and current_user.is_admin:
                return True
        return False
    
    def not_auth(self, name, **kwargs):
        abort(404)