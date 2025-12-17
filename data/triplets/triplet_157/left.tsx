import React from 'react';

interface BreadcrumbProps {
  children: React.ReactNode;
}

export default function Breadcrumb({ children }: BreadcrumbProps) {
  return (
    <div>
      {children}
    </div>
  );
}