import { BucketGrid } from "@/components/BucketGrid";
import { QuickAccess } from "@/components/QuickAccess";
import { RecentTable } from "@/components/RecentTable";
import { StorageDonut } from "@/components/StorageDonut";

export function DashboardPage() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 p-6">
      <div className="lg:col-span-2 space-y-6">
        <QuickAccess />
        <BucketGrid />
      </div>
      <div className="space-y-6">
        <StorageDonut />
        <RecentTable />
      </div>
    </div>
  );
}
