from flask import Blueprint
from flask import render_template, redirect, url_for, abort
from Forum.Posts.forms import PostForm, CommentForm
from Forum.Utility.utils import SaveDocuments
from Forum.models import Post, Comment
from Forum import db
from flask_login import current_user, login_required

posts = Blueprint('posts', __name__)

@posts.route('/post/<int:post_id>', methods = ['POST', 'GET'])
@login_required
def post(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id = post_id)
    if form.validate_on_submit():
        comm = Comment(content = form.content.data, user_id = current_user.id, post_id = post_id)
        db.session.add(comm)
        db.session.commit()
        return redirect(url_for('posts.post', post_id = post_id))
    return render_template('Post/post.html', post = post, comments = comments, form = form)


@posts.route('/post/create_post/', methods = ['POST', 'GET'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        pic = None
        if form.image.data:
            photo = SaveDocuments() 
            pic = photo.save_post_picture(form.image.data)

        post = Post(title = form.title.data,
                    content = form.content.data,
                    picture = pic,
                    user_id = current_user.id )

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('Post/create_post.html', title = 'Create new post', form = form)


@posts.route('/post/update/<int:post_id>', methods = ['POST', 'GET'])
@login_required
def update_post(post_id):
    form = PostForm()

    post = Post.query.get(post_id)

    form.title.data = post.title
    form.content.data = post.content

    if form.validate_on_submit():
        current_user.title = form.title.data
        current_user.content = form.content.data
        db.session.add()
        return redirect(url_for('main.home'))
    return render_template('Post/update_post.html', form = form, post = post)


@posts.route('/post/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort
    else:
        db.session.delete(post)
    return redirect(url_for('main.home'))



# @posts.route('/post/comment/<int:post_id>', methods = ['POST', 'GET'])
# @login_required
# def post_comment(post_id):
#     form = CommentForm()

#     if form.validate_on_submit():
#         comment = Comment(content=form.content.data, user_id = current_user.id, post_id = post_id)
#         db.session.add(comment)
#         db.session.commit()
#         return redirect(url_for('posts.post', post_id = post_id))
#     return render_template('post_comment.html', form = form, title='Comment')
