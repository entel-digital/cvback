<template>
    <q-input dense outlined v-model="dateToFilter" :label="labelInput">
      <template v-slot:prepend>
        <q-icon name="event" class="cursor-pointer">
          <q-popup-proxy cover transition-show="scale" transition-hide="scale">
            <q-card class="my-card fit column items-center">
              <q-date
                minimal
                range
                :locale="locale"
                navigation-min-year-month="2024/07"
                :navigation-max-year-month="maxYearMonth"
                :default-year-month="defaultYearMoth"
                :model-value="dateToFilter"
                mask="YYYY-MM-DD"
                @update:model-value="selectPeriod"
                style="box-shadow: none"
              >
              </q-date>
              <q-card-section class="fit row justify-start q-pt-none">
                <div class="fit col">
                  <span class="text-dark barlow-bold">Seleccionar hora:</span>
                  <q-select
                    dense
                    outlined
                    v-model="hourToFilter"
                    :options="optionsHour"
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
</template>

<script>
import { defineComponent, ref, computed } from 'vue'
import { date } from 'quasar'
import { useEventsStore } from '@/stores/events.js'

export default defineComponent({
  name: 'DatePicker',
  props: ["labelInput"],
  emits: ['filterDate'],

  setup({ emit }) {
    const dateToFilter = ref(null)
    const hourToFilter = ref({ label: '00', value: '00:00' })
    const minToFilter = ref({ label: '00', value: 0 })

    const eventStore = useEventsStore()

    const defaultYearMoth = computed(() => {
      return date.formatDate(new Date(), 'YYYY/MM')
    })
    const maxYearMonth = computed(() => {
      return date.formatDate(new Date(), 'YYYY/MM')
    })

    const locale = {
      days: 'Domingo_Lunes_Martes_Miércoles_Jueves_Viernes_Sábado'.split('_'),
      daysShort: 'Dom_Lun_Mar_Mié_Jue_Vie_Sáb'.split('_'),
      months:
        'Enero_Febrero_Marzo_Abril_Mayo_Junio_Julio_Agosto_Septiembre_Octubre_Noviembre_Diciembre'.split(
          '_'
        ),
      monthsShort: 'Ene_Feb_Mar_Abr_May_Jun_Jul_Ago_Sep_Oct_Nov_Dic'.split('_'),
      firstDayOfWeek: 1
    }

    // const displayDate = computed(() => {
    //   if (dateToFilter.value) {
    //     if (typeof dateToFilter.value === 'object') {
    //       return `${dateToFilter.value.from} - ${dateToFilter.value.to}`
    //     }
    //     return dateToFilter.value
    //   }
    //   return null
    // })

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
    }

    const selectPeriod = (value) => {
      const datetoFormart = new Date(value)

      const mydate = {
        year: datetoFormart.getFullYear(),
        month: datetoFormart.getMonth() + 1,
        day: datetoFormart.getDate(),
        hour: hourToFilter.value.value,
        min: minToFilter.value.value
      }
      const newDate = date.buildDate({year: mydate.year, month: mydate.month,  date: mydate.day, hours: hourToFilter.value.value, minutes: minToFilter.value.value})
      dateToFilter.value = newDate
      emit('filterDate', value)
    }

    const optionsHour = computed(() => [
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
    ])

    const optionsMin = computed(() => [
      { label: '00', value: 0 },
      { label: '01', value: 1 },
      { label: '02', value: 2 },
      { label: '03', value: 3 },
      { label: '04', value: 4 },
      { label: '05', value: 5 },
      { label: '06', value: 6 },
      { label: '07', value: 7 },
      { label: '08', value: 8 },
      { label: '09', value: 9 },
      { label: '10', value: 10 },
      { label: '11', value: 11 },
      { label: '12', value: 12 },
      { label: '13', value: 13 },
      { label: '14', value: 14 },
      { label: '15', value: 15 },
      { label: '16', value: 16 },
      { label: '17', value: 17 },
      { label: '18', value: 18 },
      { label: '19', value: 19 },
      { label: '20', value: 20 },
      { label: '21', value: 21 },
      { label: '21', value: 21 },
      { label: '22', value: 22 },
      { label: '23', value: 23 },
      { label: '24', value: 24 },
      { label: '25', value: 25 },
      { label: '26', value: 26 },
      { label: '27', value: 27 },
      { label: '28', value: 28 },
      { label: '29', value: 29 },
      { label: '30', value: 30 },
      { label: '31', value: 31 },
      { label: '32', value: 32 },
      { label: '33', value: 33 },
      { label: '34', value: 34 },
      { label: '35', value: 35 },
      { label: '36', value: 36 },
      { label: '37', value: 37 },
      { label: '38', value: 38 },
      { label: '39', value: 39 },
      { label: '40', value: 40 },
      { label: '41', value: 41 },
      { label: '42', value: 42 },
      { label: '43', value: 43 },
      { label: '44', value: 44 },
      { label: '45', value: 45 },
      { label: '46', value: 46 },
      { label: '47', value: 47 },
      { label: '48', value: 48 },
      { label: '49', value: 49 },
      { label: '50', value: 50 },
      { label: '51', value: 51 },
      { label: '52', value: 52 },
      { label: '53', value: 53 },
      { label: '54', value: 54 },
      { label: '55', value: 55 },
      { label: '56', value: 56 },
      { label: '57', value: 57 },
      { label: '58', value: 58 },
      { label: '59', value: 59 }
    ])

    return {
      optionsHour,
      optionsMin,
      dateToFilter,
      defaultYearMoth,
      locale,
      maxYearMonth,
      selectPeriod,
      hourToFilter,
      minToFilter
    }
  }
})
</script>

<style scoped>
.inputs {
  max-width: 150px;
  width: 100%;
}
.my-card {
  width: 100%;
  max-width: 450px;
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
