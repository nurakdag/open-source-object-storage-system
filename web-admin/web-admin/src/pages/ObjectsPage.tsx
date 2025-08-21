import { PreviewPane } from "../components/PreviewPane";
import { api } from "../lib/api";
import { useUIStore } from "../store/ui";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import type { StorageObject } from "../lib/types";
import { useEffect } from "react";

function formatBytes(bytes: number, decimals = 2) {
  if (!bytes) return "0 Bytes";
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
}

export default function ObjectsPage() {
  const { name } = useParams();
  const setSelectedBucket = useUIStore((s) => s.setSelectedBucket);
  const setSelectedObject = useUIStore((s) => s.setSelectedObject);

  useEffect(() => {
    if (name) setSelectedBucket(name);
  }, [name, setSelectedBucket]);

  const q = useQuery({
    queryKey: ["objects", name],
    enabled: !!name,
    queryFn: () => api.getObjects(name!, ""),
  });

  return (
    <div className="flex h-full">
      <div className="flex-1 p-4">
        <div className="bg-white rounded-2xl shadow-soft p-4">
          <div className="font-medium mb-3">Bucket: {name}</div>
          <table className="w-full text-sm">
            <thead className="bg-slate-50">
              <tr>
                <th className="text-left p-3">Key</th>
                <th className="text-left p-3">Size</th>
                <th className="text-left p-3">Modified</th>
              </tr>
            </thead>
            <tbody>
              {(q.data || []).map((o: StorageObject) => (
                <tr
                  key={o.key}
                  className="border-t hover:bg-slate-50 cursor-pointer"
                  onClick={() => setSelectedObject(o)}
                >
                  <td className="p-3 break-all">{o.key}</td>
                  <td className="p-3">{formatBytes(o.size)}</td>
                  <td className="p-3">{o.last_modified?.slice(0, 19) || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {!q.data?.length && <div className="text-gray-500 p-3">Nesne bulunamadı</div>}
        </div>
      </div>
      <PreviewPane />
    </div>
  );
}
