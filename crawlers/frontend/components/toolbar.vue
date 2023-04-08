<template>
  <v-app-bar :elevation="12" color="#2E7D32" dark fixed app clipped-right>
    <v-app-bar-nav-icon @click.stop="state.drawerLeft = !state.drawerLeft" />
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <button
          v-bind="attrs"
          v-on="on"
          @click="home()"
        >
          <v-app-bar-title>
            Mercado Simplificado
          </v-app-bar-title>
        </button>
      </template>
      <span>Ir para página inicial</span>
    </v-tooltip>
    <v-spacer />
    <v-app-bar-nav-icon @click.stop="pageLista()">
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-icon
            v-bind="attrs"
            v-on="on"
          >
            mdi-filter
          </v-icon>
        </template>
        <span>Filtrar</span>
      </v-tooltip>
    </v-app-bar-nav-icon>
    <v-app-bar-nav-icon @click.stop="pageLista()">
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-icon
            v-bind="attrs"
            v-on="on"
          >
            mdi-cart
          </v-icon>
        </template>
        <span>Ir para lista de compras</span>
      </v-tooltip>
    </v-app-bar-nav-icon>
    <!-- <login-dialog ref="login_dialog" /> -->
    <!-- vai dar show num dialog que fica aqui -->
  </v-app-bar>
</template>

<script>
// import loginDialog from '~/components/login-dialog.vue'
import Snacks from '~/helpers/Snacks.js'
import api from '~api'

export default {
  components: {
    // loginDialog
  },
  props: ['state'],
  computed: {
    logged_user () {
      return this.$store.state.auth.currentUser
    }
  },
  methods: {
    open_login_dialog (evt) {
      this.$refs.login_dialog.open()
      evt.stopPropagation()
    },
    async logout () {
      await api.logout()
      this.$store.commit('auth/setCurrentUser', null)
      Snacks.show(this.$store, {text: 'Até logo!'})
    },
    home () {
      this.$router.push({name: 'index'})
    },
    pageLista () {
      this.$router.push({name: 'lista'})
    }
  }
}
</script>
