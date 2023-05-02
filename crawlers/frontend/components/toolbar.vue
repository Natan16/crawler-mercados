<template>
  <v-app-bar :elevation="12" color="#01579B" dark fixed app clipped-right>
    <!-- <v-app-bar-nav-icon @click.stop="state.drawerLeft = !state.drawerLeft" /> -->
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
    <v-app-bar-nav-icon @click.stop="open_filter_dialog">
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
      <!-- a ideia aqui é começar com um filtro de distância e um de mercados (rede) -->
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
    <filter-dialog ref="filter_dialog" />
  </v-app-bar>
</template>

<script>
import filterDialog from '~/components/filter-dialog.vue'
import Snacks from '~/helpers/Snacks.js'
import api from '~api'

export default {
  components: {
    filterDialog
  },
  props: ['state'],
  computed: {
    logged_user () {
      return this.$store.state.auth.currentUser
    }
  },
  methods: {
    open_filter_dialog (evt) {
      this.$refs.filter_dialog.open()
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
