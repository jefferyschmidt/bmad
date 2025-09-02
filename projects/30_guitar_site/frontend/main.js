```javascript
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import vuetify from './plugins/vuetify'

Vue.config.productionTip = false

// Configure Axios
axios.defaults.baseURL = '/api'

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')

// Router
import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/profiles',
    name: 'Profiles',
    component: () => import('@/views/Profiles.vue')
  },
  {
    path: '/profiles/:username',
    name: 'ProfileDetails',
    component: () => import('@/views/ProfileDetails.vue')
  },
  {
    path: '/guitars',
    name: 'Guitars',
    component: () => import('@/views/Guitars.vue')
  },
  {
    path: '/guitars/:id',
    name: 'GuitarDetails',
    component: () => import('@/views/GuitarDetails.vue')
  },
  {
    path: '/account',
    name: 'Account',
    component: () => import('@/views/Account.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.isLoggedIn) {
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router

// Store
import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: null,
    guitars: [],
    comments: [],
    likes: [],
    shares: []
  },
  mutations: {
    setUser(state, user) {
      state.user = user
    },
    setGuitars(state, guitars) {
      state.guitars = guitars
    },
    setComments(state, comments) {
      state.comments = comments
    },
    setLikes(state, likes) {
      state.likes = likes
    },
    setShares(state, shares) {
      state.shares = shares
    }
  },
  actions: {
    async login({ commit }, { username, password }) {
      try {
        const response = await axios.post('/login', { username, password })
        commit('setUser', response.data.user)
        return response.data.user
      } catch (error) {
        throw error
      }
    },
    async register({ commit }, { username, email, password }) {
      try {
        const response = await axios.post('/register', { username, email, password })
        commit('setUser', response.data.user)
        return response.data.user
      } catch (error) {
        throw error
      }
    },
    async fetchGuitars({ commit }) {
      try {
        const response = await axios.get('/guitars')
        commit('setGuitars', response.data.guitars)
      } catch (error) {
        throw error
      }
    },
    async fetchComments({ commit }, guitarId) {
      try {
        const response = await axios.get(`/guitars/${guitarId}/comments`)
        commit('setComments', response.data.comments)
      } catch (error) {
        throw error
      }
    },
    async fetchLikes({ commit }, guitarId) {
      try {
        const response = await axios.get(`/guitars/${guitarId}/likes`)
        commit('setLikes', response.data.likes)
      } catch (error) {
        throw error
      }
    },
    async fetchShares({ commit }, guitarId) {
      try {
        const response = await axios.get(`/guitars/${guitarId}/shares`)
        commit('setShares', response.data.shares)
      } catch (error) {
        throw error
      }
    }
  },
  getters: {
    isLoggedIn(state) {
      return !!state.user
    }
  }
})

// App.vue
<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <v-img
          alt="Guitar Site Logo"
          class="shrink mr-2"
          contain
          src="@/assets/logo.png"
          transition="scale-transition"
          width="40"
        />
        <router-link to="/" class="text-decoration-none">
          <h1 class="title">Guitar Site</h1>
        </router-link>
      </div>

      <v-spacer></v-spacer>

      <div>
        <v-btn text to="/guitars">Guitars</v-btn>
        <v-btn text to="/profiles">Profiles</v-btn>
        <template v-if="isLoggedIn">
          <v-btn text to="/account">Account</v-btn>
          <v-btn text @click="logout">Logout</v-btn>
        </template>
        <template v-else>
          <v-btn text to="/login">Login</v-btn>
          <v-btn text to="/register">Register</v-btn>
        </template>
      </div>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>

    <v-footer app>
      <div class="px-4 py-2 text-center w-100">
        &copy; {{ new Date().getFullYear() }} Guitar Site. All rights reserved.
      </div>
    </v-footer>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters(['isLoggedIn'])
  },
  methods: {
    logout() {
      this.$store.commit('setUser', null)
      this.$router.push('/login')
    }
  }
}
</script>

// Home.vue
<template>
  <div>
    <v-container>
      <h1 class="text-h3 mb-4">Featured Guitars</h1>
      <v-row>
        <v-col
          v-for="guitar in featuredGuitars"
          :key="guitar.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <guitar-card :guitar="guitar" />
        </v-col>
      </v-row>
    </v-container>

    <v-container>
      <h1 class="text-h3 mb-4">Newest Guitars</h1>
      <v-row>
        <v-col
          v-for="guitar in newestGuitars"
          :key="guitar.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <guitar-card :guitar="guitar" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import GuitarCard from '@/components/GuitarCard.vue'

export default {
  components: {
    GuitarCard
  },
  data() {
    return {
      featuredGuitars: [],
      newestGuitars: []
    }
  },
  created() {
    this.fetchFeaturedGuitars()
    this.fetchNewestGuitars()
  },
  methods: {
    fetchFeaturedGuitars() {
      // Fetch featured guitars from the API
      this.$store.dispatch('fetchGuitars')
        .then(guitars => {
          this.featuredGuitars = guitars.slice(0, 4)
        })
        .catch(error => {
          console.error(error)
        })
    },
    fetchNewestGuitars() {
      // Fetch newest guitars from the API
      this.$store.dispatch('fetchGuitars')
        .then(guitars => {
          this.newestGuitars = guitars.slice(0, 4)
        })
        .catch(error => {
          console.error(error)
        })
    }
  }
}
</script>

// GuitarCard.vue
<template>
  <v-card class="guitar-card">
    <v-img :src="guitar.guitarPhotos[0]" height="200px" />
    <v-card-title>{{ guitar.brand }} {{ guitar.model }}</v-card-title>
    <v-card-subtitle>{{ guitar.year }}</v-card-subtitle>
    <v-card-text>{{ guitar.description }}</v-card-text>
    <v-card-actions>
      <v-btn text :to="`/guitars/${guitar.id}`">View Details</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    guitar: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.guitar-card {
  transition: transform 0.3s ease;
}

.guitar-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>

// GuitarDetails.vue
<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="6" md="4">
        <v-carousel>
          <v-carousel-item
            v-for="(photo, index) in guitar.guitarPhotos"
            :key="index"
            :src="photo"
          ></v-carousel-item>
        </v-carousel>
      </v-col>
      <v-col cols="12" sm="6" md="8">
        <h1 class="text-h3 mb-4">{{ guitar.brand }} {{ guitar.model }}</h1>
        <p class="text-h5 mb-2">Year: {{ guitar.year }}</p>
        <p class="mb-4">{{ guitar.description }}</p>
        <div class="d-flex align-center">
          <v-avatar size="40" class="mr-2">
            <img :src="guitar.user.profilePicture" alt="User Avatar" />
          </v-avatar>
          <div>
            <p class="mb-0">{{ guitar.user.username }}</p>
            <p class="caption mb-0">{{ guitar.user.bio }}</p>
          </div>
        </div>
      </v-col>
    </v-row>

    <v-divider class="my-8"></v-divider>

    <v-row>
      <v-col cols="12">
        <h2 class="text-h4 mb-4">Comments</h2>
        <v-card v-for="comment in comments" :key="comment.id" class="mb-4">
          <v-card-title>{{ comment.user.username }}</v-card-title>
          <v-card-text>{{ comment.text }}</v-card-text>
          <v-card-actions>
            <v-btn text>Reply</v-btn>
          </v-card-actions>
        </v-card>

        <div v-if="isLoggedIn">
          <v-text-field
            v-model="newComment"
            label="Add a comment"
            outlined
            @keyup.enter="postComment"
          ></v-text-field>
          <v-btn color="primary" @click="postComment">Post Comment</v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      guitar: null,
      comments: [],
      newComment: ''
    }
  },
  computed: {
    ...mapGetters(['isLoggedIn'])
  },
  created() {
    this.fetchGuitarDetails()
    this.fetchComments()
  },
  methods: {
    fetchGuitarDetails() {
      // Fetch guitar details from the API
      this.$store.dispatch('fetchGuitarById', this.$route.params.id)
        .then(guitar => {
          this.guitar = guitar
        })
        .catch(error => {
          console.error(error)
        })
    },
    fetchComments() {
      // Fetch comments for the guitar from the API
      this.$store.dispatch('fetchComments', this.$route.params.id)
        .then(comments => {
          this.comments = comments
        })
        .catch(error => {
          console.error(error)
        })
    },
    postComment() {
      // Post a new comment for the guitar
      this.$store.dispatch('postComment', {
        guitarId: this.$route.params.id,
        text: this.newComment
      })
        .then(() => {
          this.newComment = ''
          this.fetchComments()
        })
        .catch(error => {
          console.error(error)
        })
    }
  }
}
</script>

// Profiles.vue
<template>
  <v-container>
    <h1 class="text-h3 mb-4">Profiles</h1>
    <v-row>
      <v-col
        v-for="profile in profiles"
        :key="profile.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <profile-card :profile="profile" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ProfileCard from '@/components/ProfileCard.vue'

export default {
  components: {
    ProfileCard
  },
  data() {
    return {
      profiles: []
    }
  },
  created() {
    this.fetchProfiles()
  },
  methods: {
    fetchProfiles() {
      // Fetch user profiles from the API
      this.$store.dispatch('fetchProfiles')
        .then(profiles => {
          this.profiles = profiles
        })
        .catch(error => {
          console.error(error)
        })
    }
  }
}
</script>

// ProfileCard.vue
<template>
  <v-card class="profile-card">
    <v-img :src="profile.profilePicture" height="200px" />
    <v-card-title>{{ profile.username }}</v-card-title>
    <v-card-subtitle>{{ profile.bio }}</v-card-subtitle>
    <v-card-actions>
      <v-btn text :to="`/profiles/${profile.username}`">View Profile</v-btn>
    </v-card-actions>
  