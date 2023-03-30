export const state = () => ({
  mercadosLista: {correspondencias: {}}
})

export const mutations = {
  addProduto (state, result) {
    const unidades = []
    result.produtos.forEach(produto => produto.produto_crawl.forEach(item => {
      if (!unidades.includes(item.mercado.unidade)) {
        unidades.push(item.mercado.unidade)
        // ISOLAR NUM METODO
        if (!state.mercadosLista[item.mercado.unidade]) {
          state.mercadosLista[item.mercado.unidade] = {}
        }
        if (!state.mercadosLista[item.mercado.unidade][item.id]) {
          state.mercadosLista[item.mercado.unidade][item.id] = {...item, quantidade: 1}
          return
        }
        state.mercadosLista[item.mercado.unidade][item.id].quantidade += 1
      }
    }))
    state.mercadosLista.correspondencias[result.term] = unidades
  },
  addItem (state, item) {
    if (!state.mercadosLista[item.mercado.unidade]) {
      state.mercadosLista[item.mercado.unidade] = {}
    }
    if (!state.mercadosLista[item.mercado.unidade][item.id]) {
      state.mercadosLista[item.mercado.unidade][item.id] = {...item, quantidade: 1}
      return
    }
    state.mercadosLista[item.mercado.unidade][item.id].quantidade += 1
  },
  removeItem (state, item) {
    if (state.mercadosLista[item.mercado.unidade][item.id] === undefined) {
      return
    }
    if (state.mercadosLista[item.mercado.unidade][item.id].quantidade <= 1) {
      delete state.mercadosLista[item.mercado.unidade][item.id]
      if (Object.keys(state.mercadosLista[item.mercado.unidade]).length === 0) {
        delete Object.keys(state.mercadosLista[item.mercado.unidade])
      }
      return
    }
    state.mercadosLista[item.mercado.unidade][item.id].quantidade -= 1
  }
}
export const getters = {
  mercadosLista (state) {
    return state.mercadosLista
  }
}
export const actions = {
}
