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

            <div v-else style="width: 100%">
              <!-- <q-list class="q-pt-none" > -->
              <q-scroll-area style="width: 100%; height: 120px">
                <div class="full-width row wrap justify-evenly items-start content-start">
                  <q-item dense class="q-pb-sm text-center col-lg-6 col-md-6 col-sm-3 col-xs-3">
                    <q-item-section>
                      <q-item-section>
                        <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                          isFilled(eventStore.summaryEvents, 'queryTotalEventsDay')
                        }}</q-item-label>
                        <q-item-label caption class="q-mt-none barlow-bold text-dark">{{
                          datesSummary.today
                        }}</q-item-label>
                      </q-item-section>
                    </q-item-section>
                  </q-item>
                  <q-item dense class="q-pb-sm text-center col-lg-6 col-md-6 col-sm-3 col-xs-3">
                    <q-item-section>
                      <q-item-section>
                        <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                          isFilled(eventStore.summaryEvents, 'queryTotalEventsWeek')
                        }}</q-item-label>
                        <q-item-label caption class="q-mt-none barlow-bold text-dark">{{
                          datesSummary.week.start + ' - ' + datesSummary.week.end
                        }}</q-item-label>
                      </q-item-section>
                    </q-item-section>
                  </q-item>
                  <q-item dense class="q-pb-sm text-center col-lg-6 col-md-6 col-sm-3 col-xs-3">
                    <q-item-section>
                      <q-item-section>
                        <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                          isFilled(eventStore.summaryEvents, 'queryTotalEventsMonth')
                        }}</q-item-label>
                        <q-item-label caption class="q-mt-none barlow-bold text-dark"
                          >Mes {{ datesSummary.month }}</q-item-label
                        >
                      </q-item-section>
                    </q-item-section>
                  </q-item>
                  <q-item dense class="q-pb-sm text-center col-lg-6 col-md-6 col-sm-4 col-xs-4">
                    <q-item-section>
                      <q-item-section>
                        <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                          isFilled(eventStore.summaryEvents, 'queryTotalEventsYear')
                        }}</q-item-label>
                        <q-item-label caption class="q-mt-none barlow-bold text-dark">
                          Año {{ datesSummary.year }}</q-item-label
                        >
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
          <div class="barlow-bold fs-16-19 text-dark q-pb-md">
            Total Etiquetas
            <span
              ><q-icon size="22px" :name="isFiltered ? 'filter_list' : 'filter_list_off'"
            /></span>
          </div>

          <div style="max-height: 100px; max-width: 300px">
            <div v-if="!eventStore.summaryEvents">
              <q-spinner color="primary" size="3em" />
            </div>

            <div v-else class="row inline" style="width: 100%">
              <q-scroll-area style="height: 100px">
                <q-chip
                  v-for="label in allLabels"
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
          <div class="barlow-bold fs-16-19 text-dark q-pb-md">Total Tipo de Eventos</div>
          <div style="max-height: 100px; max-width: 300px">
            <div v-if="!eventStore.summaryEvents">
              <q-spinner color="primary" size="3em" />
            </div>

            <div v-else class="row inline" style="width: 100%">
              <q-scroll-area style="height: 100px">
                <q-chip
                  v-for="label in allTypes"
                  :key="label"
                  square
                  outline
                  :color="getColor(label.key, typeToFilter)"
                  class="barlow-bold fs-14-19"
                  style="width: fit-content"
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
          <div class="barlow-bold fs-16-19 text-dark q-pb-md text-left">
            Filtro de hora
            <span
              ><q-icon size="22px" :name="isFiltered ? 'filter_list' : 'filter_list_off'"
            /></span>
          </div>
          <div class="q-pa-md" style="max-width: 300px">
            <div class="row">
              <div
                class="col-6 p-2 border col-md-auto m-auto"
                style="cursor: pointer; min-width: 250px; text-align: left"
                @click="showCalendar()"
              >
                <span class="text-left">
                  <q-icon size="20px" color="blue-7" name="calendar_month" /> </span
                >{{ dateToDisplay }}
              </div>
              <div class="row mt-1 border" v-show="show.calendar">
                <Datepicker2
                  v-model="selectedDate"
                  @onSelect="showCalendar"
                  :next-prev-icon="true"
                  :last-month="todayDt"
                  :first-month="firstDt"
                  :enableSecondCalendar="true"
                  :disableDates="disableDates"
                  :disabledFromTo="disabledFromTo"
                  @filterByDate="filterDates"
                />
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>

    <!-- MOBILE VERSION -->
    <div class="lt-md q-pl-md">
      <q-list bordered class="fit justify-center rounded-borders">
        <q-expansion-item default-opened>
          <template v-slot:header>
            <q-item-section class="barlow-bold fs-16-19 text-dark"> Total eventos </q-item-section>
          </template>

          <q-card>
            <q-card-section class="fit row q-px-xs">
              <q-item dense class="q-pb-sm text-center col">
                <q-item-section>
                  <q-item-section>
                    <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                      isFilled(eventStore.summaryEvents, 'queryTotalEventsDay')
                    }}</q-item-label>
                    <q-item-label caption class="q-mt-none barlow-bold text-dark">{{
                      datesSummary.today
                    }}</q-item-label>
                  </q-item-section>
                </q-item-section>
              </q-item>
              <q-item dense class="q-pb-sm text-center col">
                <q-item-section>
                  <q-item-section>
                    <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                      isFilled(eventStore.summaryEvents, 'queryTotalEventsWeek')
                    }}</q-item-label>
                    <q-item-label caption class="q-mt-none barlow-bold text-dark">{{
                      datesSummary.week.start + ' - ' + datesSummary.week.end
                    }}</q-item-label>
                  </q-item-section>
                </q-item-section>
              </q-item>
              <q-item dense class="q-pb-sm text-center col">
                <q-item-section>
                  <q-item-section>
                    <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                      isFilled(eventStore.summaryEvents, 'queryTotalEventsMonth')
                    }}</q-item-label>
                    <q-item-label caption class="q-mt-none barlow-bold text-dark">
                      Mes {{ datesSummary.month }}</q-item-label
                    >
                  </q-item-section>
                </q-item-section>
              </q-item>
              <q-item dense class="q-pb-sm text-center col">
                <q-item-section>
                  <q-item-section>
                    <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                      isFilled(eventStore.summaryEvents, 'queryTotalEventsYear')
                    }}</q-item-label>
                    <q-item-label caption class="q-mt-none barlow-bold text-dark"
                      >Año {{ datesSummary.year }}</q-item-label
                    >
                  </q-item-section>
                </q-item-section>
              </q-item>
            </q-card-section>
          </q-card>
        </q-expansion-item>

        <q-separator />

        <q-expansion-item default-opened>
          <template v-slot:header>
            <q-item-section class="barlow-bold fs-16-19 text-dark">
              Total Etiquetas
            </q-item-section>
          </template>

          <q-card>
            <q-card-section>
              <q-chip
                v-for="label in allLabels"
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
        <q-expansion-item default-opened>
          <template v-slot:header>
            <q-item-section class="barlow-bold fs-16-19 text-dark">
              Total Tipo de Eventos
            </q-item-section>
          </template>

          <q-card>
            <q-card-section>
              <q-chip
                v-for="label in allTypes"
                :key="label"
                square
                outline
                :color="getColor(label.key, typeToFilter)"
                class="barlow-bold fs-14-19"
                style="width: fit-content"
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

        <!-- <q-expansion-item>
        <template v-slot:header>
          <q-item-section class="barlow-bold fs-16-19 text-dark">
           Filtro por fecha
          </q-item-section>
        </template>

        <q-card>
          <q-card-section>

          </q-card-section>
        </q-card>
      </q-expansion-item> -->
      </q-list>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, computed } from 'vue'
