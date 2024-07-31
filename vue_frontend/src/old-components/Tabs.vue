<template>
  <q-tabs
    no-caps
    active-color="secondary"
    align="left"
    content-class="text-grey-2 barlow-bold"
    active-class="barlow-bold"
    v-model="tabSelected"
  >
    <q-tab
      v-for="tab in tabs"
      :key="tab.value"
      :name="tab.value"
      :label="tab.label"
      :disable="tab.disable"
      class="gt-sm"
    ></q-tab>

    <q-btn-dropdown auto-close stretch flat no-caps class="lt-md">
      <template v-slot:label>
        <q-item-label class="fs-18-23 text-dark">
          Vista seleccionada:
          <span class="barlow-bold">
            {{ labelTabSelected }}
          </span></q-item-label
        >
      </template>

      <q-list class="text-dark">
        <q-item
          v-for="tab in tabs"
          :key="tab.value"
          :active="tabSelected === tab.value"
          active-class="menu-class-active barlow-bold"
          :disable="tab.disable"
        >
          <q-item-section @click="updateTabSelected(tab)">{{
            tab.label
          }}</q-item-section>
        </q-item>
      </q-list>
    </q-btn-dropdown>
  </q-tabs>
</template>

<script>
import { ref, watch, getCurrentInstance, computed } from "vue";
export default {
  name: "TabsMenu",
  props: {
    tabs: {
      type: Array,
      default: () => [],
    },
  },
  emits: ["tabSelectedChanged"], // Declarar el evento personalizado aquí

  setup(props) {
    const tabSelected = ref(props.tabs[0].value || null);
    const instance = getCurrentInstance();

    const updateTabSelected = (value) => {
      tabSelected.value = value.value;
      instance.emit("tabSelectedChanged", tabSelected.value.value); // Emitir el objeto completo en lugar del valor
    };

    watch(tabSelected, (newValue) => {
      instance.emit("tabSelectedChanged", newValue);
    });

    const labelTabSelected = computed(() => {
      const tab = props.tabs.find((tab) => tab.value === tabSelected.value);
      return tab ? tab.label : "";
    });

    return {
      tabSelected,
      labelTabSelected,

      updateTabSelected,
    };
  },
};
</script>
<style lang="scss">
.q-tabs .q-tab {
  box-shadow: 0px 2px 4px #00000012;
  border: 1px solid #ebebeb;
  height: 52px;
  min-width: 270px;
}
.q-tab__label {
  font-size: 18px;
  line-height: 22px;
}
.q-tab__indicator {
  height: 4px;
}
.menu-class-active {
  color: $accent;
  background: #ffffff1a;
  border-radius: 15px;
}
</style>
