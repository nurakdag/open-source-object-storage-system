import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { StorageObject } from "@/lib/types";
import { QuickAccess } from "@/components/QuickAccess";
import { BucketGrid } from "@/components/BucketGrid";
import { RecentTable } from "@/components/RecentTable";
import { StorageDonut } from "@/components/StorageDonut";
import { PreviewPane } from "@/components/PreviewPane";
import { useUIStore } from "@/store/ui";

export function DashboardPage() {
  const { setSelectedBucket } = useUIStore();

  const bucketsQ = useQuery({
    queryKey: ["buckets"],
    queryFn: api.getBuckets,
  });

  const objectsQ = useQuery({
    queryKey: ["recent", bucketsQ.data?.[0]?.name],
    enabled: !!bucketsQ.data?.length,
    queryFn: async () => {
      const bucketName = bucketsQ.data![0].name;
      setSelectedBucket(bucketName);
      const objects = await api.getObjects(bucketName, "");
      return objects
        .slice()
        .sort((a: StorageObject, b: StorageObject) =>
          (b.last_modified || "").localeCompare(a.last_modified || "")
        )
        .slice(0, 10);
    },
  });

  useEffect(() => {
    if (bucketsQ.data?.[0]) setSelectedBucket(bucketsQ.data[0].name);
  }, [bucketsQ.data, setSelectedBucket]);

  return (
    <div className="grid grid-cols-12 gap-6">
      <div className="col-span-8 space-y-6">
        <section>
          <div className="text-sm text-slate-500 mb-2">Quick Access</div>
          <QuickAccess items={objectsQ.data || []} />
        </section>

        <section>
          <div className="flex items-center justify-between mb-3">
            <div className="text-sm text-slate-500">My Cloud</div>
            <button className="text-sm text-blue-600">View All</button>
          </div>
          <BucketGrid buckets={bucketsQ.data} />
        </section>

        <section>
          <RecentTable items={objectsQ.data || []} />
        </section>
      </div>

      <div className="col-span-4 space-y-6">
        <StorageDonut items={objectsQ.data || []} />
        <PreviewPane />
      </div>
    </div>
  );
}