import { useEventsStore } from '@/stores/events'
import { useQuasar, date } from 'quasar'
import Datepicker2 from '@/components/Datepicker2.vue'

export default defineComponent({
  name: 'SummaryEvents',
  components: {
    Datepicker2
  },
  setup(props) {
    const eventStore = useEventsStore()
    const labelToFilter = ref(null)
    const typeToFilter = ref(null)
    const Screen = useQuasar().screen
    const show = ref({
      calendar: false
    })

    const todayDt = ref(null)
    const firstDt = ref(null)
    const selectedDate = ref([null, null])
    const disabledFromTo = ref({
      from: moment('2019-01-01'),
      to: moment('2024-06-30')
    })

    const dateToDisplay = computed(() => {
      if (selectedDate.value.lenght > 1) {
        return (
          date.formatDate(moment(selectedDate.value[0]), 'DD/MM/YYYY') +
          ' - ' +
          date.formatDate(moment(selectedDate.value[1]), 'DD/MM/YYYY')
        )
      } else return ''
    })

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
      if (labelToFilter.value?.value === label.value) {
        labelToFilter.value = null
        eventStore.labelsSelected = null
      } else {
        labelToFilter.value = label
        eventStore.labelsSelected = label.id.toString()
      }
    }
    const getType = (type) => {
      if (typeToFilter.value.value === type.value) {
        typeToFilter.value = null
      } else typeToFilter.value = type
      eventStore.typesSelected = type.id.toString()
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
    }

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

    const isFiltered = computed(() => {
      if (eventStore.summaryEvents) {
        return eventStore.summaryEvents.filtered
      } else return false
    })

    const isFilled = (value, data) => {
      return value ? value[data] : 0
    }

    const allLabels = computed(() => {
      return eventStore.summaryEvents ? eventStore.summaryEvents.labelsSummary : []
    })
    const allTypes = computed(() => {
      return eventStore.summaryEvents ? eventStore.summaryEvents.typesSummary : []
    })

    const showCalendar = () => {
      show.value.calendar = !show.value.calendar
    }

    const disableDates = computed(() => {
      let dt = []
      let sd = moment('2019-06-01').startOf()
      let ed = moment('2024-07-01').startOf()
      while (sd.isSameOrBefore(ed)) {
        dt.push(sd.clone())
        sd.add(1, 'days')
      }
      return dt
    })

    const convertToDate = (mydate) => {
      const [day, month, year] = mydate.date.split('/')

      const dateTimeLocal = new Date(year, month - 1, day, mydate.time.hour, mydate.time.min, 0)

      const finalDateTime = dateTimeLocal.toISOString()

      // const [day, month, year] = mydate.date.split('/')

      // // Crear el objeto Date en la zona horaria del navegador
      // const dateTimeLocal = new Date(year, month - 1, day, mydate.time.hour, mydate.time.min, 0)

      // // Obtener el offset dinámico del navegador en minutos y convertirlo a milisegundos
      // const timezoneOffsetMs = dateTimeLocal.getTimezoneOffset() * 60 * 1000
      // const utcDate = new Date(dateTimeLocal.getTime() - timezoneOffsetMs)

      // // Obtener el offset del navegador en formato ±HH:mm
      // const offset = -dateTimeLocal.getTimezoneOffset() // en minutos
      // const offsetHours = Math.floor(Math.abs(offset) / 60)
      // const offsetMinutes = Math.abs(offset) % 60
      // const offsetSign = offset >= 0 ? '+' : '-'
      // const formattedOffset = `${offsetSign}${String(offsetHours).padStart(2, '0')}:${String(
      //   offsetMinutes
      // ).padStart(2, '0')}`

      // // Obtener la cadena ISO sin 'Z' y agregar el offset dinámico correctamente
      // const finalDateTime = `${utcDate.toISOString().slice(0, -1)}${formattedOffset}`
      return finalDateTime
    }

    const filterDates = (data) => {
      const dateToFilter = {
        from: convertToDate(data.start),
        to: convertToDate(data.end)
      }
      console.log('dateToFilter', dateToFilter)
      eventStore.dateSelected = dateToFilter
      
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
      Screen,
      datesSummary,
      isFiltered,
      isFilled,
      allLabels,
      allTypes,
      showCalendar,
      disableDates,
      show,
      todayDt,
      firstDt,
      selectedDate,
      disabledFromTo,
      dateToDisplay,
      filterDates
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
