import { AggWindow, Device } from "@/types/types";
import { Box, LayoutDashboard, ScrollText, Settings } from "lucide-react";
import { z } from "zod";

export const typeWriterHeader = [
  {
    text: "Keep track of your",
  },
  {
    text: "Oil and Gas",
    className: "text-blue-500 dark:text-blue-500",
  },
  {
    text: "operation",
  },
];

export const sideBarOptions = [
  { name: "Dashboard", Component: LayoutDashboard, href: "/dashboard" },
  { name: "Devices", Component: Box, href: "/devices" },
];

export const dateOptions: { label: string; value: string; query: number; agg_window: string }[] = [
  { label: "Last 24 hours", value: "Last 24 hours", query: 1, agg_window: "1h" },
  { label: "Last 48 hours", value: "Last 48 hours", query: 2, agg_window: "1h" },
  { label: "Last 7 days", value: "Last 7 days", query: 7, agg_window: "1d" },
  { label: "Last 30 days", value: "Last 30 days", query: 30, agg_window: "1d" },
];

export const aggWindows: AggWindow[] = [
  { label: "5 minutes", value: "5m" },
  { label: "10 minutes", value: "10m" },
  { label: "30 minutes", value: "30m" },
  { label: "1 hour", value: "1h" },
  { label: "6 hours", value: "6h" },
  { label: "12 hours", value: "12h" },
  { label: "1 day", value: "1d" },
];
