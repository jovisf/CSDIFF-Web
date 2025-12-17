export const apiClient = {
  get: async (url: string) => {
    // API client logic
    return fetch(url);
  }
};