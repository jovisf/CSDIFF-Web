import React from 'react';

interface ComponentProps {
  children?: React.ReactNode;
}

export default function Component({ children }: ComponentProps) {
  return (
    <div>
      {children}
    </div>
  );
}