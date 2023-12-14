export const state = () => ({
  mercadosLista: {correspondencias: {}}
})

export const mutations = {
  addItem (state, {mercadoResult, idxItem}) {
    if (!state.mercadosLista[mercadoResult.mercado.unidade]) {
      state.mercadosLista[mercadoResult.mercado.unidade] = {}
    }
    const item = mercadoResult.produto_crawl[idxItem]
    if (!state.mercadosLista[mercadoResult.mercado.unidade][item.id]) {
      state.mercadosLista[mercadoResult.mercado.unidade][item.id] = {...item, quantidade: 1}
      return
    }
    state.mercadosLista[mercadoResult.mercado.unidade][item.id].quantidade += 1
  },
  removeItem (state, {mercadoResult, idxItem}) {
    const item = mercadoResult.produto_crawl[idxItem]
    if (state.mercadosLista[mercadoResult.mercado.unidade][item.id] === undefined) {
      return
    }
    if (state.mercadosLista[mercadoResult.mercado.unidade][item.id].quantidade <= 1) {
      delete state.mercadosLista[mercadoResult.mercado.unidade][item.id]
      if (Object.keys(state.mercadosLista[mercadoResult.mercado.unidade]).length === 0) {
        delete Object.keys(state.mercadosLista[mercadoResult.mercado.unidade])
      }
      return
    }
    state.mercadosLista[mercadoResult.mercado.unidade][item.id].quantidade -= 1
  }
}
export const getters = {
  mercadosLista (state) {
    return state.mercadosLista
  }
}
export const actions = {
}
