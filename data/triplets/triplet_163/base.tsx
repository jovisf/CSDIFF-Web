'use client';


import React, { useState, useEffect } from 'react';

interface EnhancedAccessibilityEnhancerProps {
  children: React.ReactNode
  enableKeyboardNavigation?: boolean
  enableScreenReaderSupport?: boolean
  enableHighContrast?: boolean
  enableFocusManagement?: boolean
  enableVoiceNavigation?: boolean
}

const EnhancedAccessibilityEnhancer: React.FC<EnhancedAccessibilityEnhancerProps> = ({
  children,
  enableKeyboardNavigation: _enableKeyboardNavigation = true,
  enableScreenReaderSupport: _enableScreenReaderSupport = true,
  enableHighContrast: _enableHighContrast = false,
  enableFocusManagement: _enableFocusManagement = true,
  enableVoiceNavigation: _enableVoiceNavigation = false,
}) => {
  const [isHighContrast, setIsHighContrast] = useState(false)
  const [_fontSize, setFontSize] = useState('medium')
  const [isReducedMotion, setIsReducedMotion] = useState(false)
  const [isVoiceEnabled, setIsVoiceEnabled] = useState(false)

  useEffect(() => {
    // Check for user's motion preferences
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    setIsReducedMotion(mediaQuery.matches)

    // Check for high contrast preference
    const highContrastQuery = window.matchMedia('(prefers-contrast: high)')
    setIsHighContrast(highContrastQuery.matches)

    // Apply accessibility enhancements
    document.documentElement.setAttribute('data-accessibility-enhanced', 'true')
    
    if (isHighContrast) {
      document.documentElement.classList.add('high-contrast')
    }
    
    if (isReducedMotion) {
      document.documentElement.classList.add('reduced-motion')
    }

    // Add keyboard navigation support
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Tab') {
        document.body.classList.add('keyboard-navigation')
      }
      
      // Add skip links functionality
      if (event.key === 'Enter' && event.target instanceof HTMLElement) {
        if (event.target.getAttribute('data-skip-link')) {
          const targetId = event.target.getAttribute('data-skip-link')
          const target = document.getElementById(targetId || '')
          if (target) {
            target.focus()
            target.scrollIntoView({ behavior: 'smooth' })
          }
        }
      }
    }

    const handleMouseDown = () => {
      document.body.classList.remove('keyboard-navigation')
    }

    document.addEventListener('keydown', handleKeyDown)
    document.addEventListener('mousedown', handleMouseDown)

    return () => {
      document.removeEventListener('keydown', handleKeyDown)
      document.removeEventListener('mousedown', handleMouseDown)
    }
  }, [isHighContrast, isReducedMotion])

  const toggleHighContrast = () => {
    setIsHighContrast(!isHighContrast)
    document.documentElement.classList.toggle('high-contrast')
  }

  const changeFontSize = (size: string) => {
    setFontSize(size)
    document.documentElement.setAttribute('data-font-size', size)
  }

  const toggleVoiceNavigation = () => {
    if (_enableVoiceNavigation && 'speechSynthesis' in window) {
      setIsVoiceEnabled(!isVoiceEnabled)
    }
  }

  return (
    <div className="accessibility-enhanced">
      <div 
        className="accessibility-controls" 
        style={{ position: 'fixed', top: '10px', right: '10px', zIndex: 1000 }}
      >
        <button
          onClick={toggleHighContrast}
          className="accessibility-button"
          aria-label="Toggle high contrast"
        >
          {isHighContrast ? 'Normal Contrast' : 'High Contrast'}
        </button>
        
        <div className="font-size-controls">
          <button
            onClick={() => changeFontSize('small')}
            className="accessibility-button"
            aria-label="Small font size"
          >
            A
          </button>
          <button
            onClick={() => changeFontSize('medium')}
            className="accessibility-button"
            aria-label="Medium font size"
          >
            A
          </button>
          <button
            onClick={() => changeFontSize('large')}
            className="accessibility-button"
            aria-label="Large font size"
          >
            A
          </button>
        </div>

        {_enableVoiceNavigation && (
          <button
            onClick={toggleVoiceNavigation}
            className="accessibility-button"
            aria-label="Toggle voice navigation"
          >
            {isVoiceEnabled ? '🔊' : '🔇'}
          </button>
        )}
      </div>
      {children}
    </div>
  )
}

export default EnhancedAccessibilityEnhancer;
