<template>
  <div>
    <date-range-picker
      ref="picker"
      :opens="opens"
      :locale-data="{ firstDay: 1, format: 'dd-mm-yyyy HH:mm:ss' }"
      :minDate="minDate"
      :maxDate="maxDate"
      :singleDatePicker="singleDatePicker"
      :timePicker="timePicker"
      :timePicker24Hour="timePicker24Hour"
      :showWeekNumbers="showWeekNumbers"
      :showDropdowns="showDropdowns"
      :autoApply="autoApply"
      v-model="dateRange"
      @update="updateValues"
      @toggle="logEvent('event: open', $event)"
      @start-selection="logEvent('event: startSelection', $event)"
      @finish-selection="logEvent('event: finishSelection', $event)"
      :linkedCalendars="linkedCalendars"
      :dateFormat="dateFormat"
    >
      <!-- <template v-slot:input="picker" style="min-width: 350px">
        {{ picker.startDate | date }} - {{ picker.endDate | date }}
      </template> -->
    </date-range-picker>
    {{ dateRange }}
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'

import DateRangePicker from 'vue2-daterange-picker'
import 'vue2-daterange-picker/dist/vue2-daterange-picker.css'

export default defineComponent({
  components: {
    DateRangePicker
  },

  setup() {
    let today = new Date()
    today.setHours(0, 0, 0, 0)

    let yesterday = new Date()
    yesterday.setDate(today.getDate() - 1)
    yesterday.setHours(0, 0, 0, 0)

    const updateValues = (value) => {
      if (!dateRange.value) {
        console.error('dateRange is null')
        // Initialize dateRange to some default value or handle the error appropriately
        dateRange.value = { startDate: new Date(), endDate: new Date() }
      }
      console.log('value updateValues', value)
    }

    const dateRange = ref({
      startDate: new Date(),
      endDate: new Date()
    })
    console.log('dateRange', dateRange)

    onMounted(() => {
      if (!dateRange.value) {
        // Ensure dateRange is not null upon component mount
        dateRange.value = { startDate: new Date(), endDate: new Date() }
      }
    })

            const opens=ref("left")
            const localeData=ref("{ firstDay: 1, format: 'dd-mm-yyyy HH:mm:ss' }")
            const minDate= ref(new Date())
            const maxDate= ref(new Date())
            const singleDatePicker=ref(false)
            const timePicker=ref(false)
            const timePicker24Hour=ref(false)
            const showWeekNumbers=ref(false)
            const showDropdowns=ref(false)
            const autoApply=ref(false)

            const linkedCalendars=ref(false)
            const dateFormat=ref(false)
    return {
      opens,
      localeData,
      minDate,
      maxDate,
      singleDatePicker,
      timePicker,
      timePicker24Hour,
      showWeekNumbers,
      showDropdowns,
      autoApply,
      linkedCalendars,
      dateFormat,
      dateRange,
      today,
      yesterday,
      updateValues
    }
  }
})
</script>
