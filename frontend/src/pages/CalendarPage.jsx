import {
  AlertTriangle,
  Calendar,
  CheckCircle,
  Clock,
  Wrench,
} from "lucide-react";
import { useEffect, useState } from "react";
import api from "../api";

export default function CalendarPage() {
  const [schedules, setSchedules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSchedules();
  }, []);

  const fetchSchedules = async () => {
    try {
      const response = await api.get("/schedules/");
      setSchedules(response.data);
      setLoading(false);
    } catch (err) {
      setError("Nie udało się pobrać kalendarza przeglądów.");
      setLoading(false);
    }
  };

  const getScheduleStatus = (next_due_date, isCompleted) => {
    if (isCompleted) {
      return {
        label: "Wykonano",
        color: "text-emerald-600",
        bg: "bg-emerald-50",
        border: "border-emerald-200",
        icon: CheckCircle,
      };
    }

    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const due = new Date(next_due_date);

    if (due < today) {
      return {
        label: "Zaległy!",
        color: "text-red-600",
        bg: "bg-red-50",
        border: "border-red-200",
        icon: AlertTriangle,
      };
    }

    const diffTime = Math.abs(due - today);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays <= 7) {
      return {
        label: `Za ${diffDays} dni`,
        color: "text-amber-600",
        bg: "bg-amber-50",
        border: "border-amber-200",
        icon: Clock,
      };
    }

    return {
      label: "Zaplanowany",
      color: "text-blue-600",
      bg: "bg-blue-50",
      border: "border-blue-200",
      icon: Calendar,
    };
  };

  if (loading)
    return (
      <div className="text-slate-500 font-medium p-4">
        Ładowanie kalendarza...
      </div>
    );
  if (error) return <div className="text-red-500 font-medium p-4">{error}</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">
            Kalendarz Przeglądów (PM)
          </h1>
          <p className="text-slate-500 mt-2">
            Harmonogram prac konserwacyjnych i prewencyjnych.
          </p>
        </div>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-lg font-medium transition-colors shadow-sm flex items-center gap-2">
          <Calendar size={20} />
          Zaplanuj przegląd
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pt-4">
        {schedules.map((task) => {
          const status = getScheduleStatus(
            task.next_due_date,
            task.is_completed,
          );
          const StatusIcon = status.icon;

          return (
            <div
              key={task.id}
              className={`bg-white border-2 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow flex flex-col h-full ${status.border}`}
            >
              <div className="flex justify-between items-start mb-4">
                <div className={`p-3 rounded-lg ${status.bg} ${status.color}`}>
                  <StatusIcon size={24} />
                </div>
                <span
                  className={`text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full ${status.bg} ${status.color}`}
                >
                  {status.label}
                </span>
              </div>

              <div className="flex-1">
                <h2 className="text-lg font-bold text-slate-800 mb-1 flex items-center gap-2">
                  <Wrench size={18} className="text-slate-400" />
                  {task.machine_name || `Maszyna ID: ${task.machine}`}
                </h2>
                <h3 className="text-md font-semibold text-slate-600 mb-3">
                  {task.title || "Przegląd okresowy"}
                </h3>
                <p className="text-sm text-slate-500 line-clamp-3 mb-4">
                  {task.description || "Brak opisu dla tego zadania."}
                </p>
              </div>

              <div className="pt-4 border-t border-slate-100 flex items-center justify-between mt-auto">
                <div className="text-sm">
                  <span className="text-slate-400 block text-xs uppercase font-semibold">
                    Termin
                  </span>
                  <span className="font-medium text-slate-700">
                    {task.next_due_date || "Nie określono"}
                  </span>
                </div>

                {!task.is_completed && (
                  <button className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-sm font-medium rounded-lg transition-colors">
                    Wykonaj
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {schedules.length === 0 && (
        <div className="p-12 text-center text-slate-500 flex flex-col items-center bg-white border border-slate-200 rounded-xl">
          <Calendar size={48} className="text-slate-300 mb-4" />
          <p>Twój kalendarz świeci pustkami.</p>
          <p className="text-sm mt-1">
            Nie masz zaplanowanych żadnych przeglądów prewencyjnych.
          </p>
        </div>
      )}
    </div>
  );
}
