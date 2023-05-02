<template>
  <v-dialog v-model="visible" max-width="500px">
    <v-card>
      <v-card-title>Filtros</v-card-title>
      <v-card-text>
        <v-container>
          <div class="mb-10">distância máxima (em km):</div>
          <v-slider
            v-model="raio"
            max="30"
            min="0"
            thumb-label="always"
          />
          <div>redes:</div>
          <v-autocomplete
            flat
            hide-details
            multiple
            attach
            chips
            dense
            clearable
            :items="['SHIBATA','SPANI', 'CARREFOUR', 'PAO_DE_ACUCAR', 'TENDA']"
            v-model="redes"
          >
            <template v-slot:selection="{ item, index }">
              <v-chip v-if="index < 5">
                <span>
                  {{ item }}
                </span>
              </v-chip>
              <!-- <span v-if="index === 5" class="grey--text caption"> -->
              <!-- (+{{ filters[header.value].length - 5 }} others) -->
              <!-- </span> -->
            </template>
          </v-autocomplete>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn class="blue--text darken-1" text @click="close()">Cancel</v-btn>
        <v-btn class="blue--text darken-1" text @click="aplicar()" :loading="loading" :disabled="loading">Aplicar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>

import { mapGetters } from 'vuex'
import api from '~api'

export default {
  data () {
    return {
      visible: false,
      loading: false,
      redes: [],
      raio: 10
    }
  },
  computed: {
    ...mapGetters({
      geolocation: 'geolocation/getGeolocation'
    })
  },
  methods: {
    open () {
      this.visible = true
    },
    close () {
      this.visible = false
    },
    async aplicar () {
      this.loading = true
      const geo = this.geolocation
      // a longitude tá undefined, o que não faz sentido ... tem que ser 1 state pra cada
      const mercadosProximos = await api.get_mercados_proximos({'latitude': geo.latitude, 'longitude': geo.longitude, 'raio': this.raio, 'redes': this.redes})
      this.$store.commit('geolocation/setMercadosProximos', mercadosProximos)
      this.$store.commit('geolocation/setRaio', this.raio)
      this.$store.commit('geolocation/setRedes', this.redes)
      this.visible = false
      this.loading = false
    }
  }
}
</script>
