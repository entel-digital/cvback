<template>
  <q-input
    outlined
    :model-value="dateSelected"
    mask="date"
    dense
    :rules="['date']"
    placeholder="Selecciona una fecha"
  >
    <template v-slot:prepend>
      <q-icon name="event" class="cursor-pointer">
        <q-popup-proxy cover transition-show="scale" transition-hide="scale">
          <q-date
            v-model="date"
            minimal
            :locale="myLocale"
            today-btn
            :default-year-month="currentYeatMonth"
            v-close-popup
          >
          </q-date>
        </q-popup-proxy>
      </q-icon>
    </template>
  </q-input>
</template>
<script>
import { useGlobalStore } from "src/stores/global-store";
import { defineComponent, ref, watch } from "vue";

export default defineComponent({
  name: "InputDatePicker",
  props: ["dateSelected"],
  setup() {
    const date = ref(null);
    const myLocale = {
      days: "Lunes_Martes_Miércoles_Jueves_Viernes_Sábado_Domingo".split("_"),
      daysShort: "Lun_Mar_Mié_Jue_Vie_Sáb_Dom".split("_"),
      months:
        "Enero_Febrero_Marzo_Abril_Mayo_Junio_Julio_Agosto_Septiembre_Octubre_Noviembre_Diciembre".split(
          "_"
        ),
      monthsShort: "Ene_Feb_Mar_Abr_May_Jun_Jul_Ago_Sep_Oct_Nov_Dic".split("_"),
      firstDayOfWeek: 0,
      format24h: true,
      pluralDay: "dias",
    };
    const currentYeatMonth = new Date()
      .toISOString()
      .substr(0, 7)
      .replace("-", "/");

    watch(date, (newDate) => {
      useGlobalStore().dateToFilter = newDate;
    });

    return { date, myLocale, currentYeatMonth };
  },
});
</script>
