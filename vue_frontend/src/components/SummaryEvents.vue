<template>
  <div>
  <div class="gt-sm fit row wrap justify-center q-gutter-md">
    <q-card class="col card-small">
      <q-card-section class="bg-white">
        <div class="barlow-bold fs-16-19 text-dark q-pb-sm">Total Eventos</div>

        <div style="max-height: 100px; max-width: 300px">
          <div v-if="!eventStore.summaryEvents">
            <q-spinner color="primary" size="3em" />
          </div>

          <div v-else  style="width: 100%">
            <!-- <q-list class="q-pt-none" > -->
              <q-scroll-area style="width: 100% ; height: 120px">
                <div class="full-width row wrap justify-evenly items-start content-start">
              <q-item dense class="q-pb-sm text-center col-lg-6 col-md-6 col-sm-3 col-xs-3" >
                <q-item-section>
                  <q-item-section>
                    <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                      eventStore.summaryEvents.queryTotalEventsDay
                    }}</q-item-label>
                    <q-item-label caption class="q-mt-none barlow-bold text-dark">{{
                      datesSummary.today
                    }}</q-item-label>
                  </q-item-section>
                </q-item-section>
              </q-item>
              <q-item dense class="q-pb-sm text-center col-lg-7 col-md-7 col-sm-4 col-xs-4" >
                <q-item-section>
                  <q-item-section>
                    <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                      eventStore.summaryEvents.queryTotalEventsWeek
                    }}</q-item-label>
                    <q-item-label caption class="q-mt-none barlow-bold text-dark">{{
                      datesSummary.week.start + ' - ' + datesSummary.week.end
                    }}</q-item-label>
                  </q-item-section>
                </q-item-section>
              </q-item>
              <q-item dense class="q-pb-sm text-center col-lg-6 col-md-6 col-sm-3 col-xs-3" >
                <q-item-section>
                  <q-item-section>
                    <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                      eventStore.summaryEvents.queryTotalEventsMonth
                    }}</q-item-label>
                    <q-item-label caption class="q-mt-none barlow-bold text-dark">Mes {{
                      datesSummary.month
                    }}</q-item-label>
                  </q-item-section>
                </q-item-section>
              </q-item>
              <q-item dense class="q-pb-sm text-center col-lg-6 col-md-6 col-sm-4 col-xs-4" >
                <q-item-section>
                  <q-item-section>
                    <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                      eventStore.summaryEvents.queryTotalEventsYear
                    }}</q-item-label>
                    <q-item-label caption class="q-mt-none barlow-bold text-dark"> Año {{
                      datesSummary.year
                    }}</q-item-label>
                  </q-item-section>
                </q-item-section>
              </q-item>
          </div>
          </q-scroll-area>
          </div>
        </div>
      </q-card-section>
    </q-card>
    <q-card class="col card-small">
      <q-card-section class="bg-white">
        <div class="barlow-bold fs-16-19 text-dark q-pb-md">Tipos de Etiquetas</div>

        <div style="max-height: 100px; max-width: 300px">
          <div v-if="!eventStore.summaryEvents">
            <q-spinner color="primary" size="3em" />
          </div>

          <div v-else class="row inline" style="width: 100%">
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

    <q-card class="col card-small">
      <q-card-section class="bg-white">
        <div class="barlow-bold fs-16-19 text-dark q-pb-md">Tipos de Eventos</div>
        <div style="max-height: 100px; max-width: 300px">
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
    <q-card class="col card-small">
      <q-card-section class="bg-white text-center">
        <div class="barlow-bold fs-16-19 text-dark q-pb-md">Filtros</div>
        <!-- <DateTimePicker /> -->
        <!-- <Picker /> -->
      </q-card-section>
    </q-card>
  </div>
  <div class="lt-md q-pl-md ">
    <q-list bordered class="fit justify-center rounded-borders">
      <q-expansion-item>
        <template v-slot:header>
          <q-item-section class="barlow-bold fs-16-19 text-dark">
            Total eventos
          </q-item-section>
        </template>

        <q-card>
          <q-card-section class="fit row q-px-xs">
            <q-item dense class="q-pb-sm text-center col" >
                <q-item-section>
                  <q-item-section>
                    <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                      eventStore.summaryEvents.queryTotalEventsDay
                    }}</q-item-label>
                    <q-item-label caption class="q-mt-none barlow-bold text-dark">{{
                      datesSummary.today
                    }}</q-item-label>
                  </q-item-section>
                </q-item-section>
              </q-item>
              <q-item dense class="q-pb-sm text-center col " >
                <q-item-section>
                  <q-item-section>
                    <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                      eventStore.summaryEvents.queryTotalEventsWeek
                    }}</q-item-label>
                    <q-item-label caption class="q-mt-none barlow-bold text-dark">{{
                      datesSummary.week.start + ' - ' + datesSummary.week.end
                    }}</q-item-label>
                  </q-item-section>
                </q-item-section>
              </q-item>
              <q-item dense class="q-pb-sm text-center col " >
                <q-item-section>
                  <q-item-section>
                    <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                      eventStore.summaryEvents.queryTotalEventsMonth
                    }}</q-item-label>
                    <q-item-label caption class="q-mt-none barlow-bold text-dark"> Mes {{
                      datesSummary.month
                    }}</q-item-label>
                  </q-item-section>
                </q-item-section>
              </q-item>
              <q-item dense class="q-pb-sm text-center col " >
                <q-item-section>
                  <q-item-section>
                    <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                      eventStore.summaryEvents.queryTotalEventsYear
                    }}</q-item-label>
                    <q-item-label caption class="q-mt-none barlow-bold text-dark">Año {{
                      datesSummary.year
                    }}</q-item-label>
                  </q-item-section>
                </q-item-section>
              </q-item>
          </q-card-section>
        </q-card>
      </q-expansion-item>

      <q-separator />

      <q-expansion-item>
        <template v-slot:header>
          <q-item-section class="barlow-bold fs-16-19 text-dark">
            Tipos de Etiquetas
          </q-item-section>
        </template>

        <q-card>
          <q-card-section>
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
          </q-card-section>
        </q-card>
      </q-expansion-item>

      <q-separator />
      <q-expansion-item>
        <template v-slot:header>
          <q-item-section class="barlow-bold fs-16-19 text-dark">
            Tipos de Eventos
          </q-item-section>
        </template>

        <q-card>
          <q-card-section>
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
          </q-card-section>
        </q-card>
      </q-expansion-item>

      <q-separator />

      <q-expansion-item>
        <template v-slot:header>
          <q-item-section class="barlow-bold fs-16-19 text-dark">
           Filtro por fecha
          </q-item-section>
        </template>

        <q-card>
          <q-card-section>

          </q-card-section>
        </q-card>
      </q-expansion-item>
    </q-list>
  </div>
