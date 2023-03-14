import Vue from 'vue'
import Router from 'vue-router'
import Index from '~/pages/index.vue'
import Lista from '~/pages/lista.vue'

Vue.use(Router)

export const routerOptions = {
  mode: 'history',
  routes: [
    {path: '/', component: Index, name: 'index'},
    {path: '/lista', component: Lista, name: 'lista'}
  ]
}

export function createRouter (ctx) {
  return new Router(routerOptions)
}
