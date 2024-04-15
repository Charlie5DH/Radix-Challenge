"use client";
import React from "react";
import { Button } from "../ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { dateOptions } from "@/constants";
import { Calendar, CheckCircle2 } from "lucide-react";
import { DateOption } from "@/types/types";

const DateRangePickerFixed = ({
  range,
  setRange,
}: {
  range: DateOption;
  setRange: React.Dispatch<React.SetStateAction<DateOption>>;
}) => {
  return (
    <div className="flex flex-col gap-1">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="outline" className="flex items-center justify-between gap-4">
            {range.label ? range.label : "Select a date range"}
            <Calendar className="h-4 w-4 ml-2" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="center" className="flex flex-col w-full">
          {dateOptions.map((option) => (
            <DropdownMenuItem
              key={option.value}
              onClick={() => setRange(option)}
              className="flex items-center justify-between w-full gap-4"
            >
              <span>{option.label}</span>
              {option.value === range.value && <CheckCircle2 className="h-4 w-4 text-primary" />}
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
};

export default DateRangePickerFixed;
