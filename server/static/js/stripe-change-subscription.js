//fectching the json published key using the fetch
document.getElementById("change-plan-link").addEventListener("click", () => {
    var priceId ='price_1KepM1HSCh2fFcDYEN6KDSXV';

    //get checkout session ID
    fetch('/stripy/change-subscription',
    {
        method: "POST",
        headers:{
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            
            priceId:priceId
        })
    })
    .then((result) => { return result.json(); })
    .then((data) =>{
        //console.log(data);
        // Redirect to stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
});