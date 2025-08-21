import { FileText } from "lucide-react";

const recentFiles = [
  { name: "proje_sunumu.pdf", size: "2.1 MB", date: "2023-10-26" },
  { name: "bütçe_2024.xlsx", size: "780 KB", date: "2023-10-25" },
  { name: "toplanti_notlari.docx", size: "120 KB", date: "2023-10-24" },
];

export function RecentTable() {
  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h3 className="font-semibold mb-2">Son Dosyalar</h3>
      <table className="w-full text-sm">
        <tbody>
          {recentFiles.map((file) => (
            <tr key={file.name} className="border-b">
              <td className="p-2">
                <FileText className="w-5 h-5 text-gray-500" />
              </td>
              <td className="p-2 font-medium">{file.name}</td>
              <td className="p-2 text-gray-500">{file.size}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
