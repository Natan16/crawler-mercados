<template>
  <v-layout justify-center align-center row>
    <v-flex xs8>
      <v-text-field v-model="term" label="digite o produto que deseja buscar" />
    </v-flex>
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
  </v-layout>
</template>

<script>
import debounce from 'lodash/debounce'
import api from '~api'

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
    }, 500)
  }
}
</script>

<style>
</style>
