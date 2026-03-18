<template>
  <div class="min-h-screen flex items-center justify-center bg-white px-4 py-12">
    <div class="w-full max-w-md space-y-8 bg-white p-8 rounded-md border border-gray-200 shadow-xl">
      
      <div class="text-center">
        <img 
          src="@/assets/logo.png" 
          alt="Echoo Logo" 
          class="mx-auto h-10 w-auto mb-4"
        />
        <h2 class="text-3xl font-extrabold text-black tracking-tight">
          {{ isSignUp ? 'Create an account' : 'Welcome back' }}
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          {{ isSignUp ? 'Chat online with Echoo' : 'Please enter your details to sign in' }}
        </p>
      </div>

      <div class="flex p-1 bg-gray-100 rounded-md border border-gray-200">
        <button 
          @click="isSignUp = true"
          :class="isSignUp ? 'bg-black text-white shadow-lg' : 'text-gray-500 hover:text-black'"
          class="cursor-pointer flex-1 py-2 text-sm font-medium rounded-md transition-all duration-200"
        >
          Sign Up
        </button>
        <button 
          @click="isSignUp = false"
          :class="!isSignUp ? 'bg-black text-white shadow-lg' : 'text-gray-500 hover:text-black'"
          class="cursor-pointer flex-1 py-2 text-sm font-medium rounded-md transition-all duration-200"
        >
          Sign In
        </button>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div class="space-y-4">
          
          <div v-if="isSignUp">
            <label class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
            <input 
              v-model="email" 
              type="email" 
              required 
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-md focus:ring-2 focus:ring-red-500 focus:border-transparent text-black placeholder-gray-400 outline-none transition-all"
              placeholder="Your email"
            >
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
            <input 
              v-model="username" 
              type="text" 
              required 
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-md focus:ring-2 focus:ring-red-500 focus:border-transparent text-black placeholder-gray-400 outline-none transition-all"
              placeholder="Your username"
            >
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input 
              v-model="password" 
              type="password" 
              required 
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-md focus:ring-2 focus:ring-red-500 focus:border-transparent text-black placeholder-gray-400 outline-none transition-all"
              placeholder="••••••••"
            >
          </div>

          <div v-if="isSignUp">
            <label class="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
            <input 
              v-model="confirmPassword" 
              type="password" 
              required 
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-md focus:ring-2 focus:ring-red-500 focus:border-transparent text-black placeholder-gray-400 outline-none transition-all"
              placeholder="••••••••"
            >
          </div>
        </div>

        <div v-if="isSignUp" class="flex items-center">
          <input id="terms" type="checkbox" required class="h-4 w-4 rounded border-gray-300 bg-gray-50 text-red-600 focus:ring-red-500">
          <label for="terms" class="ml-2 block text-sm text-gray-600">
            I accept the <a href="#" class="text-red-700 hover:underline">Terms and Conditions</a>
          </label>
        </div>

        <button 
          type="submit" 
          class="cursor-pointer w-full py-3 px-4 bg-red-700 hover:bg-red-700 text-white font-bold rounded-md shadow-lg transform transition active:scale-95 duration-200"
        >
          {{ isSignUp ? 'Create Account' : 'Sign In' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isSignUp: true,
      email: '',
      username: '',
      password: '',
      confirmPassword: ''
    }
  },
  methods: {
    async signUp() {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        const response = await fetch(`${apiUrl}/auth/users/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: this.email,
            username: this.username,
            password: this.password
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(JSON.stringify(errorData) || 'Registration failed');
        }

        alert("Your account has been created. You will be signed in automatically");
        await this.signIn();
      } catch (error) {
        console.error('Sign up error:', error);
        alert(error.message);
      }
    },

    async signIn() {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        const response = await fetch(`${apiUrl}/auth/jwt/create/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(JSON.stringify(errorData) || 'Login failed');
        }

        const data = await response.json();
        localStorage.setItem('accessToken', data.access);
        localStorage.setItem('refreshToken', data.refresh);
        localStorage.setItem('username', this.username);
        this.$router.push('/chats');
      } catch (error) {
        console.error('Sign in error:', error);
        alert(error.message);
      }
    },

    handleSubmit() {
      if (this.isSignUp) {
        if (this.password !== this.confirmPassword) {
          alert("Passwords do not match!");
          return;
        }
        console.log("Signing up to Echoo with:", this.email, this.username);
        this.signUp();
      } else {
        console.log("Signing into Echoo with:", this.username);
        this.signIn();
      }
    }
  }
}
</script>

<style scoped>
/* You can add custom animations here if needed */
</style>