import type { StorageObject } from "@/lib/types";

type Props = { items?: StorageObject[] };

export function StorageDonut({ items = [] }: Props) {
  const totalBytes = items.reduce((sum, o) => sum + (o.size || 0), 0);
  const capacity = 2 * 1024 * 1024 * 1024 * 1024; // 2 TB (örnek)
  const usedPercent = Math.min(100, Math.round((totalBytes / capacity) * 100));
  return (
    <div className="bg-white p-4 rounded-2xl shadow-soft">
      <h3 className="font-semibold mb-2">Depolama Kullanımı</h3>
      <div className="flex items-center justify-center">
        <div className="relative w-32 h-32">
          <svg className="w-full h-full" viewBox="0 0 36 36">
            <path
              d="M18 2.0845
                a 15.9155 15.9155 0 0 1 0 31.831
                a 15.9155 15.9155 0 0 1 0 -31.831"
              fill="none"
              stroke="#eee"
              strokeWidth="3"
            />
            <path
              d="M18 2.0845
                a 15.9155 15.9155 0 0 1 0 31.831"
              fill="none"
              stroke="#4f46e5"
              strokeWidth="3"
              strokeDasharray="60, 100"
            />
          </svg>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center">
            <span className="text-xl font-bold">{usedPercent}%</span>
            <span className="text-xs text-gray-500 block">Dolu</span>
          </div>
        </div>
      </div>
      <div className="text-center mt-2 text-sm text-gray-600">
        {(totalBytes / (1024*1024*1024)).toFixed(1)} GB / 2048 GB kullanılıyor
      </div>
    </div>
  );
}
