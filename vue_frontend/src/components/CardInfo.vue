<template>
  <q-card class="my-card">
    <q-card-section class="bg-white text-green">
      <div class="text-h6">{{ number }}</div>
      <div class="text-subtitle2">{{ title }}</div>
    </q-card-section>

    <q-separator />
  </q-card>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'CardInfo',
  props: {
    numberToShow: {
      type: String,
      required: true
    },
    titleToShow: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const number = props.numberToShow
    const title = props.titleToShow
    return {
      number,
      title
    }
  }
})
</script>

<style lang="sass" scoped>
.my-card
  width: 100%
  max-width: 250px
</style>
