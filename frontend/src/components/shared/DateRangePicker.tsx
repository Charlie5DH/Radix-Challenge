import React from "react";
import { Calendar } from "@/components/ui/calendar";
import { DateRange } from "react-day-picker";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Button } from "../ui/button";
import { cn } from "@/utils/cn";
import { format } from "date-fns";
import { CalendarIcon } from "lucide-react";

const DateRangePicker = ({
  range,
  setRange,
}: {
  range: DateRange | undefined;
  setRange: React.Dispatch<React.SetStateAction<DateRange | undefined>>;
}) => {
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-muted-foreground">Select a date range</span>

      <Popover>
        <PopoverTrigger asChild>
          <Button
            variant={"outline"}
            className={cn("w-[240px] pl-3 text-left font-normal", !range && "text-muted-foreground")}
          >
            {range?.from && range?.to ? (
              <span>
                {format(range.from, "MMM d, yyyy")} - {format(range.to, "MMM d, yyyy")}
              </span>
            ) : (
              <span>Pick a date</span>
            )}
            <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <Calendar
            mode="range"
            selected={range}
            onSelect={setRange}
            className="rounded-md border"
            disabled={(date) => date > new Date() || date < new Date("1900-01-01")}
          />
        </PopoverContent>
      </Popover>
    </div>
  );
};

export default DateRangePicker;
