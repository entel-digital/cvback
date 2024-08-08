<template>
  <div class="row wrap justify-center q-gutter-lg">
    <q-card class="card-small row">
      <q-card-section class="bg-white text-center">
        <div class="barlow-bold fs-16-19 text-dark">Total eventos</div>

        <div v-if="!eventStore.summaryEvents">
          <q-spinner color="primary" size="3em" />
        </div>
        <div v-else>
          <div class="barlow-semibold fs-44-46 q-pa-sm text-primary">
            {{ eventStore.summaryEvents.totalQueryEvents }}
          </div>
        </div>
      </q-card-section>
    </q-card>

    <q-card class="card-small row">
      <q-card-section class="bg-white">
        <div class="barlow-bold fs-16-19 text-dark q-pb-lg">Tipos de Etiquetas</div>

        <div v-if="!eventStore.summaryEvents">
          <q-spinner color="primary" size="3em" />
        </div>
        <div v-else class="q-gutter-sm">
          <q-list dense class="no-padding no-margin" >
            <q-scroll-area style="height: 100px; ">

              <div v-for="label in eventStore.summaryEvents.labelsSummary" :key="label">
                <q-chip square outline color="primary">
                  <q-avatar color="primary" text-color="white" class="barlow-bold fs-18-23">{{
                    label.value
                  }}</q-avatar>
                  <span class="barlow-bold fs-16-19"> {{ label.key }}</span>
                </q-chip>

              </div>
            </q-scroll-area>

          </q-list>
        </div>
      </q-card-section>
    </q-card>

    <q-card class="card-small row">
      <q-card-section class="bg-white">
        <div class="barlow-bold fs-16-19 text-dark q-pb-lg">Tipos de Eventos</div>

        <div v-if="!eventStore.summaryEvents">
          <q-spinner color="primary" size="3em" />
        </div>
        <div v-else class="q-gutter-sm">
          <q-list dense class="no-padding no-margin" >
            <q-scroll-area style="height: 100px; ">

              <div v-for="label in eventStore.summaryEvents.typesSummary" :key="label">
                <q-chip square outline color="primary">
                  <q-avatar color="primary" text-color="white" class="barlow-bold fs-18-23">{{
                    label.value
                  }}</q-avatar>
                  <span class="barlow-bold fs-16-19"> {{ label.key }}</span>
                </q-chip>

              </div>
            </q-scroll-area>

          </q-list>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'
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
  min-width: 200px;
  max-width: 350px;
  max-height: 200px;
  // max-width: fit-content;
}
.card-large {
  width: 100%;
  max-width: 400px;
}
</style>
