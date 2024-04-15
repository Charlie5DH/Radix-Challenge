"use server";

import { Device } from "@/types/types";

export async function fetchSensors(): Promise<Device[]> {
  const response = await fetch(`http://localhost:9010/sensors`);

  if (!response.ok) {
    throw new Error("Failed to fetch sensors");
  }
  return response.json();
}

export async function fetchSensorData({
  equipment_ids,
  init_timestamp,
  end_timestamp,
  aggregation_window,
}: {
  equipment_ids: string;
  init_timestamp: string;
  end_timestamp: string;
  aggregation_window: string;
}): Promise<
  {
    time: any;
    equipment_id: string;
    timestamp: string;
    value: number | "null";
  }[]
> {
  const response = await fetch(
    `http://localhost:9010/by_timestamp?equipment_ids=${equipment_ids}&init_timestamp=${init_timestamp}&end_timestamp=${end_timestamp}&aggregation_window=${aggregation_window}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch sensor data");
  }
  return response.json();
}

export async function uploadFile(file: File): Promise<void> {
  const formData = new FormData();
  formData.append("file", file);

  console.log("Uploading file");

  // check that the file is a CSV
  if (file.type !== "text/csv") {
    throw new Error("Invalid file type");
  }

  const response = await fetch(`http://localhost:9010/upload_csv`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to upload file");
  }
}
