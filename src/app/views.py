from app import app, db, lm, oid
from forms import LoginForm, SavedGraphForm, DeleteGraph, EditForm
from models import User, ROLE_USER, ROLE_ADMIN, SavedGraph
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from email import send_email
from cw_api import cw_search_keywords, cw_search_text


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    return render_template('index.html', user=user)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/jobs')
def jobs():
    return render_template('jobs.html')


@app.route('/donations')
def donations():
    return render_template('donations.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html', title='Sign In', form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = current_user


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email, role=ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
        send_email(resp.email, 'Welcome to Poligraphed', 'mail/new_user')
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    elif request.method != "POST":
        form.nickname.data = g.user.nickname
    return render_template('edit.html', form=form)


@app.route('/_search_api')
def _search_api():

    keywords = [request.args.get('keyword_1', '', type=str),
                request.args.get('keyword_2', '', type=str)
                ]

    date_low = request.args.get('date_low', '', type=str)
    date_high = request.args.get('date_high', '', type=str)
    granularity = request.args.get('granularity', '', type=str)

    api_results = cw_search_keywords(keywords, date_low, date_high, granularity)

    return jsonify(keywords=api_results)

@app.route('/_search_cr_api')
def _search_cr_api():

    keywords = [request.args.get('keyword_1', '', type=str),
                request.args.get('keyword_2', '', type=str)
                ]

    date_low = request.args.get('date_low', '', type=str)
    date_high = request.args.get('date_high', '', type=str)
    granularity = request.args.get('granularity', '', type=str)

    api_results = cw_search_text(keywords, date_low, date_high, granularity)

    return jsonify(keywords=api_results)


@app.route('/graph', methods=['GET', 'POST'])
@login_required
def test():
    user = g.user
    saved_graphs = None
    deleted_graph_id = None
    deleted_graph = None
    saved_graph_form = SavedGraphForm(prefix="saved_graph_form")
    saved_graphs = SavedGraph.query.filter_by(user_id=user.id).all()
    delete_graph_form = DeleteGraph(prefix="delete_graph_form")

    if saved_graph_form.validate_on_submit() and saved_graph_form.submit.data:
        save_graph = SavedGraph(graph_name=saved_graph_form.graph_name.data,
                                keyword_1=saved_graph_form.keyword_1.data,
                                keyword_2=saved_graph_form.keyword_2.data,
                                date_low=saved_graph_form.date_low.data,
                                date_high=saved_graph_form.date_high.data,
                                granularity=saved_graph_form.granularity.data,
                                user_id=user.id
                                )
        db.session.add(save_graph)
        db.session.commit()
        return redirect(url_for('test'))

    if delete_graph_form.validate_on_submit() and delete_graph_form.submit.data:
        deleted_graph_id = delete_graph_form.graph_id.data
        deleted_graph = db.session.query(SavedGraph).filter_by(id=deleted_graph_id).first()
        db.session.delete(deleted_graph)
        db.session.commit()
        return redirect(url_for('test'))

    return render_template('testajax.html',
                           saved_graphs=saved_graphs,
                           user=user,
                           saved_graph_form=saved_graph_form,
                           delete_graph_form=delete_graph_form)
