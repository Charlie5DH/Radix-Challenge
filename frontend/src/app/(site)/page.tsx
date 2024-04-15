"use client";
import { TypewriterEffectSmooth } from "@/components/ui/typewriter-effect";
import { typeWriterHeader } from "@/constants";
import { ContainerScroll } from "@/components/ui/container-scroll-animation";
import { LampComponent } from "@/components/ui/lamp";
import PlatformFeatures from "@/components/site/PlatformFeatures";
import InfoSection from "@/components/site/InfoSection";

export default function Home() {
  return (
    <>
      <section className="h-screen w-full rounded-md !overflow-visible relative flex flex-col items-center antialiased">
        <div className="flex flex-col mt-[-180px] md:mt-[-50px]">
          <ContainerScroll
            titleComponent={
              <div className="flex items-center flex-col w-full md:w-[640px] lg:w-[800px] xl:w-[960px] 2xl:w-[1200px]">
                <TypewriterEffectSmooth words={typeWriterHeader} />
                <h1 className="text-5xl md:text-8xl bg-clip-text text-transparent bg-gradient-to-b from-white to-neutral-600 font-sans font-bold">
                  PipeWatcher
                </h1>
              </div>
            }
          />
        </div>
      </section>

      <section className="mt-64 w-full">
        <LampComponent />
      </section>

      <section className="-mt-20 mb-20 w-full">
        <InfoSection />
      </section>
    </>
  );
}
