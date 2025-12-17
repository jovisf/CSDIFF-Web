export const analytics = {
  track: (event: string, data?: unknown) => {
    // Analytics tracking logic
    console.log('Tracking:', event, data);
  }
};