import { Folder, Upload } from "lucide-react";

export function QuickAccess() {
  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h3 className="font-semibold mb-2">Hızlı Erişim</h3>
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
