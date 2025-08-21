import { create } from "zustand";
import type { StorageObject } from "../lib/types";

export type UIState = {
  sidebarOpen: boolean;
  selectedObject: StorageObject | null;
  selectedBucket: string | null;
  toggleSidebar: () => void;
  setSelectedObject: (object: StorageObject | null) => void;
  setSelectedBucket: (bucket: string | null) => void;
};

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  selectedObject: null,
  selectedBucket: null,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setSelectedObject: (object) => set({ selectedObject: object }),
  setSelectedBucket: (bucket) => set({ selectedBucket: bucket }),
}));
