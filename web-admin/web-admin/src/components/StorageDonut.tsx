export function StorageDonut() {
  return (
    <div className="bg-white p-4 rounded-lg shadow">
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
            <span className="text-xl font-bold">60%</span>
            <span className="text-xs text-gray-500 block">Dolu</span>
          </div>
        </div>
      </div>
      <div className="text-center mt-2 text-sm text-gray-600">
        1.2 TB / 2 TB kullanılıyor
      </div>
    </div>
  );
}
