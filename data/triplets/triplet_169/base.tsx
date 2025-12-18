'use client'
import React, { useEffect } from 'react'

const PerformanceMonitor: React.FC = () => {
  useEffect(() => {
    // Performance monitoring logic
    if (typeof window !== 'undefined') {
      // Monitor Core Web Vitals
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (process.env.NODE_ENV === 'development') {
            console.log('Performance Entry:', entry.name, (entry as PerformanceEntry & { value?: number }).value || 'N/A')
          }
        }
      })

      try {
        observer.observe({ entryTypes: ['measure', 'navigation', 'paint'] })
      } catch (e) {
        if (process.env.NODE_ENV === 'development') {
          console.warn('Performance Observer not supported')
        }
      }

      // Monitor resource loading
      window.addEventListener('load', () => {
        const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming
        if (navigation && process.env.NODE_ENV === 'development') {
          console.log('Page Load Time:', navigation.loadEventEnd - navigation.loadEventStart)
        }
      })

      return () => {
        observer.disconnect()
      }
    }

    return () => {
      // Cleanup function
    }
  }, [])

  return null
}

export default PerformanceMonitor