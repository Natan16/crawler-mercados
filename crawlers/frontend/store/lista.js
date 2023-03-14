export const state = () => ({
//   lista: [], // lista genérica
  mercadosLista: {} // vai ser nome do mercado e a lista de compras
// um item e suas alternativas
// lista de cada mercado
})

export const mutations = {
  addItem (state, item) {
    // state.lista.push(item.term)
    item.produtos.forEach(produto => {
      // vai guardar quais os mercados em que esse produto já foi colocado (talvez colocar só os ids pros produtos)
      // precisa da quantidade também
      // os produtos precisam ser buscáveis, pelo id é uma boa!
      if (state.mercadosLista[produto.mercado.unidade] === undefined) {
        state.mercadosLista[produto.mercado.unidade] = [{produto, quantidade: 1}]
      } else {
        state.mercadosLista[produto.mercado.unidade].push({produto, quantidade: 1})
      }
    })
    // a ideia é que dê pra desfazer a operação também ... acho que com vuex dá fácil
    // em vez de adicionar todos, vai adicionar só o mais barato de cada mercado
    // faz sentido armazenar os outros como alternativas? talvez num segundo momento
  },
  addProduto (state, produto) {
    state.mercadosLista[produto.mercado.unidade].push({produto, quantidade: 1})
  }
  // hide (state) {
  // state.snack.visible = false
  // }
}
export const getters = {
  mercadosLista (state) {
    return state.mercadosLista
  }
}
export const actions = {
}
