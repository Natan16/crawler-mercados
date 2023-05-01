import {get, post} from './ajaxutils'

export default {
  login (username, password) {
    return post('/api/login', {username, password})
  },
  logout () {
    return post('/api/logout')
  },
  whoami () {
    return get('/api/whoami')
  },
  settings () {
    return get('/api/settings')
  },
  list_todos () {
    return get('/api/list_todos')
  },
  add_todo (newtask) {
    return post('/api/add_todo', {new_task: newtask})
  },
  search_produto (term, mercadosProximos) {
    return get('/api/search', {'search_term': term, 'mercados_proximos': mercadosProximos})
  },
  get_mercados_proximos (params) {
    return get('/api/get_mercados_proximos', {params})
  }

}
