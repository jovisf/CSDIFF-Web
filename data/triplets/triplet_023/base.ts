// Next.js type declarations
declare module 'next' {
  interface NextApiRequest {
    user?: Record<string, unknown>;
  }
  interface NextConfig {
    // Add any Next.js specific types here
    [key: string]: unknown;
  }
}

// Export a utility function
export const nextUtil = () => {
  // Implementation
  return true;
};
<<<<<<< HEAD
export default nextUtil;
=======

export default nextUtil;
>>>>>>> cursor/fix-errors-and-merge-to-main-fb5a
