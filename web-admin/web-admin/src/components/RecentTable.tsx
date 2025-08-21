import { FileText } from "lucide-react";
import type { StorageObject } from "@/lib/types";

type Props = { items?: StorageObject[] };

export function RecentTable({ items = [] }: Props) {
  return (
    <div className="bg-white p-4 rounded-2xl shadow-soft">
      <h3 className="font-semibold mb-2">Son Dosyalar</h3>
      <table className="w-full text-sm">
        <tbody>
          {items.map((file) => (
            <tr key={file.key} className="border-b">
              <td className="p-2">
                <FileText className="w-5 h-5 text-gray-500" />
              </td>
              <td className="p-2 font-medium break-all">{file.key}</td>
              <td className="p-2 text-gray-500">{(file.size/1024).toFixed(1)} KB</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
