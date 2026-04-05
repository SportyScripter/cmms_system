import { AlertCircle, Minus, Package, Plus, RefreshCw } from "lucide-react";
import { useEffect, useState } from "react";
import api from "../api";

export default function WarehousePage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [updatingId, setUpdatingId] = useState(null);

  useEffect(() => {
    fetchInventory();
  }, []);

  const fetchInventory = async () => {
    try {
      const response = await api.get("/parts/");
      setItems(response.data);
      setLoading(false);
    } catch (err) {
      setError("Nie udało się pobrać stanu magazynu.");
      setLoading(false);
    }
  };

  const handleStockChange = async (id, currentQuantity, actionType) => {
    const isAdding = actionType === "add";
    const promptMessage = isAdding
      ? "Ile sztuk chcesz PRZYJĄĆ na magazyn?"
      : "Ile sztuk chcesz WYDAĆ z magazynu?";

    const amountStr = window.prompt(promptMessage, "1");

    if (!amountStr) return;

    const amount = parseInt(amountStr, 10);

    if (isNaN(amount) || amount <= 0) {
      alert("Błąd: Podaj prawidłową liczbę całkowitą większą od zera.");
      return;
    }

    const newQuantity = isAdding
      ? currentQuantity + amount
      : currentQuantity - amount;

    if (newQuantity < 0) {
      alert(
        "Błąd: Nie możesz wydać więcej sztuk, niż jest fizycznie w magazynie!",
      );
      return;
    }

    setUpdatingId(id);

    try {
      await api.patch(`/parts/${id}/`, { quantity: newQuantity });

      setItems(
        items.map((item) =>
          item.id === id ? { ...item, quantity: newQuantity } : item,
        ),
      );
    } catch (err) {
      console.error("Błąd aktualizacji stanu:", err);
      alert("Wystąpił błąd podczas połączenia z serwerem.");
    } finally {
      setUpdatingId(null);
    }
  };

  if (loading)
    return (
      <div className="text-slate-500 font-medium p-4">
        Ładowanie magazynu...
      </div>
    );
  if (error) return <div className="text-red-500 font-medium p-4">{error}</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">Magazyn Części</h1>
          <p className="text-slate-500 mt-2">
            Zarządzaj stanem części zamiennych i materiałów eksploatacyjnych.
          </p>
        </div>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-lg font-medium transition-colors shadow-sm flex items-center gap-2">
          <Plus size={20} />
          Dodaj część
        </button>
      </div>

      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden mt-6">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 text-sm uppercase tracking-wider">
                <th className="p-4 font-medium">Nazwa części</th>
                <th className="p-4 font-medium">Typ</th>
                <th className="p-4 font-medium">Numer katalogowy</th>
                <th className="p-4 font-medium">Lokalizacja</th>
                <th className="p-4 font-medium">Ilość</th>
                <th className="p-4 font-medium text-right">Akcje</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {items.map((item) => {
                const isUpdating = updatingId === item.id;

                return (
                  <tr
                    key={item.id}
                    className={`transition-colors ${isUpdating ? "bg-blue-50/50" : "hover:bg-slate-50"}`}
                  >
                    <td className="p-4 flex items-center gap-3">
                      <div className="p-2 bg-blue-50 text-blue-600 rounded-lg">
                        {isUpdating ? (
                          <RefreshCw size={20} className="animate-spin" />
                        ) : (
                          <Package size={20} />
                        )}
                      </div>
                      <span className="font-semibold text-slate-800">
                        {item.name}
                      </span>
                    </td>
                    <td className="p-4 text-slate-600 font-mono text-sm">
                      {item.type_model || "Brak danych"}
                    </td>
                    <td className="p-4 text-slate-600 font-mono text-sm">
                      {item.supplier_catalog_number || "Brak danych"}
                    </td>
                    <td className="p-4 text-slate-600 font-mono text-sm">
                      {item.location || "Brak danych"}
                    </td>
                    <td className="p-4">
                      {item.quantity <= item.min_quantity ? (
                        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-sm font-medium bg-red-50 text-red-700 border border-red-200">
                          <AlertCircle size={16} />
                          {item.quantity} szt. (Niski stan!)
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-sm font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                          {item.quantity} szt.
                        </span>
                      )}
                    </td>
                    <td className="p-4 text-right space-x-2">
                      <button
                        onClick={() =>
                          handleStockChange(item.id, item.quantity, "subtract")
                        }
                        disabled={isUpdating}
                        className="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors disabled:opacity-50"
                        title="Wydaj z magazynu"
                      >
                        <Minus size={18} />
                      </button>
                      <button
                        onClick={() =>
                          handleStockChange(item.id, item.quantity, "add")
                        }
                        disabled={isUpdating}
                        className="p-2 text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 rounded transition-colors disabled:opacity-50"
                        title="Przyjmij na magazyn"
                      >
                        <Plus size={18} />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>

          {items.length === 0 && (
            <div className="p-12 text-center text-slate-500 flex flex-col items-center">
              <Package size={48} className="text-slate-300 mb-4" />
              <p>Twój magazyn jest pusty.</p>
              <p className="text-sm">
                Dodaj części przez panel admina Django, aby je tutaj zobaczyć.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
