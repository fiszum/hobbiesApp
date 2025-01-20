<template>
  <div class="container py-5">
    <h1 class="text-center mb-4">Profile Page</h1>

    <div v-if="user">
      <!-- Profile Display Section -->
      <div v-if="!editMode" class="card p-4 shadow">
        <h3 class="mb-3">Profile Information</h3>
        <p><strong>First Name:</strong> {{ user.first_name }}</p>
        <p><strong>Last Name:</strong> {{ user.last_name }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Date of Birth:</strong> {{ user.date_of_birth }}</p>

        <button class="btn btn-primary mt-3" @click="editMode = true">Edit Profile</button>
      </div>

      <!-- Profile Edit Form -->
      <div v-else class="card p-4 shadow">
        <h3 class="mb-3">Edit Profile</h3>
        <form @submit.prevent="saveChangesToUser" :disabled="isSaving">
          <div class="mb-3">
            <label for="first_name" class="form-label">First Name:</label>
            <input
              v-model="localFirstName"
              id="first_name"
              type="text"
              class="form-control"
            />
          </div>
          <div class="mb-3">
            <label for="last_name" class="form-label">Last Name:</label>
            <input
              v-model="localLastName"
              id="last_name"
              type="text"
              class="form-control"
            />
          </div>
          <div class="mb-3">
            <label for="email" class="form-label">Email:</label>
            <input
              v-model="localEmail"
              id="email"
              type="email"
              class="form-control"
            />
          </div>
          <div class="mb-3">
            <label for="date_of_birth" class="form-label">Date of Birth:</label>
            <input
              v-model="localDateOfBirth"
              id="date_of_birth"
              type="date"
              class="form-control"
            />
          </div>
          <div class="d-flex gap-2">
            <button type="submit" class="btn btn-success" :disabled="isSaving">Save Changes</button>
            <button class="btn btn-secondary" @click="editMode = false" type="button">Cancel</button>
          </div>
        </form>
      </div>

      <!-- Password Change Section -->
      <div class="card p-4 shadow mt-4">
        <h3 class="mb-3">Change Password</h3>
        <div v-if="!passwordEditMode">
          <button class="btn btn-warning" @click="passwordEditMode = true">Change Password</button>
        </div>
        <div v-else>
          <form @submit.prevent="changePassword">
            <div class="mb-3">
              <label for="current_password" class="form-label">Current Password:</label>
              <input
                v-model="currentPassword"
                id="current_password"
                type="password"
                class="form-control"
              />
            </div>
            <div class="mb-3">
              <label for="new_password" class="form-label">New Password:</label>
              <input
                v-model="newPassword"
                id="new_password"
                type="password"
                class="form-control"
              />
            </div>
            <div class="mb-3">
              <label for="confirm_new_password" class="form-label">Confirm New Password:</label>
              <input
                v-model="confirmNewPassword"
                id="confirm_new_password"
                type="password"
                class="form-control"
              />
            </div>
            <div class="d-flex gap-2">
              <button type="submit" class="btn btn-success">Save New Password</button>
              <button class="btn btn-secondary" @click="passwordEditMode = false" type="button">Cancel</button>
            </div>
          </form>
        </div>
      </div>

      <!-- All Hobbies Section -->
      <div class="card p-4 shadow mt-4">
        <h3 class="mb-3">Hobbies that other users have</h3>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Hobby Name</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(hobby, index) in allHobbies"
              :key="index"
            >
              <td>{{ hobby.name }}</td>
              <td>
                <button 
                  class="btn btn-secondary btn-sm"
                  @click="addHobbyToUser(hobby.id)"
                >
                  Add to my hobbies
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>



      <!-- Hobbies Section -->
      <div class="card p-4 shadow mt-4">
        <h3 class="mb-3">Your Hobbies</h3>
        <ul class="list-group mb-3">
          <li
            v-for="(hobby, index) in user.hobbies"
            :key="index"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            {{ hobby.name }}
            <button class="btn btn-danger btn-sm" @click="removeHobby(index)">Remove</button>
          </li>
        </ul>
        <div class="input-group">
          <input
            v-model="newHobby"
            type="text"
            placeholder="Add a new hobby"
            class="form-control"
          />
          <button class="btn btn-primary" @click="addHobby">Add Hobby</button>
        </div>
      </div>

      <!-- Friends Section -->
      <div class="card p-4 shadow mt-4">
        <h3 class="mb-3">Friends</h3>
        <ul class="list-group">
          <li
            v-for="(friend, index) in user.friends"
            :key="index"
            class="list-group-item"
          >
            {{ friend.username }} 
          </li>
        </ul>
      </div>
    </div>

    <div v-else class="text-center">
      <p>Loading user data...</p>
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useAuthStore } from "../stores/auth";
import { useCsrfStore } from "../stores/csrf";

