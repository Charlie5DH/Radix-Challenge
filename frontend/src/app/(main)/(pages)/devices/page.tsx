"use client";
import { Device } from "@/types/types";
import React from "react";
import DevicesTable from "./_components/DevicesTable";
import { devicesSample } from "@/constants";

const DevicesPage = () => {
  const [devices, setDevices] = React.useState<Device[]>(devicesSample);

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
