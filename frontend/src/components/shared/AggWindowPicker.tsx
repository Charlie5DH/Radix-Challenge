"use client";
import React from "react";
import { Button } from "../ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { aggWindows } from "@/constants";
import { Calendar, CheckCircle2 } from "lucide-react";
import { AggWindow } from "@/types/types";

const AggWindowPicker = ({
  aggWindow,
  setAggWindow,
}: {
  aggWindow: AggWindow;
  setAggWindow: React.Dispatch<React.SetStateAction<AggWindow>>;
}) => {
  return (
    <div className="flex flex-col gap-1">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="outline" className="flex items-center justify-between gap-4">
            {aggWindow.label ? aggWindow.label : "Select an aggregation window"}
            <Calendar className="h-4 w-4 ml-2" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="center" className="flex flex-col w-full">
          {aggWindows.map((option) => (
            <DropdownMenuItem
              key={option.value}
              onClick={() => setAggWindow(option)}
              className="flex items-center justify-between w-full gap-4"
            >
              <span>{option.label}</span>
              {option.value === aggWindow.value && <CheckCircle2 className="h-4 w-4 text-primary" />}
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
};

export default AggWindowPicker;
