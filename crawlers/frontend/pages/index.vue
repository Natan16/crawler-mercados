<template>
  <div>
    <div class="pa-4 pt-10">
      <v-text-field
        prepend-inner-icon="mdi-magnify"
        outlined
        v-model="term"
        label="Digite o produto que deseja buscar"
        hint="Clique enter para adicionar à lista"
        clearable
        autofocus
        rounded
        @keydown.enter="adicionarProduto()"
        @keydown.esc="term = ''"
      />
    </div>
    <loading v-if="loading" />
    <div v-if="buscaVazia">
      Nenhum produto corresponde à sua pesquisa
    </div>
    <div
      v-for="(produto, idx) in produtos"
      :key="idx"
    >
      <v-container v-if="mobile">
        <div v-if="produtos[idx].produto_crawl.length >= 0" class="text-center">{{produto.nome}}</div>
        <!-- TODO: mostrar quantos mercados tem ao todo -->
        <v-slide-group
          selected-class="bg-success"
        >
          <v-slide-item
            align="center" justify="center"
            v-for="(item, idxItem) in produtos[idx].produto_crawl"
            :key="idxItem"
          >
            <v-card class="ma-1" width="35vw">
              <v-card-text class="text-center">
                <div class="text-truncate bg-secondary">
                  <span>{{item.mercado.unidade}}</span>
                  <v-img height="30px" width="100%" contain :src="getLogo(item.mercado.rede)" />
                </div>
                <div class="text-h6"><strong>R$ {{ item.preco }}</strong></div>
              </v-card-text>
              <v-card-actions>
                <v-btn v-if="item.quantidade > 0" width="16px" rounded x-small @click="removerItem(idx, idxItem)"><v-icon>mdi-minus</v-icon></v-btn>
                <!-- alinhar o número no centro -->
                <span class="ml-6" v-if="item.quantidade > 0">{{item.quantidade}}</span>
                <v-spacer />
                <v-btn width="16px" rounded x-small @click="adicionarItem(idx, idxItem)"><v-icon>mdi-plus</v-icon></v-btn>
              </v-card-actions>
            </v-card>
          </v-slide-item>
        </v-slide-group>
      </v-container>
      <v-container v-else>
        <v-card class="pb-4 ma-1">
          <v-card-title v-if="produtos[idx].produto_crawl.length >= 0" class="text-center">{{produto.nome}}</v-card-title>
          <v-layout row>
            <div
              v-for="(item, idxItem) in produtos[idx].produto_crawl"
              :key="idxItem"
            >
              <v-card-text class="text-center" width="400px">
                <v-container>
                  <div>{{item.mercado.unidade}}</div>
                  <v-img height="60px" width="300px" contain :src="getLogo(item.mercado.rede)" />
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
            </div>
          </v-layout>
        </v-card>
      </v-container>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
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
        'SPANI': require('~/assets/spani.svg'),
        'CARREFOUR': require('~/assets/carrefour.svg'),
        'PAO_DE_ACUCAR': require('~/assets/pao_de_acucar.svg'),
        'TENDA': require('~/assets/tenda.svg')
      },
      loading: false,
      buscaVazia: false
    }
  },
  computed: {
    ...mapState(['raio', 'redes', 'mercadosProximos']),
    mobile () {
      return this.$vuetify.breakpoint.mobile
    }
  },
  watch: {
    term (value) {
      this.buscaVazia = false
      if (value?.length >= 3) {
        this.loading = true
        this.searchProduto(value)
      }
    }
  },
  mounted () {
    if (!this.$store.state.geolocation) {
      this.navigator.geolocation.getCurrentPosition(position => {
        this.saveLocation(position.coords.latitude, position.coords.longitude)
      })
    }
  },
  methods: {
    async saveLocation (latitude, longitude) {
      this.$store.commit('geolocation/setGeolocation', latitude, longitude)
      const raio = this.raio
      const redes = this.redes
      const mercadosProximos = await api.get_mercados_proximos({latitude, longitude, raio, redes})
      this.$store.commit('geolocation/setMercadosProximos', mercadosProximos)
    },
    searchProduto: debounce(async function (term) {
      const response = await api.search_produto(term, this.mercadosProximos)
      this.produtos = response
      this.loading = false
      if (this.produtos.length === 0 || !this.produtos.some((produto) => produto.produto_crawl.length > 0)) {
        this.buscaVazia = true
      }
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

<style scoped>
.scroll {
  background-color: #fed9ff;
  width: 600px;
  height: 150px;
  overflow-y: hidden;
  overflow-x: auto;
  text-align: center;
  padding: 20px;
  white-space: nowrap;
}
/* só tá aplicando a primeira prop */
span {
  white-space: nowrap;
  overflow: hidden;              /* "overflow" value must be different from "visible" */
  text-overflow: ellipsis;
}
</style>
