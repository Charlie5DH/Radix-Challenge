import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import React, { useState, ChangeEvent } from "react";

const FileUploadComponent: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
    }
  };

  const handleSubmit = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:9010/upload_csv", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        console.log("File uploaded successfully");
        // Handle success
      } else {
        console.error("Failed to upload file");
        // Handle error
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      // Handle error
    }
  };

  return (
    <div className="flex items-center gap-2">
      <Input type="file" onChange={handleFileChange} />
      <Button type="submit" onClick={handleSubmit}>
        Upload CSV File
      </Button>
    </div>
  );
};

export default FileUploadComponent;
