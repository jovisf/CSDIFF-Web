'use client';
import React from 'react';

interface SkipLinkProps {
  href: string;
  children: React.ReactNode;
  className?: string;
}

const EnhancedSkipLink: React.FC<SkipLinkProps> = ({
  href,
  children,
  className = ''
}) => {
  return (
    <a
      href={href}
      className={`
        sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4
        bg-cyan-600 text-white px-4 py-2 rounded-lg font-semibold
        hover:bg-cyan-700 transition-colors duration-200 z-50
        ${className}
      `}
      onClick={(e) => {
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
          (target as HTMLElement).focus();
        }
      }}
    >
      {children}
    </a>
  );
};

export default EnhancedSkipLink;