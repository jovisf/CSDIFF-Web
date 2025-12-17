'use client'
/**
 * Testing Utilities
 * Provides helper functions and utilities for testing
 */

/**
 * Wait for a specified amount of time
 */
export const wait = (ms: number): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * Wait for a condition to be true
 */
export const waitFor = async (
  condition: () => boolean,
  timeout = 5000,
  interval = 100
): Promise<void> => {
  const startTime = Date.now()
  while (!condition()) {
    if (Date.now() - startTime > timeout) {
      throw new Error(`Timeout waiting for condition after ${timeout}ms`)
    }
    await wait(interval)
  }
}

/**
 * Mock fetch for testing
 */
export const mockFetch = (
  response: unknown,
  status = 200,
  headers: Record<string, string> = {}
): void => {
  if (typeof global !== 'undefined') {
    (global as typeof global & { fetch: typeof fetch }).fetch = jest.fn(() =>
      Promise.resolve({
        ok: status >= 200 && status < 300,
        status,
        headers: new Headers(headers),
        json: async () => response,
        text: async () => JSON.stringify(response)
      } as Response)
    ) as typeof fetch
  }
}

/**
 * Mock local storage
 */
export class MockStorage implements Storage {
  private store: Map<string, string> = new Map()

  get length(): number {
    return this.store.size
  }

  clear(): void {
    this.store.clear()
  }

  getItem(key: string): string | null {
    return this.store.get(key) || null
  }

  key(index: number): string | null {
    const keys = Array.from(this.store.keys())
    return keys[index] || null
  }

  removeItem(key: string): void {
    this.store.delete(key)
  }

  setItem(key: string, value: string): void {
    this.store.set(key, value)
  }
}

/**
 * Create a mock localStorage for testing
 */
export const createMockStorage = (): MockStorage => {
  return new MockStorage()
}

/**
 * Mock window object
 */
export const mockWindow = (overrides: Partial<Window> = {}): void => {
  if (typeof global !== 'undefined') {
    Object.defineProperty(global, 'window', {
      value: {
        ...global.window,
        ...overrides
      },
      writable: true,
    })
  }
}

/**
 * Create a mock performance API
 */
export const createMockPerformance = (): Performance => {
  const entries: PerformanceEntry[] = []
  return {
    now: () => Date.now(),
    mark: (name: string) => {
      entries.push({
        name,
        entryType: 'mark',
        startTime: Date.now(),
        duration: 0,
        toJSON: () => ({})
      } as PerformanceEntry)
    },
    measure: (name: string, startMark?: string, endMark?: string) => {
      entries.push({
        name,
        entryType: 'measure',
        startTime: Date.now(),
        duration: 100,
        toJSON: () => ({})
      } as PerformanceEntry)
    },
    getEntriesByName: (name: string) => entries.filter(e => e.name === name),
    getEntriesByType: (type: string) => entries.filter(e => e.entryType === type),
    getEntries: () => entries,
    clearMarks: () => {
      entries.length = 0
    },
    clearMeasures: () => {
      entries.length = 0
    },
    clearResourceTimings: () => {},
    setResourceTimingBufferSize: () => {},
    toJSON: () => ({}),
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => true,
    onresourcetimingbufferfull: null,
    timeOrigin: Date.now()
  } as unknown as Performance
}

/**
 * Generate random test data
 */
export const generateTestData = {
  string: (length = 10): string => {
    return Math.random()
      .toString(36)
      .substring(2, length + 2)
  },
  number: (min = 0, max = 100): number => {
    return Math.floor(Math.random() * (max - min + 1)) + min
  },
  boolean: (): boolean => {
    return Math.random() > 0.5
  },
  email: (): string => {
    return `test${generateTestData.string(5)}@example.com`
  },
  url: (): string => {
    return `https://example.com/${generateTestData.string(10)}`
  },
  date: (): Date => {
    return new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000)
  },
  array: <T>(generator: () => T, length = 5): T[] => {
    return Array.from({ length }, generator)
  }
}

/**
 * Deep clone an object
 */
export const deepClone = <T>(obj: T): T => {
  return JSON.parse(JSON.stringify(obj))
}

/**
 * Compare objects for equality
 */
export const deepEqual = (obj1: unknown, obj2: unknown): boolean => {
  return JSON.stringify(obj1) === JSON.stringify(obj2)
}

/**
 * Spy on console methods
 */
export class ConsoleSpy {
  private originalConsole: Console
  private logs: string[] = []
  private errors: string[] = []
  private warnings: string[] = []

  constructor() {
    this.originalConsole = { ...console }
    this.mock()
  }

  private mock(): void {
    console.log = (...args: unknown[]) => {
      this.logs.push(args.map(String).join(' '))
    }
    console.error = (...args: unknown[]) => {
      this.errors.push(args.map(String).join(' '))
    }
    console.warn = (...args: unknown[]) => {
      this.warnings.push(args.map(String).join(' '))
    }
  }

  getLogs(): string[] {
    return [...this.logs]
  }

  getErrors(): string[] {
    return [...this.errors]
  }

  getWarnings(): string[] {
    return [...this.warnings]
  }

  restore(): void {
    console.log = this.originalConsole.log
    console.error = this.originalConsole.error
    console.warn = this.originalConsole.warn
  }

  clear(): void {
    this.logs = []
    this.errors = []
    this.warnings = []
  }
}

/**
 * Create a deferred promise
 */
export interface Deferred<T> {
  promise: Promise<T>
  resolve: (value: T) => void
  reject: (reason?: unknown) => void
}

export const createDeferred = <T>(): Deferred<T> => {
  let resolve: (value: T) => void
  let reject: (reason?: unknown) => void
  const promise = new Promise<T>((res, rej) => {
    resolve = res
    reject = rej
  })
  return { promise, resolve, reject }
}

/**
 * Retry a function with exponential backoff
 */
export const retryWithBackoff = async <T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  initialDelay = 1000
): Promise<T> => {
  let lastError: Error
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error as Error
      if (i < maxRetries - 1) {
        await wait(initialDelay * Math.pow(2, i))
      }
    }
  }
  throw lastError!
}

/**
 * Measure execution time of a function
 */
export const measureExecutionTime = async <T>(
  fn: () => T | Promise<T>
): Promise<{ result: T; duration: number }> => {
  const start = performance.now()
  const result = await fn()
  const duration = performance.now() - start
  return { result, duration }
}

export default {
  wait,
  waitFor,
  mockFetch,
  createMockStorage,
  mockWindow,
  createMockPerformance,
  generateTestData,
  deepClone,
  deepEqual,
  ConsoleSpy,
  createDeferred,
  retryWithBackoff,
  measureExecutionTime
}