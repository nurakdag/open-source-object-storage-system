import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "../store/auth";
import { useMutation } from "@tanstack/react-query";
import { api } from "../lib/api";
import type { LoginRequest } from "../lib/types";

export default function LoginPage() {
  const [email, setEmail] = useState("admin@demo.gov");
  const [password, setPassword] = useState("Admin!234");
  const navigate = useNavigate();
  const { setToken, setUser } = useAuthStore();

  const { mutate, isPending, error } = useMutation({
    mutationFn: (data: LoginRequest) => api.login(data),
    onSuccess: (data) => {
      setToken(data.access_token);
      setUser(data.user);
      navigate("/");
    },
    onError: (error: any) => {
      console.error("Login error:", error);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutate({ username: email, password });
  };

  // Error message'ı güvenli şekilde string'e dönüştür
  const getErrorMessage = (): string | null => {
    if (!error) return null;

    const detail = (error as any)?.response?.data?.detail;

    if (typeof detail === "string") {
      return detail;
    }

    if (Array.isArray(detail)) {
      // FastAPI/Pydantic v2 validation hataları: [{type, loc, msg, input}, ...]
      const msgs = detail
        .map((d: any) => (typeof d?.msg === "string" ? d.msg : JSON.stringify(d)))
        .filter(Boolean);
      if (msgs.length > 0) return msgs.join("\n");
    }

    if (detail && typeof detail === "object") {
      if (typeof detail.msg === "string") return detail.msg;
      try {
        return JSON.stringify(detail);
      } catch {
        /* ignore */
      }
    }

    const dataMessage = (error as any)?.response?.data?.message;
    if (typeof dataMessage === "string") return dataMessage;

    if (typeof (error as any)?.message === "string") return (error as any).message;

    return "Giriş başarısız";
  };

  const errorMessage = getErrorMessage();

  return (
    <div className="min-h-dvh grid place-items-center bg-slate-100">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-sm bg-white p-6 rounded-2xl shadow-soft space-y-3"
      >
        <h2 className="text-xl font-semibold">Oturum Aç</h2>
        <input
          className="w-full bg-slate-50 p-3 rounded-xl"
          placeholder="E-posta"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="w-full bg-slate-50 p-3 rounded-xl"
          placeholder="Şifre"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {errorMessage && (
          <div className="text-sm text-red-600 whitespace-pre-line">
            {errorMessage}
          </div>
        )}
        <button
          type="submit"
          disabled={isPending}
          className="w-full p-3 bg-blue-600 text-white rounded-xl disabled:bg-blue-400"
        >
          {isPending ? "Giriş yapılıyor..." : "Giriş Yap"}
        </button>
      </form>
    </div>
  );
}
