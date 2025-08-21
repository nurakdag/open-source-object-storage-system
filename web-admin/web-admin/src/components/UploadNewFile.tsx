import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRef } from "react";
import { api } from "../lib/api";
import { Upload } from "lucide-react";

export default function UploadNewFile({ bucketName }: { bucketName: string }) {
  const queryClient = useQueryClient();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const presignResponse = await api.getPresignUploadUrl({
        bucket: bucketName,
        key: file.name,
      });
      await api.uploadFile(presignResponse.url, file);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["objects", bucketName] });
    },
  });

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      uploadMutation.mutate(file);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div>
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        className="hidden"
      />
      <button
        onClick={handleClick}
        disabled={uploadMutation.isPending}
        className="bg-blue-600 text-white px-4 py-2 rounded-md flex items-center space-x-2 hover:bg-blue-700"
      >
        <Upload className="w-5 h-5" />
        <span>
          {uploadMutation.isPending ? "Yükleniyor..." : "Yeni Dosya Yükle"}
        </span>
      </button>
    </div>
  );
}
