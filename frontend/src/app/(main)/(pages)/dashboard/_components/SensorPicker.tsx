import React from "react";
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { Box } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Device } from "@/types/types";
import SensorsTable from "./SensorsTable";

const SensorPicker = ({
  devices,
  selectedDevices,
  setSelectedDevices,
}: {
  devices: Device[];
  selectedDevices: Device[];
  setSelectedDevices: React.Dispatch<React.SetStateAction<Device[]>>;
}) => {
  return (
    <Sheet>
      <SheetTrigger>
        <Button variant="outline" size="icon">
          <Box className="h-[1.2rem] w-[1.2rem]" />
        </Button>
      </SheetTrigger>
      <SheetContent className="mt-4 mr-4 pr-4 overflow-scroll w-full md:max-w-[600px]" showX>
        <SheetHeader className="text-left">
          <SheetTitle>Sensors</SheetTitle>
          <SheetDescription>Selected sensors will appear in the charts</SheetDescription>
        </SheetHeader>
        <SensorsTable devices={devices} selectedDevices={selectedDevices} setSelectedDevices={setSelectedDevices} />
      </SheetContent>
    </Sheet>
  );
};

export default SensorPicker;
