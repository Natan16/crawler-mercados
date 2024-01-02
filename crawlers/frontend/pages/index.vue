<template>
  <div>
    <div class="pa-4 pt-10">
      <v-text-field
        prepend-inner-icon="mdi-magnify"
        outlined
        v-model="term"
        label="Digite produto para buscar"
        clearable
        autofocus
        rounded
        @keydown.esc="term = ''"
      />
      <!-- TODO: No mobile assim que começar a scrollar tem que fazer o teclado desaparecer!  -->
    </div>
    <loading v-if="loading" />
    <div v-if="buscaVazia">
      Nenhum produto corresponde à sua pesquisa
    </div>
    <div
      v-for="(mercadoResponse, idx) in searchResult"
      :key="idx"
    >
      <v-layout row class="mx-2 my-2">
        <v-flex xs3>
          <v-img height="30px" width="80px" contain :src="getLogo(mercadoResponse.mercado.rede)" />
        </v-flex>
        <v-flex xs8 class="ml-2" >
          <p class="text-h8">{{mercadoResponse.mercado.unidade}} </p>
        </v-flex>
      </v-layout>
      <v-slide-group v-if="mobile"
          selected-class="bg-success"
      >
        <v-slide-item
          justify="center"
          v-for="(item, idxItem) in searchResult[idx].produto_crawl"
          :key="idxItem"
        >
          <item :item="item" :key="searchResult[idx].produto_crawl[idxItem].quantidade"
            @adicionar-item="adicionarItem(idx, idxItem)"
            @remover-item="removerItem(idx, idxItem)"
          />
        </v-slide-item>
      </v-slide-group>
      <v-row wrap v-else class="mb-2">
        <div
          v-for="(item, idxItem) in searchResult[idx].produto_crawl"
          :key="idxItem"
        >
          <item style="max-width: 20vw;" :item="item" :key="searchResult[idx].produto_crawl[idxItem].quantidade"
            @adicionar-item="adicionarItem(idx, idxItem)"
            @remover-item="removerItem(idx, idxItem)"
          />
        </div>
      </v-row>
      <v-divider class="mt-2" />
    </div>

    <div><v-icon color="green">mdi-arrow-down</v-icon>: Abaixo da média dos outros mercados</div>
    <div><v-icon color="red">mdi-arrow-up</v-icon>: Acima da média dos outros mercados</div>
    <div><v-icon color="yellow">mdi-minus</v-icon>: Na média dos outros mercados</div>
    <div><v-chip style="border-radius: 0;" small color="green" text-color="white">MAIS EM CONTA</v-chip>: Produto do mercado com melhor custo-benefício </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import debounce from 'lodash/debounce'
import Vue from 'vue'
import api from '~api'
import Snacks from '~/helpers/Snacks.js'
import loading from '~/components/loading'
import item from '~/components/item'

export default {
  components: {
    loading,
    item
  },
  data () {
    return {
      searchResult: [],
      term: '',
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
    ...mapGetters({
      redes: 'geolocation/getRedes',
      raio: 'geolocation/getRaio',
      mercadosProximos: 'geolocation/getMercadosProximos'
    }),
    mobile () {
      return this.$vuetify.breakpoint.mobile
    }
  },
  watch: {
    term (value) {
      this.searchProduto(value)
    },
    mercadosProximos (value) {
      this.searchProduto(this.term)
      if (value.length === 0) {
        Snacks.show(this.$store, {text: 'Nenhum mercado próximo encontrado, mostrando todos os resultados', timeout: 6000, color: 'warning'})
      }
    }
  },
  mounted () {
    Vue.directive('visible', function (el, binding) {
      el.style.visibility = binding.value ? 'visible' : 'hidden'
    })
    if (!this.$store.state.geolocation.geolocation) {
      navigator.geolocation.getCurrentPosition(position => {
        this.saveLocation(position.coords.latitude, position.coords.longitude)
      })
    }
  },
  methods: {
    async saveLocation (latitude, longitude) {
      this.$store.commit('geolocation/setGeolocation', {latitude, longitude})
      const raio = this.raio
      const redes = this.redes
      const mercadosProximos = await api.get_mercados_proximos({latitude, longitude, raio, redes})
      this.$store.commit('geolocation/setMercadosProximos', mercadosProximos)
    },
    searchProduto: debounce(async function (term) {
      if (term.length < 3) {
        return
      }
      this.buscaVazia = false
      this.loading = true
      const response = await api.search_produto(term, this.mercadosProximos)
      this.searchResult = response
      this.loading = false
      if (this.searchResult.length === 0 || !this.searchResult.some((mercadoResult) => mercadoResult.produto_crawl.length > 0)) {
        this.buscaVazia = true
      }
      // this should do for now, the ideal behavior is to hidekeyboard on scroll
      if (this.mobile) {
        this.hideKeyboard()
      }
      // inicializa os itens com quantidade 0
      this.searchResult.forEach(mercadoResult => {
        mercadoResult.produto_crawl.forEach(item => { item.quantidade = 0 })
      })
      // atualiza quantidades com o que já foi adicionado ao carrinho
      this.updateQuantidades()
    }, 1000),
    reset () {
      this.term = ''
      this.produtos = []
    },
    adicionarItem (idx, idxItem) {
      const mercadoResult = this.searchResult[idx]
      this.$store.commit('lista/addItem', {mercadoResult, idxItem})
      const newProdutos = this.searchResult[idx]
      newProdutos.produto_crawl[idxItem].quantidade += 1
      Vue.set(this.searchResult, idx, newProdutos)
      Snacks.show(this.$store, {text: `${newProdutos.produto_crawl[idxItem].produto.nome} adicionado à lista`, timeout: 2000})
    },
    removerItem (idx, idxItem) {
      const mercadoResult = this.searchResult[idx]
      this.$store.commit('lista/removeItem', {mercadoResult, idxItem})
      const newProdutos = this.searchResult[idx]
      newProdutos.produto_crawl[idxItem].quantidade -= 1
      Vue.set(this.searchResult, idx, newProdutos)
      Snacks.show(this.$store, {text: `${newProdutos.produto_crawl[idxItem].produto.nome} removido da lista`, timeout: 2000})
    },
    updateQuantidades () {
      const searchResult = this.searchResult
      const mercadosLista = this.$store.state.lista.mercadosLista
      searchResult.forEach((mercadoResult, idx) => {
        mercadoResult.produto_crawl.forEach((item, idxItem) => {
          const newQuantidade = (mercadosLista[mercadoResult.mercado.unidade] && mercadosLista[mercadoResult.mercado.unidade][item.id] && mercadosLista[mercadoResult.mercado.unidade][item.id].quantidade) || 0
          const newMercadoResult = mercadoResult
          if (newMercadoResult.produto_crawl[idxItem].quantidade !== newQuantidade) {
            newMercadoResult.produto_crawl[idxItem].quantidade = newQuantidade
            Vue.set(this.searchResult, idx, newMercadoResult)
          }
        })
      })
    },
    getLogo (rede) {
      return this.logoMap[rede]
    },
    hideKeyboard () {
      document.activeElement.blur()
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
</style>
