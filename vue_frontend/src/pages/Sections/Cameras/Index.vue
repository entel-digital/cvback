<template>
  <q-page>
    <div class="space-page">
      <div class="q-pt-lg">
        <!-- <p class="fs-28-34 text-dark text-bold q-pt-lg q-px-md opacity-8">
          Eventos
        </p> -->
        <!-- <p class="fs-16-19 text-grey-3 text-bold q-px-md">
          Cámaras habilitadas:
        </p> -->
      </div>
      <TabsMenu />
      <div>
        <q-tab-panels v-model="tab">
          <q-tab-panel name="event-management"> </q-tab-panel>
          <q-tab-panel name="event-historic"> </q-tab-panel>
          <q-tab-panel name="event-video"> </q-tab-panel>
          <q-tab-panel name="event-map"> </q-tab-panel>
        </q-tab-panels>
      </div>
      <div></div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted } from "vue";
import { useGlobalStore } from "stores/global-store";

import TabsMenu from "src/components/Tabs.vue";

export default defineComponent({
  name: "CamerasPage",
  components: {
    TabsMenu,
  },

  setup() {
    const globalStore = useGlobalStore();

    return {
      tab: ref("event-management"),
      globalStore,
    };
  },
  // methods: {
  //   async fetchAllEvents() {
  //     console.log("globalstore method", this.globalStore);
  //     await this.globalStore.FETCH_EVENTS();
  //   },
  // },
});
</script>
