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
        @keydown.enter="adicionarItem()"
        @keydown.esc="term = ''"
      />
    </v-flex>
    <div
      v-for="(item, idx) in produtos"
      :key="idx"
    >
      <v-flex xs12 class="ma-1">
        <!-- a ordenação pode ficar separada num filtro parecido com o que já tem -->
        <v-card>
          <v-card-text>
            <v-container>
              <div>{{item.produto.nome}}</div>
              <div>Mercado: {{item.mercado.unidade}}</div>
              <v-img width="100px" :src="getLogo(item.mercado.rede)" />
              <v-spacer />
              <div class="text-h4"><strong>R$ {{ item.preco }}</strong></div>
              <!-- o preço tem que ficar mais à mostra -->
              <!-- e o mercado pode ser substituído pelo logo -->
              <!-- <v-text-field label="Password" type="password" required v-model="password" @keyup.enter="login()" /> -->
              <!--  -->
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn v-if="item.quantidade > 0" rounded class="ma-1" @click="removerProduto(idx)"><v-icon>mdi-minus</v-icon></v-btn>
            <!-- a quantidade de cada produto vai ter no carrinho de compras ... o endpoint retorna o id? -->
            <span v-if="item.quantidade > 0">{{item.quantidade}}</span>
            <v-btn rounded class="ma-1" @click="adicionarProduto(idx)"><v-icon>mdi-plus</v-icon></v-btn>
            <!-- <v-btn class="blue--text darken-1" text @click="close()">Cancel</v-btn> -->
            <!-- <v-btn class="blue--text darken-1" text @click="login()" :loading="loading" :disabled="loading">Login</v-btn> -->
          </v-card-actions>
        </v-card>
      </v-flex>
    </div>
  </v-layout>
</template>

<script>
import debounce from 'lodash/debounce'
import Vue from 'vue'
import api from '~api'
import Snacks from '~/helpers/Snacks.js'

export default {
  data () {
    return {
      produtos: [],
      term: null,
      logoMap: {
        'SHIBATA': require('~/assets/shibata.png'),
        'SPANI': require('~/assets/spani.png'),
        'CARREFOUR': require('~/assets/carrefour.png')
      }
    }
  },
  computed: {
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
      // aqui tem que pegar do carrinho, caso já tenha
      this.produtos.forEach(item => {
        item.quantidade = 0
      })
    }, 500),
    reset () {
      this.term = ''
      this.produtos = []
    },
    adicionarItem () {
      const item = {term: this.term, produtos: this.produtos}
      this.$store.commit('lista/addItem', item)
      Snacks.show(this.$store, {text: `${this.term} adicionado à lista`, timeout: 2000})
      this.updateQuantidades()
    },
    adicionarProduto (idx) {
      this.$store.commit('lista/addProduto', this.produtos[idx])
      const newProdutos = this.produtos[idx]
      newProdutos.quantidade += 1
      Vue.set(this.produtos, idx, newProdutos)
      Snacks.show(this.$store, {text: `${this.produtos[idx].produto.nome} adicionado à lista`, timeout: 2000})
    },
    removerProduto (idx) {
      this.$store.commit('lista/removeProduto', this.produtos[idx])
      const newProdutos = this.produtos[idx]
      newProdutos.quantidade -= 1
      Vue.set(this.produtos, idx, newProdutos)
      Snacks.show(this.$store, {text: `${this.produtos[idx].produto.nome} removido da lista`, timeout: 2000})
    },
    updateQuantidades () {
      const produtos = this.produtos
      const mercadosLista = this.$store.state.lista.mercadosLista
      produtos.forEach((produto, idx) => {
        const newQuantidade = (mercadosLista[produto.mercado.unidade] && mercadosLista[produto.mercado.unidade][produto.id] && mercadosLista[produto.mercado.unidade][produto.id].quantidade) || 0
        const newProduto = this.produtos[idx]
        if (newProduto.quantidade !== newQuantidade) {
          newProduto.quantidade = newQuantidade
          Vue.set(this.produtos, idx, newProduto)
        }
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
