import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  // State: Holds the user data and authentication status
  state: () => ({
    user: null as User | null, // `User` is a TypeScript interface for typing (defined below)
  }),

  // Getters: Used to compute derived state
  getters: {
    isAuthenticated: (state) => !!state.user, // Returns true if the user is logged in
    userName: (state) => state.user?.username || "Guest", // Access user's name or show "Guest"
  },

  // Actions: Define methods to update state or handle logic
  actions: {
    // Set user data
    setUser(userData: User) {
      this.user = userData;
    },

    // Clear user data (for logout)
    clearUser() {
      this.user = null;
    },
  },
});

// Define a TypeScript interface for User
export interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  date_of_birth: string | null; // ISO string for the date of birth
  hobbies: Array<{ id: number; name: string }>; // List of hobbies
}