<template>
  <div class="gt-md datepicker-container">
    <q-card class="my-card" bordered style="width: fit-content">
      <q-card-section horizontal class="q-px-xs">
        <q-card-section class="col-3">
          <div class="q-px-xs q-gutter-y-sm column no-warp">
            <q-btn
              :outline="btnActive !== 'today'"
              no-caps
              color="primary"
              label="Hoy"
              @click="selectDateByBtn('today')"
            />
            <q-btn
              :outline="btnActive !== 'yesterday'"
              no-caps
              color="primary"
              label="Ayer"
              @click="selectDateByBtn('yesterday')"
            />
            <q-btn
              :outline="btnActive !== 'week'"
              no-caps
              color="primary"
              label="Semana"
              @click="selectDateByBtn('week')"
            />
            <q-btn
              :outline="btnActive !== 'month'"
              no-caps
              color="primary"
              label="Mes"
              @click="selectDateByBtn('month')"
            />
            <q-btn
              :outline="btnActive !== 'year'"
              no-caps
              color="primary"
              label="Año"
              @click="selectDateByBtn('year')"
            />
          </div>
        </q-card-section>

        <q-separator vertical style="padding: 1px" />

        <q-card-section style="width: fit-content; padding: 20px 50px 20px 10px">
          <div :class="calendarClass" class="q-px-md">
            <div :class="calendarContainerClass">
              <div
                :class="data.classes"
                class="q-px-md"
                v-for="(data, dataIdx) in monthsData"
                :key="'month_data' + dataIdx"
              >
                <div class="calendar-header">
                  <div class="month-name">
                    <template v-if="dataIdx == 0">
                      <q-btn
                        round
                        flat
                        color="primary"
                        icon="chevron_left"
                        :disable="isPrevMonthDisabled"
                        @click="movePrevMonth()"
                      />
                    </template>

                    <span class="month-text"> {{ data.monthName }} </span>
                    <template v-if="(!enableSecondCalendar && dataIdx == 0) || dataIdx == 1">
                      <q-btn
                        round
                        flat
                        color="primary"
                        icon="chevron_right"
                        :disable="isNextMonthDisabled"
                        @click="moveNextMonth()"
                      />
                    </template>
                  </div>
                  <div class="day-name">
                    <span v-for="(day, index) in daysName" :key="'date_name' + index">
                      {{ day }}
                    </span>
                  </div>
                </div>
                <div class="calendar-dates" style="height: 220px">
                  <template
                    v-for="dateRowIdx in data.calendarRows"
                    :key="'date_row_' + dataIdx + dateRowIdx"
                  >
                    <div class="date-row">
                      <template
                        v-for="(dt, index) in data.dates.slice(
                          7 * (dateRowIdx - 1),
                          7 * dateRowIdx
                        )"
                      >
                        <template v-if="typeof dt === 'object'">
                          <div
                            class="date"
                            :class="{
                              'date-highlighted': dt.highlighted,
                              'date-selected': dt.selected,
                              'date-disabled': dt.isDisabled,
                              'date-today': dt.isToday,
                              'date-selected-start': dt.startDateSelected,
                              'date-selected-end': dt.endDateSelected
                            }"
                            :key="'calendar_dates' + dateRowIdx + index"
                            @click="onSelectDate(dt)"
                            @mouseover="hoverDate(dt)"
                          >
                            <span>
                              {{ dt.dateNumber }}
                            </span>
                          </div>
                        </template>
                        <div v-else :key="'blank_days' + dateRowIdx + index" class="blank-day">
                        </div>
                      </template>
                    </div>
                  </template>
                </div>
              </div>
            </div>
            <q-card-section class="row">
              <div class="row inline justify-around">
                <div style="width: fit-content">
                  <select v-model="timeSelectedStart.hour" style="max-width: 50px">
                    <option disabled value="">Seleccione un elemento</option>
                    <option v-for="(option, index) in optionsHours" :key="index" :value="option">
                      {{ option }}
                    </option>
                  </select>
                  :
                  <select v-model="timeSelectedStart.min" style="max-width: 50px">
                    <option disabled value="">Seleccione un elemento</option>
                    <option v-for="(option, index) in optionsMinutes" :key="index" :value="option">
                      {{ option }}
                    </option>
                  </select>
                </div>
                <div style="width: fit-content">
                  <select v-model="timeSelectedEnd.hour" style="max-width: 50px">
                    <option v-for="(option, index) in optionsHours" :key="index" :value="option">
                      {{ option }}
                    </option>
                  </select>
                  :
                  <select v-model="timeSelectedEnd.min" style="max-width: 50px">
                    <option
                      v-for="(option, index) in optionsMinutes"
                      :key="index"
                      :value="option"
                      :label="option"
                    >
                      {{ option }}
                    </option>
                  </select>
                </div>
              </div>
            </q-card-section>
          </div>
        </q-card-section>
      </q-card-section>
      <q-separator />
      <q-card-actions align="right">
        <div :class="calendarFooterClass" class="fit">
          <div class="fit row justify-end calendar-actions q-gutter-x-md" style="width: 0">
            <q-btn
              no-caps
              color="dark"
              dense
              outline
              label="Limpiar"
              class="q-px-md"
              style="width: 100px"
              @click="clickClear"
            >
            </q-btn>
            <q-btn
              no-caps
              color="primary"
              label="Filtrar"
              class="q-px-md"
              style="width: 100px"
              @click="goToFilter"
            >
            </q-btn>
          </div>
        </div>
      </q-card-actions>
    </q-card>
  </div>

  <!-- MOBILE VERSION-->
  <div class="lt-lg bg-white">
    <q-card flat class="my-card bg-whites">
   
      <q-card-section class="bg-white">
        <div class="q-gutter-sm row q-pb-sm">
          <q-btn
            :outline="btnActive !== 'today'"
            no-caps
            dense
            color="primary"
            label="Hoy"
            class="q-px-sm"
            @click="selectDateByBtn('today')"
          />
          <q-btn
            :outline="btnActive !== 'yesterday'"
            no-caps
            dense
            color="primary"
            label="Ayer"
            class="q-px-sm"
            @click="selectDateByBtn('yesterday')"
          />
          <q-btn
            :outline="btnActive !== 'week'"
            no-caps
            dense
            color="primary"
            label="Semana"
            class="q-px-sm"
            @click="selectDateByBtn('week')"
          />
          <q-btn
            :outline="btnActive !== 'month'"
            no-caps
            dense
            color="primary"
            label="Mes"
            class="q-px-sm"
            @click="selectDateByBtn('month')"
          />
          <q-btn
            :outline="btnActive !== 'year'"
            no-caps
            dense
            color="primary"
            label="Año"
            class="q-px-sm"
            @click="selectDateByBtn('year')"
          />
        </div>
        <q-separator />
        <div :class="calendarClass">
          <div :class="calendarContainerClass">
            <div
              :class="data.classes"
              v-for="(data, dataIdx) in monthsData"
              :key="'month_data' + dataIdx"
            >
              <div class="calendar-header">
                <div class="month-name">
                  <template v-if="dataIdx == 0">
                    <q-btn
                      round
                      flat
                      color="primary"
                      icon="chevron_left"
                      :disable="isPrevMonthDisabled"
                      @click="movePrevMonth()"
                    />
                  </template>

                  <span class="month-text"> {{ data.monthName }} </span>
                  <template v-if="(!enableSecondCalendar && dataIdx == 0) || dataIdx == 1">
                    <q-btn
                      round
                      flat
                      color="primary"
                      icon="chevron_right"
                      :disable="isNextMonthDisabled"
                      @click="moveNextMonth()"
                    />
                  </template>
                </div>
                <div class="day-name">
                  <span v-for="(day, index) in daysName" :key="'date_name' + index">
                    {{ day }}
                  </span>
                </div>
              </div>
              <div class="calendar-dates" style="height: 220px">
                <template
                  v-for="dateRowIdx in data.calendarRows"
                  :key="'date_row_' + dataIdx + dateRowIdx"
                >
                  <div class="date-row">
                    <template
                      v-for="(dt, index) in data.dates.slice(7 * (dateRowIdx - 1), 7 * dateRowIdx)"
                    >
                      <template v-if="typeof dt === 'object'">
                        <div
                          class="date"
                          :class="{
                            'date-highlighted': dt.highlighted,
                            'date-selected': dt.selected,
                            'date-disabled': dt.isDisabled,
                            'date-today': dt.isToday,
                            'date-selected-start': dt.startDateSelected,
                            'date-selected-end': dt.endDateSelected
                          }"
                          :key="'calendar_dates' + dateRowIdx + index"
                          @click="onSelectDate(dt)"
                          @mouseover="hoverDate(dt)"
                        >
                          <span>
                            {{ dt.dateNumber }}
                          </span>
                        </div>
                      </template>
                      <div v-else :key="'blank_days' + dateRowIdx + index" class="blank-day"></div>
                    </template>
                  </div>
                </template>
              </div>
            </div>
          </div>
          <q-card-section class="row">
            <div class="fit row inline justify-around">
              <span>Fecha de inicio</span>
              <div style="width: fit-content">
                <select v-model="timeSelectedStart.hour" style="max-width: 50px">
                  <option disabled value="">Seleccione un elemento</option>
                  <option v-for="(option, index) in optionsHours" :key="index" :value="option">
                    {{ option }}
                  </option>
                </select>
                :
                <select v-model="timeSelectedStart.min" style="max-width: 50px">
                  <option disabled value="">Seleccione un elemento</option>
                  <option v-for="(option, index) in optionsMinutes" :key="index" :value="option">
                    {{ option }}
                  </option>
                </select>
              </div>
              <span class="q-pt-lg">Fecha de final</span>
              <div style="width: fit-content">
                <select v-model="timeSelectedEnd.hour" style="max-width: 50px">
                  <option v-for="(option, index) in optionsHours" :key="index" :value="option">
                    {{ option }}
                  </option>
                </select>
                :
                <select v-model="timeSelectedEnd.min" style="max-width: 50px">
                  <option
                    v-for="(option, index) in optionsMinutes"
                    :key="index"
                    :value="option"
                    :label="option"
                  >
                    {{ option }}
                  </option>
                </select>
              </div>
            </div>
          </q-card-section>
        </div>
      </q-card-section>
      <q-separator />
      <q-card-actions align="right">
        <div :class="calendarFooterClass" class="fit q-px-none">
          <div class="fit row justify-end calendar-actions q-gutter-x-sm" style="width: 0">
            <q-btn
              no-caps
              color="dark"
              dense
              outline
              label="Limpiar"
              class="q-px-md"
              style="width: fit-content; min-width: 70px"
              @click="clickClear"
            >
            </q-btn>
            <q-btn
              no-caps
              color="primary"
              label="Filtrar"
              class="q-px-md"
              style="width: fit-content; min-width: 70px"
              @click="goToFilter"
            >
            </q-btn>
          </div>
        </div>
      </q-card-actions>
    </q-card>
  </div>
