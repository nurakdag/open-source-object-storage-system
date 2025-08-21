import { create } from "zustand";
import { persist } from 'zustand/middleware';
import type { User } from "../lib/types";

type AuthState = {
  token: string | null;
  user: User | null;
  setToken: (t: string | null) => void;
  setUser: (u: User | null) => void;
  clear: () => void;
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      setToken: (t) => set({ token: t }),
      setUser: (u) => set({ user: u }),
      clear: () => set({ token: null, user: null }),
    }),
    {
      name: 'auth-storage',
      // Hydration sırasında sorunları önlemek için
      onRehydrateStorage: () => (state) => {
        if (state) {
          // Token expired kontrolü
          if (state.token && state.user) {
            // Token'ın geçerliliğini kontrol et
            // Burada JWT decode yapılabilir
          }
        }
      },
    }
  )
);
