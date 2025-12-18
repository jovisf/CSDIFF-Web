import React, { ReactNode } from 'react';
import { Inter } from 'next/font/google';
import SkipLink from './components/SkipLink';

const inter = Inter({ subsets: ['latin'] });
import Navigation from './components/Navigation';
import Footer from './components/Footer';

import ClientComponents from './components/ClientComponents';

import Analytics from './components/Analytics';

// import ConsolidatedPerformance from './components/consolidated/ConsolidatedPerformance';

import ConsolidatedAccessibility from './components/consolidated/ConsolidatedAccessibility';

import ConsolidatedSEO from './components/consolidated/ConsolidatedSEO';

import PerformanceMonitoring from './components/PerformanceMonitoring';

import SEOOptimization from './components/SEOOptimization';

// import SecurityEnhancement from './components/SecurityEnhancement';

import PerformanceMonitor from './components/PerformanceMonitor';
import ServiceWorkerRegistration from './components/ServiceWorkerRegistration';

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en" dir="ltr">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5, user-scalable=yes" />
        <meta name="color-scheme" content="light dark" />
        <meta name="format-detection" content="telephone=no, address=no, email=no" />
        <meta httpEquiv="x-ua-compatible" content="IE=edge" />
        <link rel="manifest" href="/manifest.json" />
        <meta name="theme-color" content="#3b82f6" />
        <meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0b1221" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="Zion Tech Group" />
        <link rel="apple-touch-icon" href="/icon-192x192.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/icon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/icon-16x16.png" />
        <link rel="preconnect" href="https://fonts.googleapis.com" crossOrigin="anonymous" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body className={inter.className}>
        <Analytics />
        {/* <ConsolidatedPerformance /> */}
        <ConsolidatedAccessibility />
        <ConsolidatedSEO />
        <ClientComponents>
            <div className="min-h-screen bg-slate-900">
              <SkipLink />
              <Navigation />
              <main className="relative z-10" id="main-content" role="main" tabIndex={-1}>
                {children}
              </main>
              <Footer />
              <PerformanceMonitor />
              <ServiceWorkerRegistration />
              <PerformanceMonitoring />
              <SEOOptimization />
              {/* <SecurityEnhancement /> */}
            </div>
          </ClientComponents>
      </body>
    </html>
  );
}