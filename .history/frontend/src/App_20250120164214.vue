<template>
    <main class="container pt-4">
        <nav class="navbar navbar-expand-lg navbar-light bg-light rounded shadow-sm mb-4">
            <div class="container-fluid">
                <router-link class="navbar-brand fw-bold" :to="{name: 'Main Page'}">CatBook</router-link>
                <button 
                    class="navbar-toggler" 
                    type="button" 
                    data-bs-toggle="collapse" 
                    data-bs-target="#navbarNav" 
                    aria-controls="navbarNav" 
                    aria-expanded="false" 
                    aria-label="Toggle navigation"
                >
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item">
                            <router-link 
                                class="nav-link" 
                                :to="{name: 'Main Page'}"
                            >
                                Main Page
                            </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link 
                                class="nav-link" 
                                :to="{name: 'Other Page'}"
                            >
                                Friends
                            </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link 
                                class="nav-link" 
                                :to="{name: 'Profile Page'}"
                            >
                                Profile Page
                            </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link 
                                class="nav-link" 
                                :to="{name: 'Threads Page'}"
                            >
                                Threads Page
                            </router-link>
                        </li>
                        <!-- Logout Button -->
                        <li class="nav-item">
                            <button 
                                class="nav-link logout-btn" 
                                @click="logout"
                            >
                                Logout
                            </button>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { RouterView } from "vue-router";
import { useCsrfStore } from "./stores/csrf";

export default defineComponent({
    components: { RouterView },
    setup() {
        const csrfStore = useCsrfStore();

        // Initialize the CSRF token on app load
        onMounted(() => {
            csrfStore.initializeCsrfToken();
        });



        const logout = async () => {
            try {
                const csrfToken = csrfStore.csrfToken;
                const response = await fetch("/logout/", {
                    method: "POST", // Use POST for logout if required
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken,
                        
                    },
                    credentials: "include", // Include session cookies
                });

                if (response.ok) {
                    console.log("this is working")
                    // Redirect to login page
                    window.location.href = "/accounts/login/";
                } else {
                    console.error("Failed to log out:", response.statusText);
                }
            } catch (error) {
                console.error("Logout error:", error);
            }
        };



        return {
            logout,
        };
    },
});
</script>

<style scoped>
.navbar {
    background-color: #8ECAE6; 
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
}

.nav-link {
    font-size: 1.1rem;
    color: #023047 !important; 
    transition: color 0.3s ease-in-out;
}

.nav-link:hover {
    color: #FB8500 !important; 
    text-decoration: underline;
}

.navbar-brand {
    color: #219EBC !important; 
    font-size: 1.5rem;
}

.navbar-toggler {
    border-color: #023047;
}

.navbar-toggler-icon {
    background-color: #023047;
}

.logout-btn {
    background-color: #FF4D4D; /* Red background */
    color: white; /* White text */
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 0.25rem; /* Rounded corners */
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease-in-out;
}

.logout-btn:hover {
    background-color: #FF0000; /* Darker red on hover */
    text-decoration: none; /* Remove underline */
}

.logout-btn:focus {
    outline: none; /* Remove focus outline */
    box-shadow: 0 0 5px rgba(255, 77, 77, 0.75); /* Focus glow */
}

.jumbotron {
    background-color: #F5F5F5;
    padding: 4rem;
    margin-bottom: 3rem;
    border-radius: 1rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.jumbotron h1 {
    font-size: 3rem;
    color: #219EBC;
}

.jumbotron p {
    font-size: 1.2rem;
    color: #023047;
}

.jumbotron hr {
    border-color: #8ECAE6;
    width: 50px;
    margin-top: 2rem;
    margin-bottom: 2rem;
}

.jumbotron .btn {
    background-color: #FFB703;
    border-radius: 50px;
    padding: 0.75rem 2rem;
    font-size: 1.25rem;
    transition: background-color 0.3s ease-in-out;
}

.jumbotron .btn:hover {
    background-color: #FB8500;
}
</style>
