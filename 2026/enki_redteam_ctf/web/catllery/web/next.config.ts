import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  devIndicators: false,
  images: {
    minimumCacheTTL: 0,
    remotePatterns: [{ protocol: "http", hostname: "**" }],
  },
};

export default nextConfig;