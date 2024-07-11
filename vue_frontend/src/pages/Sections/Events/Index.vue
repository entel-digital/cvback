<template>
  <q-page :class="$q.screen.lt.md ? 'space-page-responsive' : 'space-page'">
    <div>
      <q-tab-panels :model-value="tabPanel">
        <q-tab-panel name="event-management" class="no-padding">
          <TableEvents
            :rows="allEvents"
            :columns="columns"
            :loading="loading"
          />
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted, onUnmounted } from "vue";
import { useGlobalStore } from "stores/global-store";

import TableEvents from "src/components/TableEvents.vue";

const columns = [
  {
    name: "name",
    required: true,
    label: "Evento",
    align: "left",
    field: (row) => row.id,
    format: (val) => `${val}`,
  },
  {
    name: "date",
    label: "Fecha",
    field: "addedDate",
    align: "center",
    sortable: true,
    sort: (a, b) => console.log("A", a),
  },
  {
    name: "detected",
    label: "EPP Detectados",
    field: "labelsDetected",
    align: "center",
    sortable: true,
    sort: (a, b) => parseInt(a, 10) - parseInt(b, 10),
  },
  {
    name: "missing",
    label: "EPP No Detectados",
    field: "labelsMissing",
    align: "center",
    sortable: true,
    sort: (a, b) => parseInt(a, 10) - parseInt(b, 10),
  },
  {
    name: "action",
    label: "",
    field: "",
    align: "center",
  },
];

export default defineComponent({
  name: "EventsPage",
  components: {
    TableEvents,
  },

  setup() {
    const globalStore = useGlobalStore();
    const tabPanel = ref("event-management");
    const allEvents = ref([]);
    const loading = ref(true);
    const intervalId = ref(null);

    const fetchAllEvents = async () => {
      allEvents.value = await globalStore.FETCH_EVENTS();
      loading.value = false;
    };

    const handleTabSelected = (tabSelected) => {
      tabPanel.value = tabSelected;
    };

    const clearFilters = () => {
      useGlobalStore().dateToFilter = null;
    };
    onMounted(() => {
      fetchAllEvents();
      intervalId.value = setInterval(fetchData, 30000);
    });

    onUnmounted(() => {
      if (intervalId.value) {
        clearInterval(intervalId);
      }
    });

    return {
      tabPanel,
      columns,
      handleTabSelected,
      allEvents,
      clearFilters,
      loading,
    };
  },
});
</script>