</template>
<script>
import { useEventsStore } from '@/stores/events'
export default {
  name: 'Datepicker2',
  props: {
    modelValue: {
      type: [Date, Object, String],
      default: null
    },
    startMonth: {
      type: [Date, Object, Array, String],
      default: null
    },
    isRange: {
      type: Boolean,
      default: true
    },
    enableSecondCalendar: {
      type: Boolean,
      default: true
    },
    givenDateFormat: {
      type: String,
      default: null
    },
    monthFormat: {
      type: String,
      default: 'MMM'
    },
    givenDays: {
      type: Array,
      default: null
    },
    calendarClass: {
      type: String,
      default: 'g-calendar'
    },
    calendarContainerClass: {
      type: String,
      default: 'calendar-container'
    },
    calendarFooterClass: {
      type: String,
      default: 'calendar-footer'
    },
    currentCalendarClass: {
      type: String,
      default: 'current-calendar'
    },
    nextCalendarClass: {
      type: String,
      default: 'next-calendar'
    },
    btnCancelClass: {
      type: String,
      default: null
    },
    btnClearClass: {
      type: String,
      default: null
    },
    btnCancelText: {
      type: String,
      default: null
    },
    btnClearText: {
      type: String,
      default: null
    },
    nextPrevIcon: {
      type: Boolean,
      default: false
    },
    disabledDates: {
      type: Array,
      default: null
    },
    disabledFromTo: {
      type: Object,
      default: () => {
        return null
      }
    },
    disabledStartDates: {
      type: Array,
      default: null
    },
    disabledStartFromTo: {
      type: Object,
      default: () => {
        return null
      }
    },
    disabledEndDates: {
      type: Array,
      default: null
    },
    disabledEndFromTo: {
      type: Object,
      default: () => {
        return null
      }
    },
    isTodayHighlight: {
      type: Boolean,
      default: true
    },
    lastMonth: {
      type: [String, Object],
      default: null
    },
    firstMonth: {
      type: [String, Object],
      default: null
    },
    dateFromStore: {
      type: [String, Object],
      default: null
    }
  },
  data() {
    return {
      btnActive: null,
      eventStore: useEventsStore(),
      start_date: new Date(),
      current_date: new Date(),
      selected_date: null,
      selected: {
        start_date: null,
        end_date: null
      },
      start_date_selected: false,
      timeSelectedStart: {
        hour: '00',
        min: '00'
      },
      timeSelectedEnd: {
        hour: '23',
        min: '00'
      },
      optionsHours: [
        '00',
        '01',
        '02',
        '03',
        '04',
        '05',
        '06',
        '07',
        '08',
        '09',
        '10',
        '11',
        '12',
        '13',
        '14',
        '15',
        '16',
        '17',
        '18',
        '19',
        '20',
        '21',
        '22',
        '23'
      ],
      optionsMinutes: ['00', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'],

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
        'Sept',
        'Oct',
        'Nov',
        'Dic'
      ]
    }
  },
  created() {
    this.init()
    if (this.dateFromStore) {
      this.selected.start_date = this.dateFromStore.start_date
      this.selected.end_date = this.dateFromStore.end_date
    }
  },
  computed: {
    currentMonth() {
      return moment(this.current_date)
        .subtract(1, 'M')
        .format(this.monthFormat || 'MMMM')
    },
    nextMonth() {
      return moment(this.current_date).format(this.monthFormat || 'MMMM')
    },
    daysName() {
      if (this.givenDays && Array.isArray(this.givenDays) && this.givenDays.length) {
        return this.givenDays
      }
      return ['Lu', 'Ma', 'Mie', 'Ju', 'Vi', 'Sa', 'Do']
    },
    totalCalendarRows() {
      return Math.ceil(this.dates.length / 7)
    },
    nextCalendarRows() {
      return Math.ceil(this.nextMonthDates.length / 7)
    },
    blankDays() {
      let firstDay = moment(this.current_date).subtract(1, 'M').startOf('month').day()
      if (firstDay === 0) {
        firstDay = 7
      }
      firstDay = firstDay - 1
      if (firstDay < 0) {
        firstDay = 0
      }
      return firstDay
    },
    nextMonthBlankDays() {
      let firstDay = moment(this.current_date).startOf('M').day()
      if (firstDay === 0) {
        firstDay = 7
      }
      firstDay = firstDay - 1
      if (firstDay < 0) {
        firstDay = 0
      }
      return firstDay
    },
    nextMonthDates() {
      let startDate = moment(this.current_date).clone().startOf('month')
      let lastDate = startDate.clone().endOf('month')
      if (this.nextMonthBlankDays > 0) {
        return Array(this.nextMonthBlankDays).concat(this.getDates(startDate, lastDate))
      } else {
        return this.getDates(startDate, lastDate)
      }
    },
    dates() {
      let startDate = moment(this.current_date).subtract(1, 'M').startOf('month')
      let lastDate = moment(this.current_date).subtract(1, 'M').endOf('month')
      if (this.blankDays > 0) {
        return Array(this.blankDays).concat(this.getDates(startDate, lastDate))
      } else {
        return this.getDates(startDate, lastDate)
      }
    },
    highlightedDates() {
      let dates = []
      if (this.selected && this.selected.start_date && this.selected.end_date) {
        const startDate = this.selected.start_date.clone()
        const endDate = this.selected.end_date.clone()
        if (startDate.isBefore(endDate)) {
          let idxDate = startDate
          while (idxDate.isSameOrBefore(endDate)) {
            dates.push(idxDate.clone().format('D-M-YYYY'))
            idxDate.add(1, 'days')
          }
        } else {
          let idxDate = endDate.clone()
          while (idxDate.isSameOrBefore(startDate)) {
            dates.push(idxDate.clone().format('D-M-YYYY'))
            idxDate.add(1, 'days')
          }
        }
        dates.shift()
        if (!this.start_date_selected && dates.length) {
          dates.pop()
        }
      }
      return dates
    },
    monthsData() {
      let months = [
        {
          monthName: this.currentMonth,
          calendarRows: this.totalCalendarRows,
          dates: this.dates,
          classes: this.currentCalendarClass,
          isCurrentMonth: true
        }
      ]
      if (this.enableSecondCalendar) {
        months.push({
          monthName: this.nextMonth,
          calendarRows: this.nextCalendarRows,
          dates: this.nextMonthDates,
          classes: this.nextCalendarClass,
          isNextMonth: true
        })
      } else {
        months = [
          {
            monthName: this.nextMonth,
            calendarRows: this.nextCalendarRows,
            dates: this.nextMonthDates,
            classes: this.nextCalendarClass,
            isNextMonth: true
          }
        ]
      }
      return months
    },
    _disabledDates() {
      let disabledDates = []
      if (this.disabledDates && Array.isArray(this.disabledDates) && this.disabledDates.length) {
        disabledDates = this.transformDateIntoMoment(this.disabledDates)
      }
      if (
        this.isRange &&
        !this.start_date_selected &&
        this.disabledStartDates &&
        Array.isArray(this.disabledStartDates) &&
        this.disabledStartDates.length
      ) {
        disabledDates = disabledDates.concat(this.transformDateIntoMoment(this.disabledStartDates))
      }
      if (
        this.isRange &&
        this.start_date_selected &&
        this.disabledEndDates &&
        Array.isArray(this.disabledEndDates) &&
        this.disabledEndDates.length
      ) {
        disabledDates = disabledDates.concat(this.transformDateIntoMoment(this.disabledEndDates))
      }
      return disabledDates.map((d) => d.format('D-M-YYYY'))
    },
    isNextMonthDisabled() {
      if (this.lastMonth) {
        let currentDate = moment(this.current_date).clone()

        const lastMonth = this.transformDateIntoMoment(this.lastMonth)
        if (moment.isMoment(lastMonth)) {
          if (
            currentDate.isSameOrAfter(lastMonth, 'month') &&
            currentDate.isSameOrAfter(lastMonth, 'year')
          ) {
            return true
          }
        }
      }
      return false
    },
    isPrevMonthDisabled() {
      if (this.firstMonth) {
        let currentDate = moment(this.current_date).clone()
        if (this.enableSecondCalendar) {
          currentDate = currentDate.subtract(1, 'M')
        }
        const firstMonth = this.transformDateIntoMoment(this.firstMonth)
        if (moment.isMoment(firstMonth)) {
          if (
            currentDate.isSameOrBefore(firstMonth, 'month') &&
            currentDate.isSameOrBefore(firstMonth, 'year')
          ) {
            return true
          }
        }
      }
      return false
    }
  },
  methods: {
    init() {
      if (this.isRange) {
        if (this.modelValue && Array.isArray(this.modelValue) && this.modelValue.length == 2) {
          const startDate = this.modelValue[0]
          const endDate = this.modelValue[1]
          if (moment.isMoment(startDate)) {
            this.selected.start_date = startDate.startOf('day')
          } else {
            if (
              this.givenDateFormat &&
              this.givenDateFormat !== null &&
              this.givenDateFormat !== ''
            ) {
              this.selected.start_date = moment(startDate).startOf('day')
            } else {
              this.selected.start_date = moment(startDate, this.givenDateFormat).startOf('day')
            }
          }
          if (moment.isMoment(endDate)) {
            this.selected.end_date = endDate.startOf('day')
          } else {
            if (
              this.givenDateFormat &&
              this.givenDateFormat !== null &&
              this.givenDateFormat !== ''
            ) {
              this.selected.end_date = moment(endDate, this.givenDateFormat).startOf('day')
            } else {
              this.selected.end_date = moment(endDate).startOf('day')
            }
          }
        }
      } else {
        if (this.modelValue) {
          const selectedDate = this.modelValue
          if (moment.isMoment(selectedDate)) {
            this.selected_date = selectedDate.startOf('day')
          } else {
            if (
              this.givenDateFormat &&
              this.givenDateFormat !== null &&
              this.givenDateFormat !== ''
            ) {
              this.selected_date = moment(selectedDate, this.givenDateFormat).startOf('day')
            } else {
              this.selected_date = moment(selectedDate).startOf('day')
            }
          }
        }
      }
      if (this.startMonth && this.startMonth !== null) {
        if (moment.isMoment(this.startMonth)) {
          this.current_date = this.startMonth.toDate()
        } else {
          if (
            this.givenDateFormat &&
            this.givenDateFormat !== null &&
            this.givenDateFormat !== ''
          ) {
            this.current_date = moment(this.startMonth, this.givenDateFormat)
              .startOf('day')
              .toDate()
          } else {
            this.current_date = moment(this.startMonth).startOf('day').toDate()
          }
        }
      }
    },
    onSelectDate(dt) {
      this.btnActive = null

      if (dt.isDisabled) {
        return
      }
      if (this.isRange) {
        if (!this.start_date_selected) {
          this.start_date_selected = true
          this.selected.end_date = null
          this.selected.start_date = dt.date.clone()
        } else {
          this.start_date_selected = false
          if (this.selected.start_date.isAfter(dt.date)) {
            this.selected.end_date = this.selected.start_date
            this.selected.start_date = dt.date
          } else {
            this.selected.end_date = dt.date.clone()
          }

          this.emitRangeDate()
        }
      } else {
        this.selected_date = dt.date
        this.emitRangeDate()
      }
    },
    hoverDate(dt) {
      if (this.start_date_selected) {
        // if( this.selected.start_date.isAfter( dt.date ) ){

        this.selected.end_date = dt.date.clone()
        // }else{
        //     this.selected.end_date = this.selected.start_date;
        //     this.selected.start_date = dt.date;
        // }
      }
    },
    isStartDate(dt) {
      if (
        this.isRange &&
        this.selected.start_date &&
        this.selected.start_date.format('MM-DD-YYYY') === moment(dt).format('MM-DD-YYYY')
      ) {
        return true
      }
      return false
    },
    isEndDate(dt) {
      if (
        this.isRange &&
        !this.start_date_selected &&
        this.selected.end_date &&
        this.selected.end_date.format('MM-DD-YYYY') === moment(dt).format('MM-DD-YYYY')
      ) {
        return true
      }
      return false
    },
    isSelectedDate(dt) {
      if (!this.isRange && this.selected_date && this.selected_date.isSame(dt)) {
        return true
      }
      return false
    },
    isHighlightedDate(dt) {
      if (
        this.highlightedDates &&
        this.highlightedDates.length &&
        this.highlightedDates.includes(dt.format('D-M-YYYY'))
      ) {
        return true
      }
      return false
    },
    getDates(startDate, lastDate) {
      let dates = []
      while (startDate.isBefore(lastDate)) {
        var isHighlighted = this.isHighlightedDate(startDate)
        var isToday =
          this.isTodayHighlight &&
          moment().startOf('day').format('DD-MM-YYYY') ===
            moment(startDate).startOf('day').format('DD-MM-YYYY')
        var isStartDate = this.isStartDate(startDate)
        var isEndDate = this.isEndDate(startDate)
        var isSelected = this.isSelectedDate(startDate) || isStartDate || isEndDate
        var isDisabled = this.isDisabledDate(startDate)

        let tmpDt = {
          date: startDate.clone(),
          dateNumber: startDate.format('D'),
          highlighted: isHighlighted,
          selected: isSelected,
          toDate: startDate.toDate(),
          isDisabled: isDisabled,
          isToday: isToday,
          startDateSelected: isStartDate,
          endDateSelected: isEndDate
        }

        dates.push(tmpDt)
        startDate = startDate.add(1, 'day')
      }
      return dates
    },
    moveNextMonth() {
      if (this.isNextMonthDisabled) {
        return
      }
      this.current_date = moment(this.current_date).add(1, 'M').toDate()
    },
    movePrevMonth() {
      if (this.isPrevMonthDisabled) {
        return
      }
      this.current_date = moment(this.current_date).subtract(1, 'M').toDate()
    },
    emitRangeDate() {
      let selected
      if (this.isRange) {
        selected = [this.selected.start_date, this.selected.end_date]
      } else {
        selected = this.selected_date
      }
      // this.$emit('onSelect', selected)
      this.$emit('update:modelValue', selected)
    },
    goToFilter() {
      let selected
      if (this.isRange) {
        selected = {
          start: {
            date: moment(this.selected.start_date).format('DD/MM/YYYY'),
            time: this.timeSelectedStart
          },
          end: {
            date: moment(this.selected.end_date).format('DD/MM/YYYY'),
            time: this.timeSelectedEnd
          }
        }
      } else {
        selected = {
          start: {
            date: moment(this.selected).format('DD/MM/YYYY'),
            timeStart: this.timeSelectedStart
          },
          end: {
            date: moment(this.selected).format('DD/MM/YYYY'),
            timeEnd: this.timeSelectedEnd
          }
        }
      }
      this.$emit('onSelect', selected)

      this.$emit('filterByDate', selected)
    },
    clickClear() {
      if (this.isRange) {
        this.start_date_selected = false
        this.selected.start_date = null
        this.selected.end_date = null
        this.timeSelectedStart = {
          hour: '00',
          min: '00'
        }
        this.timeSelectedEnd = {
          hour: '23',
          min: '00'
        }
      } else {
        this.selected_date = null
      }
      this.btnActive = null
      this.eventStore.dateSelected = null
      this.$emit('onSelect')

      this.$emit('clearDates')
    },
    transformDateIntoMoment(dates) {
      if (Array.isArray(dates)) {
        return dates.map((d) => {
          if (moment.isMoment(d)) {
            return d.startOf('day')
          } else {
            if (
              this.givenDateFormat &&
              this.givenDateFormat !== null &&
              this.givenDateFormat !== ''
            ) {
              return moment(d, this.givenDateFormat).startOf('day')
            } else {
              return moment(d).startOf('day')
            }
          }
        })
      } else {
        if (moment.isMoment(dates)) {
          return dates.startOf('day')
        } else {
          if (
            this.givenDateFormat &&
            this.givenDateFormat !== null &&
            this.givenDateFormat !== ''
          ) {
            return moment(dates, this.givenDateFormat).startOf('day')
          } else {
            return moment(dates).startOf('day')
          }
        }
      }
    },
    isInRangeFromTo(data, dt) {
      let fromDate = null
      let toDate = null
      if (data && typeof data == 'object' && ('from' in data || 'to' in data)) {
        if ('from' in data) {
          fromDate = this.transformDateIntoMoment(data.from)
        }
        if ('to' in data) {
          toDate = this.transformDateIntoMoment(data.to)
        }
      }

      if (fromDate && toDate) {
        if (dt.isSameOrAfter(fromDate) && dt.isSameOrBefore(toDate)) {
          return true
        }
      } else {
        if (fromDate && dt.isSameOrAfter(fromDate)) {
          return true
        }
        if (toDate && dt.isSameOrBefore(toDate)) {
          return true
        }
      }
      return false
    },
    isDisabledDate(dt) {
      if (
        this._disabledDates &&
        this._disabledDates.length &&
        this._disabledDates.includes(dt.format('D-M-YYYY'))
      ) {
        return true
      }
      if (this.isInRangeFromTo(this.disabledFromTo, dt)) {
        return true
      }

      if (this.isRange) {
        if (!this.start_date_selected) {
          if (this.isInRangeFromTo(this.disabledStartDates, dt)) {
            return true
          }
        } else {
          if (this.isInRangeFromTo(this.disabledEndDates, dt)) {
            return true
          }
        }
      }
      return false
    },
    selectDateByBtn(selected) {
      this.btnActive = selected
      let date = new Date()
      let endDate = moment().startOf('day')
      switch (selected) {
        case 'today':
          date = moment(new Date())
          break
        case 'yesterday':
          date = moment(new Date()).subtract(1, 'days').startOf('day')
          endDate = moment().subtract(1, 'days').endOf('day')
          break
        case 'week':
          date = moment(new Date()).startOf('week').add(1, 'days')
          endDate = moment(new Date()).endOf('week').add(1, 'days')
          break
        case 'month':
          date = moment(new Date()).startOf('month')
          endDate = moment(new Date()).endOf('month')

          break
        case 'year':
          date = moment(new Date()).startOf('year')
          endDate = moment(new Date())
          break
      }

      if (this.isRange) {
        this.selected.start_date = date
        this.selected.end_date = endDate
      } else {
        this.selected_date = date
      }
      this.emitRangeDate()
    }
  }
}
</script>

