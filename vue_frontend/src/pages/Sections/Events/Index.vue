<template>
  <q-page :class="$q.screen.lt.md ? 'space-page-responsive' : 'space-page'">
    <div class="q-pt-lg q-pb-md">
      <!-- <TabsMenu :tabs="tabs" @tabSelectedChanged="handleTabSelected" /> -->
    </div>
    <div>
      <q-tab-panels :model-value="tabPanel">
        <q-tab-panel name="event-management" class="no-padding">
          <TableEvents :rows="allEvents" :columns="columns" />
        </q-tab-panel>
        <!-- <q-tab-panel name="event-historic"> table events historic </q-tab-panel> -->
        <!-- <q-tab-panel name="event-video"> table events video </q-tab-panel> -->
        <!-- <q-tab-panel name="event-map"> table events map </q-tab-panel> -->
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted } from "vue";
import { useGlobalStore } from "stores/global-store";

// import TabsMenu from "src/components/Tabs.vue";
import TableEvents from "src/components/TableEvents.vue";
import { all } from "axios";

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
    sort: (a, b) => parseInt(a, 10) - parseInt(b, 10),
  },
  {
    name: "detected",
    label: "Detectados",
    field: "labelsDetected",
    align: "center",
    sortable: true,
    sort: (a, b) => parseInt(a, 10) - parseInt(b, 10),
  },
  {
    name: "missing",
    label: "No encontrados",
    field: "labelsMissing",
    align: "center",
    sortable: true,
    sort: (a, b) => parseInt(a, 10) - parseInt(b, 10),
  },
];

const rows = [
  {
    id: "1",
    addedDate: "2024-01-04T23:28:52.256922+00:00",
    labelsDetected: {
      colorGroup: "brown",
      id: "1",
      name: "uno",
    },
    labelsMissing: {
      colorGroup: "#4rt0000",
      id: "1",
      name: "uno",
    },
  },
  {
    id: "2",
    addedDate: "2024-01-04T23:28:52.262088+00:00",
    labelsDetected: {
      colorGroup: "orange",
      id: "2",
      name: "dos",
    },
    labelsMissing: {
      colorGroup: "#4rt0000",
      id: "2",
      name: "dos",
    },
  },
  {
    id: "3",
    addedDate: "2024-01-04T23:28:52.266402+00:00",
    labelsDetected: {
      colorGroup: "yellow",
      id: "3",
      name: "tres",
    },
    labelsMissing: {
      colorGroup: "#4rt0000",
      id: "3",
      name: "tres",
    },
  },
  {
    id: "4",
    addedDate: "2024-01-04T23:28:52.270287+00:00",
    labelsDetected: {
      colorGroup: "green",
      id: "4",
      name: "cuatro",
    },
    labelsMissing: {
      colorGroup: "#4rt0000",
      id: "4",
      name: "cuatro",
    },
  },
  {
    id: "5",
    addedDate: "2024-01-04T23:28:52.275598+00:00",
    labelsDetected: {
      colorGroup: "red",
      id: "5",
      name: "cinco",
    },
    labelsMissing: {
      colorGroup: "#ggg0000",
      id: "5",
      name: "cinco",
    },
  },
  // {
  //   id: "6",
  //   addedDate: "2024-01-04T23:28:52.280904+00:00",
  // },
  // {
  //   id: "7",
  //   addedDate: "2024-01-04T23:28:52.285217+00:00",
  // },
  // {
  //   id: "8",
  //   addedDate: "2024-01-04T23:28:52.289486+00:00",
  // },
  // {
  //   id: "9",
  //   addedDate: "2024-01-04T23:28:52.293639+00:00",
  // },
  // {
  //   id: "10",
  //   addedDate: "2024-01-04T23:28:52.297668+00:00",
  // },
];

const tabs = [
  {
    value: "event-management",
    label: "Eventos",
    disable: false,
  },
  // {
  //   value: "event-historic",
  //   label: "Histórico",
  //   disable: true,
  // },
  // {
  //   value: "event-video",
  //   label: "Video",
  //   disable: true,
  // },
  // {
  //   value: "event-map",
  //   label: "Mapa",
  //   disable: true,
  // },
];

export default defineComponent({
  name: "EventsPage",
  components: {
    // TabsMenu,
    TableEvents,
  },

  setup() {
    const globalStore = useGlobalStore();
    const tabPanel = ref("event-management");
    const allEvents = ref([]);

    const fetchAllEvents = async () => {
      allEvents.value = await globalStore.FETCH_EVENTS();
      console.log(" allEvents.value", allEvents.value);
    };

    const handleTabSelected = (tabSelected) => {
      tabPanel.value = tabSelected;
    };

    onMounted(() => {
      fetchAllEvents();
    });

    return {
      tabPanel,
      globalStore,
      columns,
      rows,
      tabs,
      handleTabSelected,
      allEvents,
    };
  },
});
</script>
