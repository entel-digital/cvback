<template>
  <div>
    <Toolbar />

    <div class="q-py-md q-pr-lg q-pl-sm">
      <FilterEvents @filterData="filterData" />
    </div>

    <div class="fit row wrap justify-center items-center q-py-md q-pl-lg q-pr-md">
      <CardInfo />
    </div>

    <div class="q-py-sm">
      <TableEvents
        :rows="eventStore.allEvents"
        :columns="columns"
        :loading="eventStore.loadingEvents"
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
import CardInfo from '@/components/CardInfo.vue'
import FilterEvents from '@/components/FilterEvents.vue'
import TableEvents from '@/components/TableEvents.vue'

export default defineComponent({
  name: 'HomeView',
  components: {
    Toolbar,
    CardInfo,
    FilterEvents,
    TableEvents
  },
  setup() {
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
        label: 'Fecha',
        field: 'addedDate',
        align: 'center',
        sortable: true,
        sort: (a, b) => new Date(a) - new Date(b)
      },
      {
        name: 'labelType',
        label: 'Etiqueta',
        field: 'labelType',
        align: 'center',
        sortable: true
      },
      {
        name: 'action',
        label: '',
        field: '',
        align: 'center'
      }
    ]

    const userStore = useUserStore()
    const eventStore = useEventsStore()
    const router = useRouter()

    const signOut = async () => {
      await userStore.SIGN_OUT()
      router.push({ name: 'login' })
    }

    const fetchAllEvents = async () => {
      await eventStore.FETCH_EVENTS()
    }
    onMounted(() => {
      fetchAllEvents()
    })

    const filterData = async (data) => {
      eventStore.loadingEvents = true
      eventStore.dateSelected = data.dateToFilter
      eventStore.labelsTypeSelected = data.labelTypeToFilter
      eventStore.pagination.page = 1
      eventStore.pagination.offset = 0
      updateData(data.dateToFilter, data.labelTypeToFilter)
    }

    const updateData = async (date, label) => {
      eventStore.loadingEvents = true
      if (date !== null && label !== null) {
        eventStore.funtionToUse = 'bydateandlabel'
        await eventStore.FETCH_EVENTS_BY_DATE_BY_LABEL()
        eventStore.loadingEvents = false
      } else if (date !== null && !label) {
        eventStore.funtionToUse = 'bydate'
        await eventStore.FETCH_EVENTS_BY_DATE()
        eventStore.loadingEvents = false
      } else if (!date && label !== null) {
        eventStore.funtionToUse = 'bylabel'
        await eventStore.FETCH_EVENTS_BY_LABEL()
        eventStore.loadingEvents = false
      } else if (!date && !label) {
        eventStore.funtionToUse = 'allevents'
        await fetchAllEvents()
      }
    }

    watch(
      () => eventStore.pagination.page,
      async (newValue, oldValue) => {
        if (newValue !== oldValue) {
          updateData(eventStore.dateSelected, eventStore.labelsTypeSelected)
        }
      }
    )

    return {
      columns,
      signOut,
      filterData,
      eventStore
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
