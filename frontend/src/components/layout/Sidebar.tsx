"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import React from "react";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { sideBarOptions } from "@/constants";
import clsx from "clsx";
import { Separator } from "@/components/ui/separator";
import { ModeToggle } from "../shared/ModeToggle";
import Image from "next/image";

type Props = {};

const Sidebar = (props: Props) => {
  const pathName = usePathname();

  return (
    <nav className=" dark:bg-black h-screen overflow-scroll  justify-between flex items-center flex-col  gap-10 py-6 px-2">
      <div className="flex items-center justify-center flex-col gap-4">
        <Link className="flex font-bold flex-row text-center text-xs my-3" href="/">
          <Image src="/assets/logo.svg" alt="logo" width={30} height={30} />
        </Link>
        <Separator />
        <TooltipProvider>
          {sideBarOptions.map((menuItem) => (
            <ul key={menuItem.name}>
              <Tooltip delayDuration={0}>
                <TooltipTrigger>
                  <li>
                    <Link
                      href={menuItem.href}
                      className={clsx(
                        "group h-6 w-6 flex items-center justify-center scale-[1.5] rounded-sm p-1 cursor-pointer",
                        {
                          "dark:bg-blue-900 bg-[#EEE0FF] shadow-sm": pathName === menuItem.href,
                        }
                      )}
                    >
                      <menuItem.Component />
                    </Link>
                  </li>
                </TooltipTrigger>
                <TooltipContent side="right" className="bg-black/10 backdrop-blur-xl">
                  <p>{menuItem.name}</p>
                </TooltipContent>
              </Tooltip>
            </ul>
          ))}
        </TooltipProvider>
        <Separator />
      </div>
      <div className="flex items-center justify-center flex-col gap-8">
        <ModeToggle />
      </div>
    </nav>
  );
};

export default Sidebar;
