<template>
  <div class="fit row q-gutter-md">
    <q-card class="my-card">
      <q-card-section class="bg-white">
        <div v-if="!eventStore.summaryEvents">
          <q-spinner color="primary" size="3em" />
        </div>
        <div v-else>
          <div class="barlow-semibold fs-28-34 q-pa-md">
            {{ eventStore.summaryEvents.totalEvents }}
          </div>
        </div>
        <div class="barlow-bold fs-21-25 text-dark">Total eventos</div>
      </q-card-section>

      <q-separator />
    </q-card>
    <q-card class="my-card">
      <q-card-section class="bg-white">
        <div v-if="!eventStore.summaryEvents">
          <q-spinner color="primary" size="3em" />
        </div>
        <div v-else>
          <div class="barlow-semibold fs-28-34 q-pa-md">
            {{ eventStore.summaryEvents.queryTotalEvents }}
          </div>
        </div>
        <div class="barlow-bold fs-21-25 text-dark">Total eventos mostrando</div>
      </q-card-section>

      <q-separator />
    </q-card>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useEventsStore } from '@/stores/events'

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
    const eventStore = useEventsStore()

    const parseData = (data) => {
      const replaces = data.replace(/\\\"/g, '"').slice(1, -1)
      return JSON.parse(replaces)
    }

    return {
      number,
      title,
      eventStore,
      parseData
    }
  }
})
</script>

<style lang="sass" scoped>
.my-card
  width: 100%
</style>
