<template>
  <div class="h-screen flex flex-col bg-white text-black font-sans">
    <!-- Header -->
    <header class="bg-black text-white px-6 py-4 flex justify-between items-center shadow-md">
      <div class="flex items-center gap-3">
        <h2 class="text-lg font-bold">Share the page URL to invite new friends</h2>
      </div>
      <div class="flex items-center gap-4">
        <span class="hidden sm:inline opacity-90">Logged in as: <span class="font-bold text-yellow-400 animate-pulse decoration-2 underline-offset-4">{{ username }}</span></span>
        <button 
          @click="logout"
          class="cursor-pointer px-4 py-1.5 bg-red-700 border border-white/20 hover:bg-gray-900 text-white text-xs font-bold rounded transition-all active:scale-95"
        >
          Logout
        </button>
      </div>
    </header>

    <!-- Chat Messages -->
    <main class="flex-1 overflow-y-auto p-4 md:p-8 bg-gray-50 flex flex-col gap-6" ref="messageContainer">
      <div v-if="loading" class="flex-1 flex items-center justify-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-red-700"></div>
      </div>
      
      <div v-else-if="!uri" class="flex-1 flex items-center justify-center text-gray-500 italic">
        No active chat session. Start one from the home page.
      </div>

      <template v-else>
        <div v-for="(msg, index) in messages" :key="index" 
          :class="['flex gap-3 max-w-[85%] lg:max-w-[70%]', msg.user.username === username ? 'ml-auto flex-row-reverse' : '']">
          
          <!-- Avatar -->
          <div :class="['w-10 h-10 rounded-full flex items-center justify-center text-white font-bold shrink-0 shadow-sm', 
            msg.user.username === username ? 'bg-black' : 'bg-red-600']">
            {{ msg.user.username.charAt(0).toUpperCase() }}
          </div>

          <!-- Message Bubble -->
          <div class="flex flex-col gap-1">
            <div :class="['px-5 py-3 rounded-2xl relative shadow-sm text-[15px] leading-relaxed', 
              msg.user.username === username 
                ? 'bg-black text-white rounded-tr-none' 
                : 'bg-white border border-gray-200 text-gray-800 rounded-tl-none']">
              {{ msg.message }}
              
              <!-- Tail (Custom CSS below) -->
              <div :class="['absolute top-0 w-3 h-3', 
                msg.user.username === username 
                  ? '-right-1.5 bg-black clip-path-right' 
                  : '-left-1.5 bg-white border-l border-t border-gray-200 clip-path-left']">
              </div>
            </div>
            <span class="text-[10px] text-gray-400 mt-1" :class="msg.user.username === username ? 'text-right' : ''">
              {{ formatTime(msg.created_at) }}
            </span>
          </div>
        </div>
      </template>
    </main>

    <!-- Input Footer -->
    <footer class="p-4 bg-white border-t border-gray-200">
      <form @submit.prevent="sendMessage" class="max-w-4xl mx-auto flex gap-3">
        <input 
          v-model="newMessage"
          type="text"
          placeholder="Type a message"
          class="flex-1 px-4 py-3 bg-gray-50 border border-gray-200 rounded-md focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
          :disabled="!uri"
        />
        <button 
          type="submit"
          class="cursor-pointer px-8 py-3 bg-yellow-400 hover:bg-yellow-500 text-black font-bold rounded-md shadow-md transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="!newMessage.trim() || !uri"
        >
          Send
        </button>
      </form>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
const username = ref('');
const messages = ref([]);
const newMessage = ref('');
const loading = ref(true);
const uri = ref(route.params.uri);
const messageContainer = ref(null);
let pollingInterval = null;

const fetchMessages = async () => {
  if (!uri.value) return;
  try {
    const response = await fetch(`http://localhost:8000/api/chats/${uri.value}/messages/`, {
      headers: {
        'Authorization': `Token ${localStorage.getItem('authToken')}`
      }
    });
    if (response.ok) {
      const data = await response.json();
      if (data.messages.length !== messages.value.length) {
        messages.value = data.messages;
        await scrollToBottom();
      }
    }
  } catch (error) {
    console.error('Error fetching messages:', error);
  } finally {
    loading.value = false;
  }
};

const joinSession = async () => {
  if (!uri.value) {
    loading.value = false;
    return;
  }
  try {
    await fetch(`http://localhost:8000/api/chats/${uri.value}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${localStorage.getItem('authToken')}`
      },
      body: JSON.stringify({ username: username.value })
    });
    await fetchMessages();
  } catch (error) {
    console.error('Error joining session:', error);
    loading.value = false;
  }
};

const sendMessage = async () => {
  if (!newMessage.value.trim() || !uri.value) return;
  const text = newMessage.value;
  newMessage.value = '';
  
  try {
    const response = await fetch(`http://localhost:8000/api/chats/${uri.value}/messages/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${localStorage.getItem('authToken')}`
      },
      body: JSON.stringify({ message: text })
    });
    if (response.ok) {
      await fetchMessages();
    }
  } catch (error) {
    console.error('Error sending message:', error);
  }
};

const scrollToBottom = async () => {
  await nextTick();
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
  }
};

const formatTime = (isoString) => {
  return new Date(isoString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const logout = () => {
  localStorage.removeItem('authToken');
  localStorage.removeItem('username');
  router.push('/auth');
};

onMounted(async () => {
  username.value = localStorage.getItem('username') || 'Guest';
  await joinSession();
  pollingInterval = setInterval(fetchMessages, 3000);
});

onUnmounted(() => {
  if (pollingInterval) clearInterval(pollingInterval);
});

watch(() => route.params.uri, (newUri) => {
  uri.value = newUri;
  if (newUri) {
    loading.value = true;
    joinSession();
  }
});
</script>

<style scoped>
.clip-path-right {
  clip-path: polygon(0 0, 0 100%, 100% 0);
}
.clip-path-left {
  clip-path: polygon(100% 0, 100% 100%, 0 0);
}
</style>