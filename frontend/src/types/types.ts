import React from "react";

export type DashboardCardTypes = {
  title?: string | React.ReactNode;
  subtitle?: string | React.ReactNode;
  description?: string;
  content?: React.ReactNode;
  icon?: React.ReactNode;
  footer?: React.ReactNode;
};

export type Device = {
  _id: string;
  equipmentId: string;
  name: string;
  type: string;
  createdAt: string;
  updatedAt: string;
};

export type DateOption = {
  label: string;
  value: string;
  query: number;
  agg_window: string;
};

export type AggWindow = {
  label: string;
  value: string;
};
