"use client"

import { TrendingUp } from "lucide-react"
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"

export const description = "A multiple bar chart"

const chartData = [
  { month: "January", desktop: 186, mobile: 80 },
  { month: "February", desktop: 305, mobile: 200 },
  { month: "March", desktop: 237, mobile: 120 },
  { month: "April", desktop: 73, mobile: 190 },
  { month: "May", desktop: 209, mobile: 130 },
  { month: "June", desktop: 214, mobile: 140 },
]

const chartConfig = {
  amount: {
    label: "Amount",
    color: "hsl(var(--chart-1))",
  },
  source: {
    label: "id",
    color: "hsl(var(--chart-2))",
  },
} satisfies ChartConfig

export const Bar_:React.FC =({data=[], x_axis="", y_axis="", title="", subtitle=""})=> {
 
  return (
    <Card className="h-full w-1/3 flex flex-col mx-4">
    <CardHeader className="flex-shrink-0">
      <CardTitle>{title}</CardTitle>
      <CardDescription>{subtitle}</CardDescription>
    </CardHeader>
    <CardContent className="flex-grow">
      <ChartContainer config={chartConfig} className="h-full">
        <BarChart accessibilityLayer data={data} className="h-full">
          <CartesianGrid vertical={false} />
          <XAxis
            dataKey={x_axis}
            tickLine={false}
            tickMargin={10}
            axisLine={false}
            tickFormatter={x_axis !==""?(value) => value.slice(0, 3):""}
          />
          <ChartTooltip
            cursor={false}
            content={<ChartTooltipContent indicator="dashed" />}
          />
          <Bar dataKey={y_axis} fill="var(--color-desktop)" radius={4} />
          {/* <Bar dataKey="mobile" fill="var(--color-mobile)" radius={4} /> */}
        </BarChart>
      </ChartContainer>
    </CardContent>
    <CardFooter className="flex-col items-start gap-2 text-sm flex-shrink-0">
      {/* <div className="flex gap-2 font-medium leading-none">
        Trending up by 5.2% this month <TrendingUp className="h-4 w-4" />
      </div>
      <div className="leading-none text-muted-foreground">
        Showing total visitors for the last 6 months
      </div> */}
    </CardFooter>
  </Card>
  
  )
}
