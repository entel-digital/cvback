<template>
  <div>
    <Toolbar :homeView="false"/>

    <div class="q-py-sm q-pt-md">
      <TableEvents
        :rows="eventStore.eventById"
        :columns="columns"
        :loading="eventStore.loadingEvents"
        :homeView="false"
        @sortAsc="sortTable"
      />
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useEventsStore } from '@/stores/events.js'

import { useRouter } from 'vue-router'

import Toolbar from '@/components/Toolbar.vue'
import TableEvents from '@/components/TableEvents.vue'

export default defineComponent({
  name: 'EventView',
  components: {
    Toolbar,
    TableEvents
  },
  setup() {
    const routes = useRouter();
    const columns = [
      {
        name: 'name',
        required: true,
        label: 'Evento',
        align: 'left',
        field: (row) => row.id,
        format: (val) => `${val}`
      },
      {
        name: 'date',
        label: 'Fecha agregado',
        field: 'addedDate',
        align: 'center',
      },
      {
        name: 'labelType',
        label: 'Etiqueta',
        field: 'labelType',
        align: 'center',
      },
      {
        name: 'action',
        label: '',
        field: '',
        align: 'rigth'
      }
    ]
    
    const eventId = routes.currentRoute.value.params.eventid

    const sortTable = (sort) => {
      eventStore.sortAsc = sort      
      updateData(eventStore.dateSelected, eventStore.labelsSelected)
    }

    const userStore = useUserStore()
    const eventStore = useEventsStore()
    const router = useRouter()

    const signOut = async () => {
      await userStore.SIGN_OUT()
      router.push({ name: 'login' })
    }

    const fetchEventByID = async () => {
      await eventStore.FETCH_EVENTS_BY_ID( routes.currentRoute.value.params.token, eventId)
    }

    onMounted(async () => {
      fetchEventByID()
    })


    watch(
      () => router.currentRoute.value.query,
      (newQuery) => {
        // applyFilters(newQuery);
      },
      { immediate: true }
    )

    return {
      columns,
      signOut,
      eventStore,
      sortTable,
      eventId
    }
  }
})
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
