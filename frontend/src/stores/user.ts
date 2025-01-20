
import { defineStore } from 'pinia';
import { ref } from 'vue';

interface Friend {
  username: string;
}

interface Hobby {
  id: number;
  name: string;
}

interface User {
  first_name: string;
  last_name: string;
  email: string;
  date_of_birth: string;
  hobbies: Hobby[];
  friends: Friend[];
}

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null);
  const allHobbies = ref<Hobby[]>([]);
  const isSaving = ref(false);
  const errorMessage = ref('');
  const successMessage = ref('');
  const newHobby = ref('');
  const editMode = ref(false);
  const passwordEditMode = ref(false);
  
  const baseUrl = "http://127.0.0.1:8000/";

  // Fetch user data
  const fetchUserData = async () => {
    try {
      const response = await fetch(baseUrl + 'currentuser/', {
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const userData = await response.json();
        user.value = userData;
        return userData;
      } else {
        console.error('Failed to fetch user data');
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  // Fetch all hobbies for all users
  const fetchAllHobbies = async () => {
    try {
      const response = await fetch(baseUrl + 'all-hobbies/', {
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const hobbiesData: Hobby[] = await response.json();
        const userHobbyIds = new Set(user.value?.hobbies.map(hobby => hobby.id));
        allHobbies.value = hobbiesData.filter(hobby => !userHobbyIds.has(hobby.id));
      } else {
        console.error('Failed to fetch hobbies');
      }
    } catch (error) {
      console.error('Error fetching hobbies:', error);
    }
  };

  // Add a hobby to user
  const addHobbyToUser = async (hobbyId: number) => {
    try {
      const csrfToken = getCSRFToken();
      const response = await fetch(baseUrl + 'add_single_hobby/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'include',
        body: JSON.stringify({ hobby_id: hobbyId }),
      });

      if (response.ok) {
        console.log('Hobby added');
        await fetchUserData();
      } else {
        const errorData = await response.json();
        console.error('Failed to add hobby:', errorData.error);
      }
    } catch (error) {
      console.error('Error adding hobby:', error);
    }
  };

  // Save user profile changes
  const saveChangesToUser = async (localFirstName: string, localLastName: string, localEmail: string, localDateOfBirth: string) => {
    if (isSaving.value) return;

    isSaving.value = true;
    try {
      const csrfToken = getCSRFToken();
      const response = await fetch(baseUrl + 'updateprofile/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'include',
        body: JSON.stringify({
          first_name: localFirstName,
          last_name: localLastName,
          email: localEmail,
          date_of_birth: localDateOfBirth,
        }),
      });

      if (response.ok) {
        user.value!.first_name = localFirstName;
        user.value!.last_name = localLastName;
        user.value!.email = localEmail;
        user.value!.date_of_birth = localDateOfBirth;
        editMode.value = false;
      } else {
        console.error('Failed to update profile');
      }
    } catch (error) {
      console.error('Error saving profile changes:', error);
    } finally {
      isSaving.value = false;
    }
  };

  // Change user password
  const changePassword = async (currentPassword: string, newPassword: string, confirmNewPassword: string) => {
    if (newPassword !== confirmNewPassword) {
      errorMessage.value = 'Passwords do not match';
      return;
    }

    try {
      const csrfToken = getCSRFToken();
      const response = await fetch(baseUrl + 'changepassword/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'include',
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });

      if (response.ok) {
        successMessage.value = 'Password changed successfully';
        passwordEditMode.value = false;
      } else {
        errorMessage.value = 'Failed to change password';
      }
    } catch (error) {
      console.error('Error changing password:', error);
      errorMessage.value = 'Error changing password';
    }
  };

  // Get CSRF token from cookies
  const getCSRFToken = () => {
    const csrfToken = document.cookie
      .split(';')
      .find(cookie => cookie.trim().startsWith('csrftoken='))
      ?.split('=')[1];
    return csrfToken || '';
  };

  return {
    user,
    allHobbies,
    isSaving,
    errorMessage,
    successMessage,
    newHobby,
    editMode,
    passwordEditMode,
    fetchUserData,
    fetchAllHobbies,
    addHobbyToUser,
    saveChangesToUser,
    changePassword,
    getCSRFToken,
  };
});
