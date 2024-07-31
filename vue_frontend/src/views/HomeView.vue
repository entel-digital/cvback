<template>
  <div>
    <Toolbar />

    <div class="q-py-lg q-pr-lg q-pl-sm">
      <FilterEvents @filterData="filterData" />
    </div>

    <div
      class="fit row wrap justify-between items-center q-py-lg q-pl-lg q-pr-md"
      style="max-height: 50vh"
    >
      <!-- <CardInfo :numberToShow="'50'" :titleToShow="'Total eventos'"/> -->
      <!-- <CardInfo :numberToShow="eventStore.summaryEvents.totalEvents" :titleToShow="'Total eventos'"/> -->
      <!-- <CardInfo :numberToShow="'50'" :titleToShow="'total eventos'"/> -->
      <!-- <CardInfo :numberToShow="'50'" :titleToShow="'total eventos'"/> -->
    </div>

    <div class="q-py-md">
      <TableEvents :rows="eventStore.allEvents" :columns="columns" :loading="eventStore.loadingEvents" />
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
        sort: (a, b) => parseInt(a, 10) - parseInt(b, 10)
      },
      {
        name: 'labelType',
        label: 'Label',
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
    ];

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
      // intervalId.value = setInterval(fetchAllEvents, 30000);
    })

    // onUnmounted(() => {
    //   if (intervalId.value) {
    //     clearInterval(intervalId);
    //   }
    // });

    const filterData = async (data) => {
      eventStore.loadingEvents = true
      eventStore.dateSelected = data.dateToFilter
      eventStore.labelsTypeSelected = data.labelTypeToFilter

      switch (true) {
        case data.dateToFilter !== null && data.labelTypeToFilter !== null:
          eventStore.funtionToUse = 'bydateandlabel'
          await eventStore.FETCH_EVENTS_BY_DATE_BY_LABEL()
          eventStore.loadingEvents = false

          break
        case data.dateToFilter !== null && !data.labelTypeToFilter:
          eventStore.funtionToUse = 'bydate'

          await eventStore.FETCH_EVENTS_BY_DATE()
          eventStore.loadingEvents = false

          break
        case !data.dateToFilter && data.labelTypeToFilter !== null:
          eventStore.funtionToUse = 'bylabel'
          await eventStore.FETCH_EVENTS_BY_LABEL()
          eventStore.loadingEvents = false

          break
        default:
          eventStore.funtionToUse = 'allevents'

          await fetchAllEvents()
          eventStore.loadingEvents = false

          break
      }
    }

    watch(
      () => eventStore.pagination.page,
      async (newValue) => {
        console.log("newValue", newValue)
        if (newValue) {
          switch (true) {
            case eventStore.dateSelected && eventStore.labelsTypeSelected:
              eventStore.funtionToUse = 'bydateandlabel'
              await eventStore.FETCH_EVENTS_BY_DATE_BY_LABEL()
              break
            case eventStore.dateSelected && !eventStore.labelsTypeSelected:
              eventStore.funtionToUse = 'bydate'

              await eventStore.FETCH_EVENTS_BY_DATE()
              break
            case !eventStore.dateSelected && eventStore.labelsTypeSelected:
              eventStore.funtionToUse = 'bylabel'
              ;
              await eventStore.FETCH_EVENTS_BY_LABEL()
              break
            default:
              eventStore.funtionToUse = 'allevents'
            console.log("entro al switch del eventsotre");
              await fetchAllEvents()
              break
          }
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