const authStore = useAuthStore(); // Use Pinia store for global state
const csrfStore = useCsrfStore();


interface Friend {
  username: string; // Define the structure of a friend object
}

interface User {
  first_name: string;
  last_name: string;
  email: string;
  date_of_birth: string;
  hobbies: { id: number; name: string }[];
  friends: Friend[];
}

const user = ref<User | null>(null); // Ref to hold user data
const newHobby = ref(""); // Ref for the new hobby input
const editMode = ref(false); // Control the visibility of the edit form
const passwordEditMode = ref(false); // Control password edit mode
const isSaving = ref(false); // To disable save button while saving changes

const currentPassword = ref("");
const newPassword = ref("");
const confirmNewPassword = ref("");
const successMessage = ref("");
const errorMessage = ref("");

const allHobbies = ref<Hobby[]>([]);  // Stores all hobbies across users

interface Hobby {
  id: number;
  name: string;
}

// Local state for the form inputs
const localFirstName = ref("");
const localLastName = ref("");
const localEmail = ref("");
const localDateOfBirth = ref("");



onMounted(async () => {
  try {
    // Fetch user data
    console.log('Sending request to fetch user data...');
    const response = await fetch("/currentuser/", {
      credentials: "include", // Include cookies for session
      headers: {
        "Content-Type": "application/json",
      },
    });
  
  console.log('Response status:', response.status);
  console.log('Response ok:', response.ok);
    if (response.ok) {
      const userData = await response.json();
      console.log('Fetched user data:', userData);
      user.value = userData; // Set local user data
      // Initialize local variables for form inputs with user data
      localFirstName.value = userData.first_name;
      localLastName.value = userData.last_name;
      localEmail.value = userData.email;
      localDateOfBirth.value = userData.date_of_birth;
      

      // Fetch the list of all hobbies for all users
     // Fetch the list of all hobbies for all users
    const allHobbiesResponse = await fetch("/all-hobbies/", {
        credentials: "include", // Include cookies for session
      });

      if (allHobbiesResponse.ok) {
        const hobbiesData: Hobby[] = await allHobbiesResponse.json(); // Ensure the data is typed as Hobby[]

        // Extract the user's current hobbies' IDs into a Set
        const userHobbyIds = new Set(user.value?.hobbies.map((hobby: Hobby) => hobby.id));

        // Filter out hobbies that the user already has
        allHobbies.value = hobbiesData.filter((hobby: Hobby) => !userHobbyIds.has(hobby.id));
      } else {
        const errorData = await allHobbiesResponse.json(); // Log the error response for better debugging
        console.error("Failed to fetch hobbies data:", errorData);
      }

      // Fetch the user's friends
      const friendsResponse = await fetch("/get-friends/", {
        credentials: "include", // Include cookies for session
      });
      if (friendsResponse.ok) {
        const friendsData = await friendsResponse.json();
        console.log('Fetched friends data:', friendsData);
        user.value!.friends = friendsData; // Set friends data (user.value is not null here)
      } else {
        console.error("Failed to fetch friends data");
      }

      authStore.setUser(userData); // Update the Pinia store with user data
    } else {
      console.error('Failed to fetch user data. Response:', response);
    const errorText = await response.text();
    console.error('Error body:', errorText);  // Log the error body
    }
  } catch (error) {
      console.error("Error fetching user data:", error);
  }
});

