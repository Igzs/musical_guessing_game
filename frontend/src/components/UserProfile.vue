<template>
    <div>
      <h1>Welcome, {{ userProfile }}</h1>
      <button @click="logout">Logout</button>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, onMounted, ref } from 'vue';
  import axios from 'axios';
import router from '@/router';
  
  export default defineComponent({
    name: 'UserProfile',
    setup() {
      const userProfile = ref(''); // Initialize data property
  
      // Correctly define the async function within setup()
      const fetchUserData = async () => {
        try {
          const response = await axios.get('http://localhost:8000/user', {withCredentials: true});
          // Assuming the response data has a property you want to display
          // e.g., response.data.name if the API response includes { "name": "User Name" }
          userProfile.value = response.data.display_name; // Update the ref with the response
        } catch (error) {
          console.error("There was an error fetching the user data!", error);
        }
      };
      const logout = async () => {
      try {
        const response = await axios.get('http://localhost:8000/logout', { withCredentials: true });
        if (response.data.message === "Logged out successfully") {
          router.push('/');
        }
      } catch (error) {
        console.error("There was an error logging out!", error);
      }
    };


  
      // Use onMounted lifecycle hook within setup() to call fetchUserData
      onMounted(() => {
        fetchUserData();
      });
  
      return { userProfile, logout };
    },
  });
  </script>
  