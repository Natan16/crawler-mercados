export const state = () => ({
  mercadosLista: {correspondencias: {}}
})

export const mutations = {
  addItem (state, item) {
    const unidades = []
    item.produtos.forEach(produto => {
      if (!unidades.includes(produto.mercado.unidade)) {
        unidades.push(produto.mercado.unidade)
        // ISOLAR NUM METODO
        if (!state.mercadosLista[produto.mercado.unidade]) {
          state.mercadosLista[produto.mercado.unidade] = {}
        }
        if (!state.mercadosLista[produto.mercado.unidade][produto.id]) {
          state.mercadosLista[produto.mercado.unidade][produto.id] = {...produto, quantidade: 1}
          return
        }
        state.mercadosLista[produto.mercado.unidade][produto.id].quantidade += 1
      }
    })
    state.mercadosLista.correspondencias[item.term] = unidades
  },
  addProduto (state, produto) {
    if (!state.mercadosLista[produto.mercado.unidade]) {
      state.mercadosLista[produto.mercado.unidade] = {}
    }
    if (!state.mercadosLista[produto.mercado.unidade][produto.id]) {
      state.mercadosLista[produto.mercado.unidade][produto.id] = {...produto, quantidade: 1}
      return
    }
    state.mercadosLista[produto.mercado.unidade][produto.id].quantidade += 1
  },
  removeProduto (state, produto) {
    if (state.mercadosLista[produto.mercado.unidade][produto.id] === undefined) {
      return
    }
    if (state.mercadosLista[produto.mercado.unidade][produto.id].quantidade <= 1) {
      state.mercadosLista[produto.mercado.unidade][produto.id] = undefined
      return
    }
    state.mercadosLista[produto.mercado.unidade][produto.id].quantidade -= 1
  }
}
export const getters = {
  mercadosLista (state) {
    return state.mercadosLista
  }
}
export const actions = {
}
