<template>
  <q-layout view="lHh lpR fFf">
    <q-header>
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
          push
          icon="person_outline"
          dropdown-icon="expand_more"
        >
          <q-list separator>
            <q-item>
              <q-item-section>
                <q-btn
                  flat
                  no-caps
                  dense
                  @click="signOut"
                  class="text-grey-3 barlow-bold font-15-3"
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
    >
      <!-- drawer content -->
      <div v-if="miniState" class="flex flex-center" style="height: 68px">
        <q-btn round flat>
          <img
            src="~assets/imagotipo_vision.png"
            class="logo-header-mini"
            alt="logo vision"
          />
        </q-btn>
      </div>
      <div v-else class="flex flex-start q-pl-sm q-py-md">
        <q-btn flat push>
          <img
            src="~assets/logo_vision_blanco.png"
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
      <div class="q-mini-drawer-hide absolute" style="top: 20px; right: 0px">
        <q-btn
          dense
          unelevated
          square
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
import { useUserStore } from "stores/user-store";
import { useRouter } from "vue-router";

const menuList = [
  {
    value: "events",
    label: "Eventos",
    icon: "error",
    disable: false,
  },
];
export default defineComponent({
  name: "MainLayout",

  setup() {
    const leftDrawerOpen = ref(false);
    const miniState = ref(false);
    const activeMenu = ref("events");
    const userStore = useUserStore();
    const router = useRouter();
    const labelsHeader = {
      events: "Eventos",
      cameras: "Cámaras",
      users: "Usuarios",
      settings: "Configuración del sistema",
    };

    const labelSelected = computed(() => labelsHeader[activeMenu.value]);

    const toggleLeftDrawer = (e) => {
      if (miniState.value) {
        miniState.value = false;
        e.stopPropagation();
      }
    };
    const signOut = async () => {
      await userStore.SIGN_OUT();
      router.push({ name: "login" });
    };



    return {
      menuList,
      leftDrawerOpen,
      miniState,
      activeMenu,
      labelSelected,
      signOut,
      toggleLeftDrawer,
      user,
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
  width: 1.5rem !important;
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
