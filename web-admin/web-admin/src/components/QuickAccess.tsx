import { Folder, Upload } from "lucide-react";
import type { StorageObject } from "@/lib/types";

type Props = { items?: StorageObject[] };

export function QuickAccess({ items }: Props) {
  return (
    <div className="bg-white p-4 rounded-2xl shadow-soft">
      <h3 className="font-semibold mb-1">Hızlı Erişim</h3>
      <div className="text-xs text-slate-500 mb-2">
        Son dosyalar: {items?.length ?? 0}
      </div>
      <div className="flex space-x-4">
        <button className="flex items-center space-x-2 p-2 rounded-md bg-gray-100 hover:bg-gray-200">
          <Folder className="w-5 h-5 text-blue-600" />
          <span>Yeni Klasör</span>
        </button>
        <button className="flex items-center space-x-2 p-2 rounded-md bg-gray-100 hover:bg-gray-200">
          <Upload className="w-5 h-5 text-green-600" />
          <span>Dosya Yükle</span>
        </button>
      </div>
    </div>
  );
}
