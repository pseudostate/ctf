import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "ENKI Gallery",
  description: "Gallery seat booking challenge",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <header className="topbarWrap">
          <div className="topbar">
            <a href="/" className="brand">
              ENKI Gallery
            </a>
            <nav className="navLinks">
              <a href="/signup">Sign Up</a>
              <a href="/login">Login</a>
              <a href="/seats">Seats</a>
            </nav>
          </div>
        </header>
        {children}
      </body>
    </html>
  );
}
