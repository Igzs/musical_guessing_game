<template>
    <div>
      <h1>Musical guessing game</h1>
      <p>{{ backendData }}</p>
      <button @click="loginWithSpotify">Login with Spotify</button> <!-- The login button -->
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue';
  import axios from 'axios';
  
  export default defineComponent({
    name: 'HomePage',
    setup() {
      const backendData = ref(''); // Initialize data property
  
      const fetchData = async () => {
        try {
          const response = await axios.get('http://localhost:8000/');
          backendData.value = response.data; // Update the data property with the response
        } catch (error) {
          console.error("There was an error fetching the data!", error);
        }
      };

      const loginWithSpotify = () => {
      const clientId = import.meta.env.VITE_SPOTIFY_CLIENT_ID; // Accessing the client ID from environment variables      
      const responseType = 'code';
      // Ensure this URI is URL-encoded and matches the redirect URI registered in your Spotify application
      const redirectUri = encodeURIComponent('http://localhost:8000/callback');
      const scope = encodeURIComponent('user-read-private user-read-email user-read-recently-played user-top-read');
      const state = generateRandomString(16); // Implement this method to generate a random string
      localStorage.setItem("spotify_auth_state", state); // Store state
      const spotifyUrl = `https://accounts.spotify.com/authorize?response_type=${responseType}&client_id=${clientId}&scope=${scope}&redirect_uri=${redirectUri}&state=${state}`;

      window.location.href = spotifyUrl; // Redirect the user
    };

    function generateRandomString(length: any) {
      let result = '';
      const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      const charactersLength = characters.length;
      for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
      }
      return result;

    
    }
  
      return { backendData, fetchData, loginWithSpotify };
    },
    mounted() {
      this.fetchData(); // Call fetchData when the component mounts
    },
  });
  </script>
  