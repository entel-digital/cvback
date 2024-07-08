<template>
  <q-layout view="lHh lpR fFf">
    <q-header style="z-index: -1 !important">
      <q-toolbar
        class="bg-info fit row inline no-wrap justify-between items-center q-py-md"
      >
        <div class="fit row inline no-wrap q-gutter-x-sm q-pl-md">
          <q-btn
            flat
            @click="leftDrawerOpen = !leftDrawerOpen"
            round
            dense
            color="dark"
            icon="menu"
            class="lt-md"
          />

          <q-toolbar-title class="fs-21-25 text-dark q-px-md opacity-8">
            {{ labelSelected }}
          </q-toolbar-title>
        </div>

        <q-btn-dropdown
          id="dropdown-user"
          class="text-grey-6 text-bold"
          flat
          pushactiveMenu
          icon="person_outline"
          :ripple="false"
          dropdown-icon="expand_more"
        >
          <q-list separator>
            <q-item class="column">
              <q-item-label class="q-py-sm font-12-3 text-center text-grey-11"
                >Alerta sonora</q-item-label
              >
              <div class="row justify-center minus-mt-10">
                <q-item-label class="q-pt-md font-15-3 text-grey-11 text-bold"
                  >OFF</q-item-label
                >
                <q-toggle v-model="soundAlertActive" size="lg" color="white" />
                <q-item-label class="q-pt-md font-15-3 text-grey-11 text-bold"
                  >ON</q-item-label
                >
              </div>
            </q-item>
            <q-item>
              <q-item-section>
                <q-btn
                  flat
                  no-caps
                  dense
                  @click="signOut"
                  class="text-grey-3 text-bold font-15-3"
                  >Cerrar Sesión
                </q-btn>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      :mini="!leftDrawerOpen || miniState"
      @click.capture="toggleLeftDrawer"
      :width="200"
      :breakpoint="500"
      bordered
      class="bg-dark"
      style="z-index: 0 !important"
    >
      <!-- drawer content -->
      <div v-if="miniState" class="flex flex-center" style="height: 68px">
        <q-btn round>
          <img
            src="~assets/Imagotipo_vision.png"
            class="logo-header-mini"
            alt="logo vision"
          />
        </q-btn>
      </div>
      <div v-else class="flex flex-start q-pl-sm q-py-md">
        <q-btn push>
          <img
            src="~assets/logo_vision.png"
            class="logo-header"
            alt="logo vision"
          />
        </q-btn>
      </div>
      <q-list padding class="text-white q-gutter-y-md">
        <q-item
          v-for="item in menuList"
          :key="item.value"
          clickable
          :v-ripple="false"
          :active="activeMenu === item.value"
          :to="{ name: item.value }"
          @click="activeMenu = item.value"
          :disable="item.disable"
          active-class="menu-class-active"
          class="q-mx-sm border-radius-15"
        >
          <q-item-section avatar>
            <q-icon :name="item.icon" />
          </q-item-section>

          <q-item-section>{{ item.label }}</q-item-section>
        </q-item>
      </q-list>

      <!--
          in this case, we use a button (can be anything)
          so that user can switch back
          to mini-mode
        -->
      <div class="q-mini-drawer-hide absolute" style="top: 15px; right: -17px">
        <q-btn
          dense
          round
          unelevated
          color="accent"
          icon="chevron_left"
          @click="miniState = true"
        />
      </div>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref, computed } from "vue";

const menuList = [
  {
    value: "events",
    label: "Eventos",
    icon: "error",
    disable: false,
  },
  {
    value: "cameras",
    label: "Cámaras",
    icon: "videocam",
    disable: true,
  },
  // {
  //   value: "users",
  //   label: "Usuarios",
  //   icon: "group",
  //   disable: true,
  // },
  // {
  //   value: "settings",
  //   label: "Configuración",
  //   icon: "settings",
  //   disable: false,
  // },
];
export default defineComponent({
  name: "MainLayout",

  setup() {
    const leftDrawerOpen = ref(false);
    const miniState = ref(false);
    const activeMenu = ref("events");

    const labelsHeader = {
      events: "Gestión de eventos",
      cameras: "Gestión de cámaras",
      users: "Usuarios",
      settings: "Configuración del sistema",
    };

    const labelSelected = computed(() => labelsHeader[activeMenu.value]);

    return {
      menuList,
      leftDrawerOpen,
      miniState,
      activeMenu,
      labelSelected,

      toggleLeftDrawer(e) {
        if (miniState.value) {
          miniState.value = false;
          e.stopPropagation();
        }
      },
    };
  },
});
</script>
<style lang="scss" scoped>
div.q-item.icon-container {
  padding: 0px;
  background-color: #374274dd;
}
.q-drawer-container:not(.q-drawer--mini-animate) .q-drawer--mini .q-item {
  justify-content: center;
}
.minus-mt-10 {
  margin: -10px;
}
.logo-header {
  width: 6rem;
}
.logo-header-mini {
  width: 1.5rem;
}
aside.q-drawer--left.q-drawer--bordered {
  border-right: 0 !important;
}
aside.q-drawer--mini {
  width: 56px;
}
.menu-class-active {
  color: $accent;
  background: #ffffff1a;
  border-radius: 15px;
}
.border-radius-15 {
  border-radius: 15px;
}
</style>
