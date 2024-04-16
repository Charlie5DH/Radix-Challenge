"use client";
import React from "react";
import { AreaChartIcon, RefreshCcwIcon } from "lucide-react";
import DasboardCard from "@/components/dashboard/DasboardCard";
import { AreaChart } from "@tremor/react";
import CircleProgress from "@/components/dashboard/CircleProgress";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { AggWindow, DateOption, Device } from "@/types/types";
import { dateOptions } from "@/constants";
import DateRangePickerFixed from "@/components/shared/DateRangePickerFixed";
import { Button } from "@/components/ui/button";
import SensorPicker from "./_components/SensorPicker";
import { fetchSensorData, fetchSensors, uploadFile } from "@/actions/actions";
import AggWindowPicker from "@/components/shared/AggWindowPicker";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import FileUploadComponent from "./_components/FileUploadComponent";
import { useToast } from "@/components/ui/use-toast";

const Dashboard = (props: {}) => {
  const [range, setRange] = React.useState<DateOption>(dateOptions[2]);
  const [devices, setDevices] = React.useState<Device[]>([]);
  const [selectedDevices, setSelectedDevices] = React.useState<Device[] | []>([]);
  const [measures, setMeasures] = React.useState<any[]>([]);
  const [loading, setLoading] = React.useState<boolean>(false);
  const [maxValue, setMaxValue] = React.useState<number>(0);
  const [minValue, setMinValue] = React.useState<number>(0);
  const { toast } = useToast();
  const [aggWindow, setAggWindow] = React.useState<AggWindow>({ label: "10 minutes", value: "10m" });

  React.useEffect(() => {
    setLoading(true);
    fetchSensors().then((data) => {
      setDevices(data);
    });
    setLoading(false);
  }, []);

  React.useEffect(() => {
    if (devices.length > 0) {
      setSelectedDevices([devices[0]]);
      const init_timestamp = new Date();
      init_timestamp.setDate(init_timestamp.getDate() - range.query);
      const end_timestamp = new Date();

      fetchSensorData({
        equipment_ids: devices[0].equipmentId,
        init_timestamp: init_timestamp.toISOString(),
        end_timestamp: end_timestamp.toISOString(),
        aggregation_window: "10m",
      }).then((data) => {
        const measures = data.reduce((acc: { [key: string]: any }, measure) => {
          acc[measure.time] = { time: measure.time, [measure.equipment_id]: measure.value };
          return acc;
        }, {});
        setMeasures(Object.values(measures));
        const values = data.map((measure) => measure.value).filter((value) => value !== null && value !== "null");
        setMaxValue(Number(Math.max(...values.map(Number)).toFixed(2)));
        setMinValue(Number(Math.min(...values.map(Number)).toFixed(2)));
      });
    }
  }, [devices]);

  const handleRefresh = () => {
    const init_timestamp = new Date();
    init_timestamp.setDate(init_timestamp.getDate() - range.query);
    const end_timestamp = new Date();

    fetchSensorData({
      equipment_ids: JSON.stringify(selectedDevices.map((device) => device.equipmentId)),
      init_timestamp: init_timestamp.toISOString(),
      end_timestamp: end_timestamp.toISOString(),
      aggregation_window: aggWindow.value,
    })
      .then((data) => {
        const measures = data.reduce((acc: { [key: string]: any }, measure) => {
          acc[measure.time] = { time: measure.time, [measure.equipment_id]: measure.value };
          return acc;
        }, {});
        setMeasures(Object.values(measures));

        toast({
          title: "Data refreshed",
          description: `Data has been refreshed for the ${range.label}. Measures loaded: ${data.length}`,
        });

        const values = data.map((measure) => measure.value).filter((value) => value !== null && value !== "null");
        if (values.length === 0) {
          setMaxValue(0);
          setMinValue(0);
          return;
        }
        setMaxValue(Number(Math.max(...values.map(Number)).toFixed(2)));
        setMinValue(Number(Math.min(...values.map(Number)).toFixed(2)));
      })
      .catch((error) => {
        toast({
          title: "Failed to refresh data",
          description: "An error occurred while refreshing the data",
          variant: "destructive",
        });
      });
  };

  React.useEffect(() => {
    if (selectedDevices.length > 0) {
      handleRefresh();
    }
  }, [selectedDevices, range, aggWindow]);

  return (
    <div className="flex flex-col gap-4 relative">
      <div className="sticky top-0 z-[10] px-5 py-3 bg-background/50 backdrop-blur-lg flex flex-col border-b">
        <div className="flex flex-wrap items-center justify-between w-full">
          <h1 className="text-3xl font-bold ">Dashboard</h1>
          <div className="flex items-center gap-2 mx-4">
            <FileUploadComponent />
            <DateRangePickerFixed range={range} setRange={setRange} />
            <AggWindowPicker aggWindow={aggWindow} setAggWindow={setAggWindow} />
            <SensorPicker devices={devices} selectedDevices={selectedDevices} setSelectedDevices={setSelectedDevices} />
            <Button variant="outline" size="icon" onClick={handleRefresh}>
              <RefreshCcwIcon className="h-[1.2rem] w-[1.2rem]" />
            </Button>
          </div>
        </div>
        <div className="flex items-center gap-4 mt-2">
          <span className="text-white text-xs">Sensors selected</span>
          {selectedDevices.length > 0 && (
            <div className="flex gap-4">
              {selectedDevices.map((device) => (
                <div key={device.equipmentId} className="flex gap-2 items-center">
                  <div className="h-2 w-2 rounded-full bg-muted-foreground"></div>
                  <span className="text-muted-foreground text-xs">{device.equipmentId}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="flex flex-col gap-4 pb-6 px-4">
        <div className="flex gap-4 flex-col xl:!flex-row">
          <DasboardCard
            title={measures.length.toString()}
            subtitle={`Since the ${range.label}`}
            description="Total number of measures"
            content={`We have received a total of ${measures.length} measures from sensors in the field for the selected interval`}
          />
          <DasboardCard
            title={devices.length.toString()}
            subtitle="Active sensors"
            description="Total number of sensors"
            content={`We have ${devices.length} sensors in the field that are currently active`}
          />
          <DasboardCard
            title={minValue.toString() || "0"}
            subtitle={"For an accepted min of 46. "}
            description="Minimum value"
            content={`A minimum of 0 indicates a sensor failure.`}
          />
          <DasboardCard
            subtitle={<CircleProgress value={maxValue} description={"A maximum of 100 indicates a sensor failure."} />}
            description="Maximum value"
          />
        </div>
        <div className="flex gap-4 flex-col xl:!flex-row">
          <Card className="flex-1 relative">
            <CardHeader>
              <CardTitle className="text-2xl">Sensor measures</CardTitle>
              <CardDescription>{`Mean value of selected sensors for the ${range.label}`}</CardDescription>
            </CardHeader>
            <CardContent>
              <AreaChart
                className="text-sm stroke-primary"
                data={[...(measures || [])]}
                index="time"
                categories={selectedDevices.map((device) => device.equipmentId)}
                showLegend={true}
                //colors={["primary"]}
                yAxisWidth={30}
                showAnimation={true}
                connectNulls={true}
              />
            </CardContent>
            <CardFooter>
              <small>
                From {selectedDevices.length} sensors for the {range.label}
              </small>
            </CardFooter>
            <div className="absolute right-4 top-4 text-muted-foreground"></div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
