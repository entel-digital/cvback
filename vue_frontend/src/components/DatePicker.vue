<template>
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
              <span
                @click="movePrevMonth()"
                class="prev-icon"
                v-if="nextPrevIcon"
                :class="{ disabled: isPrevMonthDisabled }"
              >
              </span>
              <span @click="movePrevMonth()" class="prev-text" v-else> PREV </span>
            </template>

            <span class="month-text"> {{ data.monthName }} </span>
            <template v-if="(!enableSecondCalendar && dataIdx == 0) || dataIdx == 1">
              <span
                @click="moveNextMonth()"
                class="next-icon"
                v-if="nextPrevIcon"
                :class="{ disabled: isNextMonthDisabled }"
              >
              </span>
              <span @click="moveNextMonth()" class="next-text" v-else> NEXT </span>
            </template>
          </div>
          <div class="day-name">
            <span v-for="(day, index) in daysName" :key="'date_name' + index">
              {{ day }}
            </span>
          </div>
        </div>
        <div class="calendar-dates">
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
                <div v-else :key="'blank_days' + dateRowIdx + index" class="blank-day">
                  <!-- <span ></span> -->
                </div>
              </template>
            </div>
          </template>
        </div>
      </div>
    </div>
    <div :class="calendarFooterClass">
      <div class="calendar-actions">
        <button class="btn btn-cancel" :class="btnCancelClass" @click="clickCancel">
          {{ btnCancelText || 'Cancel' }}
        </button>
        <button class="btn btn-clear" :class="btnClearClass" @click="clickClear">
          {{ btnClearText || 'Clear' }}
        </button>
      </div>
    </div>
  </div>
</template>
<script>
import { date } from 'quasar'
//   import "./datepicker.scss";

