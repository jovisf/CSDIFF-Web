interface PerformanceMetrics {
  loadTime: number | null;
  firstContentfulPaint: number | null;
  largestContentfulPaint: number | null;
  firstInputDelay: number | null;
  cumulativeLayoutShift: number | null;
  timeToInteractive: number | null;
  totalBlockingTime: number | null;
}

// Global performance monitoring utilities
export const performanceUtils = {
  // Measure custom performance marks
  mark: (name: string) => {
    if (typeof window !== 'undefined' && 'performance' in window) {
      performance.mark(name);
    }
  },

  // Measure time between marks
  measure: (name: string, startMark: string, endMark?: string) => {
    if (typeof window !== 'undefined' && 'performance' in window) {
      if (endMark) {
        performance.measure(name, startMark, endMark);
      } else {
        performance.measure(name, startMark);
      }
    }
  },
  // Get performance entries
  getEntries: (type?: string) => {
    if (typeof window !== 'undefined' && 'performance' in window) {
      return type ? performance.getEntriesByType(type) : performance.getEntries();
    }
    return [];
  },

  // Clear performance entries
  clearEntries: (type?: string) => {
    if (typeof window !== 'undefined' && 'performance' in window) {
      if (type) {
        performance.clearMeasures(type);
        performance.clearMarks(type);
      } else {
        performance.clearMeasures();
        performance.clearMarks();
      }
    }
  },

  // Monitor Web Vitals
  monitorWebVitals: () => {
    if (typeof window !== 'undefined' && 'performance' in window) {
      // Basic Web Vitals monitoring
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          console.log('Performance entry:', entry);
        }
      });
<<<<<<< HEAD
      observer.observe({ entryTypes: ['measure', 'navigation'] });
=======
      observer.observe({ entryTypes: ['measure', 'navigation', 'paint'] });
>>>>>>> origin/main
    }
  },

  // Optimize images
  optimizeImages: () => {
    if (typeof window !== 'undefined') {
      const images = document.querySelectorAll('img');
      images.forEach(img => {
        if (!img.loading) {
          img.loading = 'lazy';
        }
      });
    }
  },

  // Optimize fonts
  optimizeFonts: () => {
    if (typeof window !== 'undefined') {
      // Preload critical fonts
      const link = document.createElement('link');
      link.rel = 'preload';
      link.href = '/fonts/inter-var.woff2';
      link.as = 'font';
      link.type = 'font/woff2';
      link.crossOrigin = 'anonymous';
      document.head.appendChild(link);
    }
  },

  // Optimize third-party scripts
  optimizeThirdPartyScripts: () => {
    if (typeof window !== 'undefined') {
      // Defer non-critical scripts
<<<<<<< HEAD
      const scripts = document.querySelectorAll<HTMLScriptElement>('script[src]');
      scripts.forEach(script => {
        if (!script.defer && !script.async) {
          script.defer = true;
=======
      const scripts = document.querySelectorAll('script[src]');
      scripts.forEach(script => {
        const htmlScript = script as HTMLScriptElement;
        if (!htmlScript.defer && !htmlScript.async) {
          htmlScript.defer = true;
>>>>>>> origin/main
        }
      });
    }
  },

  // Cleanup resources
  cleanup: () => {
    if (typeof window !== 'undefined' && 'performance' in window) {
      performance.clearMeasures();
      performance.clearMarks();
    }
  },

  // Preload resource
  preloadResource: (href: string, as: string) => {
    if (typeof window !== 'undefined') {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.href = href;
      link.as = as;
      document.head.appendChild(link);
    }
  }
}
// Google Analytics integration for performance tracking
export const trackPerformanceToGA = (metrics: PerformanceMetrics) => {
  if (typeof window !== 'undefined' && 'gtag' in window) {
    (window as unknown as { gtag: (..._args: unknown[]) => void }).gtag('event', 'performance_metrics', {
      event_category: 'Performance',
      event_label: 'Core Web Vitals',
      custom_map: {
        load_time: metrics.loadTime,
        first_contentful_paint: metrics.firstContentfulPaint,
        largest_contentful_paint: metrics.largestContentfulPaint,
        first_input_delay: metrics.firstInputDelay,
        cumulative_layout_shift: metrics.cumulativeLayoutShift,
        time_to_interactive: metrics.timeToInteractive,
        total_blocking_time: metrics.totalBlockingTime
      }
    });
  }
};

declare global {
  interface Window {
    gtag: (..._args: unknown[]) => void;
  }
}