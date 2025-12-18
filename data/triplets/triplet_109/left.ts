export interface EnhancedConfig {
    features: string[];
    performance: PerformanceConfig;
    security: SecurityConfig;
  }

  export interface PerformanceConfig {
    enabled: boolean;
    threshold: number;
  }

  export interface SecurityConfig {
    enabled: boolean;
    level: string;
  }