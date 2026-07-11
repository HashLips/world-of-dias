import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DIAS — A World Between Frequencies",
  description:
    "Enter Dias, explore its fractured frequency realms, and recover the stories of a living world.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
