<template>
  <div class="h-screen flex flex-col bg-white text-black font-sans">
    <!-- Header -->
    <header class="bg-black text-white px-6 py-4 flex justify-between items-center shadow-md">
      <div class="flex items-center gap-3">
        <div v-if="uri" class="flex items-center gap-3">
          <button 
            @click="shareSession"
            class="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 border border-white/20 rounded-md text-sm transition-all active:scale-95 group relative"
            title="Copy chat link to invite friends"
          >
            <i class="fa-solid fa-share-nodes text-yellow-400"></i>
            <span class="font-bold">Invite Friends</span>
            
            <!-- Tooltip -->
            <transition name="fade">
              <div v-if="isCopied" class="absolute -bottom-10 left-1/2 -translate-x-1/2 px-3 py-1 bg-yellow-400 text-black text-[11px] font-bold rounded shadow-xl whitespace-nowrap z-50">
                Link copied!
              </div>
            </transition>
          </button>
        </div>
        <h2 v-else class="text-lg font-bold text-gray-400 italic">No active session</h2>
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
      
      <div v-else-if="!uri" class="flex-1 flex flex-col items-center justify-center text-center p-6">
        <p class="text-gray-600 mb-8 max-w-md">
          To start chatting with friends click on the button below, it'll start a new chat session
          and then you can invite your friends over to chat!
        </p>
        <button 
          @click="startChatSession" 
          class="cursor-pointer px-8 py-3 bg-black hover:bg-gray-900 text-white font-bold rounded-md shadow-lg transition-all active:scale-95"
        >
          Start Chatting
        </button>
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
const isCopied = ref(false);
const socket = ref(null);
const userId = ref(null);

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
      messages.value = data.messages;
      await scrollToBottom();
    }
  } catch (error) {
    console.error('Error fetching messages:', error);
  } finally {
    loading.value = false;
  }
};

const connectWebSocket = () => {
  if (socket.value) {
    socket.value.close();
  }

  const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
  const wsUrl = `${wsScheme}://localhost:8000/ws/chats/${uri.value}/`;
  
  socket.value = new WebSocket(wsUrl);

  socket.value.onmessage = (event) => {
    const data = JSON.parse(event.data);
    messages.value.push(data.message);
    scrollToBottom();
  };

  socket.value.onclose = () => {
    console.log('WebSocket disconnected. Retrying in 3 seconds...');
    setTimeout(connectWebSocket, 3000);
  };

  socket.value.onerror = (error) => {
    console.error('WebSocket error:', error);
    socket.value.close();
  };
};

const joinSession = async () => {
  if (!uri.value) {
    loading.value = false;
    return;
  }
  try {
    const response = await fetch(`http://localhost:8000/api/chats/${uri.value}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${localStorage.getItem('authToken')}`
      },
      body: JSON.stringify({ username: username.value })
    });
    if (response.ok) {
      const data = await response.json();
      userId.value = data.user.id;
    }
    await fetchMessages();
    connectWebSocket();
  } catch (error) {
    console.error('Error joining session:', error);
    loading.value = false;
  }
};

const sendMessage = async () => {
  if (!newMessage.value.trim() || !uri.value || !socket.value) return;
  const text = newMessage.value;
  newMessage.value = '';
  
  socket.value.send(JSON.stringify({
    'message': text,
    'user_id': userId.value
  }));
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

const startChatSession = async () => {
  loading.value = true;
  try {
    const response = await fetch('http://localhost:8000/api/chats/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${localStorage.getItem('authToken')}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to create chat session');
    }

    const data = await response.json();
    router.push(`/chats/${data.uri}`);
  } catch (error) {
    console.error('Error creating chat session:', error);
    alert('Could not start a new chat. Please try again.');
  } finally {
    loading.value = false;
  }
};

const shareSession = async () => {
  const shareData = {
    title: 'Echoo Chat',
    text: 'Join my chat session on Echoo!',
    url: window.location.href,
  };

  try {
    if (navigator.share && navigator.canShare && navigator.canShare(shareData)) {
      await navigator.share(shareData);
    } else {
      await navigator.clipboard.writeText(window.location.href);
      showCopyTooltip();
    }
  } catch (error) {
    if (error.name !== 'AbortError') {
      console.error('Error sharing:', error);
      // Fallback to clipboard if share fails for non-abort reasons
      await navigator.clipboard.writeText(window.location.href);
      showCopyTooltip();
    }
  }
};

const showCopyTooltip = () => {
  isCopied.value = true;
  setTimeout(() => {
    isCopied.value = false;
  }, 2000);
};

onMounted(async () => {
  username.value = localStorage.getItem('username') || 'Guest';
  await joinSession();
});

onUnmounted(() => {
  if (socket.value) {
    socket.value.onclose = null;
    socket.value.close();
  }
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translate(-50%, 10px);
}
</style>
```