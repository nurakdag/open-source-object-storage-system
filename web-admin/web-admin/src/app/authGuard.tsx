import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "../store/auth";
import { useEffect, useState } from "react";

export default function AuthGuard() {
  const [isHydrated, setIsHydrated] = useState(false);
  const token = useAuthStore((s) => s.token);

  useEffect(() => {
    // Zustand store'un hydrate olmasını bekle
    setIsHydrated(true);
  }, []);

  // Hydration tamamlanana kadar loading göster
  if (!isHydrated) {
    return (
      <div className="min-h-dvh grid place-items-center">
        <div className="text-lg">Yükleniyor...</div>
      </div>
    );
  }

  return token ? <Outlet /> : <Navigate to="/login" replace />;
}
