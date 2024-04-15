import React from "react";

const LogsPage = (props: {}) => {
  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-3xl font-bold sticky top-0 z-[10] p-5 bg-background/50 backdrop-blur-lg flex items-center border-b">
        <span>Logs</span>
      </h1>
    </div>
  );
};

export default LogsPage;
