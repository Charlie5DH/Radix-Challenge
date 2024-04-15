import Image from "next/image";
import React from "react";
import { StickyScroll } from "../ui/sticky-scroll-reveal";

const InfoSection = () => {
  const content = [
    {
      title: "IoT ready streaming architecture",
      description:
        "Our platform is built on an IoT-ready streaming architecture based on Kafka that allows you to monitor your sensors in real time. With our platform, you can track every change as it happens, ensuring that you're always working with the most up-to-date information. Say goodbye to outdated data and hello to real-time monitoring.",
      content: (
        <div className="h-full w-full bg-[linear-gradient(to_bottom_right,var(--indigo-500),var(--purple-500))] flex items-center justify-center text-white gap-3">
          <Image src="/assets/Apache_kafka.svg" width={140} height={140} alt="kafka" />
          <span className="font-bold text-7xl">Kafka Streaming</span>
        </div>
      ),
    },
    {
      title: "Time series database",
      description:
        "Our platform is built on InfluxDB, a time series database that allows you to store and analyze time-stamped data. With InfluxDB, you can easily track changes over time, identify trends, and make data-driven decisions. Our platform ensures that you have access to the most accurate and up-to-date information, so you can stay ahead of the curve.",
      content: (
        <div className="h-full w-full flex items-center justify-center bg-[linear-gradient(to_bottom_right,var(--cyan-500),var(--emerald-500))] text-white gap-3">
          <Image src="/assets/influxdb-svgrepo-com.svg" width={200} height={200} alt="linear board demo" />
          <span className="font-bold text-8xl">InfluxDB</span>
        </div>
      ),
    },
    {
      title: "MQTT and HTTP support",
      description:
        "Our platform supports both MQTT and HTTP protocols, making it easy to connect your devices and sensors to our platform. With MQTT and HTTP support, you can easily integrate your existing devices, ensuring that you have access to all the data you need, when you need it.",
      content: (
        <div className="h-full w-full bg-[linear-gradient(to_bottom_right,var(--slate-900),var(--neutral-700))] flex flex-col items-center justify-center">
          <span className="font-bold text-7xl text-white">MQTT &</span>
          <span className="font-bold text-7xl text-blue-600">HTTP Support</span>
        </div>
      ),
    },
    {
      title: "Microservices architecture",
      description:
        "Our platform is built on a microservices architecture that allows you to scale and customize your monitoring solution to meet your specific needs. With our platform, you can easily add new features, integrate with other systems, and scale your monitoring solution as your needs evolve.",
      content: (
        <div className="h-full w-full bg-[linear-gradient(to_bottom_right,var(--cyan-500),var(--emerald-500))] flex items-center justify-center text-white">
          <Image src="/assets/microservices.svg" width={600} height={600} alt="microservices" />
          <span className="font-bold text-6xl">Microservices</span>
        </div>
      ),
    },
  ];
  return (
    <div className="p-10 flex flex-col mx-auto items-center justify-center w-full">
      <StickyScroll content={content} />
    </div>
  );
};

export default InfoSection;
