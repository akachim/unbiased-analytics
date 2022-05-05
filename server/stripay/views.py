import json
import os
from ..models import StripeCustomer
from flask_login import current_user, login_required
from . import stripay
import stripe
from flask import flash, jsonify, render_template, render_template_string, request, url_for, redirect
from flask_cors import cross_origin
from server import db

stripe_keys={
            "publishable_key":os.environ.get("STRIPE_PUBLISHABLE_KEY"),
            "secret_key":os.environ.get("STRIPE_SECRET_KEY"),
            "endpoint_secret": os.environ.get("STRIPE_ENDPOINT_SECRET"),
            }


@stripay.route('/subscription', methods=['GET','POST'])
@login_required
def subscription():
    customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
    if customer:
        next = request.args.get('next')
        if next is None or not next.startswith('/'):
            next = url_for('main.home')
            return redirect(next)
    return render_template('stripay/index.html')



'''@stripay.route('/', methods=["GET","POST"])
@login_required
def index():

    """
    #This route is to display the subscription of a particular stripe customer
    """

    stripe.api_key = stripe_keys["secret_key"]
    
    customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()

    if customer:
        subscription = stripe.Subscription.retrieve(customer.StripeSubscriptionId)
        product = stripe.Product.retrieve(subscription.plan.product)

        context ={
            "subscription":subscription,
            "product":product,
        }

        return render_template("stripay/stripay.html", **context)


    return render_template('stripay/stripay.html')'''



@stripay.route("/config")
def get_publishabel_key():
    stripe_config = {'publicKey':stripe_keys["publishable_key"]}

    return stripe_config


@stripay.route('/create-checkout-session', methods=["GET", "POST"])
@cross_origin()
def create_checkout_session():

    data = request.json

    domain_url ="http://127.0.0.1:5000/stripy/order/"
    
    stripe.api_key = stripe_keys["secret_key"]

    try:
        checkout_session = stripe.checkout.Session.create(
            #Get the user id here and pass it along as client_reference_id
            #This will allow you to associate the stripe session with  the user saved in the database
            #eg: Client_reference_id = user.id,
            client_reference_id = current_user.id,
            success_url = "https://127.0.0.1:5000/dashboard", #domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url = domain_url + "cancel",
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price":data["priceId"],
                    "quantity":1
                },
            ]
        )

        return {"sessionId": checkout_session["id"]}

    except Exception as e:
        error=str(e)

        return error, 403


@stripay.route('/webhook', methods=["POST"])
def stripe_webhook():

    payload = request.get_data(as_text=True)

    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )
    except ValueError as e:
        #Invalid payload
        return "Invalid payload", 400
    
    except stripe.error.SignatureVerificationError as e:

        #Invalid signature

        return "Invalid signature", 400

    #handling checkout.session.completed event

    if event['type'] == "checkout.session.completed":
        
        session = event["data"]["object"]

        handle_checkout_session(session)


        out_file = open("myfile.json", "w")
  
        json.dump(session, out_file, indent = 6)
  
        out_file.close()

        #Fulfill the purchase
        


    return "Success", 200


def handle_checkout_session(session):
    """
    This where information from the season is fetched and stored in
    the database. eg.(associate the user with their subscription)

    """
    
    #subscription_database = StripeCustomer.query.filter_by(StripeSubscriptionId=session["subscription"]).first()


    #if subscription_database:
        #pass

    new_checkout= StripeCustomer( user_id = session['client_reference_id'],
                    StripeCustomerId=session["customer"],
                  StripeSubscriptionId= session["subscription"])

    db.session.add(new_checkout)
    db.session.commit()

    message = "Subscription was successful"

    print(message)



@stripay.route('/order/success', methods=["GET"])
def success():

    sess = stripe.checkout.Session.retrieve(request.args.get('session_id'))

    customer = stripe.Customer.retrieve(sess.customer)

    return render_template_string('<html><body><h1>Thanks for your order, {{ customer.name }}!</h1></body></html>', customer=customer)




@stripay.route('/order/cancel', methods=["GET"])
def cancel():
    flash("Subscription cancelled")
    return redirect(url_for('main.home'))







@stripay.route('/change-subscription', methods=["POST"])
def change_subscription():
    stripe.api_key = stripe_keys["secret_key"]

    data = request.json
    
    customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()

    subscription = stripe.Subscription.retrieve(customer.StripeSubscriptionId)

    modified_subscription = stripe.Subscription.modify(
        subscription.id,
        cancel_at_period_end=False,
        proration_behavior='create_prorations',
        items=[{
            'id':subscription['items']['data'][0].id,
            'price': data["priceId"]
        }]
    )


    message = 'Plan upgrade successfully'

    return message 
