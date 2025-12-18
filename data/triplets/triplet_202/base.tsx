import type { Metadata} from 'next';
import { Inter} from 'next/font/google';
import './globals.css';
<<<<<<< HEAD
// import Navigation from './components/Navigation';
// import Footer from './components/Footer';
=======
>>>>>>> origin/main
import Analytics from './components/Analytics';
import PerformanceOptimizer from './components/PerformanceOptimizer';
import AccessibilityEnhancer from './components/AccessibilityEnhancer';
import PerformanceMonitor from './components/PerformanceMonitor';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Zion Tech Group - Leading AI & Technology Solutions Provider',
  description: 'Transform your business with cutting-edge AI, cloud architecture, cybersecurity, and innovative development services. Expert technology solutions for modern enterprises.',
  keywords: 'AI solutions, artificial intelligence, cloud architecture, web development, mobile apps, data analytics, cybersecurity, machine learning, cloud computing, digital transformation',
  authors: [{ name: 'Zion Tech Group' }],
  creator: 'Zion Tech Group',
  publisher: 'Zion Tech Group',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://ziontechgroup.com'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: 'Zion Tech Group - Leading AI & Technology Solutions Provider',
    description: 'Transform your business with cutting-edge AI, cloud architecture, cybersecurity, and innovative development services.',
    url: 'https://ziontechgroup.com',
    siteName: 'Zion Tech Group',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'Zion Tech Group - AI & Technology Solutions',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Zion Tech Group - Leading AI & Technology Solutions Provider',
    description: 'Transform your business with cutting-edge AI, cloud architecture, cybersecurity, and innovative development services.',
    images: ['/og-image.jpg'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'your-google-verification-code',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode}) {
  return (
    <html lang="en" className="scroll-smooth">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
        <link rel="manifest" href="/site.webmanifest" />
        <meta name="theme-color" content="#3b82f6" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className={`${inter.className} antialiased`}>
        <Analytics />
        <PerformanceOptimizer>
          <AccessibilityEnhancer>
            {children}
          </AccessibilityEnhancer>
        </PerformanceOptimizer>
        <PerformanceMonitor />
      </body>
    </html>
  );
}
