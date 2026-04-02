import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

export default function DashboardPage() {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await api.get('/users/');
        setUsers(response.data);
      } catch (err) {
        console.error("Błąd pobierania danych:", err);
        setError("Brak uprawnień lub sesja wygasła.");
      }
    };

    fetchUsers();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <div className="max-w-4xl mx-auto space-y-6">
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-slate-800">Panel Główny CMMS</h1>
            <p className="text-slate-600">Pomyślnie zautoryzowano token JWT.</p>
          </div>
          <button 
            onClick={handleLogout}
            className="px-4 py-2 bg-red-50 text-red-600 font-medium rounded-lg hover:bg-red-100 transition"
          >
            Wyloguj się
          </button>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">Użytkownicy w systemie (Zaciągnięci z bazy)</h2>
          
          {error ? (
            <p className="text-red-500 font-medium">{error}</p>
          ) : (
            <ul className="divide-y divide-slate-100">
              {users.map((user) => (
                <li key={user.id} className="py-3 flex justify-between">
                  <span className="font-medium text-slate-700">{user.username}</span>
                  <span className="text-sm px-2 py-1 bg-blue-50 text-blue-700 rounded">Rola: {user.role}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}