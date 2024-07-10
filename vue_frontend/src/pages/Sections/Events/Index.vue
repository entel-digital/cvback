<template>
  <q-page :class="$q.screen.lt.md ? 'space-page-responsive' : 'space-page'">
    <!-- <div class="q-pt-lg q-pb-md row justify-between">
      <TabsMenu :tabs="tabs" @tabSelectedChanged="handleTabSelected" />
      <q-btn
        color="secondary"
        label="Filtros"
        icon="filter_list"
        icon-right="arrow_drop_down"
        flat
      >
        <q-menu anchor="bottom right" self="top right">
          <q-list style="min-width: 200px" class="q-pa-md">
            <q-item>
              <q-item-section>
                <q-item-label class="text-dark barlow-bold fs-16-19">
                  Tipo de Evento:
                </q-item-label>
                <div class="q-py-md">
                  <SelectOptionsMultiple />
                </div>
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section>
                <q-item-label class="text-dark barlow-bold fs-16-19">
                  Fecha:
                </q-item-label>
                <div class="q-py-md">
                  <InputDatePicker :dateSelected="globalStore.dateToFilter" />
                </div>
              </q-item-section>
            </q-item>

            <q-separator />
            <div class="row justify-end q-py-md q-gutter-x-md">
              <q-btn label="Filtrar" dense color="primary" class="q-px-sm" />
              <q-btn
                label="Limpiar"
                flat
                dense
                color="primary"
                class="q-px-sm"
                @click="clearFilters"
              />
            </div>
          </q-list>
        </q-menu>
      </q-btn>
    </div> -->
    <div>
      <q-tab-panels :model-value="tabPanel">
        <q-tab-panel name="event-management" class="no-padding">
          <TableEvents :rows="allEvents" :columns="columns" />
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted } from "vue";
import { useGlobalStore } from "stores/global-store";

import TabsMenu from "src/components/Tabs.vue";
import TableEvents from "src/components/TableEvents.vue";
// import InputDatePicker from "src/components/InputDatePicker.vue";
// import SelectOptionsMultiple from "src/components/SelectOptionsMultiple.vue";

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

