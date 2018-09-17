from flask import render_template,request,redirect,url_for, abort
from .forms import UpdateProfile, PostForm
from . import main
from ..models import Post, User
from flask_login import login_required
from .. import db ,photos
from flask_login import login_required, current_user
import markdown2  


@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data.
    '''

    form = PostForm()
    if form.validate_on_submit():
       post = form.post.data
       title = form.category.data

       new_post = Post(body = post,title = title,user = current_user)

       # save pitch
       db.session.add(new_post)
       db.session.commit()

       return redirect(url_for('.index'))
    return render_template('index.html',form=form)

    
@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)    

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        # path = f'images/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))    

@main.route('/movie/review/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_post(id):
    form = ReviewForm()
    post = get_post(id)
    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data

        # Updated review instance
        new_post = Post(post_id=post.id,post_title=title,post_review=review,user=current_user)

        # save review method
        new_post.save_review()
        return redirect(url_for('.posts',id = post.id ))