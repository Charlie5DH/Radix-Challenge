import React from "react";
import Sidebar from "@/components/layout/Sidebar";
import InfoBar from "@/components/layout/Infobar";

const Layout = (props: { children: React.ReactNode }) => {
  return (
    <div className="flex overflow-hidden h-screen">
      <Sidebar />
      <div className="w-full">
        <InfoBar />
        {props.children}
      </div>
    </div>
  );
};

export default Layout;
