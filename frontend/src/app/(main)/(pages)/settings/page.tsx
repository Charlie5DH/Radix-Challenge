import React from "react";
import { currentUser } from "@clerk/nextjs";

type Props = {};

const SettingsPage = async (props: Props) => {
  const authUser = await currentUser();
  if (!authUser) return null;

  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-3xl font-bold sticky top-0 z-[10] p-5 bg-background/50 backdrop-blur-lg flex items-center border-b">
        <span>Settings</span>
      </h1>
    </div>
  );
};

export default SettingsPage;
