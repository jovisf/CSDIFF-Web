"use client";

/**
 * Accessibility Utilities
 * Helper functions for improving accessibility
 */

export const accessibilityUtils = {
  // Focus management
  focusElement: (selector: string) => {
    const element = document.querySelector(selector) as HTMLElement;
    if (element) {
      element.focus();
    }
  },

  // Skip to main content
  skipToMain: () => {
    const main = document.querySelector('main') as HTMLElement;
    if (main) {
      main.focus();
      main.scrollIntoView();
    }
  },

  // Announce to screen readers
  announce: (message: string) => {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;
    document.body.appendChild(announcement);
    setTimeout(() => {
      document.body.removeChild(announcement);
    }, 1000);
  },

  // Check if element is visible
  isVisible: (element: HTMLElement) => {
    const rect = element.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0;
  },

  // Get accessible name
  getAccessibleName: (element: HTMLElement) => {
    return element.getAttribute('aria-label') ||
           element.getAttribute('aria-labelledby') ||
           element.textContent ||
           element.getAttribute('alt') ||
           element.getAttribute('title') ||
           '';
  }
};

export default accessibilityUtils;