// Initialize Stripe and Elements
var stripe = Stripe("pk_test_51NjhguKVBom7gkba2kZk2XmoJbwLk1QkOCtHT6PxSrPRFkM9155fCq9npFL2m970cbuoXGao2NWCdBui2RdXX2Sz00lu0yxXsQ");
var elements = stripe.elements();

// Create an instance of the card Element
var card = elements.create('card');

// Add an instance of the card Element into the `card-element` div
card.mount('#card-element');

// Listen to change events on the card Element and display any errors
card.addEventListener('change', function (event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent = event.error.message;
    } else {
        displayError.textContent = '';
    }
});

// Create Stripe token when form is submitted
var form = document.getElementById('payment-form');
form.addEventListener('submit', function (event) {
    event.preventDefault();

    stripe.createToken(card).then(function (result) {
        if (result.error) {
            var errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error.message;
        } else {
            // Send Stripe token to your server
            var form = document.getElementById('payment-form');
            var hiddenInput = document.createElement('input');
            hiddenInput.setAttribute('type', 'hidden');
            hiddenInput.setAttribute('name', 'stripeToken');
            hiddenInput.setAttribute('value', result.token.id);
            form.appendChild(hiddenInput);

            // Submit the form
            form.submit();
        }
    });
});