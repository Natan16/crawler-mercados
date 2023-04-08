<template>
  <div>
    <v-expansion-panels v-if="mercadosLista">
      <v-expansion-panel
        v-for="(itens,mercado) in mercadosLista"
        :key="mercado"
      >
        <v-expansion-panel-header>
          {{ mercado }}  - TOTAL: R${{totais[mercado]}} - {{quantidades[mercado]}} &nbsp;<span v-if="quantidades[mercado] > 1">itens</span><span v-else>item</span>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <li
            v-for="(item,idx) in itens" :key="idx"
          >
            <!-- clicar no nome do item pra ter alteranativas -->
            {{ item.produto_nome }} - R$ {{ item.preco }} - <button @click="removerItem(mercado, idx)"><v-icon>mdi-minus</v-icon></button> {{ item.quantidade }}Un <button @click="adicionarItem(mercado, idx)"><v-icon>mdi-plus</v-icon></button> - R$ {{ (item.quantidade * item.preco).toFixed(2) }}
          </li>
          <br>
          <div v-if="ausentes[mercado]">
            Produtos indisponíveis:
            <li
              v-for="(produto,idx) in ausentes[mercado]" :key="idx"
            >
              <span color="red">{{ produto }}</span>
            </li>
          </div>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
    <div v-else>
      Sua lista de compras está vazia, retorne à pagina inicial para adicionar produtos
    </div>
  </div>
</template>

<script>

export default {
  layout: 'default',
  data () {
    const {correspondencias: _, ...lista} = this.$store.state.lista.mercadosLista
    return {mercadosLista: lista}
  },
  computed: {
    totais () {
      const totais = {}
      const lista = this.mercadosLista
      for (const unidade in lista) {
        const total = Object.values(lista[unidade]).reduce(function (previous, produto) {
          return previous + parseFloat(produto.preco) * produto.quantidade
        }, 0)
        totais[unidade] = total.toFixed(2)
      }
      return totais
    },
    quantidades () {
      const quantidades = {}
      const lista = this.mercadosLista
      for (const unidade in lista) {
        const total = Object.values(lista[unidade]).reduce(function (previous, produto) {
          return previous + 1
        }, 0)
        quantidades[unidade] = total
      }
      return quantidades
    },
    ausentes () {
      const ausentes = {}
      const correspondencias = this.$store.state.lista.mercadosLista.correspondencias
      Object.keys(this.mercadosLista).forEach(mercado => {
        Object.keys(correspondencias).forEach(corresp => {
          if (!correspondencias[corresp].includes(mercado)) {
            if (!Object.keys(ausentes).includes(mercado)) {
              ausentes[mercado] = [corresp]
            } else {
              ausentes[mercado].push(corresp)
            }
          }
        })
      })
      return ausentes
    }
  },
  methods: {
    adicionarItem (mercado, idx) {
      this.$store.commit('lista/addItem', this.mercadosLista[mercado][idx])
      const {correspondencias: _, ...lista} = this.$store.state.lista.mercadosLista
      this.mercadosLista = lista
    },
    removerItem (mercado, idx) {
      this.$store.commit('lista/removeItem', this.mercadosLista[mercado][idx])
      const {correspondencias: _, ...lista} = this.$store.state.lista.mercadosLista
      this.mercadosLista = lista
    }
  }
}
</script>

<style>
</style>
