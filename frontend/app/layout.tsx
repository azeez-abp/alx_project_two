import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";


const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  
  return (
    <html lang="en">
      <body className={inter.className}>
      {/* <input  className='toggle theme-controller' type='checkbox' value={'mytheme'}/> */}
        {children}
        <script src="./global.js"></script>
      </body>
    </html>
  );
}
