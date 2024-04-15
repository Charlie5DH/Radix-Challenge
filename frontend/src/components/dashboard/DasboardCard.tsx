import React from "react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "../ui/card";
import { DashboardCardTypes } from "@/types/types";

const DasboardCard = ({ title, description, subtitle, content, icon, footer }: DashboardCardTypes) => {
  return (
    <Card className="flex-1 relative">
      <CardHeader>
        <CardDescription>{description}</CardDescription>
        {title && <CardTitle className="text-4xl">{title}</CardTitle>}
        {subtitle && <small className="text-xs text-muted-foreground">{subtitle}</small>}
      </CardHeader>
      {content && <CardContent className="text-sm text-muted-foreground">{content}</CardContent>}
      {footer && <CardFooter>{footer}</CardFooter>}
      <div className="absolute right-4 top-4 text-muted-foreground">{icon}</div>
    </Card>
  );
};

export default DasboardCard;
