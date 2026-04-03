import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute"; // Importujemy naszego Strażnika
import MachinesPage from "./pages/MachinesPage";
import WarehousePage from "./pages/WarehousePage";
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/machines" element={<MachinesPage />} />
          <Route path="/warehouse" element={<WarehousePage />} />
          <Route path="/calendar" element={<div>Tu będzie kalendarz</div>} />
          <Route path="/messages" element={<div>Tu będą wiadomości</div>} />
        </Route>
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
