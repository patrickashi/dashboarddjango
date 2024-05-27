import React from 'react';
import PaymentForm from './components/PaymentForm';
import CsrfTokenDisplay from './components/CsrfTokenDisplay';


function App() {
  return (
    <div className="App">
      <h1>School App Payment</h1>
      {/* <PaymentForm /> */}
      <CsrfTokenDisplay />
    </div>
  );
}

export default App;
