"use client";
import { Device } from "@/types/types";
import React from "react";
import DevicesTable from "./_components/DevicesTable";
import { fetchSensors } from "@/actions/actions";

const DevicesPage = () => {
  const [devices, setDevices] = React.useState<Device[]>([]);
  const [loading, setLoading] = React.useState<boolean>(false);

  React.useEffect(() => {
    setLoading(true);
    fetchSensors().then((data) => {
      setDevices(data);
    });
    setLoading(false);
  }, []);

  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-3xl font-bold sticky top-0 z-[10] p-5 bg-background/50 backdrop-blur-lg flex items-center border-b">
        Devices
      </h1>

      <div className="flex flex-col gap-4 pb-6 px-4">
        <DevicesTable devices={devices} />
      </div>
    </div>
  );
};

export default DevicesPage;
