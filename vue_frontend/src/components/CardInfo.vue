<template>
  <div class="fit row q-gutter-md">
    <!-- <q-card class="card-small">
      <q-card-section class="bg-white">
        <div v-if="!eventStore.summaryEvents">
          <q-spinner color="primary" size="3em" />
        </div>
        <div v-else>
          <div class="barlow-semibold fs-28-34 q-pa-md text-primary">
            {{ eventStore.summaryEvents.totalEvents }}
          </div>
        </div>
        <div class="barlow-bold fs-16-19 text-primary">Total eventos</div>
      </q-card-section>
    </q-card> -->

    <q-card class="card-small">
      <q-card-section class="bg-white">
        <div v-if="!eventStore.summaryEvents">
          <q-spinner color="primary" size="3em" />
        </div>
        <div v-else>
          <div class="barlow-semibold fs-28-34 q-pa-md text-primary">
            {{ eventStore.summaryEvents.totalQueryEvents }}
          </div>
        </div>
        <div class="barlow-bold fs-16-19 text-primary">Total eventos</div>
      </q-card-section>
    </q-card>

    <q-card class="card-large row">
      <q-card-section class="bg-white" style="max-width: 150px">
        <div v-if="!eventStore.summaryEvents">
          <q-spinner color="primary" size="3em" />
        </div>
        <div v-else>
          <div class="barlow-semibold fs-28-34 q-pa-md text-positive">
            {{
              eventStore.summaryEvents.labelsSummary.total -
              eventStore.summaryEvents.labelsSummary.no_cumple
            }}
          </div>

        </div>
        <div class="barlow-bold fs-16-19 text-positive">Cumple</div>
      </q-card-section>
      <q-card-section class="bg-white" style="max-width: 150px">
        <div v-if="!eventStore.summaryEvents">
          <q-spinner color="primary" size="3em" />
        </div>
        <div v-else>
          <div class="barlow-semibold fs-28-34 q-pa-md text-negative">
            {{ eventStore.summaryEvents.totalQueryEvents }}
          </div>
        </div>
        <div class="barlow-bold fs-16-19 text-negative">No cumple</div>
      </q-card-section>
    </q-card>

    <q-card class="card-large row">
      <q-card-section class="bg-white" style="max-width: 150px">
        <div v-if="!eventStore.summaryEvents">
          <q-spinner color="primary" size="3em" />
        </div>
        <div v-else>
          <div class="barlow-semibold fs-28-34 q-pa-md text-positive">
            {{
              eventStore.summaryEvents.labelsSummary.total -
              eventStore.summaryEvents.labelsSummary.no_cumple
            }}
          </div>
        </div>
        <div class="barlow-bold fs-16-19 text-positive">Total Cumple mostrando</div>
      </q-card-section>
      <q-card-section class="bg-white" style="max-width: 150px">
        <div v-if="!eventStore.summaryEvents">
          <q-spinner color="primary" size="3em" />
        </div>
        <div v-else>
          <div class="barlow-semibold fs-28-34 q-pa-md text-negative">
            {{ eventStore.summaryEvents.totalQueryEvents }}
          </div>
        </div>
        <div class="barlow-bold fs-16-19 text-negative">Total No cumple mostrando</div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import { defineComponent , ref} from 'vue'
import { useEventsStore } from '@/stores/events'

export default defineComponent({
  name: 'CardInfo',
  setup(props) {
    const number = props.numberToShow
    const title = props.titleToShow
    const eventStore = ref(useEventsStore())

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

<style lang="scss" scoped>
.card-small {
  width: 100%;
  max-width: 200px;
}
.card-large {
  width: 100%;
  max-width: 400px;
}
</style>
