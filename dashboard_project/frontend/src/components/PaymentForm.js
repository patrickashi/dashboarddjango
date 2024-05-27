import React, { useState } from 'react';
// import Cookies from 'js-cookie';
// import { csrfToken } from '../components/utils/csrf';

const PaymentForm = () => {
    const [email, setEmail] = useState('');
    const [amount, setAmount] = useState('');
    const [txRef, setTxRef] = useState(`tx-${Date.now()}`);

    const getCsrfToken = () => {
        const csrfElement = document.querySelector('meta[name="csrf-token"]');
        return csrfElement ? csrfElement.getAttribute('content') : '';
    };

    // Helper function to get the CSRF token from the cookie
    // function getCookie(name) {
    //     let cookieValue = null;
    //     if (document.cookie && document.cookie !== '') {
    //         const cookies = document.cookie.split(';');
    //         for (let i = 0; i < cookies.length; i++) {
    //             const cookie = cookies[i].trim();
    //             if (cookie.substring(0, name.length + 1) === (name + '=')) {
    //                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
    //                 break;
    //             }
    //         }
    //     }
    //     return cookieValue;
    // }

    // const csrftoken = getCookie('csrftoken');
    const csrfToken = getCsrfToken();

    const handlePayment = async (e) => {
        e.preventDefault();
        
        try {
            // const csrfToken = Cookies.get('csrftoken'); // Fetch CSRF token from cookie
            const response = await fetch('http://127.0.0.1:8000/api/initiate-payment/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ email, amount, tx_ref: txRef }),
            });

            if (response.ok) {
                const data = await response.json();
                window.location.href = data.payment_url;  // Redirect to the payment page
            } else {
                console.error('Payment initiation failed.');
            }
        }  catch (error) {
            // Handle promise rejection (error)
            console.error('Payment initiation error:', error.message);
            // Display error message to user or handle appropriately
        }
    };

    return (
        <form onSubmit={handlePayment}>
            {/* <input type="hidden" name="csrfmiddlewaretoken" value={getCsrfToken()} /> */}
            <div>
                <label htmlFor="email">Email:</label>
                <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email"
                    required
                    autoComplete="email" // Set autocomplete attribute to "email"
                />
            </div>
            <div>
                <label htmlFor="amount">Amount:</label>
                <input
                    type="number"
                    id="amount"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="Amount"
                    required
                    autoComplete="off" // Set autocomplete attribute to "off" to disable autocomplete for this field
                />
            </div>
            <button type="submit">Pay</button>
        </form>
    );
};

export default PaymentForm;

