<template>
  <!-- <div class="q-pa-md">
    <q-input readonly outlined v-model="date" mask="date" :rules="['date']">
      <template v-slot:prepend>
        <q-icon name="event" class="cursor-pointer">
          <q-popup-proxy cover transition-show="scale" transition-hide="scale">
            {{ startDate }} - {{ endDate }}
            <q-card class="fit my-card row q-px-md" flat>
              <q-card-section horizontal>
                <q-card-section
                  class="q-pl-none q-py-md"
                  style="max-width: fit-content; border-right: 1px solid #eeeeee"
                >
                  <div class="column q-pt-md items-start">
                    <q-btn flat no-caps align="left" label="Hoy" />
                    <q-btn flat no-caps align="left" label="Ayer" />
                    <q-btn flat no-caps align="left" label="Semana" />
                    <q-btn flat no-caps align="left" label="Mes" />
                    <q-btn flat no-caps align="left" label="Año" />
                  </div>
                </q-card-section>

                <q-card-section style="max-width: fit-content">
                  <div class="q-pt-none q-mt-none q-pb-md">
                    <q-date
                      minimal
                      flat
                      range
                      :locale="locale"
                      navigation-min-year-month="2024/07"
                      :navigation-max-year-month="maxYearMonth"
                      :default-year-month="defualtStartYearMonth"
                      v-model="startDate"
                      @update:model-value="validateRange('start', $event)"
                      mask="YYYY-MM-DD"
                    />
                    <div class="row justify-center items-center" style="margin-top: -40px">
                      <q-select
                        outlined
                        dense
                        options-dense
                        v-model="startHour"
                        :options="optionsHour"
                        style="max-width: 100px"
                      ></q-select>
                      <span class="q-pr-md" style="margin-left: -20px; max-width: fit-content"
                        >:</span
                      >
                      <q-select
                        outlined
                        dense
                        options-dense
                        v-model="startMin"
                        :options="optionsMin"
                        style="max-width: 100px"
                      ></q-select>
                    </div>
                  </div>
                </q-card-section>
                <q-card-section style="max-width: fit-content">
                  <div class="q-pt-none q-mt-none q-pb-md">
                    <q-date
                      minimal
                      flat
                      :locale="locale"
                      navigation-min-year-month="2024/07"
                      :default-year-month="defaultYearMoth"
                      @update:model-value="validateRange('end', $event)"
                      v-model="endDate"
                      mask="YYYY-MM-DD"
                    />
                    <div class="row justify-center items-center" style="margin-top: -45px">
                      <q-select
                        outlined
                        dense
                        v-model="endHour"
                        :options="optionsHour"
                        style="max-width: 100px"
                      ></q-select>
                      <span class="q-pr-md" style="margin-left: -20px; max-width: fit-content"
                        >:</span
                      >
                      <q-select
                        outlined
                        dense
                        v-model="endMin"
                        :options="optionsMin"
                        style="max-width: 100px"
                      ></q-select>
                    </div>
                  </div>
                </q-card-section>
              </q-card-section>
            </q-card>
          </q-popup-proxy>
        </q-icon>
      </template>
    </q-input>
  </div> -->

  <div class="row">
    <div
      class="col-6 p-2 border col-md-auto m-auto"
      style="cursor: pointer"
      @click="showCalendar()"
    >
      <!-- {{ selectedDate[0].format("DD MMM, YYYY") }} -
      {{ selectedDate[1].format("D MMM, 2022") }} -->
      <i class="fa fa-calendar"></i>
    </div>
    <!-- <div class="row mt-1 border" v-show="show.calendar">
      <DatePicker
        v-model="selectedDate"
        @onSelect="showCalendar"
        :next-prev-icon="true"
        :last-month="todayDt"
        :first-month="firstDt"
        :enableSecondCalendar="true"
      />
    </div> -->
  </div>
</template>

<script>
import { defineComponent, ref, computed } from 'vue'
import { date } from 'quasar'

// import DatePicker from '@/components/DatePicker.vue';

export default defineComponent({
  name: 'MyCard',
  components: {},
  setup() {
    // const date = ref(new Date())
    const optionsHour = ref([
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
      { label: '22', value: 22 },
      { label: '23', value: 23 }
    ])
    const optionsMin = ref([
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

    const defaultYearMoth = computed(() => {
      return date.formatDate(new Date(), 'YYYY/MM')
    })
    const defualtStartYearMonth = computed(() => {
      return date.formatDate(date.subtractFromDate(new Date(), { months: 1 }), 'YYYY/MM')
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

    const show = ref({
      calendar: false
    })

    const showCalendar = () => {
      show.calendar.value = !show.calendar.value
    }

    const todayDt = new Date()
    const firstDt = date.subtractFromDate(new Date(), { months: 8 })

    const selectedDate = ref([
      date.startOfDate(date.subtractFromDate(new Date(), { days: 7 }), 'date'),
      date.endOfDate(new Date(), 'date')
    ])

    const disabledFromTo = ref({
      from: new Date('2022-07-01'),
      to: new Date('2022-07-21')
    })

    const disabledDates = computed(() => {
      let dt = [];
      let sd =  date.startOfDate(new Date("2022-10-22"))
      let ed =  date.startOfDate(new Date("2022-11-02"))
      while (sd <= (ed)) {
        dt.push(date.clone(sd));
        date.addToDate(sd, {days: 1})
      }
      return dt;
    });

    return {
      defaultYearMoth,
      defualtStartYearMonth,
      maxYearMonth,
      locale,
      optionsHour,
      optionsMin,
      todayDt,
      firstDt,
      selectedDate,
      disabledFromTo,
      show,
      disabledDates,
      showCalendar,
      todayDt,
      firstDt,
      selectedDate,
      disabledFromTo,
      disabledDates
    }
  }
})
</script>

<style lang="scss" scoped>
.my-card {
  width: 100%;
  // max-width: 500px;
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
:deep(.q-field__append.q-field__marginal.row.no-wrap.items-center.q-anchor--skip) {
  padding-left: 22px;
}
</style>
