<template>
  <div>
    <div class="gt-md fit row wrap justify-center q-gutter-md">
      <q-card v-for="date in datesSummary" :key="date" style="width: 100%; max-width: 300px">
        <q-item dense class="q-pb-sm text-center" style="width: 100%; max-width: 300px">
          <q-item-section>
            <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">
              {{ hasValue(date.queryName) }}
            </q-item-label>
            <q-item-label class="q-mt-none barlow-bold text-dark">{{ date.label }}</q-item-label>
            <q-item-label caption class="q-mt-none barlow-bold text-dark">
              {{ date.value }}
            </q-item-label>
          </q-item-section>
        </q-item>
      </q-card>
      <!-- <q-card class="col card-small">
        <q-card-section class="bg-white">
          <div class="barlow-bold fs-16-19 text-dark q-pb-sm">Total Eventos</div>

          <div style="max-height: 100px; max-width: 300px">
            <div v-if="!eventStore.summaryEvents">
              <q-spinner color="primary" size="3em" />
            </div>

            <div v-else style="width: 100%">
              <q-scroll-area style="width: 100%; height: 120px">
                <div class="full-width row wrap justify-evenly items-start content-start">
                  <q-item dense class="q-pb-sm text-center col-lg-6 col-md-6 col-sm-3 col-xs-3">
                    <q-item-section>
                      <q-item-section>
                        <q-item-label class="barlow-semibold q-px-sm text-primary fs-23-28">{{
                          hasValue(eventStore.summaryEvents, 'queryTotalEventsDay')
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
                          hasValue(eventStore.summaryEvents, 'queryTotalEventsWeek')
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
                          hasValue(eventStore.summaryEvents, 'queryTotalEventsMonth')
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
                          hasValue(eventStore.summaryEvents, 'queryTotalEventsYear')
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
      </q-card> -->
      <q-card class="col card-small">
        <q-card-section class="bg-white">
          <div class="barlow-bold fs-16-19 text-dark q-pb-md">
            Total Etiquetas
            <span class="q-px-sm"
              ><q-icon size="22px" :name="isFilterByLabel ? 'filter_list' : 'filter_list_off'"
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
              ><q-icon size="22px" :name="isFilterByDate ? 'filter_list' : 'filter_list_off'"
            /></span>
          </div>
          <div class="q-pa-md" style="max-width: 300px">
            <div class="row">
              <div
                class="col-6 p-2 border col-md-auto q-px-sm"
                style="cursor: pointer; width: fit-content; min-width: 300px; text-align: left"
                @click="showCalendar()"
              >
                <span class="text-left q-pr-md">
                  <q-icon size="20px" color="blue-7" name="calendar_month" />
                </span>
                {{ dateToDisplay }}
              </div>
              <div class="row mt-1 border" v-show="show.calendar" style="z-index: 10">
                <Datepicker
                  v-model="selectedDate"
                  @onSelect="showCalendar"
                  :next-prev-icon="true"
                  :last-month="todayDt"
                  :first-month="firstDt"
                  :enableSecondCalendar="true"
                  :disableDates="disableDates"
                  :disabledFromTo="disabledFromTo"
                  :dateFromStore="eventStore.dateSelected"
                  @filterByDate="filterDates"
                />
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>

    <!-- MOBILE VERSION -->
    <div class="lt-lg q-pl-md">
      <div class="fit row justify-center q-gutter-md">
        <q-card
          v-for="date in datesSummary"
          :key="date"
          class="fit row"
          style="width: fit-content; max-width: 150px"
        >
          <q-item
            dense
            class="q-pb-sm fit justify-between q-px-xs"
            style="width: fit-content; max-width: 150px"
          >
            <q-item-section class="no-padding" style="min-height: 50px; height: 50px">
              <q-item-label class="q-mt-none barlow-bold text-dark fs-12-14">{{
                date.label
              }}</q-item-label>
              <q-item-label class="q-mt-none barlow text-dark fs-10-12">{{
                date.value
              }}</q-item-label>
            </q-item-section>
            <q-item-section>
              <q-item-label class="barlow-semibold q-px-sm text-primary fs-18-23 ellipsis">
                {{ hasValue(date.queryName) }}
                <q-tooltip>
                  {{ hasValue(date.queryName) }}
                </q-tooltip>
              </q-item-label>
            </q-item-section>
          </q-item>
        </q-card>
      </div>
      <q-card class="card-small q-mt-sm">
        <q-card-section class="bg-white">
          <div class="barlow-bold fs-12-14 text-dark q-pb-md q-pl-md">
            Total Etiquetas
            <span
              ><q-icon size="18px" :name="isFilterByLabel ? 'filter_list' : 'filter_list_off'"
            /></span>
          </div>

          <div style="max-height: 100px; max-width: 300px">
            <div v-if="!eventStore.summaryEvents" class="q-pl-md">
              <q-spinner color="primary" size="2em" />
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
                  class="barlow-bold fs-12-14"
                  style="width: fit-content"
                  @click="getLabel(label)"
                >
                  <q-avatar
                    :color="getColor(label.key, labelToFilter)"
                    size="2em"
                    text-color="white"
                    font-size="12px"
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

      <q-card class="card-small q-mt-sm">
        <q-card-section class="bg-white">
          <div class="barlow-bold fs-12-14 text-dark q-pb-md q-pl-md">Total Eventos</div>

          <div style="max-height: 100px; max-width: 300px">
            <div v-if="!eventStore.summaryEvents" class="q-pl-md">
              <q-spinner color="primary" size="2em" />
            </div>

            <div v-else class="row inline" style="width: 100%">
              <q-scroll-area style="height: 100px">
                <q-chip
                  v-for="label in allTypes"
                  :key="label"
                  square
                  outline
                  clickable
                  :color="getColor(label.key, typeToFilter)"
                  class="barlow-bold fs-12-14"
                  style="width: fit-content"
                  @click="getLabel(label)"
                >
                  <q-avatar
                    :color="getColor(label.key, typeToFilter)"
                    size="2em"
                    text-color="white"
                    font-size="12px"
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

      <q-card class="col card-small q-mt-sm">
        <q-card-section class="bg-white text-center">
          <div class="barlow-bold fs-12-14 text-dark q-pb-xs text-left q-pl-md">
            Filtro de hora
            <span
              ><q-icon size="18px" :name="isFilterByDate ? 'filter_list' : 'filter_list_off'"
            /></span>
          </div>
          <div class="q-pa-md" style="max-width: 300px">
            <div class="row no-padding">
              <div
                class="col-6 p-1 border q-px-sm q-py-none"
                style="cursor: pointer; width: fit-content; min-width: 280px; text-align: left"
                @click="showCalendar()"
              >
                <span class="text-left q-pr-md q-pl-sm">
                  <q-icon size="18px" color="blue-7" name="calendar_month" />
                </span>
                {{ dateToDisplay }}
              </div>
              <div class="row mt-1 border" v-show="show.calendar" style="z-index: 5">
                <Datepicker
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
  </div>
</template>

<script>
import { defineComponent, ref, computed } from 'vue'
import { useEventsStore } from '@/stores/events'
import { useQuasar, date } from 'quasar'
import Datepicker from '@/components/Datepicker.vue'

export default defineComponent({
  name: 'SummaryEvents',
  components: {
    Datepicker
  },
  setup(props) {
    const eventStore = useEventsStore()
    const labelToFilter = ref(null)
    const typeToFilter = ref(null)
    const Screen = useQuasar().screen

    const show = ref({
      calendar: false
    })

    const todayDt = ref(moment().startOf('day'))
    const firstDt = ref(moment('07-01-2024'))
    const selectedDate = ref([null, null])

    const disabledFromTo = ref({
      from: moment().add(1, 'days').endOf('day'),
      to: moment('2030-06-30')
    })

    const dateToDisplay = computed(() => {
      if (eventStore.dateSelected) {
        return (
          date.formatDate(moment(eventStore.dateSelected.from), 'DD/MM/YYYY | HH:mm') +
          ' - ' +
          date.formatDate(moment(eventStore.dateSelected.to), 'DD/MM/YYYY | HH:mm')
        )
      } else return 'Selecciona una fecha'
    })

    const isFilterByDate = computed(() => {
      return eventStore.dateSelected
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
      return [
        {
          name: 'today',
          label: 'Hoy',
          queryName: 'queryTotalEventsDay',
          value: date.formatDate(new Date(), 'DD MMMM', formattingDates)
        },
        {
          name: 'week',
          label: 'Semana',
          queryName: 'queryTotalEventsWeek',
          value:
            date.formatDate(getWeekBounds(new Date()).startOfWeek, 'DD MMM', formattingDates) +
            ' - ' +
            date.formatDate(getWeekBounds(new Date()).endOfWeek, 'DD MMM', formattingDates)
        },
        {
          name: 'month',
          label: 'Mes',
          queryName: 'queryTotalEventsMonth',
          value: date.formatDate(new Date(), 'MMMM', formattingDates)
        },
        {
          name: 'year',
          label: 'Año',
          queryName: 'queryTotalEventsYear',
          value: date.formatDate(new Date(), 'YYYY')
        }
      ]
    })

    const isFilterByLabel = computed(() => {
      if (eventStore.summaryEvents?.filtered && eventStore.labelsSelected) {
        return true
      } else return false
    })

    const hasValue = (data) => {
      return eventStore.summaryEvents
        ? eventStore.summaryEvents[data]
          ? eventStore.summaryEvents[data]
          : 0
        : 0
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

      const dateTimeLocal = new Date(
        Date.UTC(year, month - 1, day, mydate.time.hour, mydate.time.min, 59, 999)
      )

      // Obtiene la diferencia de zona horaria del browser
      const offset = -dateTimeLocal.getTimezoneOffset()
      const sign = offset >= 0 ? '+' : '-'
      const pad = (num) => String(Math.abs(num)).padStart(2, '0')
      const timezoneOffset = `${sign}${pad(Math.floor(offset / 60))}:${pad(offset % 60)}`

      // Formato deseado con el timezone dinámico
      const finalDateTime = dateTimeLocal.toISOString().slice(0, -1) + timezoneOffset
      return finalDateTime
    }

    const filterDates = (data) => {
      const dateToFilter = {
        from: convertToDate(data.start),
        to: convertToDate(data.end)
      }
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
      isFilterByLabel,
      hasValue,
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
      filterDates,
      isFilterByDate
    }
  }
})
</script>

<style lang="scss" scoped>
.card-small {
  max-height: 200px;
}
.q-card__section.q-card__section--vert.bg-white {
  padding: 16px 4px;
}
.my-card {
  width: 100%;
  max-width: 350px;
}
.q-focus-helper {
  display: none !important;
}
</style>
