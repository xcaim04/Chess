/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  async rewrites() {
    // Reemplaza esta URL con la URL de tu API real
    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000'
    
    return [
      {
        source: '/auth/:path*',
        destination: `${API_URL}/auth/:path*`,
      },
      {
        source: '/chess/:path*',
        destination: `${API_URL}/chess/:path*`,
      },
    ]
  },
}

export default nextConfig
