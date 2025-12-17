'use client'
/**
 * Comprehensive Monitoring Utility
 * Real-time application monitoring, performance tracking, and error reporting
 */

import { performanceConfig } from '../../performance.config'

export interface PerformanceMetrics {
  lcp?: number;
  fid?: number;
  cls?: number;
  fcp?: number;
  ttfb?: number;
  inp?: number;
}

export interface ErrorReport {
  message: string;
  stack?: string;
  component?: string;
  timestamp: number;
  userAgent: string;
  url: string;
}

class MonitoringService {
  private metrics: PerformanceMetrics = {}
  private errors: ErrorReport[] = []
  private observer: PerformanceObserver | null = null

  constructor() {
    if (typeof window !== 'undefined') {
      this.initializeMonitoring()
    }
  }

  private initializeMonitoring(): void {
    // Monitor Web Vitals
    this.monitorWebVitals()
    // Monitor Long Tasks
    this.monitorLongTasks()
    // Monitor Resource Loading
    this.monitorResourceTiming()
    // Global Error Handler
    this.setupErrorHandling()
  }

  private monitorWebVitals(): void {
    if ('PerformanceObserver' in window) {
      try {
        // Largest Contentful Paint
        const lcpObserver = new PerformanceObserver((list) => {
          const entries = list.getEntries()
          const lastEntry = entries[entries.length - 1] as PerformanceEntry & { renderTime?: number; loadTime?: number }
          this.metrics.lcp = lastEntry.renderTime || lastEntry.loadTime || 0
          this.reportMetric('lcp', this.metrics.lcp)
        })
        lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] })

        // First Input Delay
        const fidObserver = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          entries.forEach((entry: PerformanceEntry) => {
            this.metrics.fid = (entry as any).processingStart - entry.startTime;
            this.reportMetric('fid', this.metrics.fid);
          });
        });
        fidObserver.observe({ entryTypes: ['first-input'] });

        // Cumulative Layout Shift
        let clsValue = 0;
        const clsObserver = new PerformanceObserver(list => {
          const entries = list.getEntries();
          entries.forEach((entry: PerformanceEntry) => {
            if (!(entry as any).hadRecentInput) {
              clsValue += entry.value;
              this.metrics.cls = clsValue;
              this.reportMetric('cls', clsValue);
            }
          })
        })
        clsObserver.observe({ entryTypes: ['layout-shift'] })

        // First Contentful Paint
        const fcpObserver = new PerformanceObserver(list => {
          const entries = list.getEntries();
          entries.forEach(entry => {
            this.metrics.fcp = entry.startTime;
            this.reportMetric('fcp', entry.startTime);
          });
        });
        fcpObserver.observe({ entryTypes: ['paint'] });
      } catch (error) {
        // console.error('Error setting up performance observers:', error)
      }
    }
  }

  private monitorLongTasks(): void {
    if ('PerformanceObserver' in window && performanceConfig.monitoring.enableLongTaskDetection) {
      try {
        const longTaskObserver = new PerformanceObserver((list) => {
          for (const entry of list.getEntries()) {
            // console.warn('Long task detected:', {
            //   duration: entry.duration,
            //   startTime: entry.startTime
            // })
          }
        })
        longTaskObserver.observe({ entryTypes: ['longtask'] })
      } catch (error) {
        // Long task API might not be available
      }
    }
  }

  private monitorResourceTiming(): void {
    if ('PerformanceObserver' in window) {
      try {
        const resourceObserver = new PerformanceObserver((list) => {
          const entries = list.getEntries()
          entries.forEach((entry: PerformanceEntry) => {
            const resourceEntry = entry as PerformanceResourceTiming
            if (resourceEntry.duration > 1000) {
              // console.warn('Slow resource detected:', {
              //   name: resourceEntry.name,
              //   duration: resourceEntry.duration,
              //   type: resourceEntry.initiatorType
              // })
            }
          })
        })
        resourceObserver.observe({ entryTypes: ['resource'] })
      } catch (_error) {
        // console.error('Error monitoring resources:', _error)
      }
    }
  }

  private setupErrorHandling(): void {
    // Global error handler
    window.addEventListener('error', (event) => {
      this.logError({
        message: event.message,
        stack: event.error?.stack,
        timestamp: Date.now(),
        userAgent: navigator.userAgent,
        url: window.location.href
      })
    })

    // Unhandled promise rejection handler
    window.addEventListener('unhandledrejection', (event) => {
      this.logError({
        message: `Unhandled Promise Rejection: ${event.reason}`,
        timestamp: Date.now(),
        userAgent: navigator.userAgent,
        url: window.location.href
      })
    })
  }

  private reportMetric(name: string, value: number): void {
    // Sample rate
    if (Math.random() > performanceConfig.monitoring.sampleRate) {
      return
    }
    const thresholds = performanceConfig.webVitals[name as keyof typeof performanceConfig.webVitals]
    if (thresholds) {
      const rating = value <= thresholds.good ? 'good' : value <= thresholds.needsImprovement ? 'needs-improvement' : 'poor'
      // console.log(`[Performance] ${name}:`, {
      //   value,
      //   rating,
      //   unit: name === 'cls' ? 'score' : 'ms'
      // })
    }

    // Send to analytics (if configured)
    if (typeof gtag === 'function') {
      gtag('event', name, {
        value: Math.round(name === 'cls' ? value * 1000 : value),
        event_category: 'Web Vitals'
      })
    }
  }

  public logError(_error: ErrorReport): void {
    this.errors.push(error)
    // Keep only last 50 errors
    if (this.errors.length > 50) {
      this.errors = this.errors.slice(-50)
    }
    // console.error('[Error]', error)
    // Send to error tracking service (if configured)
  }

  public getMetrics(): PerformanceMetrics {
    return { ...this.metrics }
  }

  public getErrors(): ErrorReport[] {
    return [...this.errors]
  }

  public clearErrors(): void {
    this.errors = []
  }

  public measureMemory(): void {
    if ('memory' in performance && performanceConfig.monitoring.enableMemoryMonitoring) {
      const memory = (performance as Performance & { memory?: { usedJSHeapSize: number; totalJSHeapSize: number; jsHeapSizeLimit: number } }).memory
      if (memory) {
        // console.log('[Memory]', {
        //   used: `${Math.round(memory.usedJSHeapSize / 1048576)}MB`,
        //   total: `${Math.round(memory.totalJSHeapSize / 1048576)}MB`,
        //   limit: `${Math.round(memory.jsHeapSizeLimit / 1048576)}MB`
        // })
      }
    }
  }

  public measureNavigationTiming(): void {
    if ('performance' in window && 'getEntriesByType' in performance) {
      const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming
      if (navigation) {
        // console.log('[Navigation Timing]', {
        //   'DNS Lookup': `${Math.round(navigation.domainLookupEnd - navigation.domainLookupStart)}ms`,
        //   'TCP Connect': `${Math.round(navigation.connectEnd - navigation.connectStart)}ms`,
        //   'TTFB': `${Math.round(navigation.responseStart - navigation.requestStart)}ms`,
        //   'Download': `${Math.round(navigation.responseEnd - navigation.responseStart)}ms`,
        //   'DOM Interactive': `${Math.round(navigation.domInteractive - navigation.fetchStart)}ms`,
        //   'DOM Complete': `${Math.round(navigation.domComplete - navigation.fetchStart)}ms`,
        //   'Load Complete': `${Math.round(navigation.loadEventEnd - navigation.fetchStart)}ms`
        // })
      }
    }
  }
}

// Singleton instance
const monitoring = new MonitoringService()
export default monitoring