export default {
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
      type: String,
      default: null
    },
    firstMonth: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      start_date: new Date(),
      current_date: new Date(),
      selected_date: null,
      selected: {
        start_date: null,
        end_date: null
      },
      start_date_selected: false
    }
  },
  created() {
    this.init()
  },
  computed: {
    currentMonth() {
      return date.formatDate(
        date.subtractFromDate(this.current_date, { months: 1 }),
        this.monthFormat || 'MMMM'
      )
    },
    nextMonth() {
      return date.formatDate(this.current_date, this.monthFormat || 'MMMM')
    },
    daysName() {
      if (this.givenDays && Array.isArray(this.givenDays) && this.givenDays.length) {
        return this.givenDays
      }
      return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    totalCalendarRows() {
      return Math.ceil(this.dates.length / 7)
    },
    nextCalendarRows() {
      return Math.ceil(this.nextMonthDates.length / 7)
    },
    blankDays() {
      let subtractMonth = date.subtractFromDate(this.current_date, { months: 1 })
      let firstDay = date.startOfDate(subtractMonth, 'month')
      let dayOfWeek = firstDay.getDate()

      if (dayOfWeek === 0) {
        dayOfWeek = 7
      }
      dayOfWeek = dayOfWeek - 1
      if (dayOfWeek < 0) {
        dayOfWeek = 0
      }
      return dayOfWeek
    },
    nextMonthBlankDays() {
      let subtractMonth = date.subtractFromDate(this.current_date, { months: 1 })
      let firstDay = date.startOfDate(subtractMonth, 'month')
      let dayOfWeek = firstDay.getDate()
      if (dayOfWeek === 0) {
        dayOfWeek = 7
      }
      dayOfWeek = dayOfWeek - 1
      if (dayOfWeek < 0) {
        dayOfWeek = 0
      }
      return dayOfWeek
    },
    nextMonthDates() {
      let startDate = date.startOfDate(this.current_date, 'month') // Primer día del mes
      let lastDate = date.endOfDate(startDate, 'month') // Último día del mes
      if (this.nextMonthBlankDays > 0) {
        return Array(this.nextMonthBlankDays).concat(this.getDates(startDate, lastDate))
      } else {
        return this.getDates(startDate, lastDate)
      }
    },
    dates() {
      let currentDate = date.subtractFromDate(this.current_date, { months: 1 })
      let startDate = date.startOfDate(currentDate, 'month')
      console.log(startDate, 'startDate');
      let lastDate = date.endOfDate(
        date.subtractFromDate(this.current_date, { months: 1 }),
        'month'
      )
      if (this.blankDays > 0) {
        return Array(this.blankDays).concat(this.getDates(startDate, lastDate))
      } else {
        return this.getDates(startDate, lastDate)
      }
    },
    highlightedDates() {
      let dates = [];
  if (this.selected && this.selected.start_date && this.selected.end_date) {
    const startDate = date.clone(this.selected.start_date); // Clonando la fecha de inicio
    const endDate = date.clone(this.selected.end_date); // Clonando la fecha de fin

    if (startDate < endDate) { // Comparando fechas
      let idxDate = startDate;
      while (idxDate <= endDate) { // Mientras idxDate es igual o anterior a endDate
        dates.push(date.formatDate(idxDate, "D-M-YYYY")); // Formateando la fecha
        idxDate = date.addToDate(idxDate, { days: 1 }); // Añadiendo un día
      }
    } else {
      let idxDate = endDate;
      while (idxDate <= startDate) { // Mientras idxDate es igual o anterior a startDate
        dates.push(date.formatDate(idxDate, "D-M-YYYY")); // Formateando la fecha
        idxDate = date.addToDate(idxDate, { days: 1 }); // Añadiendo un día
      }
    }

    dates.shift(); // Elimina el primer elemento del array

    if (!this.start_date_selected && dates.length) {
      dates.pop(); // Elimina el último elemento del array si la fecha de inicio no está seleccionada
    }
  }
  return dates;
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
        let currentDate = date.extractDate(this.current_date)
        const lastMonth = this.transformDateIntoMoment(this.lastMonth)
        if (date.isValid(lastMonth)) {
          const currentDateObj = new Date(currentDate)
          const lastMonthObj = new Date(lastMonth)

          // Comprobando si currentDate es igual o posterior a lastMonth en el contexto de mes
          const isSameOrAfterMonth =
            currentDateObj.getFullYear() > lastMonthObj.getFullYear() ||
            (currentDateObj.getFullYear() === lastMonthObj.getFullYear() &&
              currentDateObj.getMonth() >= lastMonthObj.getMonth())

          // Comprobando si currentDate es igual o posterior a lastMonth en el contexto de año
          const isSameOrAfterYear = currentDateObj.getFullYear() >= lastMonthObj.getFullYear()

          if (isSameOrAfterMonth && isSameOrAfterYear) {
            return true
          }
        }
      }
      return false
    },
    isPrevMonthDisabled() {
      if (this.firstMonth) {
        let currentDate = date.extractDate(this.current_date)
        if (this.enableSecondCalendar) {
          currentDate = date.subtractFromDate(currentDate, { months: 1 })
        }
        const firstMonth = this.transformDateIntoMoment(this.firstMonth)
        if (date.isValid(firstMonth)) {
          const currentDateObj = new Date(currentDate)
          const firstMonthObj = new Date(firstMonth)

          // Comprobando si currentDate es igual o anterior a firstMonth en el contexto de mes
          const isSameOrBeforeMonth =
            currentDateObj.getFullYear() < firstMonthObj.getFullYear() ||
            (currentDateObj.getFullYear() === firstMonthObj.getFullYear() &&
              currentDateObj.getMonth() <= firstMonthObj.getMonth())

          // Comprobando si currentDate es igual o anterior a firstMonth en el contexto de año
          const isSameOrBeforeYear = currentDateObj.getFullYear() <= firstMonthObj.getFullYear()

          if (isSameOrBeforeMonth && isSameOrBeforeYear) {
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
          if (date.isValid(startDate)) {
            this.selected.start_date = date.startOfDate(startDate, 'date')
          } else {
            if (
              this.givenDateFormat &&
              this.givenDateFormat !== null &&
              this.givenDateFormat !== ''
            ) {
              this.selected.start_date = date.startOfDate(startDate, 'date')
            } else {
              let parsedDate = date.extractDate(startDate, this.givenDateFormat)
              this.selected.start_date = date.startOfDate(parsedDate, 'date')
            }
          }
          if (date.isValid(endDate)) {
            this.selected.end_date = date.endOfDate(endDate, 'date')
          } else {
            if (
              this.givenDateFormat &&
              this.givenDateFormat !== null &&
              this.givenDateFormat !== ''
            ) {
              let parsedDate = date.extractDate(endDate, this.givenDateFormat)
              this.selected.end_date = date.startOfDate(parsedDate, 'date')
            } else {
              this.selected.end_date = date.startOfDate(endDate, 'date')
            }
          }
        }
      } else {
        if (this.modelValue) {
          const selectedDate = this.modelValue
          if (date.isValid(selectedDate)) {
            this.selected_date = date.startOfDate(selectedDate, 'date')
          } else {
            if (
              this.givenDateFormat &&
              this.givenDateFormat !== null &&
              this.givenDateFormat !== ''
            ) {
              let parsedDate = date.extractDate(selectedDate, this.givenDateFormat)
              this.selected_date = date.startOfDate(parsedDate, 'date')
            } else {
              this.selected_date = moment(selectedDate).startOf('day')
            }
          }
        }
      }
      if (this.startMonth && this.startMonth !== null) {
        if (date.isValid(this.startMonth)) {
          this.current_date = this.startMonth.toDate()
        } else {
          if (
            this.givenDateFormat &&
            this.givenDateFormat !== null &&
            this.givenDateFormat !== ''
          ) {
            let parsedDate = date.extractDate(this.startMonth, this.givenDateFormat)
            this.current_date = date.startOfDate(parsedDate, 'date').toDate()
          } else {
            this.current_date = date.startOfDate(this.startMonth, 'date').toDate()
          }
        }
      }
    },
    onSelectDate(dt) {
      if (dt.isDisabled) {
        return
      }
      if (this.isRange) {
        if (!this.start_date_selected) {
          this.start_date_selected = true
          this.selected.end_date = null
          this.selected.start_date = date.clone(dt.date)
        } else {
          this.start_date_selected = false
          if (new Date(this.selected.start_date) > new Date(dt.date)) {
            this.selected.end_date = this.selected.start_date
            this.selected.start_date = dt.date
          } else {
            this.selected.end_date = date.clone(dt.date)
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

        this.selected.end_date = date.clone(dt.date)
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
        new Date(this.selected.start_date) == new Date(dt)
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
        new Date(this.selected.end_date) == new Date(dt)
      ) {
        return true
      }
      return false
    },
    isSelectedDate(dt) {
      if (!this.isRange && this.selected_date && new Date(this.selected) == new Date(dt)) {
        return true
      }
      return false
    },
    isHighlightedDate(dt) {
      if (
        this.highlightedDates &&
        this.highlightedDates.length &&
        this.highlightedDates.includes(date.formatDate(dt, 'D-M-YYYY'))
      ) {
        return true
      }
      return false
    },
    getDates(startDate, lastDate) {
      let dates = []
      while (new Date(startDate) < new Date(lastDate)) {
        var isHighlighted = this.isHighlightedDate(startDate)
        var isToday =
          this.isTodayHighlight &&
          new Date(date.startOfDate(new Date(), 'date')) == new Date(startDate)
        var isStartDate = this.isStartDate(startDate)
        var isEndDate = this.isEndDate(startDate)
        var isSelected = this.isSelectedDate(startDate) || isStartDate || isEndDate
        var isDisabled = this.isDisabledDate(startDate)
        let tmpDt = {
          date: date.clone(startDate),
          dateNumber: date.formatDate(startDate, 'D'),
          highlighted: isHighlighted,
          selected: isSelected,
          toDate: startDate,
          isDisabled: isDisabled,
          isToday: isToday,
          startDateSelected: isStartDate,
          endDateSelected: isEndDate
        }
        dates.push(tmpDt)
        startDate = date.addToDate(startDate, { days: 1 })
      }
      return dates
    },
    moveNextMonth() {
      if (this.isNextMonthDisabled) {
        return
      }
      this.current_date = date.addToDate(this.current_date, { months: 1 }).toDate()
    },
    movePrevMonth() {
      if (this.isPrevMonthDisabled) {
        return
      }
      this.current_date = date.subtractFromDate(this.current_date, { months: 1 }).toDate()
    },
    emitRangeDate() {
      let selected
      if (this.isRange) {
        selected = [this.selected.start_date, this.selected.end_date]
      } else {
        selected = this.selected_date
      }
      this.$emit('onSelect', selected)
      this.$emit('update:modelValue', selected)
    },
    clickClear() {
      if (this.isRange) {
        this.start_date_selected = false
        this.selected.start_date = null
        this.selected.end_date = null
      } else {
        this.selected_date = null
      }
      this.$emit('clearDates')
    },
    clickCancel() {
      this.$emit('onCancel')
    },
    transformDateIntoMoment(dates) {
      if (Array.isArray(dates)) {
        return dates.map((d) => {
          if (date.isValid(d)) {
            return date.startOfDate(d, 'date')
          } else {
            if (
              this.givenDateFormat &&
              this.givenDateFormat !== null &&
              this.givenDateFormat !== ''
            ) {
              let parseDate = date.extractDate(d, this.givenDateFormat)
              return date.startOfDate(parseDate, 'date')
            } else {
              return date.startOfDate(d, 'date')
            }
          }
        })
      } else {
        if (date.isValid(dates)) {
          return date.startOfDate(dates, 'date')
        } else {
          if (
            this.givenDateFormat &&
            this.givenDateFormat !== null &&
            this.givenDateFormat !== ''
          ) {
            let parseDate = date.extractDate(dates, this.givenDateFormat)
            return date.startOfDate(parseDate, 'date')
          } else {

            return date.startOfDate(dates, 'date')
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
        if (new Date(fromDate) <= new Date(dt) && new Date(dt) <= new Date(toDate)) {
          return true
        }
      } else {
        if (fromDate && new Date(fromDate) <= new Date(dt) && new Date(dt) <= new Date(fromDate)) {
          return true
        }
        if (toDate && new Date(toDate) <= new Date(dt) && new Date(dt) <= new Date(toDate)) {
          return true
        }
      }
      return false
    },
    isDisabledDate(dt) {
      if (
        this._disabledDates &&
        this._disabledDates.length &&
        this._disabledDates.includes(date.formatDate(dt, 'D-MM-YYYY'))
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
    }
  }
}
</script>

<style lang="scss" scoped>
.g-calendar {

  .calendar-container {
    display: flex;

    .current-calendar,
    .next-calendar {
      flex: 1;
    }
    .current-calendar {
      padding-right: 5px;
      border-right: #999 1px solid;
    }
    .next-calendar {
      margin-left: 2px;
      padding-left: 2px;
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
          background: #7a7575;
          color: #a19c9cf0;
        }
        &.date-today {
          background: #5a7fe6;
          color: rgb(45, 45, 45);
        }
        &.date-highlighted {
          background: red !important;
          color: #fff;
        }
        &.date-selected {
          background: purple !important;
          color: #fff;
        }
      }
    }
  }
}
</style>
