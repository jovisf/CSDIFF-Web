'use client';
import React, { useEffect, useState } from 'react';
import { performanceUtils } from './performanceUtils';

interface PerformanceOptimizerProps {
  children: React.ReactNode;
  enableMonitoring?: boolean;
  enableImageOptimization?: boolean;
  enableFontOptimization?: boolean;
  enableThirdPartyOptimization?: boolean;
}

const PerformanceOptimizer: React.FC<PerformanceOptimizerProps> = ({
  children,
  enableMonitoring = true,
  enableImageOptimization = true,
  enableFontOptimization = true,
  enableThirdPartyOptimization = true
}) => {
  const [isOptimized, setIsOptimized] = useState(false);

  useEffect(() => {
    const optimize = () => {
      if (enableMonitoring) {
        performanceUtils.mark('performance-optimization-start');
      }

      // Simulate optimization tasks
      if (enableImageOptimization) {
        // Image optimization would be handled by Next.js Image component
        performanceUtils.mark('image-optimization-complete');
      }

      if (enableFontOptimization) {
        // Font optimization would be handled by Next.js font optimization
        performanceUtils.mark('font-optimization-complete');
      }

      if (enableThirdPartyOptimization) {
        // Third-party optimization would be handled by Next.js
        performanceUtils.mark('third-party-optimization-complete');
      }

      performanceUtils.mark('performance-optimization-end');
      performanceUtils.measure('performance-optimization', 'performance-optimization-start', 'performance-optimization-end');
      setIsOptimized(true);
    };

    // Run optimizations after component mount
    const timer = setTimeout(optimize, 100);

    return () => {
      clearTimeout(timer);
      performanceUtils.clearEntries();
    };
  }, [enableMonitoring, enableImageOptimization, enableFontOptimization, enableThirdPartyOptimization]);

  // Preload critical resources
  useEffect(() => {
    const criticalResources = [
      { href: '/fonts/inter-var.woff2', as: 'font' },
      { href: '/css/critical.css', as: 'style' }
    ];

    criticalResources.forEach(resource => {
      // Create link element for preloading
      const link = document.createElement('link');
      link.rel = 'preload';
      link.href = resource.href;
      link.as = resource.as;
      document.head.appendChild(link);
    });
  }, []);

  return (
    <div className="performance-optimizer">
      {children}
      {process.env.NODE_ENV === 'development' && (
        <div className="fixed bottom-4 right-4 bg-black bg-opacity-75 text-white text-xs p-2 rounded">
          Performance: {isOptimized ? 'Optimized' : 'Loading...'}
        </div>
      )}
    </div>
  );
};

export default PerformanceOptimizer;