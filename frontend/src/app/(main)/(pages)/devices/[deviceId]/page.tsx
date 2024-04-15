"use client";
import React from "react";
import DateRangePicker from "@/components/shared/DateRangePicker";
import { DateRange } from "react-day-picker";

const DevicePage = ({ params }: { params: { deviceId: string } }) => {
  const pastWeek = new Date();
  pastWeek.setDate(pastWeek.getDate() - 7);
  const defaultSelected: DateRange = {
    from: pastWeek,
    to: new Date(),
  };
  const [range, setRange] = React.useState<DateRange | undefined>(defaultSelected);

  return (
    <div className="flex flex-col gap-4">
      <div className="sticky top-0 z-[10] p-5 bg-background/50 backdrop-blur-lg flex items-center justify-between border-b">
        <div className="flex flex-col gap-2">
          <h1 className="text-3xl font-bold ">Device {params.deviceId}</h1>
          <span className="text-sm text-muted-foreground">Device details</span>
        </div>
        <DateRangePicker range={range} setRange={setRange} />
      </div>
    </div>
  );
};

export default DevicePage;