// Function to save the edited user data
const saveChangesToUser = async () => {
  if (isSaving.value) return; // Prevent multiple submissions
  isSaving.value = true; // Set saving flag

  try {
    if (!user.value) {
      console.error("No user data to update");
      return;
    }
    const csrfToken = csrfStore.csrfToken;



    const response = await fetch("/updateprofile/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      credentials: "include", // Include cookies for session
      body: JSON.stringify({
        first_name: localFirstName.value,
        last_name: localLastName.value,
        email: localEmail.value,
        date_of_birth: localDateOfBirth.value,
      }),
    });

    if (!response.ok) {
      console.error("Failed to update profile");
    } else {
      // Update local user data after saving
      user.value.first_name = localFirstName.value;
      user.value.last_name = localLastName.value;
      user.value.email = localEmail.value;
      user.value.date_of_birth = localDateOfBirth.value;
      editMode.value = false; // Close the edit form
    }
  } catch (error) {
    console.error("Error saving profile changes:", error);
  } finally {
    isSaving.value = false; // Reset saving flag
  }
};
const addHobbyToUser = async (hobbyId: number) => {
  try {
    const csrfToken = csrfStore.csrfToken;
    const response = await fetch("/add_single_hobby/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({ hobby_id: hobbyId }),
      credentials: "include", // Include cookies for session authentication
    });

    if (response.ok) {
      console.log("Hobby added successfully");

      // Temporarily store current friends to prevent overwriting
      const currentFriends = user.value?.friends || [];

      // Fetch updated user data
      await fetchUserData();

      // Restore the friends list to the updated user object
      if (user.value) {
        user.value.friends = currentFriends;
      }
    } else {
      const errorData = await response.json();
      console.error("Failed to add hobby:", errorData.error);
      alert(`Error: ${errorData.error}`);
    }
  } catch (error) {
    console.error("Error adding hobby:", error);
    alert("An error occurred while adding the hobby.");
  }
};


// Function to add a new hobby
const addHobby = () => {
  if (newHobby.value.trim()) {
    user.value?.hobbies.push({ id: Date.now(), name: newHobby.value.trim() });
    newHobby.value = ""; // Clear the input after adding
    updateUserHobby(); // Sync with the backend
  }
};

// Function to remove a hobby by index
const removeHobby = (index: number) => {
  user.value?.hobbies.splice(index, 1);
  updateUserHobby(); // Sync with the backend
};

// Function to sync hobbies with the backend
const updateUserHobby = async () => {
  if (user.value) {
    try {
      const csrfToken = csrfStore.csrfToken;
      await fetch("/updatehobbies/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        credentials: "include", // Include cookies for session
        body: JSON.stringify({ hobbies: user.value.hobbies }),
      });

      // Fetch updated user data, retaining friends
      const currentFriends = user.value?.friends || [];
      await fetchUserData();
      if (user.value) {
        user.value.friends = currentFriends;
      }
    } catch (error) {
      console.error("Error updating hobbies:", error);
    }
  }
};

// Function to handle password change
const changePassword = async () => {
  if (newPassword.value !== confirmNewPassword.value) {
    errorMessage.value = "Passwords do not match!";
    return;
  }

  try {
    const csrfToken = csrfStore.csrfToken;
    const response = await fetch("/changepassword/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      credentials: "include", // Include cookies for session
      body: JSON.stringify({
        current_password: currentPassword.value,
        new_password: newPassword.value,
      }),
    });

    if (response.ok) {
      successMessage.value = "Password changed successfully!";
      passwordEditMode.value = false; // Close the password change form
    } else {
      errorMessage.value = "Failed to change password";
    }
  } catch (error) {
    console.error("Error changing password:", error);
    errorMessage.value = "Error changing password";
  }
};

const fetchUserData = async () => {
  try {
    // Fetch the current user's data
    const response = await fetch("/currentuser/", {
      credentials: "include", // Include cookies for session
    });

    if (response.ok) {
      const userData = await response.json();
      user.value = userData;

      // Extract the user's current hobbies' IDs into a Set
      const userHobbyIds = new Set(userData.hobbies.map((hobby: Hobby) => hobby.id));

      // Fetch all hobbies for all users
      const allHobbiesResponse = await fetch("/all-hobbies/", {
        credentials: "include", // Include cookies for session
      });

      if (allHobbiesResponse.ok) {
        const hobbiesData: Hobby[] = await allHobbiesResponse.json();

        // Filter out hobbies that the user already has
        allHobbies.value = hobbiesData.filter((hobby: Hobby) => !userHobbyIds.has(hobby.id));
      } else {
        const errorData = await allHobbiesResponse.json();
        console.error("Failed to fetch hobbies data:", errorData);
      }
    } else {
      console.error("Failed to fetch user data");
    }
  } catch (error) {
    console.error("Error fetching user data:", error);
  }
};


</script>
