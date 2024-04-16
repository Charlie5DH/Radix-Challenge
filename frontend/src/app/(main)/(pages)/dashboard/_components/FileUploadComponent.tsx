import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useToast } from "@/components/ui/use-toast";
import React, { useState, ChangeEvent } from "react";

const FileUploadComponent: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const { toast } = useToast();

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

    // check if file is a CSV file
    if (file.name.split(".").pop() !== "csv") {
      toast({
        title: "Invalid file type",
        description: "Please upload a CSV file",
        variant: "destructive",
      });
      return;
    }

    try {
      const response = await fetch("http://localhost:9010/upload_csv", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        console.log("File uploaded successfully");
        toast({
          title: "File uploaded successfully",
          description: "The file has been uploaded successfully",
        });
        // Handle success
      } else {
        console.error("Failed to upload file");
        toast({
          title: "Failed to upload file",
          description: "An error occurred while uploading the file",
          variant: "destructive",
        });
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      toast({
        title: "Failed to upload file",
        description: "An error occurred while uploading the file",
        variant: "destructive",
      });
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
