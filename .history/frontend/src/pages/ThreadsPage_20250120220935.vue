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
</script>
