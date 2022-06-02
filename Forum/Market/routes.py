from flask import Blueprint, redirect, render_template, url_for
from Forum.models import Product, User, ProductComment, Product
from flask_login import current_user, login_required
from Forum.Market.forms import ProductForm
from Forum.Posts.forms import CommentForm
from Forum import db
from Forum.Utility.utils import SaveDocuments

market = Blueprint('market', __name__)

@market.route('/market')
@login_required
def market_place():
    product = Product.query.order_by(Product.date_created.desc()).all()
    return render_template('Market/market.html', title = 'Market', products = product)


@market.route('/sell', methods = ['POST', 'GET'])
@login_required
def sell():
    form = ProductForm()
    if form.validate_on_submit():
        pic = None
        if form.image.data:
            photo = SaveDocuments()
            pic = photo.save_product_picture(form.image.data)

        fname = form.name.data
        fcondition = form.condition.data
        fcategory = form.category.data
        fprice = form.price.data
        fdescription = form.description.data

        product = Product(product_name = fname, condition = fcondition, 
                        category = fcategory, price = fprice, description = fdescription,
                        seller_id = current_user.id, image = pic)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('market.market_place'))
    return render_template('Market/sell.html', form = form, title = 'Sell')



@market.route('/market/product/<int:product_id>', methods = ['POST', 'GET'])
@login_required
def product(product_id):
    
    form = CommentForm()
    prodct = Product.query.get_or_404(product_id)
    comment = ProductComment.query.filter_by(product_id = product_id)
    
    if form.validate_on_submit():
        prod = ProductComment(content = form.content.data, user_id = current_user.id, product_id = prodct.id)
        db.session.add(prod)
        db.session.commit()
        return redirect(url_for('market.product', product_id = product_id))
        
    return render_template('Market/product.html', form = form, product=prodct, comments = comment)







