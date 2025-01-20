import { defineStore } from "pinia";

export const useCsrfStore = defineStore("csrf", {
  state: () => ({
    csrfToken: "" as string, // Store the CSRF token
  }),
  actions: {
    // Initialize the CSRF token by extracting it from cookies
    initializeCsrfToken() {
      const csrfCookie = document.cookie
        .split(";")
        .find((cookie) => cookie.trim().startsWith("csrftoken="));
      if (csrfCookie) {
        this.csrfToken = csrfCookie.split("=")[1];
      } else {
        console.error("CSRF token not found in cookies.");
      }
    },
    
    setCsrfToken(token: string) {
      this.csrfToken = token;
    },
  },
});