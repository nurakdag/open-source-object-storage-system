import { Folder } from "lucide-react";
import { Link } from "react-router-dom";
import type { Bucket } from "@/lib/types";

type Props = { buckets?: Bucket[] };

export function BucketGrid({ buckets }: Props) {
  const isLoading = buckets === undefined;
  const error = false;

  if (isLoading) {
    return (
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="font-semibold mb-2">Bucket'lar</h3>
        <div>Yükleniyor...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="font-semibold mb-2">Bucket'lar</h3>
        <div className="text-red-600">Bucket'lar yüklenirken hata oluştu</div>
      </div>
    );
  }

  if (!buckets || buckets.length === 0) {
    return (
      <div className="bg-white p-4 rounded-2xl shadow-soft">
        <h3 className="font-semibold mb-2">Bucket'lar</h3>
        <div className="text-gray-500">Henüz bucket bulunmuyor</div>
      </div>
    );
  }

  return (
    <div className="bg-white p-4 rounded-2xl shadow-soft">
      <h3 className="font-semibold mb-2">Bucket'lar</h3>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {buckets.map((bucket) => (
          <Link
            to={`/bucket/${bucket.name}`}
            key={bucket.name}
            className="flex flex-col items-center p-4 rounded-lg bg-gray-50 hover:bg-gray-100"
          >
            <Folder className="w-12 h-12 text-blue-500" />
            <span className="mt-2 text-sm font-medium">{bucket.name}</span>
          </Link>
        ))}
      </div>
    </div>
  );
}
