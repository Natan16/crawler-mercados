<template>
  <div>
    <v-expansion-panels>
      <v-expansion-panel
        v-for="(produtos,mercado) in mercadosLista"
        :key="mercado"
      >
        <v-expansion-panel-header>
          <!-- pluralize aqui -->
          {{ mercado }}  - TOTAL: R${{totais[mercado]}} - {{quantidades[mercado]}} itens
          <!-- é bom saber o que foi adicionado junto pra saber quais os itens indisponíveis em cada mercado -->
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <li
            v-for="(produto,idx) in produtos" :key="idx"
          >
            {{ produto.produto.nome }} - R$ {{ produto.preco }} - {{ produto.quantidade }}Un - R$ {{ produto.quantidade * produto.preco }}
          </li>
          <br>
          Itens indisponíveis:
          <li
            v-for="(produto,idx) in ausentes[mercado]" :key="idx"
          >
            <span color="red">{{ produto }}</span>
          </li>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script>

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
      const {correspondencias: _, ...lista} = this.$store.state.lista.mercadosLista
      return lista
    },
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
            if (!ausentes.mercado) {
              ausentes[mercado] = [corresp]
            } else {
              ausentes[mercado].push(corresp)
            }
          }
        })
      })
      return ausentes
    }
  }
}
</script>

<style>
</style>
