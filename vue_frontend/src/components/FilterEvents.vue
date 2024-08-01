<template>
  <q-expansion-item
    expand-separator
    :icon="iconFilter"
    label="Filtros"
    default-opened
    :class="colorFilter"
    class="barlow-bold fs-21-25"
  >
    <div class="fit row wrap justify-end items-center content-start q-gutter-sm q-py-md">
      <q-input dense outlined v-model="displayDate" class="inputs" label="Fecha">
        <template v-slot:prepend>
          <q-icon name="event" class="cursor-pointer">
            <q-popup-proxy cover transition-show="scale" transition-hide="scale">
              <q-card class="my-card fit column items-center">
                <q-date
                  minimal
                  :locale="locale"
                  range
                  navigation-min-year-month="2024/07"
                  :navigation-max-year-month="maxYearMonth"
                  :default-year-month="defaultYearMoth"
                  v-model="dateToFilter"
                  mask="YYYY-MM-DD"
                >
                </q-date>
                <q-card-section class="fit row justify-start q-pt-none">
                  <div class="fit row">

                  <span class="text-dark barlow-bold">Seleccionar hora inicio:</span>
                  <q-select
                    dense
                    :disable="disableTimeToFilter"
                    outlined
                    v-model="timeStart"
                    :options="optionsTime"
                    options-dense
                    class="inputs"
                  />

                  <span class="text-dark barlow-bold">Seleccionar hora final:</span>
                  <q-select
                    dense
                    :disable="disableTimeToFilter"
                    outlined
                    v-model="timeEnd"
                    :options="optionsTime"
                    options-dense
                    class="inputs"
                  />
                </div>

                </q-card-section>
              </q-card>
            </q-popup-proxy>
          </q-icon>
        </template>
      </q-input>
      <q-select
        dense
        outlined
        v-model="labelTypeToFilter"
        :options="optionsLabelTypes"
        :options-label="opt => opt.key"
        options-dense
        label="Etiqueta"
        class="inputs"
      />

      <q-btn
        unelevated
        no-caps
        dense
        class="q-mr-md q-px-sm"
        label="Filtrar"
        color="primary"
        @click="filterEvents"
      />
      <q-btn
        unelevated
        no-caps
        dense
        class="q-px-sm"
        label="Limpiar"
        color="info"
        text-color="grey-6"
        @click="clearFilter"
      />
    </div>
  </q-expansion-item>
</template>

<script>
import { defineComponent, ref, computed, watch } from 'vue'
import { date, event } from 'quasar'
import { useEventsStore } from '@/stores/events.js'

