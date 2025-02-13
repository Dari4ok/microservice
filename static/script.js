document.addEventListener("DOMContentLoaded", function () {
    const cardNumberInput = document.getElementById("card_number");
    const expiryInput = document.getElementById("expiry");
    const paymentForm = document.getElementById("payment-form");

    // Function to format card number with spaces
    function formatCardNumber(input) {
        return input.replace(/\D/g, '') // Remove all non-digit characters
                    .substring(0, 16) // Limit to 16 digits
                    .replace(/(\d{4})/g, '$1 ') // Add space every 4 digits
                    .trim(); // Remove trailing space if any
    }

    // Card number input formatting
    cardNumberInput.addEventListener("input", function (e) {
        let value = e.target.value.replace(/\s/g, ''); // Remove spaces before processing
        e.target.value = formatCardNumber(value);
    });

    // Format expiration date (MM/YY)
    expiryInput.addEventListener("input", function (e) {
        let value = e.target.value.replace(/\D/g, '').slice(0, 4);
        if (value.length >= 2) {
            value = value.slice(0, 2) + "/" + value.slice(2);
        }
        e.target.value = value;
    });

    // Validate form before submission
    paymentForm.addEventListener("submit", function (e) {
        const cardNumber = cardNumberInput.value.replace(/\s/g, ""); // Remove spaces for validation
        const expiry = expiryInput.value;
        const cvv = document.getElementById("cvv").value;

        if (cardNumber.length !== 16 || !/^\d+$/.test(cardNumber)) {
            alert("Invalid card number. Please enter exactly 16 digits.");
            e.preventDefault();
        }

        if (!/^\d{2}\/\d{2}$/.test(expiry)) {
            alert("Invalid expiration date. Format should be MM/YY.");
            e.preventDefault();
        }

        if (!/^\d{3}$/.test(cvv)) {
            alert("Invalid CVV. Please enter a 3-digit code.");
            e.preventDefault();
        }
    });
});


function printReceipt() {
    window.print();
}


function goBack() {
    window.history.back();
}