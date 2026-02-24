<template>
  <div class="min-h-screen bg-white text-black selection:bg-red-500/30">
    <nav class="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto border-b border-gray-200">
      <div class="flex items-center gap-2">
        <img src="@/assets/logo.png" alt="Echoo Logo" class="h-8 w-8 object-contain" />
        <span class="text-xl font-bold tracking-tight">Echoo</span>
      </div>
      
      <div class="flex items-center gap-4">
        <router-link to="/auth" class="text-sm font-medium hover:text-gray-600 transition-colors">
          Sign In
        </router-link>
        <router-link to="/auth" class="px-5 py-2 bg-black hover:bg-gray-900 text-white text-sm font-bold rounded-md transition-all shadow-lg">
          Get Started
        </router-link>
      </div>
    </nav>

    <main class="relative overflow-hidden">
      <section class="max-w-7xl mx-auto px-6 pt-24 pb-32 text-center relative z-10">

        <h1 class="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 text-black">
          Connect. In Real Time. <br />
          <span class="text-red-700">Instantly.</span>
        </h1>

        <p class="max-w-2xl mx-auto text-lg md:text-xl text-gray-600 leading-relaxed mb-10">
          Echoo is a seamless real-time chat experience. Built with a modern stack for high performance, low latency, and infinite scalability.
        </p>

        <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
          <button 
            @click="handleStartChatting"
            class="cursor-pointer w-full sm:w-auto px-8 py-4 bg-black text-white font-bold rounded-md hover:bg-gray-900 transition-all flex items-center justify-center gap-2"
          >
            Start Chatting Now
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-700 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-red-700"></span>
            </span>
          </button>

          <a 
            href="https://github.com/tonybnya/echoo" 
            target="_blank" 
            class="w-full sm:w-auto px-8 py-4 bg-white border border-gray-200 text-black font-bold rounded-md hover:bg-gray-50 transition-all text-center"
          >
            View on GitHub
          </a>
        </div>
      </section>
    </main>

    <footer class="fixed bottom-0 left-0 right-0 border-t border-gray-800 bg-black py-8">
      <div class="max-width-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
        <div class="flex items-center gap-2">
          <img src="@/assets/logo.png" alt="Echoo Logo" class="h-6 w-6" />
          <!-- <img src="@/assets/logo.png" alt="Echoo Logo" class="h-6 w-6 opacity-50 invert" /> -->
          <p class="text-white text-sm">
            &copy; {{ currentYear }} Echoo.
            <!-- &copy; {{ currentYear }} Echoo Chat. Built with Vue & Django. -->
          </p>
        </div>
        <div class="flex gap-6">
          <a href="https://linkedin.com/in/tonybnya/" target="_blank" class="text-gray-400 hover:text-white transition-colors" title="LinkedIn">
            <span class="sr-only">LinkedIn</span>
            <i class="fa-brands fa-linkedin text-xl"></i>
          </a>
          <a href="https://github.com/tonybnya/" target="_blank" class="text-gray-400 hover:text-white transition-colors">
            <span class="sr-only">GitHub</span>
            <i class="fab fa-github text-xl"></i>
          </a>
          <a href="https://x.com/tonybnya" target="_blank" class="text-gray-400 hover:text-white transition-colors">
            <span class="sr-only">X</span>
            <i class="fa-brands fa-x-twitter text-xl"></i>
          </a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
  data() {
    return {
      currentYear: new Date().getFullYear()
    }
  },
  methods: {
    handleStartChatting() {
      const isAuthenticated = localStorage.getItem('authToken') !== null;
      if (isAuthenticated) {
        this.createChatSession();
      } else {
        this.$router.push('/auth');
      }
    },
    async createChatSession() {
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
        this.$router.push(`/chats/${data.uri}`);
      } catch (error) {
        console.error('Error creating chat session:', error);
        alert('Could not start a new chat. Please try again.');
      }
    }
  }
}
</script>

<style scoped>
/* Optional: Adding a smooth font smoothing for dark mode */
div {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>