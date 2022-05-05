var createCheckoutSession = function(priceId) {
    return fetch("/stripy/create-checkout-session",{
        method: "POST",
        headers:{
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            priceId : priceId
        })
    }).then((result) => {
        return result.json()
    });
};



const PREMIUM_PRICE_ID = "price_1KepM1HSCh2fFcDYEN6KDSXV";

const BASIC_PRICE_ID = "price_1KddHBHSCh2fFcDYGd3kg9WU";

fetch("/stripy/config")
.then((result) => { return result.json(); })
.then((data) => {
  const stripe = Stripe(data.publicKey);

    

    document.getElementById("checkout-basic").addEventListener("click", () => {

        createCheckoutSession(BASIC_PRICE_ID).then((data) => {
            stripe.redirectToCheckout({ sessionId: data.sessionId })
        });

    });

    document.getElementById("checkout-premium").addEventListener("click", () => {

        createCheckoutSession(PREMIUM_PRICE_ID).then((data) => {
            stripe.redirectToCheckout({ sessionId: data.sessionId })
        });

    });

    
})



