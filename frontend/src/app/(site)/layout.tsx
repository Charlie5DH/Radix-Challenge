import Navbar from "@/components/site/Navbar";
import { BackgroundBeams } from "@/components/ui/background-beams";
import { TracingBeam } from "@/components/ui/tracing-beam";
import { ClerkProvider } from "@clerk/nextjs";
import { dark } from "@clerk/themes";
import React from "react";

const SiteLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      <Navbar />
      <BackgroundBeams />
      <TracingBeam className="relative mx-32 mt-20">
        <main className="flex items-center justify-center flex-col mb-10">{children}</main>
      </TracingBeam>
    </>
  );
};

export default SiteLayout;
