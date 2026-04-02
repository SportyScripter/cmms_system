import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(''); // Do wyświetlania błędów
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(''); // Czyścimy stary błąd przed nową próbą

    try {
      // Uderzamy do naszego Django przez Proxy!
      const response = await axios.post('/api/token/', {
        username: username,
        password: password
      });

      // Zapisujemy tokeny do pamięci przeglądarki (Local Storage)
      localStorage.setItem('access', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);

      // Przenosimy użytkownika do panelu
      navigate('/dashboard');

    } catch (err) {
      // Jeśli Django zwróci błąd 401 (złe hasło), ustawiamy komunikat
      setError('Nieprawidłowy login lub hasło.');
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 space-y-6">
        
        <div className="text-center">
          <h2 className="text-3xl font-extrabold text-slate-900">System CMMS</h2>
          <p className="mt-2 text-sm text-slate-500">Zaloguj się do swojego konta</p>
        </div>

        {/* Jeśli jest błąd, pokaż czerwoną ramkę */}
        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm text-center border border-red-200">
            {error}
          </div>
        )}

        <form className="space-y-4" onSubmit={handleLogin}>
          <div>
            <label className="block text-sm font-medium text-slate-700">Nazwa użytkownika</label>
            <input 
              type="text" 
              required 
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="mt-1 block w-full px-4 py-3 border border-slate-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500"
              placeholder="Wpisz swój login"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700">Hasło</label>
            <input 
              type="password" 
              required 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 block w-full px-4 py-3 border border-slate-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500"
              placeholder="••••••••"
            />
          </div>

          <button 
            type="submit" 
            className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none transition-colors"
          >
            Zaloguj się
          </button>
        </form>

      </div>
    </div>
  );
}