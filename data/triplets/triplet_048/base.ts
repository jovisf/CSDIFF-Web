// Logger utility for consistent logging across the application
interface LogContext {
  component?: string;
  userId?: string;
  sessionId?: string;
  [key: string]: string | number | boolean | null | undefined;
}

class Logger {
  private isDevelopment = process.env.NODE_ENV === 'development';

  private formatMessage(level: string, message: string, context?: LogContext): string {
    const timestamp = new Date().toISOString();
    const contextStr = context ? ` | ${JSON.stringify(context)}` : '';
    return `[${timestamp}] ${level.toUpperCase()}: ${message}${contextStr}`;
  }

  private log(level: string, message: string, context?: LogContext): void {
    if (this.isDevelopment) {
      const formattedMessage = this.formatMessage(level, message, context);
      console.log(formattedMessage);
    }
    
    // In production, you would send logs to your logging service
    if (process.env.NODE_ENV === 'production') {
      this.sendToLoggingService(level, message, context);
    }
  }

  debug(message: string, context?: LogContext): void {
    this.log('debug', message, context);
  }

  info(message: string, context?: LogContext): void {
    this.log('info', message, context);
  }

  warn(message: string, context?: LogContext): void {
    this.log('warn', message, context);
  }

  error(message: string, error?: Error, context?: LogContext): void {
    const errorContext = {
      ...context,
      error: error ? {
        name: error.name,
        message: error.message,
        stack: error.stack
      } : undefined
    };
    this.log('error', message, errorContext);
  }

  private sendToLoggingService(level: string, message: string, context?: LogContext): void {
    // Implement your logging service integration here
    // Examples: Sentry, LogRocket, DataDog, etc.
    if (typeof window !== 'undefined' && (window as unknown as { gtag?: (...args: unknown[]) => void }).gtag) {
      (window as unknown as { gtag: (...args: unknown[]) => void }).gtag('event', 'log', {
        event_category: 'logging',
        event_label: level,
        value: 1,
        custom_parameters: {
          message,
          context: JSON.stringify(context)
        }
      });
    }
  }
}

const logger = new Logger();
export default logger;