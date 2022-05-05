import os
from flask import jsonify, render_template, request, session
from flask_cors import cross_origin
from . import main
from server import db
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound
from ..models import User,StripeCustomer #THis will be used to load the user model
from ..decorators import subscription_required
import stripe


@main.route('/', methods=["GET","POST"])
def home():
    return render_template('Home/layout/main-layout.html')


@main.route('/dashboard', methods=["GET","POST"])
@cross_origin()
@login_required
@subscription_required #New subscription required decorator
def dashboard():
    try:

        stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
        
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()

        subscription = stripe.Subscription.retrieve(customer.StripeSubscriptionId)
        product = stripe.Product.retrieve(subscription.plan.product)

        context ={
            "subscription":subscription,
            "product":product,
        }
    except:
        return render_template('dashboard/index.html', segment='index')
        
    return render_template('dashboard/index.html', segment='index', **context)

    

@main.route('/profile', methods=['GET, POST'])
@login_required
def profile():
    return render_template('dashboard/page-user.html', segment='page-user')




@main.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            pass

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template('dashboard/' + template, segment=segment)

    except TemplateNotFound:
        return render_template('dashboard/page-404.html'), 404

    except:
        return render_template('dashboard/page-500.html'), 500



def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'home'

        return segment

    except:
        return None