<style lang="scss">
.datepicker-container {
  background-color: white;
  width: fit-content;
  position: absolute;
  left: -350px;
}
.datepicker-container-mobile {
  background-color: white;
  width: fit-content;
  position: absolute;
  left: 0px;
}

.g-calendar {
  width: 100%;
  z-index: 100;
  .calendar-container {
    display: flex;

    .current-calendar,
    .next-calendar {
      flex: 1;
    }
    .current-calendar {
      padding-right: 15px;
      border-right: #999 1px solid;
    }
    .next-calendar {
      margin-left: 20px;
      padding-left: 20px;
    }
    .next-icon {
      width: 0;
      height: 0;
      border-top: 12px solid transparent;
      border-bottom: 12px solid transparent;

      border-left: 12px solid grey;
    }
    .prev-icon {
      width: 0;
      height: 0;
      border-top: 12px solid transparent;
      border-bottom: 12px solid transparent;

      border-right: 12px solid grey;
    }
    .next-icon,
    .prev-icon {
      &.disabled {
        border-right-color: #a7a4a46b;
        border-left-color: #a7a4a46b;
      }
    }
    // width: 50%;
    .day-name {
      display: flex;
      justify-content: space-between;
      padding-top: 2px;
      padding-bottom: 2px;
      span {
        width: 100%;
        text-align: center;
        font-weight: 550;
      }
    }
    .month-name {
      display: flex;
      // justify-content: space-evenly;
      padding: 5px;
      font-size: 22px;
      font-weight: 480;

      .prev-icon {
        padding-left: 7px;
      }
      .month-text {
        margin: auto;
        color: #999999;
      }
    }
    .calendar-dates .date-row {
      display: flex;
      // justify-content: space-between;

      .blank-day,
      .date {
        width: 14.28%;
        text-align: center;
        padding: 7px;

        &.date-selected-start {
          border-top-left-radius: 8px;
          border-bottom-left-radius: 8px;
        }
        &.date-selected-end {
          border-top-right-radius: 8px;
          border-bottom-right-radius: 8px;
        }
        &.date-disabled {
          color: #e3e3e3;
        }
        &.date-today {
          color: #363636;
          // background-color: #005cff4d;
          background-color: #ffc4b1;
          border-radius: 8px;
        }
        &.date-highlighted {
          background: #c5d0f0 !important;
          color: #fff;
        }
        &.date-selected {
          background: #374eaf !important;
          color: #fff;
        }
      }
    }
  }
}
@media screen and (max-width: 1024px) {
  .g-calendar {
    .calendar-container {
      display: block;
      .current-calendar {
        border-right: none;
      }
    }
  }
}
</style>
