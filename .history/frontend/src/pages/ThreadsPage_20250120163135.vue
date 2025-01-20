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
            <strong>{{ thread.user.username }}</strong>
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
  
  <script>
  export default {
    data() {
      return {
        threads: [], // List of threads to be fetched from the backend
        newThreadContent: "", // New thread content from the user
      };
    },
    created() {
      this.fetchThreads(); // Fetch threads when the component is created
    },
    methods: {
      // Fetch threads from the backend (Django API)
      async fetchThreads() {
        try {
          const response = await fetch("/api/threads/"); // Replace with your API endpoint
          const data = await response.json();
          this.threads = data; // Store threads in the component's data
        } catch (error) {
          console.error("Error fetching threads:", error);
        }
      },
  
      // Create a new thread
      async createThread() {
        if (!this.newThreadContent.trim()) {
          return; // Don't post if content is empty
        }
  
        const newThread = {
          content: this.newThreadContent,
        };
  
        try {
          const response = await fetch("/api/threads/", { // Replace with your API endpoint
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              
            },
            body: JSON.stringify(newThread),
          });
  
          if (response.ok) {
            const createdThread = await response.json();
            this.threads.push(createdThread); // Add the new thread to the list
            this.newThreadContent = ""; // Clear the input
          } else {
            console.error("Error creating thread:", response.statusText);
          }
        } catch (error) {
          console.error("Error creating thread:", error);
        }
      },
  
      // Format the date in a readable format
      formatDate(dateString) {
        const date = new Date(dateString);
        return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
      },
    },
  };
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
  