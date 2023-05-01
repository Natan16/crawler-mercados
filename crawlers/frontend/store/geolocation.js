export const state = () => ({
  geolocation: undefined,
  raio: 10,
  redes: null,
  mercadosProximos: undefined
})

export const mutations = {
  setGeolocation (state, latitude, longitude) {
    state.geolocation = {latitude, longitude}
  },
  setMercadosProximos (state, mercadosProximos) {
    state.mercadosProximos = mercadosProximos
  },
  setRaio (state, raio) {
    state.raio = raio
  },
  setRedes (state, redes) {
    state.redes = redes
  }
}

export const getters = {
  getGeolation (state) {
    return state.geolocation
  },
  getMercadosProximos (state) {
    return state.mercadosProximos
  },
  getRaio (state) {
    return state.raio
  },
  getRedes (state) {
    return state.redes
  }
}

// export const actions = {
//   async whoami ({ commit }) {
//     const data = await api.whoami()
//     if (data.authenticated) {
//       commit('setCurrentUser', data.user)
//     } else {
//       commit('setCurrentUser', null)
//     }
//   }
// }
