<template>
  <div class="container mt-5">
    <div class="card shadow-sm">
      <div class="card-header bg-primary text-white text-center">
        <h2>Threads</h2>
      </div>
      <div class="card-body">
        <!-- Form to create a new thread -->
        <form class="mb-4" @submit.prevent="createThread">
          <div class="form-group">
            <textarea
              v-model="newThreadContent"
              class="form-control"
              placeholder="Write your thread..."
              rows="4"
            ></textarea>
          </div>
          <button
            class="btn btn-primary btn-block"
            :disabled="!newThreadContent.trim()"
          >
            Post Thread
          </button>
        </form>

        <!-- List of threads -->
        <div v-if="threads.length">
          <div
            v-for="thread in threads"
            :key="thread.id"
            class="card mb-3 shadow-sm"
          >
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <h5 class="card-title text-primary mb-1">{{ thread.user__username }}</h5>
                <small class="text-muted">{{ formatDate(thread.created_at) }}</small>
              </div>
              <p class="card-text">{{ thread.content }}</p>
            </div>
          </div>
        </div>
        <div v-else class="text-center text-muted">
          <p>No threads yet! Be the first to post.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * This component handles the display and creation of threads.
 * 
 * Data:
 * - threads: A list of threads fetched from the backend.
 * - newThreadContent: The content of a new thread to be created by the user.
 * 
 * Methods:
 * - fetchThreads: Fetches threads from the backend (Django API) when the component is mounted.
 * - createThread: Creates a new thread and posts it to the backend (Django API).
 * - formatDate: Formats a date string into a readable format.
 * 
 * Dependencies:
 * - ref, onMounted from 'vue'
 * - useCsrfStore from '../stores/csrf'
 * 
 * Usage:
 * - The component fetches threads when it is mounted.
 * - Users can create new threads, which are posted to the backend and added to the top of the list.
 * - Dates are formatted for readability.
 */
import { ref, onMounted } from 'vue';
import { useCsrfStore } from '../stores/csrf';

const csrfStore = useCsrfStore();

interface Thread {
  id: number;
  user__username: string;
  content: string;
  created_at: string;
}

const threads = ref<Thread[]>([]); // List of threads to be fetched from the backend
const newThreadContent = ref<string>(''); // New thread content from the user

// Fetch threads when the component is mounted
onMounted(() => {
  fetchThreads();
});

// Fetch threads from the backend (Django API)
async function fetchThreads() {
  try {
    const response = await fetch('/threads/');
    const data = await response.json();
    console.log(data);
    threads.value = data; // Store threads in the component's data
  } catch (error) {
    console.error('Error fetching threads:', error);
  }
}

// Create a new thread
async function createThread() {
  if (!newThreadContent.value.trim()) {
    return; // Don't post if content is empty
  }

  const newThread = {
    content: newThreadContent.value,
  };

  try {
    const csrfToken = csrfStore.csrfToken; // Retrieve CSRF token from store
    const response = await fetch('/threads/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      credentials: 'include',
      body: JSON.stringify(newThread),
    });

    if (response.ok) {
      const createdThread = await response.json();
      threads.value.unshift(createdThread); // Add the new thread to the top of the list
      newThreadContent.value = ''; // Clear the input
    } else {
      console.error('Error creating thread:', response.statusText);
    }
  } catch (error) {
    console.error('Error creating thread:', error);
  }
}

// Format the date in a readable format
function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
}
</script>

<style scoped>
.card {
  border-radius: 0.5rem;
}

.card-header {
  font-size: 1.5rem;
  font-weight: bold;
}

textarea.form-control {
  resize: none;
  border-radius: 0.5rem;
}

button {
  border-radius: 0.5rem;
}

.card-title {
  margin-bottom: 0;
}
</style>
