from flask import flash, jsonify, render_template, redirect, request, url_for
from flask_cors import cross_origin
from flask_login import login_required, login_user, logout_user, current_user


from . import auth
from ..models import User
from server import db
from ..tasks import send_async_email
from .forms import LoginForm, SignUpForm





@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.home'))
    return render_template('auth/unconfirmed.html')



@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user=User.query.filter_by(email=email).first()
        if user is not None and user.verify_password(password):
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.home')
            return redirect(next)
    return render_template ("auth/login.html", form=form)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))



@auth.route('/signup', methods=["GET", "POST"])
def signup():

    form = SignUpForm()                                                                             

    if form.validate_on_submit():

        email = form.email.data
        username= form.username.data
        password = form.password.data

        #check username exist

        user=User.query.filter_by(username=username).first()
        
        if user:
                return render_template('auth/signup.html',
                                    msg='Username already registered',
                                    success=False,
                                    form=form)

            # Check email exists
        user = User.query.filter_by(email=email).first()

        if user:
            return render_template('auth/signup.html',
                                msg='Email already registered',
                                   success=False,
                                   form=form)

        new_user = User(email=email,
                    username=username,
                    password=password)

        db.session.add(new_user)
        db.session.commit()

        token = new_user.generate_confirmation_token()

        
        email_data={
            "to": email,
            "subject": 'Confirm Your Account',
            "template": 'auth/email/confirm',
            "username": username,
            "token":token
        }

        send_async_email.apply_async(args=[email_data], countdown=5)

        flash('A confirmation email has been sent to you by email.')

        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.home'))

    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')

    else:
        flash('The confirmation link is invalid or has expired.')

    return redirect(url_for('main.home'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()

    email = current_user.email
    username = current_user.username

    email_data={
            "to":email,
            "subject": 'Confirm Your Account',
            "template": 'auth/email/confirm',
            "username": username,
            "token":token
        }
    send_async_email(email_data)#.apply_async(args=[email_data], countdown=5)

    flash('A new confirmation email has been sent to you!.')

    return redirect(url_for('main.home'))
