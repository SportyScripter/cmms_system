import axios from 'axios';

// Tworzymy własną, skonfigurowaną wersję axiosa
const api = axios.create({
  // Dzięki naszemu proxy w Vite, to poleci prosto do Django na port 8000
  baseURL: '/api', 
});

// "Przechwytujemy" każde zapytanie tuż przed jego wylotem z przeglądarki
api.interceptors.request.use(
  (config) => {
    // Wyciągamy token z sejfu przeglądarki
    const token = localStorage.getItem('access');
    
    // Jeśli mamy token, doczepiamy go do nagłówka zapytania jako nasz "Dowód Osobisty"
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;