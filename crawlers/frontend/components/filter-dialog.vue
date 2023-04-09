<template>
  <v-dialog v-model="visible" max-width="500px">
    <v-card>
      <v-card-title>Filtros</v-card-title>
      <v-card-text>
        <v-container>
          <div class="mb-10">distância máxima (em km):</div>
          <v-slider
            v-model="distancia"
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
            :items="['shibata','spani', 'carrefour', 'pao de acucar', 'tenda']"
            v-model="mymodel"
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

// import api from '~api'

export default {
  data () {
    return {
      visible: false,
      loading: false,
      username: '',
      password: '',
      error: false,
      distancia: 10
    }
  },
  methods: {
    open () {
      this.visible = true
    },
    close () {
      this.visible = false
    },
    aplicar () {
      this.loading = true
      this.error = false
      // const user = await api.login(this.username, this.password)
      // this.$store.commit('auth/setCurrentUser', user)
      // tem que salvar essa distancia numa store ( pode chamar filter store )
      // bem como os mercados aceitos
      this.visible = false
      // } else {
      // this.error = true
      // }
      this.loading = false
    }
  }
}
</script>
