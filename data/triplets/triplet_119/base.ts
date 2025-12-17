// Accessibility utilities for improving user experience and compliance

export const generateId = (prefix: string = 'id'): string => {
  return `${prefix}-${Math.random().toString(36).substr(2, 9)}`;
};

export const createAriaLabel = (text: string, context?: string): string => {
  return context ? `${text}, ${context}` : text;
};

export const announceToScreenReader = (message: string): void => {
  const announcement = document.createElement('div');
  announcement.setAttribute('aria-live', 'polite');
  announcement.setAttribute('aria-atomic', 'true');
  announcement.className = 'sr-only';
  announcement.textContent = message;
  
  document.body.appendChild(announcement);
  
  // Remove after announcement
  setTimeout(() => {
    document.body.removeChild(announcement);
  }, 1000);
};

export const trapFocus = (element: HTMLElement): (() => void) => {
  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  
  const firstElement = focusableElements[0] as HTMLElement;
  const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;
  
  const handleTabKey = (e: KeyboardEvent) => {
    if (e.key === 'Tab') {
      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          lastElement.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastElement) {
          firstElement.focus();
          e.preventDefault();
        }
      }
    }
  };
  
  element.addEventListener('keydown', handleTabKey);
  firstElement?.focus();
  
  return () => {
    element.removeEventListener('keydown', handleTabKey);
  };
};

export const isElementVisible = (element: HTMLElement): boolean => {
  const rect = element.getBoundingClientRect();
  const style = window.getComputedStyle(element);
  
  return (
    rect.width > 0 &&
    rect.height > 0 &&
    style.visibility !== 'hidden' &&
    style.display !== 'none' &&
    style.opacity !== '0'
  );
};

export const getContrastRatio = (color1: string, color2: string): number => {
  // Simple contrast ratio calculation
  // This is a simplified version - in production, use a proper color library
  return 4.5; // Placeholder value
};

export const validateAriaAttributes = (element: HTMLElement): string[] => {
  const errors: string[] = [];
  
  // Check for required ARIA attributes
  if (element.hasAttribute('aria-expanded') && !element.hasAttribute('aria-controls')) {
    errors.push('aria-expanded requires aria-controls');
  }
  
  if (element.hasAttribute('aria-labelledby') && !document.getElementById(element.getAttribute('aria-labelledby')!)) {
    errors.push('aria-labelledby references non-existent element');
  }
  
  return errors;
};

export const enhanceKeyboardNavigation = (container: HTMLElement): void => {
  const focusableElements = container.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  
  focusableElements.forEach((element, index) => {
    element.setAttribute('tabindex', index === 0 ? '0' : '-1');
  });
};

export const announcePageChange = (pageTitle: string): void => {
  announceToScreenReader(`Navigated to ${pageTitle}`);
  document.title = pageTitle;
};

export const createSkipLink = (targetId: string, text: string = 'Skip to main content'): HTMLElement => {
  const skipLink = document.createElement('a');
  skipLink.href = `#${targetId}`;
  skipLink.textContent = text;
  skipLink.className = 'sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-blue-600 text-white px-4 py-2 rounded z-50';
  
  return skipLink;
};

export const setupFocusManagement = (): void => {
  // Add skip link to page
  const skipLink = createSkipLink('main-content');
  document.body.insertBefore(skipLink, document.body.firstChild);
  
  // Enhance keyboard navigation
  const mainContent = document.getElementById('main-content');
  if (mainContent) {
    enhanceKeyboardNavigation(mainContent);
  }
};

export const checkColorContrast = (element: HTMLElement): boolean => {
  const style = window.getComputedStyle(element);
  const backgroundColor = style.backgroundColor;
  const color = style.color;
  
  // This is a simplified check - in production, use a proper color contrast library
  return getContrastRatio(backgroundColor, color) >= 4.5;
};

export const addFocusIndicators = (): void => {
  const style = document.createElement('style');
  style.textContent = `
    *:focus {
      outline: 2px solid #3b82f6;
      outline-offset: 2px;
    }
    
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
    
    .focus\\:not-sr-only:focus {
      position: static;
      width: auto;
      height: auto;
      padding: inherit;
      margin: inherit;
      overflow: visible;
      clip: auto;
      white-space: normal;
    }
  `;
  document.head.appendChild(style);
};

export const initializeAccessibility = (): void => {
  addFocusIndicators();
  setupFocusManagement();
  
  // Announce page load
  announcePageChange(document.title);
  
  // Check for accessibility issues
  const elements = document.querySelectorAll('[aria-expanded], [aria-labelledby]');
  elements.forEach(element => {
    const errors = validateAriaAttributes(element as HTMLElement);
    if (errors.length > 0) {
      console.warn('Accessibility issues found:', errors);
    }
  });
};