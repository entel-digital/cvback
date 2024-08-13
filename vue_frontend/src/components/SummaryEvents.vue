<template>
  <div class="fit row wrap justify-center q-gutter-lg">
    <q-card class="col card-small">
      <div v-if="!eventStore.summaryEvents" class="text-center q-pa-md">
        <q-spinner color="primary" size="3em" />
      </div>
      <div v-else class="fit row q-py-md">
        <q-card-section class="bg-white text-center q-py-sm" style="width: 130px">
          <div class="barlow-bold fs-16-19 text-dark">Total hoy</div>
          <div class="barlow-semibold fs-34-18 q-pa-sm text-primary">
            {{ eventStore.summaryEvents.totalQueryEvents }}
          </div>
        </q-card-section>
        <q-card-section class="bg-white text-center q-py-sm" style="width: 130px">
          <div class="barlow-bold fs-16-19 text-dark">Total semana</div>
          <div class="barlow-semibold fs-34-18 q-pa-sm text-primary">17</div>
        </q-card-section>
        <q-card-section class="bg-white text-center q-py-sm" style="width: 130px">
          <div class="barlow-bold fs-16-19 text-dark">Total mes</div>
          <div class="barlow-semibold fs-34-18 q-pa-sm text-primary">20</div>
        </q-card-section>
        <q-card-section class="bg-white text-center q-py-sm" style="width: 130px">
          <div class="barlow-bold fs-16-19 text-dark">Total año</div>
          <div class="barlow-semibold fs-34-18 q-pa-sm text-primary">24</div>
        </q-card-section>
      </div>
    </q-card>

    <q-card class="col">
      <q-card-section class="bg-white">
        <div class="barlow-bold fs-16-19 text-dark q-pb-md">Tipos de Etiquetas</div>

        <div style="max-height: 100px">
          <div v-if="!eventStore.summaryEvents">
            <q-spinner color="primary" size="3em" />
          </div>

          <div v-else class="q-gutter-x-sm row inline" style="width: 100%">
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

    <q-card class="col">
      <q-card-section class="bg-white">
        <div class="barlow-bold fs-16-19 text-dark q-pb-md">Tipos de Eventos</div>
        <div style="max-height: 100px">
          <div v-if="!eventStore.summaryEvents">
            <q-spinner color="primary" size="3em" />
          </div>

          <div v-else class="q-gutter-x-sm row inline" style="width: 100%">
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
    <q-card class="col">
      <q-card-section class="bg-white text-center">
        <div class="barlow-bold fs-16-19 text-dark">Filtros</div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import { defineComponent, ref, computed } from 'vue'
import { useEventsStore } from '@/stores/events'

export default defineComponent({
  name: 'SummaryEvents',
  setup(props) {
    const number = props.numberToShow
    const title = props.titleToShow
    const eventStore = ref(useEventsStore())
    const labelToFilter = ref({})
    const typeToFilter = ref({})

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
      if (labelToFilter.value.key === label.key) {
        labelToFilter.value = {}
      } else labelToFilter.value = label
    }
    const getType = (label) => {
      if (typeToFilter.value.key === label.key) {
        typeToFilter.value = {}
      } else typeToFilter.value = label
    }

    const getColor = (label, tofilter) => {
      if (!tofilter.key) {
        return 'primary'
      } else if (label === tofilter.key) {
        return 'primary'
      } else return 'blue-9'
    }

    return {
      number,
      title,
      eventStore,
      parseData,
      selection,
      getLabel,
      getType,
      getColor,
      labelToFilter,
      typeToFilter
    }
  }
})
</script>

<style lang="scss" scoped>
.card-small {
  max-height: 250px;
}
</style>
