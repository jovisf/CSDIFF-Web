'use client';
import React, { Suspense, ReactNode } from 'react';
import FuturisticLoader from './FuturisticLoader';

interface LazyWrapperProps {
  children: ReactNode;
  fallback?: ReactNode;
  className?: string;
}

const LazyWrapper: React.FC<LazyWrapperProps> = ({
  children,
  fallback,
  className = ''
}) => {
  const defaultFallback = (
    <div className="flex items-center justify-center min-h-[200px]">
      <FuturisticLoader text="Loading content..." />
    </div>
  );

  return (
    <div className={className}>
      <Suspense fallback={fallback || defaultFallback}>
        {children}
      </Suspense>
    </div>
  );
};

export default LazyWrapper;