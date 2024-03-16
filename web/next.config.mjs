/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    FORTUNA_API_BASE: process.env.FORTUNA_API_BASE,
  }
};

export default nextConfig;
