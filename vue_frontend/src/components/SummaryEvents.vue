<template>
  <div class="fit row wrap justify-center q-gutter-md">
    <q-card class="col card-small">
      <div v-if="!eventStore.summaryEvents" class="text-center q-pa-md">
        <q-spinner color="primary" size="3em" />
      </div>
      <div v-else class="row justify-around">
        <q-card-section class="bg-white text-center q-py-none" :style="Screen.lt.lg ? 'width: 70px' : 'width: 130px'">
          <div class="barlow-bold text-dark" :class="Screen.lt.lg ? 'fs-12-14': 'fs-16-19'">Total hoy</div>
          <div class="barlow-semibold q-pa-sm text-primary" :class="Screen.lt.lg ? 'fs-18-23': 'fs-28-34'">
            {{ eventStore.summaryEvents.queryTotalEventsDay }}
          </div>
        </q-card-section>
        <q-card-section class="bg-white text-center q-py-none" :style="Screen.lt.lg ? 'width: 70px' : 'width: 130px'">
          <div class="barlow-bold text-dark" :class="Screen.lt.lg ? 'fs-12-14': 'fs-16-19'">Total semana</div>
          <div class="barlow-semibold q-pa-sm text-primary" :class="Screen.lt.lg ? 'fs-18-23': 'fs-28-34'">
            {{ eventStore.summaryEvents.queryTotalEventsWeek }}
          </div>
        </q-card-section>
        <q-card-section class="bg-white text-center  q-py-none" :style="Screen.lt.lg ? 'width: 70px' : 'width: 130px'">
          <div class="barlow-bold text-dark" :class="Screen.lt.lg ? 'fs-12-14': 'fs-16-19'">Total mes</div>
          <div class="barlow-semibold q-pa-sm text-primary" :class="Screen.lt.lg ? 'fs-18-23': 'fs-28-34'">
            {{ eventStore.summaryEvents.queryTotalEventsMonth }}
          </div>
        </q-card-section>
        <q-card-section class="bg-white text-center  q-py-none" :style="Screen.lt.lg ? 'width: 70px' : 'width: 130px'">
          <div class="barlow-bold text-dark" :class="Screen.lt.lg ? 'fs-12-14': 'fs-16-19'">Total año</div>
          <div class="barlow-semibold q-pa-sm text-primary" :class="Screen.lt.lg ? 'fs-18-23': 'fs-28-34'">
            {{ eventStore.summaryEvents.queryTotalEventsYear }}
          </div>
        </q-card-section>
      </div>
    </q-card>

    <q-card :class="Screen.lt.md ? 'row': 'col card-small'">
      <q-card-section class="bg-white">
        <div class="gt-sm barlow-bold fs-16-19 text-dark q-pb-md">Tipos de Etiquetas</div>
        <div class="lt-md barlow-bold fs-12-14 text-dark q-pb-md">Tipos de Etiquetas</div>

        <div style="max-height: 100px; max-width: 300px;">
          <div v-if="!eventStore.summaryEvents">
            <q-spinner color="primary" size="3em" />
          </div>

          <div v-else class=" row inline" style="width: 100%">
            <q-scroll-area style="height: 100px">
              <q-chip
                v-for="label in eventStore.summaryEvents.labelsSummary"
                :key="label"
                square
                outline
                clickable
                :color="getColor(label.key, labelToFilter)"
                class="barlow-bold fs-14-19"
                style="width: fit-content"
                @click="getLabel(label)"
              >
                <q-avatar
                  :color="getColor(label.key, labelToFilter)"
                  size="2em"
                  text-color="white"
                  font-size="14px"
                  class="barlow-bold"
                  style="width: auto; padding: 0 15px"
                >
                  {{ label.value }}
                </q-avatar>
                {{ label.key }}
              </q-chip>
            </q-scroll-area>
          </div>
        </div>
      </q-card-section>
    </q-card>


    <q-card :class="Screen.lt.md ? 'row': 'col card-small'">
      <q-card-section class="bg-white">
        <div class="gt-sm barlow-bold fs-16-19 text-dark q-pb-md">Tipos de Eventos</div>
        <div class="lt-md barlow-bold fs-12-14 text-dark q-pb-md">Tipos de Eventos</div>
        <div style="max-height: 100px; max-width: 300px;">
          <div v-if="!eventStore.summaryEvents">
            <q-spinner color="primary" size="3em" />
          </div>

          <div v-else class="row inline" style="width: 100%">
            <q-scroll-area style="height: 100px">
              <q-chip
                v-for="label in eventStore.summaryEvents.typesSummary"
                :key="label"
                square
                outline
                clickable
                :color="getColor(label.key, typeToFilter)"
                class="barlow-bold fs-14-19"
                style="width: fit-content"
                @click="getType(label)"
              >
                <q-avatar
                  :color="getColor(label.key, typeToFilter)"
                  size="2em"
                  text-color="white"
                  font-size="14px"
                  class="barlow-bold"
                  style="width: auto; padding: 0 15px"
                >
                  {{ label.value }}
                </q-avatar>
                {{ label.key }}
              </q-chip>
            </q-scroll-area>
          </div>
        </div>
      </q-card-section>
    </q-card>
    <q-card :class="Screen.lt.md ? 'row': 'col card-small'">
      <q-card-section class="bg-white text-center">
        <div class="gt-sm barlow-bold fs-16-19 text-dark q-pb-md">Filtros</div>
        <div class="lt-md barlow-bold fs-12-14 text-dark q-pb-md">Filtros</div>
         <!-- <DateTimePicker /> -->
          <!-- <Picker /> -->
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import { defineComponent, ref, computed } from 'vue'
import { useEventsStore } from '@/stores/events'
import { useQuasar } from 'quasar';

import DateTimePicker from '@/components/DateTimePicker.vue';
import Picker from '@/components/Picker.vue';

export default defineComponent({
  name: 'SummaryEvents',
  components: {
    // DateTimePicker
    Picker
  },
  setup(props) {
    const eventStore = useEventsStore()
    const labelToFilter = ref(null)
    const typeToFilter = ref(null)
    const Screen =  useQuasar().screen

    const parseData = (data) => {
      const replaces = data.replace(/\\\"/g, '"').slice(1, -1)
      return JSON.parse(replaces)
    }
    const selection = computed(() => {
      return Object.keys(desert)
        .filter((type) => desert[type] === true)
        .join(', ')
    })

    const getLabel = (label) => {
      if (labelToFilter.value?.key === label.key) {
        labelToFilter.value = null
        eventStore.labelsSelected = null
      } else {
        labelToFilter.value = label
        eventStore.labelsSelected = label.key
      }
    }
    const getType = (label) => {
      if (typeToFilter.value.key === label.key) {
        typeToFilter.value = null
      } else typeToFilter.value = label
      eventStore.typesSelected = label.key
    }

    const getColor = (label, tofilter) => {
      if (!tofilter) {
        return 'primary'
      } else if (label === tofilter.key) {
        return 'primary'
      } else return 'blue-9'
    }

    return {
      eventStore,
      parseData,
      selection,
      getLabel,
      getType,
      getColor,
      labelToFilter,
      typeToFilter,
      Screen
    }
  }
})
</script>

<style lang="scss" scoped>
.card-small {
  max-height: 250px;
}
.q-card__section.q-card__section--vert.bg-white{
 padding: 16px 4px
}
</style>
