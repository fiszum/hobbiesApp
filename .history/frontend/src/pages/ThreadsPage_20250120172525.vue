<template>
    <div class="threads-page">
      <h1>Threads</h1>
  
      <!-- Form to create a new thread -->
      <div class="new-thread-form">
        <textarea v-model="newThreadContent" placeholder="Write your thread..." rows="4" cols="50"></textarea>
        <button @click="createThread">Post Thread</button>
      </div>
  
      <!-- List of threads -->
      <div v-if="threads.length">
        <div v-for="thread in threads" :key="thread.id" class="thread">
          <div class="thread-header">
            <strong>{{ thread.user. }}</strong>
            <span>{{ formatDate(thread.created_at) }}</span>
          </div>
          <p>{{ thread.content }}</p>
        </div>
      </div>
      <div v-else>
        <p>No threads yet!</p>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useCsrfStore } from '../stores/csrf';
  
  const csrfStore = useCsrfStore();

  // Define types for thread and response
  interface Thread {
    id: number;
    user: {
      username: string;
    };
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
      console.log(csrfToken);
      const response = await fetch('/threads/', { // Replace with your API endpoint
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
        threads.value.push(createdThread); // Add the new thread to the list
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
  .threads-page {
    max-width: 600px;
    margin: auto;
    padding: 20px;
  }
  
  .new-thread-form {
    margin-bottom: 20px;
  }
  
  textarea {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
  }
  
  button {
    padding: 10px 20px;
    background-color: #219ebc;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #023047;
  }
  
  .thread {
    border-bottom: 1px solid #ccc;
    padding: 10px 0;
  }
  
  .thread-header {
    display: flex;
    justify-content: space-between;
    font-size: 0.9em;
    color: #555;
  }
  
  .thread-header strong {
    color: #219ebc;
  }
  </style>
  