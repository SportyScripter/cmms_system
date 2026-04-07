import {
  Activity,
  AlertTriangle,
  ArrowRight,
  Calendar,
  Package,
  Settings,
} from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";

export default function DashboardPage() {
  const [stats, setStats] = useState({
    totalMachines: 0,
    brokenMachines: 0,
    lowStockParts: 0,
    overdueSchedules: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [machinesRes, partsRes, schedulesRes] = await Promise.all([
        api.get("/machines/"),
        api.get("/parts/"),
        api.get("/schedules/"),
      ]);

      const machines = machinesRes.data;
      const parts = partsRes.data;
      const schedules = schedulesRes.data;

      const today = new Date();
      today.setHours(0, 0, 0, 0);

      setStats({
        totalMachines: machines.length,
        brokenMachines: machines.filter((m) => m.status === "BR").length,
        lowStockParts: parts.filter((p) => p.quantity <= p.min_quantity).length,
        overdueSchedules: schedules.filter((s) => {
          const dueDate = new Date(s.due_date);
          return !s.is_completed && dueDate < today;
        }).length,
      });

      setLoading(false);
    } catch (err) {
      console.error("Błąd pobierania danych dashboardu:", err);
      setError(
        "Nie udało się pobrać statystyk. Sprawdź połączenie z serwerem.",
      );
      setLoading(false);
    }
  };

  if (loading)
    return (
      <div className="text-slate-500 font-medium p-8">
        Ładowanie Centrum Dowodzenia...
      </div>
    );

  return (
    <div className="space-y-8">
      <div className="bg-gradient-to-r from-slate-900 to-slate-800 rounded-2xl p-8 text-white shadow-lg">
        <h1 className="text-3xl font-extrabold mb-2">Witaj w CMMS.pro</h1>
        <p className="text-slate-300 max-w-2xl">
          To jest Twoje centrum dowodzenia. Poniżej znajdziesz kluczowe
          wskaźniki wydajności (KPI) oraz ostrzeżenia wymagające Twojej
          natychmiastowej uwagi.
        </p>
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-200 flex items-center gap-3">
          <AlertTriangle size={24} />
          <span className="font-medium">{error}</span>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col">
          <div className="flex justify-between items-start mb-4">
            <div className="p-3 bg-red-50 text-red-600 rounded-lg">
              <Activity size={24} />
            </div>
            <span className="text-3xl font-black text-slate-800">
              {stats.brokenMachines}
            </span>
          </div>
          <h3 className="text-slate-500 font-medium mb-1">Zgłoszone awarie</h3>
          <p className="text-sm text-slate-400 mb-4">
            Maszyny wyłączone z ruchu
          </p>
          <Link
            to="/machines"
            className="mt-auto text-sm font-bold text-red-600 hover:text-red-700 flex items-center gap-1"
          >
            Przejdź do maszyn <ArrowRight size={16} />
          </Link>
        </div>

        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col">
          <div className="flex justify-between items-start mb-4">
            <div className="p-3 bg-amber-50 text-amber-600 rounded-lg">
              <Calendar size={24} />
            </div>
            <span className="text-3xl font-black text-slate-800">
              {stats.overdueSchedules}
            </span>
          </div>
          <h3 className="text-slate-500 font-medium mb-1">Zaległe przeglądy</h3>
          <p className="text-sm text-slate-400 mb-4">
            Wymagają natychmiastowej akcji
          </p>
          <Link
            to="/calendar"
            className="mt-auto text-sm font-bold text-amber-600 hover:text-amber-700 flex items-center gap-1"
          >
            Sprawdź kalendarz <ArrowRight size={16} />
          </Link>
        </div>

        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col">
          <div className="flex justify-between items-start mb-4">
            <div className="p-3 bg-blue-50 text-blue-600 rounded-lg">
              <Package size={24} />
            </div>
            <span className="text-3xl font-black text-slate-800">
              {stats.lowStockParts}
            </span>
          </div>
          <h3 className="text-slate-500 font-medium mb-1">Braki magazynowe</h3>
          <p className="text-sm text-slate-400 mb-4">Części poniżej minimum</p>
          <Link
            to="/warehouse"
            className="mt-auto text-sm font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1"
          >
            Zamów części <ArrowRight size={16} />
          </Link>
        </div>

        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col">
          <div className="flex justify-between items-start mb-4">
            <div className="p-3 bg-slate-50 text-slate-600 rounded-lg">
              <Settings size={24} />
            </div>
            <span className="text-3xl font-black text-slate-800">
              {stats.totalMachines}
            </span>
          </div>
          <h3 className="text-slate-500 font-medium mb-1">Park maszynowy</h3>
          <p className="text-sm text-slate-400 mb-4">
            Wszystkie maszyny w systemie
          </p>
          <Link
            to="/machines"
            className="mt-auto text-sm font-bold text-slate-600 hover:text-slate-700 flex items-center gap-1"
          >
            Zarządzaj parkiem <ArrowRight size={16} />
          </Link>
        </div>
      </div>
    </div>
  );
}
