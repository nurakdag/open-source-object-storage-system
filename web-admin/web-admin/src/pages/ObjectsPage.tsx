import { PreviewPane } from "../components/PreviewPane";
import UploadNewFile from "../components/UploadNewFile";
import { api } from "../lib/api";
import { useUIStore } from "../store/ui";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { Icons } from "../components/Icons";
import { useState } from "react";
import type { StorageObject } from "../lib/types";
import type { UIState } from "../store/ui";

export default function ObjectsPage() {
  const { FileText, Folder, Search } = Icons;
  const { name: bucketName } = useParams();
  const [prefix, setPrefix] = useState("");
  const setSelectedObject = useUIStore((s: UIState) => s.setSelectedObject);

  const { data: objects, isLoading, error } = useQuery({
    queryKey: ["objects", bucketName, prefix],
    queryFn: () => api.getObjects(bucketName!, prefix),
    enabled: !!bucketName,
  });

  if (!bucketName) return <div>Bucket bulunamadı.</div>;

  return (
    <div className="flex h-full">
      <div className="flex-1 flex flex-col">
        <div className="p-4 border-b flex justify-between items-center">
          <h2 className="text-xl font-semibold">{bucketName}</h2>
          <UploadNewFile bucketName={bucketName} />
        </div>
        <div className="p-4 border-b">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Prefix'e göre filtrele..."
              className="pl-10 w-full"
              value={prefix}
              onChange={(e) => setPrefix(e.target.value)}
            />
          </div>
        </div>
        <div className="flex-1 overflow-y-auto">
          {isLoading && <div className="p-4">Yükleniyor...</div>}
          {error && <div className="p-4 text-red-600">Nesneler yüklenirken hata oluştu</div>}
          {!isLoading && !error && objects && objects.length > 0 && (
            <ul>
              {objects.map((obj: StorageObject) => (
                <li
                  key={obj.key}
                  onClick={() => setSelectedObject(obj)}
                  className="flex items-center p-3 hover:bg-gray-100 cursor-pointer border-b"
                >
                  {obj.isDir ? (
                    <Folder className="w-6 h-6 mr-3 text-blue-500" />
                  ) : (
                    <FileText className="w-6 h-6 mr-3 text-gray-600" />
                  )}
                  <span>{obj.key.replace(prefix, "")}</span>
                </li>
              ))}
            </ul>
          )}
          {!isLoading && !error && (!objects || objects.length === 0) && (
            <div className="p-4 text-gray-500">Bu bucket'ta nesne bulunamadı</div>
          )}
        </div>
      </div>
      <PreviewPane />
    </div>
  );
}
