<template>
  <!-- Landing Page -->
  <div class="jumbotron bg-light p-5 rounded shadow-lg text-center">
    <h1 class="display-4 fw-bold" style="color: #219EBC;">Welcome to CatBook!</h1>
    <p class="lead mt-3" style="color: #023047;">
        Your one-stop platform to connect with friends and share your favorite moments.
    </p>
    <hr class="my-4" style="border-color: #8ECAE6;" />
    <p class="mb-4" style="color: #FB8500;">
        Explore profiles, make new connections, and enjoy a seamless user experience.
    </p>
</div>
</template>

/**
 * MainPage.vue
 * 
 * This component represents the main page of the application.
 * 
 * Data:
 * - title: A string representing the title of the page, initialized to "Main Page".
 * 
 * Usage:
 * This component can be used as the main entry point for the application's user interface.
 */
<script lang="ts">
    import { defineComponent } from "vue";

    export default defineComponent({
        data() {
            return {
                title: "Main Page",
            }
        }
    })
</script>

<style scoped>
</style>