</div>
</template>

<script>
import { defineComponent, ref, computed } from 'vue'
import { useEventsStore } from '@/stores/events'
import { useQuasar, date } from 'quasar'
import DateTimePicker from '@/components/DateTimePicker.vue'

export default defineComponent({
  name: 'SummaryEvents',
  components: {
    // DateTimePicker
  },
  setup(props) {
    const eventStore = useEventsStore()
    const labelToFilter = ref(null)
    const typeToFilter = ref(null)
    const Screen = useQuasar().screen

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
    const formattingDates = {
      months: [
        'Enero',
        'Febrero',
        'Marzo',
        'Abril',
        'Mayo',
        'Junio',
        'Julio',
        'Agosto',
        'Septiembre',
        'Octubre',
        'Noviembre',
        'Diciembre'
      ],
      monthsShort: [
        'Ene',
        'Feb',
        'Mar',
        'Abr',
        'May',
        'Jun',
        'Jul',
        'Ago',
        'Sep',
        'Oct',
        'Nov',
        'Dic'
      ]
    }
    const getWeekBounds = (dateInput) => {
      const startOfWeek = date.startOfDate(
        date.subtractFromDate(dateInput, { days: (date.getDayOfWeek(dateInput) + 6) % 7 }),
        'day'
      )

      const endOfWeek = date.addToDate(startOfWeek, { days: 6 })

      return {
        startOfWeek,
        endOfWeek
      }
    };

    const datesSummary = computed(() => {
      return {
        today: date.formatDate(new Date(), 'DD MMMM', formattingDates),
        week: {
          start: date.formatDate(getWeekBounds(new Date()).startOfWeek, 'DD MMM', formattingDates),
          end: date.formatDate(getWeekBounds(new Date()).endOfWeek, 'DD MMM', formattingDates)
        },
        month: date.formatDate(new Date(), 'MMMM', formattingDates),
        year: date.formatDate(new Date(), 'YYYY')
      }
    })

    return {
      eventStore,
      parseData,
      selection,
      getLabel,
      getType,
      getColor,
      labelToFilter,
      typeToFilter,
      Screen,
      datesSummary
    }
  }
})
</script>

<style lang="scss" scoped>
.card-small {
  max-height: 250px;
}
.q-card__section.q-card__section--vert.bg-white {
  padding: 16px 4px;
}
</style>
