<template>
  <div class="min-h-screen bg-[#0F172A] text-white selection:bg-blue-500/30">
    <nav class="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto border-b border-[#F3F4F6]/10">
      <div class="flex items-center gap-2">
        <img src="@/assets/logo.png" alt="Echoo Logo" class="h-8 w-8 object-contain" />
        <span class="text-xl font-bold tracking-tight">Echoo</span>
      </div>
      
      <div class="flex items-center gap-4">
        <router-link to="/auth" class="text-sm font-medium hover:text-blue-400 transition-colors">
          Sign In
        </router-link>
        <router-link to="/auth" class="px-5 py-2 bg-[#5EA3FA] hover:bg-blue-700 text-sm font-bold rounded-full transition-all shadow-lg shadow-blue-500/20">
          Get Started
        </router-link>
      </div>
    </nav>

    <main class="relative overflow-hidden">
      <!-- <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-125 bg-[#5EA3FA] blur-[120px] rounded-full pointer-events-none"></div> -->

      <section class="max-w-7xl mx-auto px-6 pt-24 pb-32 text-center relative z-10">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold mb-6">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-yellow-500 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-yellow-500"></span>
          </span>
          Powered by WebSockets & RabbitMQ
        </div>

        <h1 class="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 bg-clip-text text-transparent bg-linear-to-b from-white to-gray-400">
          Connect. In Real Time. <br />
          <span class="text-[#5EA3FA]">Instantly.</span>
        </h1>

        <p class="max-w-2xl mx-auto text-lg md:text-xl text-[#F3F4F6] leading-relaxed mb-10">
          Echoo is a seamless real-time chat experience. Built with a modern stack for high performance, low latency, and infinite scalability.
        </p>

        <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
          <router-link to="/auth" custom v-slot="{ navigate }">
            <button 
              @click="navigate"
              class="cursor-pointer w-full sm:w-auto px-8 py-4 bg-white text-[#0F172A] font-bold rounded-xl hover:bg-gray-200 transition-all flex items-center justify-center gap-2"
            >
              Start Chatting Now
              <span class="relative flex h-2 w-2">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-yellow-500 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-yellow-500"></span>
              </span>
            </button>
          </router-link>

          <a 
            href="https://github.com/tonybnya/echoo" 
            target="_blank" 
            class="w-full sm:w-auto px-8 py-4 bg-[#0F172A] border border-gray-800 text-white font-bold rounded-xl hover:bg-[#161d2f] transition-all text-center"
          >
            View on GitHub
          </a>
        </div>
      </section>
    </main>

    <footer class="fixed bottom-0 left-0 right-0 border-t border-gray-900 bg-[#171717] py-8">
      <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
        <div class="flex items-center gap-2">
          <img src="@/assets/logo.png" alt="Echoo Logo" class="h-6 w-6 opacity-50" />
          <p class="text-[#F3F4F6] text-sm">
            &copy; {{ currentYear }} Echoo Chat. Built with Vue & Django.
          </p>
        </div>
        <div class="flex gap-6">
          <a href="https://linkedin.com/in/tonybnya/" target="_blank" class="text-[#F3F4F6] hover:text-white transition-colors" title="LinkedIn">
            <span class="sr-only">LinkedIn</span>
            <i class="fa-brands fa-linkedin text-xl"></i>
          </a>
          <a href="https://github.com/tonybnya/" target="_blank" class="text-[#F3F4F6] hover:text-white transition-colors">
            <span class="sr-only">GitHub</span>
            <i class="fab fa-github text-xl"></i>
          </a>
          <a href="https://x.com/tonybnya" target="_blank" class="text-[#F3F4F6] hover:text-white transition-colors">
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
      // Logic for dynamic year
      currentYear: new Date().getFullYear()
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