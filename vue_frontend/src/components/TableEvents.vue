<template>
  <div>
    <div class="fit row no-wrap justify-between items-start content-start q-py-md">
      <div class="gt-sm fit col-12">
        <q-table
          class="fit my-sticky-dynamic fs-15-18"
          flat
          bordered
          :rows="rows"
          :columns="columns"
          row-key="id"
          :loading="loading"
          v-model:pagination="pagination"
          v-model:expanded="expanded"
          hide-pagination
        >
          <template v-slot:body="props">
            <q-tr
              :props="props"
              :class="colorRowSelected(props.row)"
              @click="getRowSelected(props.row)"
            >
              <q-td key="name" :props="props">
                <span class="barlow-semibold fs-15-18">
                  {{ props.row.eventType.name }}
                </span>
              </q-td>
              <q-td key="date" :props="props">
                <span class="barlow-semibold fs-15-18">
                  {{ formatDateEvent(props.row.addedDate).date }}
                </span>

                <span class="fs-15-18"> | {{ formatDateEvent(props.row.addedDate).time }}</span>
              </q-td>
              <q-td key="name" :props="props" class="text-center">
                <span class="barlow-semibold fs-15-18">
                  {{ props.row.eventLabel.name }}
                </span>
              </q-td>
              <q-td class="text-rigth">
                <q-btn
                  size="sm"
                  color="accent"
                  round
                  dense
                  :icon="props.expand ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                />
              </q-td>
            </q-tr>
            <q-tr v-show="props.expand" :props="props">
              <q-td colspan="100%" class="no-padding">
                <div class="fit row justify-between q-py-sm" style="min-height: 400px">
                  <div class="col-4 text-left q-pa-md q-gutter-md">
                    <q-list class="fit">
                      <q-item>
                        <q-item-section>
                          <q-item-label
                            >Confiabilidad:
                            <span class="barlow-bold">
                              {{ toPercentage(props.row.confidence) }}%
                            </span>
                          </q-item-label>
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section>
                          <q-item-label
                            >Fecha creado:
                            <span class="barlow-bold">
                              {{ formatDateEvent(props.row.addedDate).date }}%
                            </span>
                          </q-item-label>
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section>
                          <q-item-label
                            >Fecha informado:
                            <span class="barlow-bold">
                              {{ formatDateEvent(props.row.informateDate).date }}%
                            </span>
                          </q-item-label>
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section>
                          <q-item-label
                            >Patente:
                            <span class="barlow-bold">
                              {{ toPercentage(props.row.confidence) }}%
                            </span>
                          </q-item-label>
                        </q-item-section>
                      </q-item>
                      <q-item v-for="label in props.row.labelsDetected" :key="label.id">
                        <q-item-section avatar>
                          <q-icon color="positive" name="check_circle" />
                        </q-item-section>

                        <q-item-section>{{ label.name }}</q-item-section>
                      </q-item>
                      <q-item v-for="label in props.row.labelsMissing" :key="label.id">
                        <q-item-section avatar>
                          <q-icon color="negative" name="cancel" />
                        </q-item-section>

                        <q-item-section>{{ label.name }}</q-item-section>
                      </q-item>
                    </q-list>
                  </div>
                  <div class="col-8">
                    <CarouselImages :frames="props.row.frames" />
                  </div>
                </div>
              </q-td>
            </q-tr>
          </template>
        </q-table>
        <div class="row justify-center q-mt-md">
          <q-pagination v-model="pagination.page" color="grey-8" :max="pagesNumber" size="sm" />
        </div>
      </div>
    </div>

    <div class="lt-md">
      <q-list bordered separator class="rounded-borders">
        <q-expansion-item group="events" bordered v-for="row in rows" :key="row.id">
          <template v-slot:header>
            <q-item-section class="column">
              <q-item-label class="barlow-bold text-dark fs-21-25 q-py-sm">
                {{ row.eventType.name }}
              </q-item-label>

              <q-item-label class="fs-14-19 text-grey-3">
                <span class="barlow-semibold fs-15-18">
                  {{ formatDateEvent(row.addedDate).date }}
                </span>

                <span class="fs-15-18"> | {{ formatDateEvent(row.addedDate).time }}</span>
              </q-item-label>
              <q-item-label class="barlow-bold text-dark fs-21-25 q-py-sm">
                {{ row.eventLabel.name }}
              </q-item-label>
            </q-item-section>
          </template>

          <!-- <q-card>
            <q-card-section>
              <q-item-label class="text-grey-3 fs-14-19 q-py-sm"
                >Confiabilidad:
                <span class="barlow-bold fs-15-18"> {{ toPercentage(row.confidence) }}% </span>
              </q-item-label>

            </q-card-section>
            <q-card-section>
              <CarouselImages :frames="row.frames" />
            </q-card-section>
          </q-card> -->
        </q-expansion-item>

        <q-separator />
      </q-list>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, computed, nextTick } from 'vue'
