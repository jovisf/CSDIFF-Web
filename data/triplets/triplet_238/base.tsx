'use client';
<<<<<<< HEAD
import React, { useEffect, useState, createContext, useContext } from 'react';
import { AccessibilitySettings, AccessibilityContextType } from '../types/accessibility';
import { Settings } from 'lucide-react';;
=======
>>>>>>> origin/main

import React, { useEffect, useState } from 'react';
import { AccessibilityContextType } from '../types/accessibility';
import { AccessibilityContext } from '../contexts/AccessibilityContext';
import { useAccessibility } from '../hooks/useAccessibility';

interface EnhancedAccessibilityProps {
  children: React.ReactNode;
}

const EnhancedAccessibility: React.FC<EnhancedAccessibilityProps> = ({ children }) => {
  const [settings, setSettings] = useState<any>({
    highContrast: false,
    reducedMotion: false,
    fontSize: 'medium',
    focusVisible: false,
    screenReaderMode: false,
    keyboardNavigation: false
  });

  const [announcements, setAnnouncements] = useState<string[]>([]);

  // Load settings from localStorage
  useEffect(() => {
    const savedSettings = localStorage.getItem('accessibility-settings');
    if (savedSettings) {
      try {
        const parsed = JSON.parse(savedSettings);
        setSettings((prev: any) => ({ ...prev, ...parsed }));
      } catch (error) {
        console.warn('Failed to parse accessibility settings:', error);
      }
    }
  }, []);

  // Save settings to localStorage
  useEffect(() => {
    localStorage.setItem('accessibility-settings', JSON.stringify(settings));
  }, [settings]);

  // Apply accessibility settings
  useEffect(() => {
    const root = document.documentElement;
    
    // High contrast
    if (settings.highContrast) {
      root.classList.add('high-contrast');
    } else {
      root.classList.remove('high-contrast');
    }

    // Reduced motion
    if (settings.reducedMotion) {
      root.classList.add('reduced-motion');
    } else {
      root.classList.remove('reduced-motion');
    }

    // Font size
    root.classList.remove('font-small', 'font-medium', 'font-large');
    root.classList.add(`font-${settings.fontSize}`);

    // Focus visible
    if (settings.focusVisible) {
      root.classList.add('focus-visible');
    } else {
      root.classList.remove('focus-visible');
    }

    // Screen reader mode
    if (settings.screenReaderMode) {
      root.classList.add('screen-reader-mode');
    } else {
      root.classList.remove('screen-reader-mode');
    }
  }, [settings]);

  // Keyboard navigation detection
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Tab') {
        setSettings((prev: any) => ({ ...prev, keyboardNavigation: true }));
        document.body.classList.add('keyboard-navigation');
      }
    };

    const handleMouseDown = () => {
      setSettings((prev: any) => ({ ...prev, keyboardNavigation: false }));
      document.body.classList.remove('keyboard-navigation');
    };

    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('mousedown', handleMouseDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.removeEventListener('mousedown', handleMouseDown);
    };
  }, []);

  // Focus management
  useEffect(() => {
    const handleFocusIn = (event: FocusEvent) => {
      const target = event.target as HTMLElement;
      if (target && typeof target.scrollIntoView === 'function') {
        target.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    };

    document.addEventListener('focusin', handleFocusIn);
    return () => document.removeEventListener('focusin', handleFocusIn);
  }, []);

  // Screen reader announcements
  useEffect(() => {
    if (announcements.length > 0) {
      const announcement = announcements[announcements.length - 1];
      const announcementElement = document.createElement('div');
      announcementElement.setAttribute('aria-live', 'polite');
      announcementElement.setAttribute('aria-atomic', 'true');
      announcementElement.className = 'sr-only';
      announcementElement.textContent = announcement;
      
      document.body.appendChild(announcementElement);
      
      setTimeout(() => {
        document.body.removeChild(announcementElement);
        setAnnouncements(prev => prev.slice(1));
      }, 1000);
    }
  }, [announcements]);

  const updateSetting = (key: string, value: any) => {
    setSettings((prev: any) => ({ ...prev, [key]: value }));
  };

  const announceToScreenReader = (message: string) => {
    setAnnouncements(prev => [...prev, message]);
  };

  const contextValue: AccessibilityContextType = {
    settings,
    updateSetting,
    announceToScreenReader
  };

  return (
    <AccessibilityContext.Provider value={contextValue}>
      <div className="accessibility-enhanced">
        {children}
        <AccessibilityControls />
      </div>
    </AccessibilityContext.Provider>
  );
};

// Accessibility controls component
const AccessibilityControls: React.FC = () => {
  const { settings, updateSetting } = useAccessibility();
  const [isOpen, setIsOpen] = useState(false);

  if (typeof window === 'undefined') return null;

  return (
    <>
      <button
        className="fixed bottom-4 left-4 bg-blue-600 text-white p-3 rounded-full shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 z-50"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Accessibility controls"
        aria-expanded={isOpen}
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v2m0-6a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
        </svg>
      </button>

      {isOpen && (
        <div className="fixed bottom-20 left-4 bg-white rounded-lg shadow-xl p-4 w-80 z-50 border">
          <h3 className="text-lg font-semibold mb-4">Accessibility Settings</h3>
          
          <div className="space-y-4">
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={settings.highContrast}
                onChange={(e) => updateSetting('highContrast', e.target.checked)}
                className="rounded"
              />
              <span>High Contrast</span>
            </label>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={settings.reducedMotion}
                onChange={(e) => updateSetting('reducedMotion', e.target.checked)}
                className="rounded"
              />
              <span>Reduce Motion</span>
            </label>

            <div>
              <label className="block text-sm font-medium mb-2">Font Size</label>
              <select
                value={settings.fontSize}
                onChange={(e) => updateSetting('fontSize', e.target.value)}
                className="w-full p-2 border rounded"
              >
                <option value="small">Small</option>
                <option value="medium">Medium</option>
                <option value="large">Large</option>
              </select>
            </div>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={settings.focusVisible}
                onChange={(e) => updateSetting('focusVisible', e.target.checked)}
                className="rounded"
              />
              <span>Enhanced Focus Indicators</span>
            </label>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={settings.screenReaderMode}
                onChange={(e) => updateSetting('screenReaderMode', e.target.checked)}
                className="rounded"
              />
              <span>Screen Reader Mode</span>
            </label>
          </div>

          <button
            onClick={() => setIsOpen(false)}
            className="mt-4 w-full bg-gray-200 text-gray-800 py-2 px-4 rounded hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500"
          >
            Close
          </button>
        </div>
      )}
    </>
  );
};

export default EnhancedAccessibility;