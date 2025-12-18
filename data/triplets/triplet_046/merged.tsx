import React from 'react';

interface EnhancedAnalyticsProps {
  children: React.ReactNode;
}

export default function EnhancedAnalytics({ children }: EnhancedAnalyticsProps) {
  return (
    <div>
      {children}
    </div>
  );
}