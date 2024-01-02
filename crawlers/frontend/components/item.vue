<template>
  <v-card class="d-flex flex-column" width="35vw" >
    <v-chip style="border-radius: 0;" v-visible="item.tags.includes('mais em conta')" small color="green" text-color="white">MAIS EM CONTA</v-chip>
    <v-card-title>
      <v-row>
        R$ {{ item.preco }}
        <v-icon v-if="item.tags.includes('abaixo da média')" color="green">mdi-arrow-down</v-icon>
        <v-icon v-else-if="item.tags.includes('acima da média')" color="red">mdi-arrow-up</v-icon>
        <v-icon v-else color="yellow">mdi-minus</v-icon>
      </v-row>
    </v-card-title>
    <v-card-text style="text-align: left;">
      <v-row>
        {{item.produto.nome}}
      </v-row>
    </v-card-text>
    <v-spacer></v-spacer>
    <v-card-actions class="pa-0">
      <v-list-item>
        <v-row
          justify="end"
        >
          <v-btn v-visible="item.quantidade > 0" rounded x-small @click="removerItem()"><v-icon>mdi-minus</v-icon></v-btn>
          <span v-visible="item.quantidade > 0">{{item.quantidade}}</span>
          <v-btn rounded x-small @click="adicionarItem()"><v-icon>mdi-plus</v-icon></v-btn>
        </v-row>
      </v-list-item>
    </v-card-actions>
  </v-card>
</template>

<script>

export default {
  props: {
    item: Object
  },
  methods: {
    adicionarItem () {
      this.$emit('adicionar-item')
    },
    removerItem () {
      this.$emit('remover-item')
    }
  }
}
</script>
