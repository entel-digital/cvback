<template>
  <div class="datepicker-container">
    <div :class="calendarClass">
      <div :class="calendarContainerClass">
        <div class="q-px-xs q-py-md q-gutter-sm fit column">
          <q-btn color="primary" label="Hoy" />
          <q-btn color="primary" label="Ayer" />
          <q-btn color="primary" label="Semana" />
          <q-btn color="primary" label="Mes" />
          <q-btn color="primary" label="Año" />
        </div>
        <div
          :class="data.classes"
          v-for="(data, dataIdx) in monthsData"
          :key="'month_data' + dataIdx"
        >
          <div class="calendar-header q-px-lg">
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
          <div class="calendar-dates q-px-lg" style="height: 250px">
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
                'date-selected-end': dt.endDateSelected,
                'date-hover': dt.isHovered
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
          <div>
            <select v-model="selected" style="max-width: 50px">
              <option disabled value="">Seleccione un elemento</option>
              <option>A</option>
              <option>B</option>
              <option>C</option>
            </select>
            :
            <select v-model="selected" style="max-width: 50px">
              <option disabled value="">Seleccione un elemento</option>
              <option>A</option>
              <option>B</option>
              <option>C</option>
            </select>
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
  </div>
</template>

<script>
import { date } from 'quasar'

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
      start_date_selected: false,
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
  },
  computed: {
    currentMonth() {
      return date.formatDate(
        date.subtractFromDate(new Date(this.current_date), { months: 1 }),
        'MMMM',
        { months: this.months, monthsShort: this.monthsShort }
      )
    },
    nextMonth() {
      return date.formatDate(new Date(this.current_date), 'MMMM', {
        months: this.months,
        monthsShort: this.monthsShort
      })
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
      let firstDay = date
        .startOfDate(date.subtractFromDate(new Date(this.current_date), { months: 1 }))
        .getDay()
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
      let firstDay = date.startOfDate(new Date(this.current_date), 'month').getDay()
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
      let startDate = date.startOfDate(date.clone(new Date(this.current_date)), 'month')
      let lastDate = date.endOfDate(date.clone(startDate), 'month')
      if (this.nextMonthBlankDays > 0) {
        return Array(this.nextMonthBlankDays).concat(this.getDates(startDate, lastDate))
      } else {
        return this.getDates(startDate, lastDate)
      }
    },
    dates() {
      let startDate = date.startOfDate(
        date.subtractFromDate(new Date(this.current_date), { months: 1 }),
        'month'
      )
      let lastDate = date.endOfDate(
        date.subtractFromDate(new Date(this.current_date), { months: 1 }),
        'month'
      )
      if (this.blankDays > 0) {
        return Array(this.blankDays).concat(this.getDates(startDate, lastDate))
      } else {
        return this.getDates(startDate, lastDate)
      }
    },
    highlightedDates() {
      let dates = []
      if (this.selected && this.selected.start_date && this.selected.end_date) {
        const startDate = date.clone(this.selected.start_date)
        const endDate = date.clone(this.selected.end_date)
        if (startDate.getTime() < endDate.getTime()) {
          let idxDate = startDate
          while (idxDate.getTime() <= endDate.getTime()) {
            dates.push(date.formatDate(date.clone(idxDate), 'D-M-YYYY'))
            date.addToDate(idxDate, { days: 1 })
          }
        } else {
          let idxDate = date.clone(endDate)
          while (idxDate.getTime() <= startDate.getTime()) {
            dates.push(date.formatDate(date.clone(idxDate), 'D-M-YYYY'))
            date.addToDate(idxDate, { days: 1 })
          }
        }
      }
      dates.shift()
      if (!this.start_date_selected && dates.length) {
        dates.pop()
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
      return disabledDates.map((d) => date.formatDate(d, 'D-M-YYYY'))
    },
    isNextMonthDisabled() {
      if (this.lastMonth) {
        let currentDate = date.clone(new Date(this.current_date))
        // moment(this.current_date).clone();

        const lastMonth = this.transformDateIntoMoment(this.lastMonth)
        if (lastMonth instanceof Date) {
          const currentDate = new Date(this.current_date) // La fecha actual
          const lastMonth = new Date(this.last_month) // La fecha del mes anterior

          // Comprobar si currentDate es el mismo o posterior a lastMonth en mes y año
          const isSameOrAfterMonth =
            currentDate.getFullYear() > lastMonth.getFullYear() ||
            (date.isSameDate(currentDate.getFullYear(), lastMonth.getFullYear()) &&
              currentDate.getMonth() >= lastMonth.getMonth())

          const isSameOrAfterYear = currentDate.getFullYear() >= lastMonth.getFullYear()

          if (isSameOrAfterMonth && isSameOrAfterYear) {
            return true
          }
        }
      }
      return false
    },
    isPrevMonthDisabled() {
      if (this.firstMonth) {
        let currentDate = date.clone(this.current_date)
        // let currentDate = moment(this.current_date).clone();
        if (this.enableSecondCalendar) {
          currentDate = date.subtractFromDate(currentDate, { months: 1 })

          // currentDate = currentDate.subtract(1, "M");
        }
        const firstMonth = this.transformDateIntoMoment(this.firstMonth)
        if (firstMonth instanceof Date) {
          const currentDate = new Date(this.current_date) // La fecha actual
          const firstMonth = new Date(this.first_month) // La fecha del primer mes

          // Comprobar si currentDate es el mismo o anterior a firstMonth en mes y año
          const isSameOrBeforeMonth =
            currentDate.getFullYear() < firstMonth.getFullYear() ||
            (date.isSameDate(currentDate.getFullYear(), firstMonth.getFullYear()) &&
              currentDate.getMonth() <= firstMonth.getMonth())

          const isSameOrBeforeYear = currentDate.getFullYear() <= firstMonth.getFullYear()

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
            const startDate = this.modelValue[0];
            const endDate = this.modelValue[1];

            // Manejo de la fecha de inicio
            if (startDate instanceof Date) {
                this.selected.start_date = date.startOfDate(startDate, 'day');
            } else {
                if (this.givenDateFormat && this.givenDateFormat !== null && this.givenDateFormat !== '') {
                    this.selected.start_date = date.startOfDate(
                        date.formatDate(startDate, this.givenDateFormat),
                        'day'
                    );
                } else {
                    this.selected.start_date = date.startOfDate(startDate, 'day');
                }
            }

            // Manejo de la fecha de fin
            if (endDate instanceof Date) {
                this.selected.end_date = date.endOfDate(endDate, 'day');
            } else {
                if (this.givenDateFormat && this.givenDateFormat !== null && this.givenDateFormat !== '') {
                    this.selected.end_date = date.startOfDate(
                        date.formatDate(endDate, this.givenDateFormat),
                        'day'
                    );
                } else {
                    this.selected.end_date = date.startOfDate(endDate, 'day');
                }
            }
        }
    } else {
        if (this.modelValue) {
            const selectedDate = this.modelValue;

            // Manejo de la fecha seleccionada
            if (selectedDate instanceof Date) {
                this.selected_date = date.startOfDate(selectedDate, 'day');
            } else {
                if (this.givenDateFormat && this.givenDateFormat !== null && this.givenDateFormat !== '') {
                    this.selected_date = date.startOfDate(
                        date.formatDate(selectedDate, this.givenDateFormat),
                        'day'
                    );
                } else {
                    this.selected_date = date.startOfDate(selectedDate, 'day');
                }
            }
        }
    }

    // Manejo de la fecha del mes de inicio
    if (this.startMonth && this.startMonth !== null) {
        if (this.startMonth instanceof Date) {
            this.current_date = date.startOfDate(this.startMonth, 'day');
        } else {
            if (this.givenDateFormat && this.givenDateFormat !== null && this.givenDateFormat !== '') {
                this.current_date = date.startOfDate(
                    date.formatDate(new Date(this.startMonth), this.givenDateFormat),
                    'day'
                );
            } else {
                this.current_date = date.startOfDate(new Date(this.startMonth), 'day');
            }
        }
    }
},
    onSelectDate(dt) {
    if (dt.isDisabled) {
        return;
    }
    
    const cloneDate = (date) => {
        return new Date(date.getTime()); // Clona la fecha creando un nuevo objeto Date con el mismo timestamp
    };
    
    if (this.isRange) {
        if (!this.start_date_selected) {
            this.start_date_selected = true;
            this.selected.end_date = null;
            this.selected.start_date = cloneDate(dt.date); // Clona la fecha seleccionada
        } else {
            this.start_date_selected = false;
            if (this.selected.start_date.getTime() > dt.date.getTime()) {
                this.selected.end_date = cloneDate(this.selected.start_date); // Clona la fecha de inicio
                this.selected.start_date = cloneDate(dt.date); // Clona la nueva fecha seleccionada
            } else {
                this.selected.end_date = cloneDate(dt.date); // Clona la nueva fecha seleccionada
            }
            this.emitRangeDate();
        }
    } else {
        this.selected_date = cloneDate(dt.date); // Clona la fecha seleccionada
        this.emitRangeDate();
    }
},

    hoverDate(dt) {
    if (this.start_date_selected) {
        const cloneDate = (date) => {
            return new Date(date.getTime()); // Clona la fecha creando un nuevo objeto Date con el mismo timestamp
        };

        // Clona la fecha seleccionada antes de asignarla
        this.selected.end_date = cloneDate(dt.date);

        // Si quieres restaurar la lógica de comparación (descomentando el código original):
        /*
        if (this.selected.start_date.getTime() > dt.date.getTime()) {
            this.selected.end_date = this.selected.start_date;
            this.selected.start_date = cloneDate(dt.date);
        } else {
            this.selected.end_date = cloneDate(dt.date);
        }
        */
    }
    
    // Si quieres manejar el estado de `isHovered`, como en la nueva función:
    dt.isHovered = true;
},isStartDate(dt) {
    if (
        this.isRange &&
        this.selected.start_date &&
        this.selected.start_date.getTime() === dt.getTime()
    ) {
        return true;
    }
    return false;
},
isEndDate(dt) {
    if (
        this.isRange &&
        !this.start_date_selected &&
        this.selected.end_date &&
        date.isSameDate(this.selected.end_date, dt) // Corregido de 'selected.selected' a 'selected.end_date'
    ) {
        return true;
    }
    return false;
},
isSelectedDate(dt) {
    if (
        !this.isRange &&
        this.selected_date &&
        this.selected_date.getTime() === dt.getTime()
    ) {
        return true;
    }
    return false;
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
    let dates = [];
    while (startDate.getTime() < lastDate.getTime()) {
        var isHighlighted = this.isHighlightedDate(startDate);
        var isToday =
            this.isTodayHighlight && date.isSameDate(date.startOfDate(new Date(), 'day'), startDate);

        var isStartDate = this.isStartDate(startDate);
        var isEndDate = this.isEndDate(startDate);
        var isSelected = this.isSelectedDate(startDate) || isStartDate || isEndDate;
        var isDisabled = this.isDisabledDate(startDate);

        let tmpDt = {
            date: date.clone(startDate),
            dateNumber: date.formatDate(startDate, 'D'),
            highlighted: isHighlighted,
            selected: isSelected,
            toDate: new Date(startDate),
            isDisabled: isDisabled,
            isToday: isToday,
            startDateSelected: isStartDate,
            endDateSelected: isEndDate
        };
        dates.push(tmpDt);

        startDate = date.addToDate(startDate, { day: 1 });
    }
    return dates;
},
moveNextMonth() {
    if (this.isNextMonthDisabled) {
        return;
    }
    this.current_date = date.addToDate(new Date(this.current_date), { months: 1 });
},
movePrevMonth() {
    if (this.isPrevMonthDisabled) {
        return;
    }
    this.current_date = date.subtractFromDate(new Date(this.current_date), { months: 1 });
},
emitRangeDate() {
    let selected;
    if (this.isRange) {
        selected = [this.selected.start_date, this.selected.end_date];
    } else {
        selected = this.selected_date;
    }
    this.$emit("onSelect", selected);
    this.$emit("update:modelValue", selected);
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
    const transformDate = (d) => {
        if (d instanceof Date) {
            return date.startOfDate(d, 'day');
        } else {
            if (this.givenDateFormat && this.givenDateFormat.trim() !== '') {
                const parsedDate = date.parseDate(d, this.givenDateFormat);
                if (parsedDate) {
                    return date.startOfDate(parsedDate, 'day');
                } else {
                    // Manejar el caso donde la fecha no se puede parsear
                    return null; // O lanzar un error, dependiendo de tus necesidades
                }
            } else {
                const newDate = new Date(d);
                return date.startOfDate(newDate, 'day');
            }
        }
    };

    if (Array.isArray(dates)) {
        return dates.map(transformDate);
    } else {
        return transformDate(dates);
    }
},
isInRangeFromTo(data, dt) {
    let fromDate = null;
    let toDate = null;

    // Verificar si 'data' es un objeto con propiedades 'from' o 'to'
    if (data && typeof data === 'object' && ('from' in data || 'to' in data)) {
        if ('from' in data) {
            fromDate = this.transformDateIntoMoment(data.from);
        }
        if ('to' in data) {
            toDate = this.transformDateIntoMoment(data.to);
        }
    }

    // Comparar las fechas
    if (fromDate && toDate) {
        // Comparación utilizando el método isSameOrAfter y isSameOrBefore
        if (dt.getTime() >= fromDate.getTime() && dt.getTime() <= toDate.getTime()) {
            return true;
        }
    } else {
        if (fromDate && dt.getTime() >= fromDate.getTime()) {
            return true;
        }
        if (toDate && dt.getTime() <= toDate.getTime()) {
            return true;
        }
    }
    return false;
},
isDisabledDate(dt) {
    // Verificar si la fecha está en la lista de fechas deshabilitadas
    if (
        this._disabledDates &&
        this._disabledDates.length &&
        this._disabledDates.includes(date.formatDate(dt, 'D-M-YYYY'))
    ) {
        return true;
    }

    // Verificar si la fecha está dentro del rango de fechas deshabilitadas
    if (this.isInRangeFromTo(this.disabledFromTo, dt)) {
        return true;
    }

    // Verificar si estamos en un rango
    if (this.isRange) {
        // Si no se ha seleccionado la fecha de inicio
        if (!this.start_date_selected) {
            // Verificar si la fecha está dentro de las fechas de inicio deshabilitadas
            if (this.isInRangeFromTo(this.disabledStartDates, dt)) {
                return true;
            }
        } else {
            // Verificar si la fecha está dentro de las fechas de fin deshabilitadas
            if (this.isInRangeFromTo(this.disabledEndDates, dt)) {
                return true;
            }
        }
    }

    // Si ninguna condición se cumple, devolver false
    return false;
}
  }
}
</script>

<style lang="scss">
.datepicker-container {
  background-color: white; 
  width: fit-content;
   border: 1px solid red;
   position: absolute;
   left: -350px
}
.border-right-line {
  border-right: 1px solid blue;
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
          background: rgb(67, 237, 182);
          color: rgb(45, 45, 45);
        }
        &.date-highlighted {
          background: #478f8b9c !important;
          color: #fff;
        }
        &.date-selected {
          background: #4fa5a1 !important;
          color: #fff;
        }
      }
    }
  }
}
</style>
