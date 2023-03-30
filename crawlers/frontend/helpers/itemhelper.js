// import Vue from 'vue'
// export default {
//   adicionarItem (idx, idxItem) {
//     this.$store.commit('lista/addItem', this.produtos[idx].produto_crawl[idxItem])
//     const newProdutos = this.produtos[idx]
//     newProdutos.produto_crawl[idxItem].quantidade += 1
//     Vue.set(this.produtos, idx, newProdutos)
//     // Snacks.show(this.$store, {text: `${this.produtos[idx].produto.nome} adicionado à lista`, timeout: 2000})
//   },
//   removerItem (idx, idxItem) {
//     this.$store.commit('lista/removeItem', this.produtos[idx].produto_crawl[idxItem])
//     const newProdutos = this.produtos[idx]
//     newProdutos.produto_crawl[idxItem].quantidade -= 1
//     Vue.set(this.produtos, idx, newProdutos)
//     // Snacks.show(this.$store, {text: `${this.produtos[idx].produto.nome} removido da lista`, timeout: 2000})
//   }
// }
