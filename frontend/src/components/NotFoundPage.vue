<template>
  <div class="min-h-screen bg-white flex items-center justify-center px-6 overflow-hidden">
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-red-500/5 blur-[120px] rounded-full pointer-events-none"></div>

    <div class="text-center relative z-10">
      <h1 class="text-8xl md:text-9xl font-black text-red-600 mb-4 opacity-80 tracking-tighter">
        404
      </h1>
      
      <div class="space-y-4">
        <h2 class="text-3xl md:text-4xl font-bold text-black tracking-tight">
          Lost in the Echoo?
        </h2>
        <p class="text-gray-600 max-w-sm mx-auto leading-relaxed">
          The page you're looking for doesn't exist or has been moved to another frequency.
        </p>
      </div>

      <div class="mt-12">
        <router-link 
          to="/" 
          class="inline-flex items-center gap-2 px-8 py-4 bg-black hover:bg-gray-900 text-white font-bold rounded-md transition-all shadow-lg active:scale-95"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L7.414 9H15a1 1 0 110 2H7.414l2.293 2.293a1 1 0 010 1.414z" clip-rule="evenodd" />
          </svg>
          Back to Home
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundPage'
}
</script>