<template>
  <div class="container mt-5">
    <h1 class="mb-4">Top 10 Users</h1>

    <!-- Filters -->
    <div class="mb-4">
      <label for="min-age" class="form-label">Min Age:</label>
      <input type="number" id="min-age" v-model="minAge" class="form-control mb-3" />

      <label for="max-age" class="form-label">Max Age:</label>
      <input type="number" id="max-age" v-model="maxAge" class="form-control mb-3" :min="1" @input="validateMaxAge" />

      <button @click="fetchTopUsers" class="btn btn-primary w-100">Submit</button>
    </div>

    <!-- Users Table -->
    <table class="table table-bordered table-striped mb-4">
      <thead>
        <tr>
          <th>#</th>
          <th>Username</th>
          <th>Action</th>
          <th>Similar Hobbies</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, index) in users" :key="user.id">
          <td>{{ index + 1 }}</td>
          <td>{{ user.username }}</td>
          <td>
            <button @click="sendFriendRequest(user.id)" class="btn btn-primary btn-sm">Add Friend</button>
          </td>
          <td>{{ user.common_hobby_count }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination Controls -->
    <div class="d-flex justify-content-between align-items-center">
      <button @click="changePage('prev')" :disabled="currentPage === 1" class="btn btn-secondary">
        Back
      </button>
      <span>Page {{ currentPage }}</span>
      <button @click="changePage('next')" :disabled="currentPage === totalPages" class="btn btn-secondary">
        Next
      </button>
    </div>

    <!-- Friend Requests Section -->
    <h2 class="mt-5 mb-4">Friend Requests</h2>
    <table class="table table-bordered table-striped">
      <thead>
        <tr>
          <th>#</th>
          <th>From</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(request, index) in friendRequests" :key="request.id">
          <td>{{ index + 1 }}</td>
          <td>{{ request.from_user.username }}</td>
          <td>
            <button @click="acceptFriendRequest(request.id)" class="btn btn-success btn-sm">Accept</button>
            <button @click="declineFriendRequest(request.id)" class="btn btn-danger btn-sm">Decline</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

/**
 * FriendsPage.vue
 * 
 * This component is responsible for displaying the top users and managing friend requests.
 * It fetches data from the server and handles user interactions such as sending, accepting,
 * and declining friend requests.
 * 
 * Data:
 * - users: List of top users.
 * - friendRequests: List of friend requests.
 * - currentPage: Current page number for pagination.
 * - totalPages: Total number of pages available.
 * - minAge: Minimum age filter for fetching top users.
 * - maxAge: Maximum age filter for fetching top users.
 * 
 * Methods:
 * - fetchTopUsers: Fetches the top users from the server based on the current page and age filters.
 * - changePage: Changes the current page and fetches the top users for the new page.
 * - validateMaxAge: Ensures the max age is not set to 0.
 * - fetchFriendRequests: Fetches the list of friend requests from the server.
 * - sendFriendRequest: Sends a friend request to a user.
 * - acceptFriendRequest: Accepts a friend request.
 * - declineFriendRequest: Declines a friend request.
 * 
 * Lifecycle Hooks:
 * - onMounted: Fetches the top users and friend requests when the component is mounted.
 */
<script lang="ts">
import { ref, onMounted } from "vue";
import { useCsrfStore } from "../stores/csrf";

interface User {
  id: number;
  username: string;
  common_hobby_count: number;
}

interface FriendRequest {
  id: number;
  from_user: {
    username: string;
  };
}

export default {
  name: "TopUsers",
  setup() {
    const csrfStore = useCsrfStore();

    const users = ref<User[]>([]);
    const friendRequests = ref<FriendRequest[]>([]);
    const currentPage = ref(1);
    const totalPages = ref(1);
    const minAge = ref<number | null>(null);
    const maxAge = ref<number | null>(null);

    // Fetch top users
    const fetchTopUsers = async () => {
      console.log(minAge.value, maxAge.value);

      try {
        // Get the CSRF token
        const csrfToken = csrfStore.csrfToken;
        if (!csrfToken) {
          console.error("CSRF token not found");
          return;
        }
        const response = await fetch("/top-users/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken, // Include CSRF token in headers
          },
          body: JSON.stringify({
            page: currentPage.value,
            min_age: minAge.value || 0,
            max_age: maxAge.value || 200,
          }),
          credentials: "include", // Ensure session cookies are sent
        });

        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }
        const data = await response.json();
        users.value = data.users;
        totalPages.value = data.total_pages;
      } catch (error) {
        console.error("Error fetching top users:", error);
      }
    };

    // Change page
    const changePage = (direction: string) => {
      if (direction === "next" && currentPage.value < totalPages.value) {
        currentPage.value++;
      } else if (direction === "prev" && currentPage.value > 1) {
        currentPage.value--;
      }
      fetchTopUsers(); // Fetch data for the new page
    };

    const validateMaxAge = () => {
      if (maxAge.value === 0) {
        maxAge.value = 1; // Automatically reset to 1 if 0 is entered
      }
    };

    // Fetch friend requests
    const fetchFriendRequests = async () => {
      try {
        const response = await fetch("/get-friend-requests/", {
          credentials: "include", // Ensure session cookies are sent
        });
        if (!response.ok) {
          throw new Error("Failed to fetch friend requests");
        }
        friendRequests.value = await response.json();
      } catch (error) {
        console.error("Error fetching friend requests:", error);
      }
    };

    // Send a friend request
    const sendFriendRequest = async (userId: number) => {
      const csrfToken = csrfStore.csrfToken;
      try {
        const response = await fetch("/send-friend-request/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({ to_user_id: userId }),
          credentials: "include",
        });
        if (response.ok) {
          alert("Friend request sent!");
        } else {
          console.error("Failed to send friend request");
        }
      } catch (error) {
        console.error("Error sending friend request:", error);
      }
    };

    // Accept a friend request
    const acceptFriendRequest = async (requestId: number) => {
      const csrfToken = csrfStore.csrfToken;
      try {
        const response = await fetch(`/accept-friend-request/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({ request_id: requestId }),
          credentials: "include",
        });
        if (response.ok) {
          alert("Friend request accepted!");
          fetchFriendRequests(); // Refresh the friend requests
        } else {
          console.error("Failed to accept friend request");
        }
      } catch (error) {
        console.error("Error accepting friend request:", error);
      }
    };

    // Decline a friend request
    const declineFriendRequest = async (requestId: number) => {
      const csrfToken = csrfStore.csrfToken;
      try {
        const response = await fetch(`/decline-friend-request/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({ request_id: requestId }),
          credentials: "include",
        });
        if (response.ok) {
          alert("Friend request declined!");
          fetchFriendRequests(); // Refresh the friend requests
        } else {
          console.error("Failed to decline friend request");
        }
      } catch (error) {
        console.error("Error declining friend request:", error);
      }
    };

    onMounted(() => {
      fetchTopUsers();
      fetchFriendRequests();
    });

    return {
      users,
      friendRequests,
      sendFriendRequest,
      acceptFriendRequest,
      declineFriendRequest,
      currentPage,
      totalPages,
      changePage,
      minAge,
      maxAge,
      fetchTopUsers,
      validateMaxAge,
    };
  },
};
</script>

<style scoped>
/* Add some padding and margins to avoid clutter */
.container {
  max-width: 800px;
}

/* Space between form fields */
.form-label {
  font-weight: bold;
}

.mb-3 {
  margin-bottom: 15px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  border: 1px solid #ddd;
  padding: 12px;
}

.table th {
  background-color: #f8f9fa;
  text-align: left;
}

.table-bordered {
  border: 1px solid #dee2e6;
}

.btn {
  font-weight: bold;
}

.w-100 {
  width: 100%;
}

.d-flex {
  display: flex;
}

.justify-content-between {
  justify-content: space-between;
}

.align-items-center {
  align-items: center;
}

.mt-5 {
  margin-top: 30px;
}

.mt-4 {
  margin-top: 20px;
}

.mb-4 {
  margin-bottom: 20px;
}
</style>
