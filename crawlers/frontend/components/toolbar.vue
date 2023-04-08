<template>
  <v-app-bar color="blue-grey" dark fixed app clipped-right>
    <v-toolbar-title class="ml-4">
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <button
            v-bind="attrs"
            v-on="on"
            @click="home()"
          >
            <v-img :src="require('~/assets/logo.png')" style="width: 120px; object-fit: cover; object-position: 1000px;" />
          </button>
        </template>
        <span>Ir para home</span>
      </v-tooltip>
    </v-toolbar-title>
    <v-spacer />
    <v-menu v-if="logged_user" offset-y>
      <template v-slot:activator="{ on }">
        <v-btn icon v-on="on" class="ma-0 ml-5">
          <v-avatar size="36px">
            <img src="https://graph.facebook.com/4/picture?width=300&height=300">
          </v-avatar>
        </v-btn>
      </template>
      <v-card class="no-padding">
        <v-list two-line>
          <v-list-item>
            <v-list-item-avatar>
              <v-avatar>
                <img src="https://graph.facebook.com/4/picture?width=300&height=300">
              </v-avatar>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title>{{logged_user.first_name}} {{logged_user.last_name}}</v-list-item-title>
              <v-list-item-subtitle>{{logged_user.email}}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <v-divider />
        <v-list>
          <v-list-item @click="logout()">
            <v-list-item-content>
              <v-list-item-title>Log out</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card>
    </v-menu>
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <button @click="pageLista()">
          <v-icon
            size="200%"
            v-bind="attrs"
            v-on="on"
          >
            mdi-filter
          </v-icon>
        </button>
      </template>
      <span>Filtrar</span>
    </v-tooltip>
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <button @click="pageLista()">
          <v-icon
            size="200%"
            v-bind="attrs"
            v-on="on"
          >
            mdi-cart
          </v-icon>
        </button>
      </template>
      <span>Ir para lista de compras</span>
    </v-tooltip>
    <!-- <v-app-bar-nav-icon @click.stop="state.drawerRight = !state.drawerRight" /> -->
    <login-dialog ref="login_dialog" />
  </v-app-bar>
</template>

<script>
import loginDialog from '~/components/login-dialog.vue'
import Snacks from '~/helpers/Snacks.js'
import api from '~api'

export default {
  components: {
    loginDialog
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
