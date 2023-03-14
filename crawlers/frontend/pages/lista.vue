<template>
  <v-layout justify-left>
    <!-- a lista de todos pode ser a base pra lista de compras -->
    <!-- pegar da store os itens -->
    {{ mercadosLista }}
    <!-- <todo-list /> -->
  </v-layout>
</template>

<script>
// import todoList from '~/components/todo-list.vue'

export default {
  layout: 'default',
  //   components: {
  //     todoList
  //   },
  data () {
    return {}
  },
  computed: {
    mercadosLista () {
      // store.getters['settings/loaded']
      return this.$store.state.lista.mercadosLista
    }
  }
}
</script>

<style>
</style>
