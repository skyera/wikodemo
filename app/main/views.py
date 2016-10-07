import os,json,re
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, AddWordForm, SubPostForm
from .. import db
#from app import wikidictionary
from ..models import Permission, Role, User, Post, EntityStream,SearchKey, SubPost
from ..decorators import admin_required
from config import basedir
from datetime import datetime
from utils import id_generator, utcnow, remove_punct, LOG


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/post/<stream>', methods=['GET', 'POST'])
@login_required
def add_post(stream):
    post = Post()   #.query.get_or_404()
    form = PostForm()
    if form.validate_on_submit():
       post.title = form.title.data
       post.body = form.body.data
       post.body_html = form.link.data
       post.stream_id = stream
       post.timestamp = datetime.utcnow()
       post.author_id = current_user.username
       db.session.add(post)
       flash('The post has been updated.')
       return redirect(url_for('.go_entity', name=stream))    
    form.body.data = post.body
    return render_template('edit_post.html', form=form, caption=stream)

@main.route('/gosubpost/<int:id>', methods=['GET', 'POST'])
def go_subpost(id):
    post = Post.query.get_or_404(id)
    subposts = SubPost.query.filter_by(post_id=id).all()
    return render_template('subpost.html', post=post, subposts=subposts)
            
@main.route('/addsubpost/<int:id>', methods=['GET', 'POST'])
@login_required
def add_subpost(id):
    post = Post.query.get_or_404(id)
    nupost = SubPost()
    nupost.body = request.form['comment']
    nupost.post_id = id
    nupost.timestamp = datetime.utcnow()
    nupost.author_id = current_user.username
    db.session.add(nupost)
    flash('The post has been updated.')
    subposts = SubPost.query.filter_by(post_id=id).all()
    return redirect(url_for('.go_subpost', id=id)) 

def prefix_suggestion(word):
    temp = remove_punct(word).lower()
    temp =  re.split(' ',temp)[0:4]
    suggestion = [ ' '.join(temp[0:i]) for i in range(1,min(4,1+len(temp))) ]
    return suggestion
            
@main.route('/addword',methods=['GET', 'POST'])
@login_required
def add_word():
    form = AddWordForm()
    if form.validate_on_submit():
         entity = EntityStream.query.filter_by(caption=form.name.data).first()
         if entity == None: 
             entity=EntityStream()
             entity.eid = form.name.data + '-' + id_generator()
             entity.creator = current_user.username
             entity.creation_time = utcnow()
             entity.caption = form.name.data
             entity.alias = form.alias.data
             entity.description = form.description.data
             for s in  prefix_suggestion(entity.caption):
                 searchkey = SearchKey.query.filter_by(word=s).first()
                 if searchkey == None: 
                     searchkey = SearchKey(s)
                 else:
                     print "found searchkey", searchkey.word, searchkey.id 
                 entity.suggestion.append(searchkey)
         db.session.add(entity)
         db.session.commit()
         flash('The new word has been created.')
#         else:
#             LOG("add_word(): entity found in db")
         return  redirect(url_for('.go_entity', name=entity.eid))
                 
    return render_template('add_word.html', form=form)            
            

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,
                           pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    form.title.data = post.title
    return render_template('edit_post.html', form=form)
            
            
@main.route('/go_entity/<name>')
def go_entity(name):
    stream = EntityStream.query.filter_by(eid=name).first_or_404()
    if stream!=None:
        page = request.args.get('page', 1, type=int)
        pagination = stream.posts.order_by(Post.timestamp.desc()).paginate(
                page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                error_out=False)
        posts = pagination.items
        return render_template('open_entity_bs.html', caption=stream.caption, description=stream.description, eid=stream.eid, posts=posts,
                   pagination=pagination)



@main.route('/search', methods=['POST'])
def search_entity():
    entity = request.form['entityname']
    #from unicode to str
    skey =  SearchKey.query.filter_by(word=str(entity.strip())).all()                     
    if len(skey)==0:
        return abort(404)
    else:
        streams = []
        for item in skey:
            streams += item.streams.all()
        return render_template('select_entity.html', entries=streams)

                    
                    
                    
                    
                    
                    
                    
                    