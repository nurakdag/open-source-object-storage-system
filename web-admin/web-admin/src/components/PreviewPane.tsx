import { useUIStore } from "../store/ui";
import { X, FileText, Download } from "lucide-react";
import { api } from "../lib/api";
import { useMutation } from "@tanstack/react-query";

function formatBytes(bytes: number, decimals = 2) {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
}

export function PreviewPane() {
  const { selectedObject, setSelectedObject, selectedBucket } = useUIStore();

  const downloadMutation = useMutation({
    mutationFn: async () => {
      if (!selectedObject) return;
      const res = await api.getPresignDownloadUrl({ bucket: selectedBucket || "default", key: selectedObject.key });
      window.open(res.url, "_blank");
    },
  });

  if (!selectedObject) {
    return (
      <div className="w-80 border-l bg-gray-50 flex items-center justify-center">
        <p className="text-gray-500">Önizlemek için bir nesne seçin.</p>
      </div>
    );
  }

  return (
    <div className="w-80 border-l bg-gray-50 flex flex-col">
      <div className="p-4 border-b flex justify-between items-center">
        <h3 className="font-semibold">Detaylar</h3>
        <button onClick={() => setSelectedObject(null)}>
          <X className="w-5 h-5" />
        </button>
      </div>
      <div className="flex-1 p-4 flex flex-col items-center text-center">
        <FileText className="w-24 h-24 text-gray-400 mb-4" />
        <p className="font-semibold break-all">{selectedObject.key}</p>
        <p className="text-sm text-gray-500">
          {formatBytes(selectedObject.size)}
        </p>
        <p className="text-xs text-gray-400 mt-1">
          Son Değişiklik: {new Date(selectedObject.last_modified).toLocaleString()}
        </p>
      </div>
      <div className="p-4 border-t">
        <button
          onClick={() => downloadMutation.mutate()}
          disabled={downloadMutation.isPending}
          className="w-full bg-blue-600 text-white py-2 rounded-md flex items-center justify-center space-x-2 hover:bg-blue-700"
        >
          <Download className="w-5 h-5" />
          <span>İndir</span>
        </button>
      </div>
    </div>
  );
}
