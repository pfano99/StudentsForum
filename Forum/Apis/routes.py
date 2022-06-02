from flask import Blueprint, render_template, redirect, abort, jsonify
from Forum.models import User, Post, Comment, Product, ProductComment

api = Blueprint('api', __name__)


@api.route('/api/user/<int:user_id>')
def get_user(user_id):
    user = User.query.get(user_id)

    if user:
        post_count = Post.query.filter_by(author=user).count()
        user_information = { "id":user.id, 
            "First Name":user.first_name,
            "Last Name":user.last_name,
            "Email":user.email,
            "Join date":user.joindate,
            "School":user.school,
            "Course":user.course,
            "Location": user.location,
            "About me": user.about_me,
            "Total Post Count": post_count  }

        return jsonify(user_information)
    else:
        abort(404)

@api.route('/api/user/posts/<int:user_id>')
def get_user_posts(user_id):
    user = User.query.get(user_id)

    if user:
        user_posts = Post.query.filter_by(author=user).all()
        #comment_count = Post.query.filter_by(post=user).count()

        #posts = { 'comment count':  comment_count }
        posts = {}
        for post in user_posts:
            posts[post.post_id] = { 'author': post.author.first_name,
                                    'title': post.title,
                                    'content': post.content,
                                    'date_created': post.date_created }
        return jsonify(posts)
    else:
        abort(404)


@api.route('/api/post/<int:post_id>')
def get_post(post_id):
    posts = Post.query.get(post_id)

    if posts:
        post = { 'title': posts.title,
                'content': posts.content,
                'date_created': posts.date_created }

        return jsonify(post)
    else:
        abort(404)



@api.route('/api/post/comments/<int:post_id>')
def get_post_comments(post_id):
    post = Post.query.get(post_id)

    if post:
        post_comments = Comment.query.filter_by(post = post).all()
        if post_comments:
            comments = {}
            for comment in post_comments:
            
                comments[Comment.comment_id] = {  
                    'author': comment.user_id.first_name,
                    'content': comment.content,
                    'date_created': comment.date_created,
                    'post id': comment.post_id}

            return jsonify(comments)
        return jsonify({"Comment":"Post have no commets"})
                
    else:
        abort(404)


        

@api.route('/api/market/product/<int:id>')
def get_product(id):
    products = Product.query.get(id)
    if products:
        image = False
        if products.image:
            image = True
        product = {
            'Product id':products.id,
            'Product Name':products.product_name,
            'Condition':products.condition,
            'Description':products.description,
            'Price':products.price,
            'Date Created':products.date_created,
            'Category':products.category,
            'Seller':products.seller.first_name,
            'Image': image

        }
        return jsonify(product)
    else:
        abort(404)



