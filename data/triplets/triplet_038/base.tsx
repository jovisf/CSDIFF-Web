"use client";
import React, { useRef, useEffect } from 'react';

interface FuturisticGlowProps {
  children: React.ReactNode;
  intensity?: 'low' | 'medium' | 'high';
  color?: string;
  className?: string;
}

export default function FuturisticGlow({
  children,
  intensity = 'medium',
  color = 'cyan',
  className = ''
}: FuturisticGlowProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const getIntensityValue = () => {
      switch (intensity) {
        case 'low': return '0.3';
        case 'high': return '0.8';
        default: return '0.5';
      }
    };

    const getColorValue = () => {
      switch (color) {
        case 'cyan': return '34, 211, 238';
        case 'purple': return '168, 85, 247';
        case 'pink': return '236, 72, 153';
        case 'green': return '34, 197, 94';
        default: return '34, 211, 238';
      }
    };

    const rgb = getColorValue();
    const opacity = getIntensityValue();
    // Apply CSS custom properties for dynamic glow
    container.style.setProperty('--glow-color', `rgba(${rgb}, ${opacity})`);
    container.style.setProperty('--glow-color-strong', `rgba(${rgb}, ${parseFloat(opacity) + 0.3})`);
  }, [intensity, color]);

  return (
    <div
      ref={containerRef}
      className={`
        relative
        before:absolute
        before:inset-0
        before:rounded-inherit
        before:bg-gradient-to-r
        before:from-transparent
        before:via-[var(--glow-color)]
        before:to-transparent
        before:opacity-0
        before:transition-opacity
        before:duration-500
        hover:before:opacity-100
        after:absolute
        after:inset-0
        after:rounded-inherit
        after:shadow-[0_0_20px_var(--glow-color)]
        after:opacity-0
        after:transition-opacity
        after:duration-500
        hover:after:opacity-100
        ${className}
      `}
    >
      {children}
    </div>
  );
}