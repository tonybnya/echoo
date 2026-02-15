<template>
  <div class="min-h-screen bg-[#030712] text-white p-8">
    <div class="max-w-4xl mx-auto flex justify-between items-center mb-8 border-b border-gray-800 pb-4">
      <h1 class="text-3xl font-bold tracking-tight">Chat</h1>
      <div class="flex items-center gap-4">
        <span class="text-gray-400">Logged in as: <span class="text-blue-400 font-medium">{{ username }}</span></span>
        <button 
          @click="logout"
          class="cursor-pointer px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-semibold rounded-lg transition-colors shadow-lg active:scale-95"
        >
          Logout
        </button>
      </div>
    </div>
    
    <div class="bg-[#0b101f] rounded-2xl border border-gray-800 p-8 shadow-2xl">
      <p class="text-gray-400 text-center italic">Select a conversation to start messaging</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');

onMounted(() => {
  username.value = localStorage.getItem('username') || 'Guest';
});

const logout = () => {
  localStorage.removeItem('authToken');
  localStorage.removeItem('username');
  router.push('/auth');
};
</script>

<style scoped>
</style>