export default defineComponent({
  name: 'FilterEvents',

  emits: ['filterData'],

  setup(props, { emit }) {
    const colorFilter = ref('border-box')
    const iconFilter = ref('filter_alt_off')
    const timeStart = ref({ label: '00:00', value: '00:00' })
    const timeEnd = ref({ label: '00:00', value: '00:00' })

    const dateToFilter = ref(null)

    const labelTypeToFilter = ref(null)
    const eventStore = useEventsStore()

    const defaultYearMoth = computed(() => {
      return date.formatDate(new Date(), 'YYYY/MM')
    })
    const maxYearMonth = computed(() => {
      return date.formatDate(new Date(), 'YYYY/MM')
    });
    const optionsLabelTypes = computed(() => {
      return eventStore.labelsTypes ? eventStore.labelsTypes : []
    });

    const locale = {
      days: 'Domingo_Lunes_Martes_Miércoles_Jueves_Viernes_Sábado'.split('_'),
      daysShort: 'Dom_Lun_Mar_Mié_Jue_Vie_Sáb'.split('_'),
      months:
        'Enero_Febrero_Marzo_Abril_Mayo_Junio_Julio_Agosto_Septiembre_Octubre_Noviembre_Diciembre'.split(
          '_'
        ),
      monthsShort: 'Ene_Feb_Mar_Abr_May_Jun_Jul_Ago_Sep_Oct_Nov_Dic'.split('_'),
      firstDayOfWeek: 1
    };

    const displayDate = computed(() => {
      if (dateToFilter.value) {
        if (typeof dateToFilter.value === 'object') {
          return `${dateToFilter.value.from} | ${timeStart.value.value} - ${dateToFilter.value.to} | ${timeEnd.value.value}`
        }
        return `${dateToFilter.value} | ${timeStart.value.value} - ${timeEnd.value.value}`
      }
      return null
    });

    const disableTimeToFilter = computed(() => {
      return typeof dateToFilter.value === 'object'
    });

    const getTimeZoneOffset = () => {
      const currentDate = new Date()
      const timeZoneOffset = currentDate.getTimezoneOffset()

      let hours = Math.floor(Math.abs(timeZoneOffset) / 60)
      let minutes = Math.abs(timeZoneOffset) % 60

      // Formatear el offset en el formato ±HH:MM
      let sign = timeZoneOffset <= 0 ? '+' : '-'
      let formattedOffset =
        sign + String(hours).padStart(2, '0') + ':' + String(minutes).padStart(2, '0')
      return formattedOffset
    };

    const optionsTime = computed(() => [
      { label: '00:00', value: '00:00' },
      { label: '01:00', value: '01:00' },
      { label: '02:00', value: '02:00' },
      { label: '03:00', value: '03:00' },
      { label: '04:00', value: '04:00' },
      { label: '05:00', value: '05:00' },
      { label: '06:00', value: '06:00' },
      { label: '07:00', value: '07:00' },
      { label: '08:00', value: '08:00' },
      { label: '09:00', value: '09:00' },
      { label: '10:00', value: '10:00' },
      { label: '11:00', value: '11:00' },
      { label: '12:00', value: '12:00' },
      { label: '13:00', value: '13:00' },
      { label: '14:00', value: '14:00' },
      { label: '15:00', value: '15:00' },
      { label: '16:00', value: '16:00' },
      { label: '17:00', value: '17:00' },
      { label: '18:00', value: '18:00' },
      { label: '19:00', value: '19:00' },
      { label: '20:00', value: '20:00' },
      { label: '21:00', value: '21:00' },
      { label: '22:00', value: '22:00' },
      { label: '23:00', value: '23:00' }
    ]);

    const clearFilter = () => {
      timeStart.value = { label: '00:00', value: '00:00' }
      timeEnd.value = { label: '00:00', value: '00:00' }
      dateToFilter.value = null
      labelTypeToFilter.value = null
      eventStore.dateSelected = null
      eventStore.timeSelected = null
      eventStore.labelsTypeSelected = null
      colorFilter.value = 'border-box'
      iconFilter.value = 'filter_alt_off'
      eventStore.funtionToUse = 'allevents'
      eventStore.FETCH_EVENTS()
    };

    const filterEvents = () => {
      if (typeof dateToFilter.value === 'object') {
        timeStart.value = { label: '00:00', value: '00:00' }
        timeEnd.value = { label: '00:00', value: '00:00' }

      }
      const dateAsObject = dateToFilter.value
        ? typeof dateToFilter.value === 'object'
          ? {
                from:
                date.formatDate((dateToFilter.value.from), 'YYYY-MM-DD') +
                'T' +
                timeStart.value.value +
                ':00' +
                getTimeZoneOffset(),
              to:
                date.formatDate((dateToFilter.value.to), 'YYYY-MM-DD') +
                'T' +
                timeEnd.value.value +
                ':00' +
                getTimeZoneOffset()
            }
          : {
              from:
                date.formatDate(new Date(dateToFilter.value), 'YYYY-MM-DD') +
                'T' +
                timeStart.value.value +
                ':00' +
                getTimeZoneOffset(),
              to:
                date.formatDate(new Date(dateToFilter.value), 'YYYY-MM-DD') +
                'T' +
                timeEnd.value.value+':00'+
                getTimeZoneOffset()
            }
        : null
      colorFilter.value = 'border-box-filter'
      iconFilter.value = 'filter_alt'

      emit('filterData', {
        dateToFilter: dateAsObject,
        labelTypeToFilter: labelTypeToFilter.value
      })
    };



    return {
      timeStart,
      timeEnd,
      optionsTime,
      optionsLabelTypes,
      dateToFilter,
      labelTypeToFilter,
      defaultYearMoth,
      locale,
      maxYearMonth,
      clearFilter,
      filterEvents,
      displayDate,
      disableTimeToFilter,
      iconFilter,
      colorFilter,
    }
  }
})
</script>

<style scoped>
.border-box {
  border-left: 20px solid #5a7fe6;
  border-top: 1px solid #a0aad0;
  border-bottom: 1px solid #a0aad0;
  border-right: 1px solid #a0aad0;
  padding: 0 10px;
  border-radius: 10px;
}
.border-box-filter {
  border-left: 20px solid #ff8660;
  border-top: 1px solid #a0aad0;
  border-bottom: 1px solid #a0aad0;
  border-right: 1px solid #a0aad0;
  padding: 0 10px;
  border-radius: 10px;
}
.inputs {
  max-width: 300px;
  width: 100%;
}
:deep(.q-field__append.q-field__marginal.row.no-wrap.items-center.q-anchor--skip) {
  width: 0px !important;
}
:deep(.q-field__prepend.q-field__marginal.row.no-wrap.items-center) {
  width: 80px !important;
}
:deep(.q-date__navigation.row.items-center.no-wrap) {
  max-width: 145px !important;
  padding: 0 45px !important;
}
/* :deep(.row.items-center.q-date__arrow){
  max-width: 150px !important;
} */
:deep(.relative-position.overflow-hidden.flex.flex-center.col) {
  max-width: 155px !important;
  padding: 0 40px !important;
}
</style>
