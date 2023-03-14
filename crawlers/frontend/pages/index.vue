<template>
  <v-layout justify-center align-center row>
    <v-flex xs6 class="pt-4">
      <v-text-field
        outlined
        v-model="term"
        label="Digite o produto que deseja buscar"
        clearable
        autofocus
        @keydown.enter="adicionarItem()"
      />
    </v-flex>
    <v-flex xs7>
      <v-data-table
        :headers="headers"
        :items="produtos"
      >
        <template v-slot:items="props">
          <td>{{ props.item.produto.nome }}</td>
          <td>{{ props.item.mercado.unidade }}</td>
          <td>{{ props.item.preco }}</td>
        </template>
      </v-data-table>
    </v-flex>
  </v-layout>
</template>

<script>
import debounce from 'lodash/debounce'
import api from '~api'
import Snacks from '~/helpers/Snacks.js'

export default {
  data () {
    return {
      produtos: [],
      term: null,
      headers: [
        {
          text: 'Nome',
          value: 'produto.nome'
        },
        {
          text: 'Mercado',
          value: 'mercado.unidade'
        },
        {
          text: 'Preco (R$)',
          value: 'preco'
        }
      ]
    }
  },
  watch: {
    term (value) {
      if (value?.length >= 3) {
        this.searchProduto(value)
      }
    }
  },
  mounted () {
  },
  methods: {
    searchProduto: debounce(async function (term) {
      const response = await api.search_produto(term)
      this.produtos = response
    }, 500),
    reset () {
      this.term = ''
      this.produtos = []
    },
    adicionarItem () {
      const item = {term: this.term, produtos: this.produtos}
      this.$store.commit('lista/addItem', item)
      Snacks.show(this.$store, {text: `${this.term} adicionado à lista`, timeout: 2000})
      this.reset()
      // vai ter um contador que vai ser incrementado a cada commit
      // tem que ter um adicionar produto também, pra adicionar item específico
      // faz sentido ter um segundo endpoint pra fazer a computação? Acho que sim!
    },
    adicionarProduto () {
      // na verdade é um produto em específico
      Snacks.show(this.$store, {text: `${this.term} adicionado à lista`})
    }
  }
}
</script>

<style>
</style>
