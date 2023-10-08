<template>
  <v-app id="inspire">
    <toolbar :state="layout" />
    <!-- <sidenav-left :state="layout" /> -->
    <v-main>
      <v-container fluid>
        <nuxt />
      </v-container>
    </v-main>
    <le-footer />
    <v-snackbar
      :timeout="timeout"
      :color="color"
      bottom
      v-model="show"
    >
      {{message}}
      <!-- <v-btn dark text @click.native="closeSnack">Close</v-btn> -->
    </v-snackbar>
  </v-app>
</template>

<script>
import toolbar from '~/components/toolbar.vue'
// import sidenavLeft from '~/components/sidenav-left.vue'
import footer from '~/components/footer.vue'
export default {
  components: {
    toolbar,
    // sidenavLeft,
    leFooter: footer
  },
  data: () => ({
    layout: {
      drawer: true
    },
    show: false,
    message: '',
    color: '',
    timeout: 2000
  }),
  created () {
    this.$store.subscribe((mutation, state) => {
      if (mutation.type === 'snack/set') {
        this.message = state.snack.snack.text
        this.color = state.snack.snack.color
        this.timeout = state.snack.snack.timeout
        this.show = true
      }
    })
  }
}
</script>
