import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api'; // Importujemy naszego nowego, uzbrojonego axiosa!

export default function DashboardPage() {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);

  // useEffect uruchomi się automatycznie zaraz po załadowaniu tego ekranu
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        // Zauważ, że nie musimy podawać '/api/users/', bo bazę '/api' ustawiliśmy w api.js
        // Nie musimy też ręcznie dodawać tokena - interceptor zrobi to za nas!
        const response = await api.get('/users/');
        setUsers(response.data);
      } catch (err) {
        console.error("Błąd pobierania danych:", err);
        setError("Brak uprawnień lub sesja wygasła.");
        // Jeśli token wygasł lub jest zły, wylogowujemy profilaktycznie
        handleLogout(); 
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
        
        {/* Górny panel */}
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

        {/* Sekcja z pobranymi danymi */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">Użytkownicy w systemie (Zaciągnięci z bazy)</h2>
          
          {error ? (
            <p className="text-red-500">{error}</p>
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