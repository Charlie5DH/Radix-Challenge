import { currentUser } from "@clerk/nextjs";
import React from "react";

const Layout = async ({ children }: { children: React.ReactNode }) => {
  const user = await currentUser();
  if (!user) return null;

  return (
    <div className="border-l-[1px] border-t-[1px] pb-20 h-screen rounded-l-xl border-muted-foreground/20 overflow-scroll shadow-md dark:shadow-lg dark:shadow-neutral-700">
      {children}
    </div>
  );
};

export default Layout;
