"use client"

import React, { useEffect } from "react"

interface AnalyticsProps {
  className?: string;
}

const Analytics: React.FC<AnalyticsProps> = () => {
  useEffect(() => {
    const initAnalytics = () => {
      if (typeof window !== "undefined" && window.gtag) {
        window.gtag("config", "GA_MEASUREMENT_ID", {
          page_title: document.title,
          page_location: window.location.href,
        })
      }
    }
    initAnalytics()
  }, [])

  return null; // Analytics component doesn't render anything
}

export default Analytics