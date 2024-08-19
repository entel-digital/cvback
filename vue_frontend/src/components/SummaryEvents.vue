<template>
  <div class="fit row wrap justify-center q-gutter-md">
    <q-card class="col card-small ">

      <div v-if="!eventStore.summaryEvents" class="text-center q-pa-md">
        <q-spinner color="primary" size="3em" />
      </div>
      <div v-else class="row q-py-md q-px-none">
        <q-card-section class="bg-white text-center q-py-sm" :style="Screen.lt.md ? 'width: 70px' : 'width: 130px'">
          <div class="barlow-bold text-dark" :class="Screen.lt.md ? 'fs-12-14': 'fs-16-19'">Total hoy</div>
          <div class="barlow-semibold q-pa-sm text-primary" :class="Screen.lt.md ? 'fs-18-23': 'fs-28-34'">
            {{ eventStore.summaryEvents.totalQueryEvents }}
          </div>
        </q-card-section>
        <q-card-section class="bg-white text-center q-py-sm" :style="Screen.lt.md ? 'width: 70px' : 'width: 130px'">
          <div class="barlow-bold text-dark" :class="Screen.lt.md ? 'fs-12-14': 'fs-16-19'">Total semana</div>
          <div class="barlow-semibold q-pa-sm text-primary" :class="Screen.lt.md ? 'fs-18-23': 'fs-28-34'">17</div>
        </q-card-section>
        <q-card-section class="bg-white text-center q-py-sm" :style="Screen.lt.md ? 'width: 70px' : 'width: 130px'">
          <div class="barlow-bold text-dark" :class="Screen.lt.md ? 'fs-12-14': 'fs-16-19'">Total mes</div>
          <div class="barlow-semibold q-pa-sm text-primary" :class="Screen.lt.md ? 'fs-18-23': 'fs-28-34'">20</div>
        </q-card-section>
        <q-card-section class="bg-white text-center q-py-sm" :style="Screen.lt.md ? 'width: 70px' : 'width: 130px'">
          <div class="barlow-bold text-dark" :class="Screen.lt.md ? 'fs-12-14': 'fs-16-19'">Total año</div>
          <div class="barlow-semibold q-pa-sm text-primary" :class="Screen.lt.md ? 'fs-18-23': 'fs-28-34'">24</div>
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
                  style="width: auto; padding: 0 10px"
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
                  style="width: auto; padding: 0 10px"
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
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import { defineComponent, ref, computed } from 'vue'
import { useEventsStore } from '@/stores/events'
import { useQuasar } from 'quasar';

export default defineComponent({
  name: 'SummaryEvents',
  setup(props) {
    const eventStore = useEventsStore()
    const labelToFilter = ref(null)
    const typeToFilter = ref(null)
    const Screen =  useQuasar().screen
    console.log("screen", Screen.lt.sm)

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
