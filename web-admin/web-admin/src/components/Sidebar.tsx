import { Link } from "react-router-dom";
import { useAuthStore } from "../store/auth";
import { api } from "../lib/api";
import { useQuery } from "@tanstack/react-query";
import { Folder } from "lucide-react";

export default function Sidebar({ bucketName }: { bucketName?: string }) {
  const { user } = useAuthStore();
  const { data: buckets, isLoading } = useQuery({
    queryKey: ["buckets"],
    queryFn: () => api.getBuckets(),
  });

  return (
    <div className="w-64 bg-gray-800 text-white flex flex-col">
      <div className="p-4 font-semibold text-xl border-b border-gray-700">
        Kamu OSS
      </div>
      <nav className="flex-1 p-2 space-y-1">
        <h3 className="px-2 text-xs font-semibold text-gray-400 uppercase">
          Buckets
        </h3>
        {isLoading && (
          <div className="px-3 py-2 text-sm text-gray-400">Yükleniyor...</div>
        )}
        {!isLoading && buckets && buckets.length > 0 && buckets.map((bucket) => (
          <Link
            key={bucket.name}
            to={`/bucket/${bucket.name}`}
            className={`block px-3 py-2 rounded-md text-sm font-medium ${
              bucketName === bucket.name
                ? "bg-gray-900"
                : "hover:bg-gray-700"
            }`}
          >
            <Folder className="w-4 h-4 inline-block mr-2" />
            {bucket.name}
          </Link>
        ))}
        {!isLoading && (!buckets || buckets.length === 0) && (
          <div className="px-3 py-2 text-sm text-gray-400">Bucket bulunamadı</div>
        )}
      </nav>
      <div className="p-4 border-t border-gray-700">
        <div className="text-sm">{user?.email || "Kullanıcı"}</div>
        <div className="text-xs text-gray-400">{user?.role || "Rol"}</div>
      </div>
    </div>
  );
}
