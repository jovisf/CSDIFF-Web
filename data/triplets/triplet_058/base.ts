// Performance utilities for optimization
export const defaultConfig = {
  enabled: true,
  debug: false
};

export const defaultFunction = () => {
  return null;
};

// Performance utilities object
export const performanceUtils = {
  measurePerformance: (name: string, fn: () => void) => {
    const start = performance.now();
    fn();
    const end = performance.now();
    console.log(`${name} took ${end - start} milliseconds`);
  },

  monitorWebVitals: () => {
    if (typeof window !== 'undefined' && 'performance' in window) {
      // Monitor Core Web Vitals
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.entryType === 'largest-contentful-paint') {
            console.log('LCP:', entry.startTime);
          }
          if (entry.entryType === 'first-input') {
            console.log('FID:', entry.processingStart - entry.startTime);
          }
          console.log('Performance metric:', entry.name, entry.value);
        }
      });
      
      try {
        observer.observe({ entryTypes: ['largest-contentful-paint', 'first-input', 'measure', 'navigation'] });
      } catch (e) {
        // Fallback for older browsers
        console.log('Performance monitoring not fully supported');
      }
    }
  },

  optimizeImages: () => {
    if (typeof window !== 'undefined') {
      // Lazy load images with intersection observer
      const images = document.querySelectorAll('img[data-src]');
      const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target as HTMLImageElement;
            img.src = img.dataset.src || '';
            img.classList.remove('lazy');
            imageObserver.unobserve(img);
          }
        });
      });

      images.forEach(img => imageObserver.observe(img));
      
      // Also set loading="lazy" for regular images
      const regularImages = document.querySelectorAll('img:not([data-src])');
      regularImages.forEach(img => {
        if (!img.loading) {
          img.loading = 'lazy';
        }
      });
    }
    return true;
  },

  optimizeFonts: () => {
    if (typeof window !== 'undefined') {
      // Preload critical fonts
      const fontPreloads = [
        { href: '/fonts/inter-var.woff2', as: 'font', type: 'font/woff2' },
        { href: '/fonts/inter-var.woff', as: 'font', type: 'font/woff' }
      ];

      fontPreloads.forEach(font => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.href = font.href;
        link.as = font.as;
        if (font.type) link.type = font.type;
        link.crossOrigin = 'anonymous';
        document.head.appendChild(link);
      });
    }
    return true;
  },

<<<<<<< HEAD
  debounce: (func: (...args: any[]) => void, wait: number) => {
    let timeout: NodeJS.Timeout;
    return function executedFunction(...args: any[]) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  throttle: (func: (...args: any[]) => void, limit: number) => {
    let inThrottle: boolean;
    return function executedFunction(...args: any[]) {
      if (!inThrottle) {
        func.apply(this, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
=======
  optimizeThirdParty: () => {
    if (typeof window !== 'undefined') {
      // Defer non-critical scripts
      const scripts = document.querySelectorAll('script[data-defer]');
      scripts.forEach(script => {
        script.setAttribute('defer', '');
      });
      
      // Also optimize regular scripts
      const regularScripts = document.querySelectorAll('script[src]:not([data-defer])');
      regularScripts.forEach(script => {
        if (!script.async && !script.defer) {
          script.async = true;
        }
      });
    }
    return true;
  },

  preloadResource: (href: string, as: string) => {
    if (typeof window !== 'undefined') {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.href = href;
      link.as = as;
      document.head.appendChild(link);
    }
>>>>>>> origin/main
  },

  cleanup: () => {
    // Cleanup function for component unmount
    if (typeof window !== 'undefined') {
      // Remove any performance observers or timers
      const observers = document.querySelectorAll('[data-performance-observer]');
      observers.forEach(observer => observer.remove());
      console.log('Performance utilities cleanup');
    }
  }
};
