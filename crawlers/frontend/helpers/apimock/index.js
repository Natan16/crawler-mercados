import { zuck } from './db_people'
import { todos } from './db_todos'
import { mockasync } from './mockutils'
import {produtos} from './db_produtos'

const keepLoggedIn = true

export default {
  login (username, password) {
    return mockasync(zuck)
  },
  logout () {
    return mockasync({})
  },
  whoami () {
    const iam = {authenticated: keepLoggedIn}
    if (iam.authenticated) {
      iam.user = zuck
    }
    return mockasync(iam)
  },
  settings () {
    return mockasync({
      SENTRY_DSN_FRONT: ''
      // SENTRY_DSN_FRONT: 'https://abcd1234@sentry.example.com/10'
    })
  },
  list_todos () {
    return mockasync(todos)
  },
  add_todo (newtask) {
    return mockasync({description: newtask, done: false})
  },
  search_produto (term, mercadosProximos) {
    return mockasync(produtos)
  }
}
