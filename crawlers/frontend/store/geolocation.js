export const state = () => ({
  geolocation: undefined,
  latitude: undefined,
  longitude: undefined,
  raio: 10,
  redes: null,
  mercadosProximos: undefined
})

export const mutations = {
  setGeolocation (state, geolocation) {
    state.latitude = geolocation.latitude
    state.longitude = geolocation.longitude
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
  getGeolocation (state) {
    return {'latitude': state.latitude, 'longitude': state.longitude}
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
