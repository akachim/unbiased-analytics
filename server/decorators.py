from functools import wraps
from flask import g, request, redirect, url_for
from flask_login import current_user
from .models import StripeCustomer


def subscription_required(f):
    """
    A decorated that checks whether a user is a customer
    Before allowing them to acesss the dashboard
    if not a customer, it redirects them to the subscription page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
        if customer is None:
            return redirect(url_for('stripay.subscription', next=request.url))
        return f(*args, **kwargs)
    return decorated_function