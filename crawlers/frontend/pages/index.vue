<template>
  <v-layout column>
    <v-flex row xs6 class="pa-4">
      <v-text-field
        prepend-icon="mdi-magnify"
        outlined
        v-model="term"
        label="Digite o produto que deseja buscar"
        hint="Clique enter para adicionar à lista"
        clearable
        autofocus
        @keydown.enter="adicionarProduto()"
        @keydown.esc="term = ''"
      />
    </v-flex>
    <loading v-if="loading" />
    <div
      v-for="(produto, idx) in produtos"
      :key="idx"
    >
      <div
        v-for="(item, idxItem) in produtos[idx].produto_crawl"
        :key="idxItem"
      >
        <v-flex xs12 class="ma-1">
          <!-- a ordenação pode ficar separada num filtro parecido com o que já tem -->
          <v-card>
            <v-card-text>
              <v-container>
                <div>{{produto.nome}}</div>
                <div>Mercado: {{item.mercado.unidade}}</div>
                <v-img width="100px" :src="getLogo(item.mercado.rede)" />
                <v-spacer />
                <div class="text-h4"><strong>R$ {{ item.preco }}</strong></div>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn v-if="item.quantidade > 0" rounded class="ma-1" @click="removerItem(idx, idxItem)"><v-icon>mdi-minus</v-icon></v-btn>
              <span v-if="item.quantidade > 0">{{item.quantidade}}</span>
              <v-btn rounded class="ma-1" @click="adicionarItem(idx, idxItem)"><v-icon>mdi-plus</v-icon></v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </div>
    </div>
  </v-layout>
</template>

<script>
import debounce from 'lodash/debounce'
import Vue from 'vue'
import api from '~api'
import Snacks from '~/helpers/Snacks.js'
import loading from '~/components/loading'

export default {
  components: {
    loading
  },
  data () {
    return {
      produtos: [],
      term: null,
      logoMap: {
        'SHIBATA': require('~/assets/shibata.svg'),
        'SPANI': require('~/assets/spani.png'),
        'CARREFOUR': require('~/assets/carrefour.png'),
        'PAO_DE_ACUCAR': require('~/assets/pao_de_acucar.png')
      },
      loading: false
    }
  },
  computed: {
  },
  watch: {
    term (value) {
      if (value?.length >= 3) {
        this.loading = true
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
      this.loading = false
      this.produtos.forEach(produto => {
        produto.produto_crawl.forEach(item => { item.quantidade = 0 })
      })
      this.updateQuantidades()
    }, 1000),
    reset () {
      this.term = ''
      this.produtos = []
    },
    // o toast tem que aparecer sempre
    adicionarProduto () {
      const result = {term: this.term, produtos: this.produtos}
      this.$store.commit('lista/addProduto', result)
      Snacks.show(this.$store, {text: `${this.term} adicionado à lista`, timeout: 2000})
      this.updateQuantidades()
    },
    adicionarItem (idx, idxItem) {
      this.$store.commit('lista/addItem', this.produtos[idx].produto_crawl[idxItem])
      const newProdutos = this.produtos[idx]
      newProdutos.produto_crawl[idxItem].quantidade += 1
      Vue.set(this.produtos, idx, newProdutos)
      // Snacks.show(this.$store, {text: `${this.produtos[idx].produto.nome} adicionado à lista`, timeout: 2000})
    },
    removerItem (idx, idxItem) {
      this.$store.commit('lista/removeItem', this.produtos[idx].produto_crawl[idxItem])
      const newProdutos = this.produtos[idx]
      newProdutos.produto_crawl[idxItem].quantidade -= 1
      Vue.set(this.produtos, idx, newProdutos)
      // Snacks.show(this.$store, {text: `${this.produtos[idx].produto.nome} removido da lista`, timeout: 2000})
    },
    updateQuantidades () {
      const produtos = this.produtos
      const mercadosLista = this.$store.state.lista.mercadosLista
      produtos.forEach((produto, idx) => {
        produto.produto_crawl.forEach((item, idxItem) => {
          const newQuantidade = (mercadosLista[item.mercado.unidade] && mercadosLista[item.mercado.unidade][item.id] && mercadosLista[item.mercado.unidade][item.id].quantidade) || 0
          const newProduto = this.produtos[idx]
          if (newProduto.produto_crawl[idxItem].quantidade !== newQuantidade) {
            newProduto.produto_crawl[idxItem].quantidade = newQuantidade
            Vue.set(this.produtos, idx, newProduto)
          }
        })
      })
    },
    getLogo (rede) {
      return this.logoMap[rede]
    }
  }
}
</script>

<style>
</style>
