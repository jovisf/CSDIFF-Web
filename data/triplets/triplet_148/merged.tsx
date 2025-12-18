import React from 'react';

interface AnalyticsProps {
  children: React.ReactNode;
}

export default function Analytics({ children }: AnalyticsProps) {
  return (
    <div>
      {children}
    </div>
  );
}