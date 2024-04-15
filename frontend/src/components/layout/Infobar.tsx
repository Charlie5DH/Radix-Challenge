"use client";
import React, { useState } from "react";
import { UserButton } from "@clerk/nextjs";
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "../ui/sheet";
import { Bell } from "lucide-react";
import { Card } from "../ui/card";

type Props = {};

const Infobar = (props: Props) => {
  const [allNotifications, setAllNotifications] = useState([]);

  return (
    <div className="flex flex-row justify-end gap-6 items-center px-4 py-4 w-full dark:bg-black ">
      <Sheet>
        <SheetTrigger>
          <div className="rounded-full w-9 h-9 bg-primary-foreground flex items-center justify-center dark:text-white">
            <Bell size={17} />
          </div>
        </SheetTrigger>
        <SheetContent className="mt-4 mr-4 pr-4 overflow-scroll" showX>
          <SheetHeader className="text-left">
            <SheetTitle>Notifications</SheetTitle>
            <SheetDescription>
              <Card className="flex items-center justify-between p-4">Current Account</Card>
            </SheetDescription>
          </SheetHeader>
          {allNotifications?.map((notification, index) => (
            <div key={index} className="flex flex-col gap-y-2 mb-2 overflow-x-scroll text-ellipsis">
              {/* Notification */}
            </div>
          ))}
          {allNotifications?.length === 0 && (
            <div className="flex items-center justify-center text-muted-foreground mt-4 mb-4">
              You have no notifications
            </div>
          )}
        </SheetContent>
      </Sheet>
      <UserButton afterSignOutUrl="/" />
    </div>
  );
};

export default Infobar;
