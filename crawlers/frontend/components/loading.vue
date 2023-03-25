<template>
  <div>
    <v-layout
      :justify-center="center"
      column
      align-center
    >
      <v-progress-circular
        indeterminate
        :size="size || 50"
        color="secondary"
      />
      <p
        v-if="!!title"
        class="mt-3 text-xs-center fw-bold"
      >
        {{ title }}
      </p>
    </v-layout>
  </div>
</template>

<script>
export default {
  props: ['title', 'center', 'size']
}
</script>
