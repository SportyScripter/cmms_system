import { useEffect, useState } from "react";
import {
  Settings,
  AlertTriangle,
  CheckCircle,
  Activity,
  RefreshCw,
} from "lucide-react";
import api from "../api";

export default function MachinesPage() {
  const [machines, setMachines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [updatingId, setUpdatingId] = useState(null); 

  useEffect(() => {
    fetchMachines();
  }, []);

  const fetchMachines = async () => {
    try {
      const response = await api.get("/machines/");
      setMachines(response.data);
      setLoading(false);
    } catch (err) {
      setError("Nie udało się pobrać listy maszyn.");
      setLoading(false);
    }
  };

  const updateMachineStatus = async (machineId, newStatus) => {
    setUpdatingId(machineId); // Blokujemy interfejs dla tej maszyny
    try {
      await api.patch(`/machines/${machineId}/`, { status: newStatus });

      setMachines(
        machines.map((m) =>
          m.id === machineId ? { ...m, status: newStatus } : m,
        ),
      );
    } catch (err) {
      console.error("Błąd aktualizacji:", err);
      alert("Nie udało się zmienić statusu maszyny. Sprawdź konsolę.");
    } finally {
      setUpdatingId(null); 
    }
  };

  const getStatusStyles = (status) => {
    switch (status) {
      case "OP":
        return {
          color: "text-emerald-600",
          bg: "bg-emerald-50",
          icon: CheckCircle,
          label: "Sprawna",
        };
      case "MA":
        return {
          color: "text-amber-600",
          bg: "bg-amber-50",
          icon: Settings,
          label: "Przegląd",
        };
      case "BR":
        return {
          color: "text-red-600",
          bg: "bg-red-50",
          icon: AlertTriangle,
          label: "Awaria",
        };
      default:
        return {
          color: "text-slate-600",
          bg: "bg-slate-50",
          icon: Activity,
          label: "Nieznany",
        };
    }
  };

  if (loading)
    return (
      <div className="text-slate-500 font-medium p-4">Ładowanie maszyn...</div>
    );
  if (error) return <div className="text-red-500 font-medium p-4">{error}</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">
            Maszyny i Awarie
          </h1>
          <p className="text-slate-500 mt-2">
            Zarządzaj parkiem maszynowym i zgłaszaj usterki.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pt-4">
        {machines.map((machine) => {
          const statusStyle = getStatusStyles(machine.status);
          const StatusIcon = statusStyle.icon;
          const isUpdating = updatingId === machine.id;

          return (
            <div
              key={machine.id}
              className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start mb-4">
                <div
                  className={`p-3 rounded-lg ${statusStyle.bg} ${statusStyle.color}`}
                >
                  {isUpdating ? (
                    <RefreshCw size={28} className="animate-spin" />
                  ) : (
                    <StatusIcon size={28} />
                  )}
                </div>
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400 bg-slate-100 px-3 py-1 rounded-full">
                  Seryjny: {machine.serial_number}
                </span>
              </div>
              <h2 className="text-xl font-bold text-slate-800 mb-1">
                {machine.name}
              </h2>
              <div className="flex items-center justify-between mt-6 pt-4 border-t border-slate-100">
                <span className="text-sm font-medium text-slate-500">
                  Zmień status:
                </span>
                <select
                  value={machine.status}
                  onChange={(e) =>
                    updateMachineStatus(machine.id, e.target.value)
                  }
                  disabled={isUpdating}
                  className={`text-sm font-bold bg-slate-50 border border-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer disabled:opacity-50 ${statusStyle.color}`}
                >
                  <option value="OP">Sprawna</option>
                  <option value="MA">Przegląd</option>
                  <option value="BR">Awaria</option>
                </select>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