const rows = [
  {
    id: "11",
    addedDate: "2024-07-02T01:49:10.374375+00:00",
    confidence: 0.9114600162581257,
    eventType: {
      name: "food",
      id: "11",
    },
    inferenceDetectionClassification: null,
    frames: [
      {
        image: "~assets/img_test.jpeg",
        id: "11",
        keyframesSet: [
          {
            id: "11",
          },
          {
            id: "16",
          },
          {
            id: "17",
          },
          {
            id: "18",
          },
          {
            id: "19",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "12",
        keyframesSet: [
          {
            id: "12",
          },
          {
            id: "13",
          },
          {
            id: "17",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "18",
        keyframesSet: [
          {
            id: "15",
          },
          {
            id: "19",
          },
          {
            id: "20",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "20",
        keyframesSet: [
          {
            id: "12",
          },
          {
            id: "14",
          },
          {
            id: "17",
          },
        ],
      },
    ],
    labelsDetected: [
      {
        colorGroup: "PERSON",
        name: "part",
      },
      {
        colorGroup: "PERSON",
        name: "member",
      },
      {
        colorGroup: "OTHER",
        name: "heart",
      },
    ],
    labelsMissing: [
      {
        colorGroup: "ANIMAL",
        name: "history",
        id: "18",
      },
    ],
  },
  {
    id: "12",
    addedDate: "2024-07-02T01:49:10.484511+00:00",
    confidence: 0.24076672633495677,
    eventType: {
      name: "respond",
      id: "20",
    },
    inferenceDetectionClassification: null,
    frames: [
      {
        image: "src/assets/img_test.jpeg",
        id: "12",
        keyframesSet: [
          {
            id: "12",
          },
          {
            id: "13",
          },
          {
            id: "17",
          },
        ],
      },
    ],
    labelsDetected: [
      {
        colorGroup: "PERSON",
        name: "member",
      },
      {
        colorGroup: "OTHER",
        name: "heart",
      },
      {
        colorGroup: "ANIMAL",
        name: "history",
      },
      {
        colorGroup: "ID",
        name: "put",
      },
      {
        colorGroup: "VEHICLE",
        name: "garden",
      },
    ],
    labelsMissing: [
      {
        colorGroup: "PERSON",
        name: "member",
        id: "13",
      },
      {
        colorGroup: "VEHICLE",
        name: "garden",
        id: "20",
      },
    ],
  },
  {
    id: "13",
    addedDate: "2024-07-02T01:49:10.580912+00:00",
    confidence: 0.6332379000791042,
    eventType: {
      name: "create",
      id: "18",
    },
    inferenceDetectionClassification: null,
    frames: [
      {
        image: "src/assets/img_test.jpeg",
        id: "12",
        keyframesSet: [
          {
            id: "12",
          },
          {
            id: "13",
          },
          {
            id: "17",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "13",
        keyframesSet: [
          {
            id: "13",
          },
          {
            id: "17",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "14",
        keyframesSet: [
          {
            id: "12",
          },
          {
            id: "20",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "16",
        keyframesSet: [
          {
            id: "11",
          },
          {
            id: "13",
          },
          {
            id: "15",
          },
          {
            id: "16",
          },
          {
            id: "17",
          },
          {
            id: "19",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "18",
        keyframesSet: [
          {
            id: "15",
          },
          {
            id: "19",
          },
          {
            id: "20",
          },
        ],
      },
    ],
    labelsDetected: [
      {
        colorGroup: "ID",
        name: "he",
      },
      {
        colorGroup: "OTHER",
        name: "heart",
      },
      {
        colorGroup: "VEHICLE",
        name: "leg",
      },
      {
        colorGroup: "ANIMAL",
        name: "history",
      },
    ],
    labelsMissing: [
      {
        colorGroup: "PERSON",
        name: "part",
        id: "11",
      },
    ],
  },
  {
    id: "14",
    addedDate: "2024-07-02T01:49:10.651401+00:00",
    confidence: 0.21189269742846206,
    eventType: {
      name: "create",
      id: "18",
    },
    inferenceDetectionClassification: null,
    frames: [
      {
        image: "src/assets/img_test.jpeg",
        id: "12",
        keyframesSet: [
          {
            id: "12",
          },
          {
            id: "13",
          },
          {
            id: "17",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "15",
        keyframesSet: [
          {
            id: "11",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "16",
        keyframesSet: [
          {
            id: "11",
          },
          {
            id: "13",
          },
          {
            id: "15",
          },
          {
            id: "16",
          },
          {
            id: "17",
          },
          {
            id: "19",
          },
        ],
      },
    ],
    labelsDetected: [
      {
        colorGroup: "OTHER",
        name: "heart",
      },
      {
        colorGroup: "ID",
        name: "design",
      },
    ],
    labelsMissing: [
      {
        colorGroup: "PERSON",
        name: "member",
        id: "13",
      },
      {
        colorGroup: "ID",
        name: "he",
        id: "14",
      },
      {
        colorGroup: "ID",
        name: "design",
        id: "17",
      },
      {
        colorGroup: "ID",
        name: "put",
        id: "19",
      },
      {
        colorGroup: "VEHICLE",
        name: "garden",
        id: "20",
      },
    ],
  },
  {
    id: "15",
    addedDate: "2024-07-02T01:49:10.763423+00:00",
    confidence: 0.6481553611879278,
    eventType: {
      name: "animal",
      id: "16",
    },
    inferenceDetectionClassification: null,
    frames: [
      {
        image: "src/assets/img_test.jpeg",
        id: "11",
        keyframesSet: [
          {
            id: "11",
          },
          {
            id: "16",
          },
          {
            id: "17",
          },
          {
            id: "18",
          },
          {
            id: "19",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "17",
        keyframesSet: [
          {
            id: "15",
          },
          {
            id: "16",
          },
          {
            id: "20",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "20",
        keyframesSet: [
          {
            id: "12",
          },
          {
            id: "14",
          },
          {
            id: "17",
          },
        ],
      },
    ],
    labelsDetected: [
      {
        colorGroup: "PERSON",
        name: "part",
      },
      {
        colorGroup: "OTHER",
        name: "story",
      },
      {
        colorGroup: "OTHER",
        name: "heart",
      },
      {
        colorGroup: "ID",
        name: "design",
      },
      {
        colorGroup: "ANIMAL",
        name: "history",
      },
    ],
    labelsMissing: [
      {
        colorGroup: "PERSON",
        name: "member",
        id: "13",
      },
    ],
  },
  {
    id: "16",
    addedDate: "2024-07-02T01:49:10.886688+00:00",
    confidence: 0.15164848558258626,
    eventType: {
      name: "food",
      id: "11",
    },
    inferenceDetectionClassification: null,
    frames: [
      {
        image: "src/assets/img_test.jpeg",
        id: "13",
        keyframesSet: [
          {
            id: "13",
          },
          {
            id: "17",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "18",
        keyframesSet: [
          {
            id: "15",
          },
          {
            id: "19",
          },
          {
            id: "20",
          },
        ],
      },
    ],
    labelsDetected: [
      {
        colorGroup: "PERSON",
        name: "part",
      },
      {
        colorGroup: "OTHER",
        name: "heart",
      },
      {
        colorGroup: "VEHICLE",
        name: "leg",
      },
    ],
    labelsMissing: [
      {
        colorGroup: "OTHER",
        name: "story",
        id: "12",
      },
      {
        colorGroup: "ID",
        name: "put",
        id: "19",
      },
      {
        colorGroup: "VEHICLE",
        name: "garden",
        id: "20",
      },
    ],
  },
  {
    id: "17",
    addedDate: "2024-07-02T01:49:11.008979+00:00",
    confidence: 0.6564961744772145,
    eventType: {
      name: "site",
      id: "12",
    },
    inferenceDetectionClassification: null,
    frames: [
      {
        image: "src/assets/img_test.jpeg",
        id: "11",
        keyframesSet: [
          {
            id: "11",
          },
          {
            id: "16",
          },
          {
            id: "17",
          },
          {
            id: "18",
          },
          {
            id: "19",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "13",
        keyframesSet: [
          {
            id: "13",
          },
          {
            id: "17",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "15",
        keyframesSet: [
          {
            id: "11",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "17",
        keyframesSet: [
          {
            id: "15",
          },
          {
            id: "16",
          },
          {
            id: "20",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "20",
        keyframesSet: [
          {
            id: "12",
          },
          {
            id: "14",
          },
          {
            id: "17",
          },
        ],
      },
    ],
    labelsDetected: [
      {
        colorGroup: "PERSON",
        name: "part",
      },
      {
        colorGroup: "OTHER",
        name: "heart",
      },
    ],
    labelsMissing: [
      {
        colorGroup: "PERSON",
        name: "member",
        id: "13",
      },
      {
        colorGroup: "ID",
        name: "he",
        id: "14",
      },
      {
        colorGroup: "ID",
        name: "design",
        id: "17",
      },
      {
        colorGroup: "VEHICLE",
        name: "garden",
        id: "20",
      },
    ],
  },
  {
    id: "18",
    addedDate: "2024-07-02T01:49:11.124678+00:00",
    confidence: 0.39248141466529285,
    eventType: {
      name: "food",
      id: "11",
    },
    inferenceDetectionClassification: null,
    frames: [
      {
        image: "src/assets/img_test.jpeg",
        id: "12",
        keyframesSet: [
          {
            id: "12",
          },
          {
            id: "13",
          },
          {
            id: "17",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "13",
        keyframesSet: [
          {
            id: "13",
          },
          {
            id: "17",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "15",
        keyframesSet: [
          {
            id: "11",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "20",
        keyframesSet: [
          {
            id: "12",
          },
          {
            id: "14",
          },
          {
            id: "17",
          },
        ],
      },
    ],
    labelsDetected: [
      {
        colorGroup: "PERSON",
        name: "member",
      },
      {
        colorGroup: "ID",
        name: "design",
      },
      {
        colorGroup: "ANIMAL",
        name: "history",
      },
      {
        colorGroup: "ID",
        name: "put",
      },
    ],
    labelsMissing: [
      {
        colorGroup: "ANIMAL",
        name: "history",
        id: "18",
      },
    ],
  },
  {
    id: "19",
    addedDate: "2024-07-02T01:49:11.195044+00:00",
    confidence: 0.7395576532356747,
    eventType: {
      name: "site",
      id: "12",
    },
    inferenceDetectionClassification: null,
    frames: [
      {
        image: "src/assets/img_test.jpeg",
        id: "13",
        keyframesSet: [
          {
            id: "13",
          },
          {
            id: "17",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "16",
        keyframesSet: [
          {
            id: "11",
          },
          {
            id: "13",
          },
          {
            id: "15",
          },
          {
            id: "16",
          },
          {
            id: "17",
          },
          {
            id: "19",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "18",
        keyframesSet: [
          {
            id: "15",
          },
          {
            id: "19",
          },
          {
            id: "20",
          },
        ],
      },
      {
        image: "src/assets/img_test.jpeg",
        id: "19",
        keyframesSet: [
          {
            id: "11",
          },
          {
            id: "12",
          },
          {
            id: "18",
          },
          {
            id: "19",
          },
        ],
      },
    ],
    labelsDetected: [
      {
        colorGroup: "PERSON",
        name: "part",
      },
      {
        colorGroup: "OTHER",
        name: "heart",
      },
    ],
    labelsMissing: [
      {
        colorGroup: "OTHER",
        name: "heart",
        id: "15",
      },
    ],
  },
  {
    id: "20",
    addedDate: "2024-07-02T01:49:11.262915+00:00",
    confidence: 0.8062176328609658,
    eventType: {
      name: "animal",
      id: "16",
    },
    inferenceDetectionClassification: null,
    frames: [
      {
        image: "src/assets/img_test.jpeg",
        id: "13",
        keyframesSet: [
          {
            id: "13",
          },
          {
            id: "17",
          },
        ],
      },
    ],
    labelsDetected: [
      {
        colorGroup: "OTHER",
        name: "story",
      },
      {
        colorGroup: "PERSON",
        name: "member",
      },
      {
        colorGroup: "ID",
        name: "he",
      },
    ],
    labelsMissing: [
      {
        colorGroup: "PERSON",
        name: "member",
        id: "13",
      },
      {
        colorGroup: "OTHER",
        name: "heart",
        id: "15",
      },
      {
        colorGroup: "VEHICLE",
        name: "leg",
        id: "16",
      },
    ],
  },
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
    // InputDatePicker,
    // SelectOptionsMultiple,
  },

  setup() {
    const globalStore = useGlobalStore();
    const tabPanel = ref("event-management");
    const allEvents = ref([]);

    const fetchAllEvents = async () => {
      allEvents.value = await globalStore.FETCH_EVENTS();
      // allEvents.value = rows;
      console.log(" allEvents.value", allEvents.value);
    };

    const handleTabSelected = (tabSelected) => {
      tabPanel.value = tabSelected;
    };

    const clearFilters = () => {
      useGlobalStore().dateToFilter = null;
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
      clearFilters,
    };
  },
});
</script>
