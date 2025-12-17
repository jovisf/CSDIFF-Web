export interface AccessibilityConfig {
    enabled: boolean;
    features: string[];
    compliance: string;
  }

  export interface AccessibilityFeatures {
    screenReader: boolean;
    keyboardNavigation: boolean;
    highContrast: boolean;
    fontSize: string;
  }

  export interface AccessibilityAudit {
    score: number;
    issues: string[];
    recommendations: string[];
  }

  export interface AccessibilityContextType {
    config: AccessibilityConfig;
    features: AccessibilityFeatures;
    audit: AccessibilityAudit;
  }