import { types } from '@/utils/colors'
import { Loading } from 'quasar'

import CarouselImages from '@/components/CarouselImages.vue'

export default defineComponent({
  name: 'TableEvents',

  props: ['rows', 'columns', 'loading'],
  components: {
    CarouselImages
  },
  setup(props) {
    // const nextPage = ref(2)
    const rowSelected = ref(null)
    const slide = ref(1)
    const fullscreen = ref(false)
    const expanded = ref([])

    const pagination = ref({
      sortBy: 'desc',
      descending: false,
      page: 1,
      rowsPerPage: 50
      // rowsNumber: xx if getting data from a server
    })

    const pagesNumber = computed(() => Math.ceil(props.rows.length / pagination.value.rowsPerPage))

    const getRowSelected = (row, column, event) => {
      if (rowSelected.value?.id === row.id) {
        rowSelected.value = null
        expanded.value = []
      } else {
        rowSelected.value = row
        expanded.value = [row.id]
      }
    }

    const formatDateEvent = (date) => {
      const dateObj = new Date(date)
      const month =
        dateObj.getMonth() + 1 < 10 ? `0${dateObj.getMonth() + 1}` : dateObj.getMonth() + 1
      const day = dateObj.getDate() < 10 ? `0${dateObj.getDate()}` : dateObj.getDate()
      const year = dateObj.getFullYear()
      const hour =
        dateObj.getHours() + 1 < 10 ? `0${dateObj.getHours() + 1}` : dateObj.getHours() + 1
      const minutes = dateObj.getMinutes()
      const newDate = {
        date: `${day}/${month}/${year}`,
        time: `${hour}:${minutes}`
      }
      return newDate
    }

    const colorRowSelected = (row) => {
      if (rowSelected.value?.id === row.id) {
        return 'bg-blue-3'
      }
    }
    const toggleExpand = (row, event) => {
      event.stopPropagation()
      this.getRowSelected(row, event)
    }

    const toPercentage = (value) => {
      // if ((value * 100).lenght > 4) {
      //   return Math.round(value * 100)
      // }
      return value * 100
    }

    const findColor = (value) => {
      const color = types[value.colorGroup.toLowerCase()]

      if (color == '#000000') {
        return `background-color: ${color}; boder: 2px solid ${color}; color: white`
      } else {
        return `background-color: ${color}; boder: 2px solid ${color}; `
      }
    }


    return {
      rowSelected,
      pagination,
      pagesNumber,
      getRowSelected,
      formatDateEvent,
      colorRowSelected,
      slide,
      fullscreen,
      expanded,
      toggleExpand,
      toPercentage,
      findColor
    }
  }
})
</script>

<style lang="sass">
.my-sticky-dynamic
  /* height or max-height is important */
  height: 60vh


  .q-table__top,
  .q-table__bottom,
  thead tr:first-child th /* bg color is important for th; just specify one */
    background-color: #ffffff

  thead tr th
    position: sticky
    z-index: 2
    color: #4A4A4A
  /* this will be the loading indicator */
  thead tr:last-child th
    /* height of all previous header rows */
    top: 48px
    font-size: 16px
    line-height: 19px
    font-weight: 600
    color: #4A4A4A

  thead tr:first-child th
    top: 0
    padding-left: 50px
  /* prevent scrolling behind sticky top row on focus */
  tbody
    /* height of all previous header rows */
    scroll-margin-top: 48px
    color: #828282

.q-table--horizontal-separator tbody tr > td
    padding-left: 50px

tbody tr:nth-child(odd) // Add this selector
  background-color: #FAFAFA // Add your desired color here
</style>
