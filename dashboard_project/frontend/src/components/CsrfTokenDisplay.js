import React, { useEffect, useState } from 'react';
import axios from 'axios';

const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

const CsrfTokenDisplay = () => {
  const [csrfToken, setCsrfToken] = useState('');

  useEffect(() => {
    const token = getCookie('csrftoken');
    setCsrfToken(token);
    axios.defaults.headers.common['X-CSRFToken'] = token;
  }, []);

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/initiate-payment/', { data: 'your data' });
      console.log(response.data);
    } catch (error) {
      console.error('Error submitting data:', error);
    }
  };

  return (
    <div>
      <p>CSRF Token: {csrfToken}</p>
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};

export default CsrfTokenDisplay;
