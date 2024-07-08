<template>
  <div
    class="fit row no-wrap justify-between items-start content-start q-py-md gt-sm"
  >
    <div class="col-12">
      <q-table
        class="my-sticky-dynamic fs-15-18"
        flat
        bordered
        :rows="rows"
        :columns="columns"
        :loading="loading"
        row-key="id"
        :pagination="pagination"
        v-model:expanded="expanded"
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

              <span class="fs-15-18">
                | {{ formatDateEvent(props.row.addedDate).time }}</span
              >
            </q-td>
            <q-td key="detected" :props="props">
              <span class="barlow-semibold fs-15-18">
                {{ props.row.labelsDetected.length }}
              </span>

              <span class="barlow fs-15-18">
                {{ checkIfPlural(props.row.labelsDetected.length) }}
              </span>
            </q-td>
            <q-td key="missing" :props="props">
              <span class="barlow-semibold fs-15-18">
                {{ props.row.labelsMissing.length }}
                <!-- {{ checkIfPlural(props.row.labelsMissing.length) }} -->
              </span>
              <span class="barlow fs-15-18">
                {{ checkIfPlural(props.row.labelsMissing.length) }}
              </span>
            </q-td>
            <q-td auto-width>
              <q-toggle
                v-model="props.expand"
                checked-icon="add"
                unchecked-icon="remove"
              />
            </q-td>
          </q-tr>
          <q-tr v-show="props.expand" :props="props">
            <q-td colspan="100%">
              <div class="text-left">
                <q-list>
                  <q-item>
                    <q-item-section>
                      <q-item-label
                        >Confiabilidad:
                        <span class="barlow-bold">
                          {{ Math.round(props.row.confidence * 100) }}%
                        </span>
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label
                        >Detectados:
                        <span>
                          <q-chip
                            v-for="label in props.row.labelsDetected"
                            :key="label.id"
                            color="primary"
                            text-color="white"
                          >
                            {{ label.name }}
                          </q-chip>
                        </span>
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label
                        >No encontrados:
                        <span>
                          <q-chip
                            v-for="label in props.row.labelsMissing"
                            :key="label.id"
                            color="primary"
                            text-color="white"
                          >
                            {{ label.name }}
                          </q-chip>
                        </span>
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
                <!-- This is expand slot for row above: {{ props.row.name }}. -->
              </div>
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
    <!-- <div v-if="rowSelected" :class="rowSelected ? 'col-5' : 'col-12'">
      <div class="flex flex-center">
       <q-carousel animated v-model="slide" infinite>
          <q-carousel-slide name="soft-jazz">
            <q-img src="~assets/img_test.jpeg" />
          </q-carousel-slide>

          <q-carousel-slide name="Rihanna">
            <q-img src="~assets/img_test.jpeg" />
          </q-carousel-slide>

          <q-carousel-slide name="ibiza">
            <q-img src="~assets/img_test.jpeg" />
          </q-carousel-slide>
        </q-carousel>
        <q-carousel
          v-if="!fullscreen"
          id="carousel-frames"
          class="carousel_slides"
          swipeable
          animated
          v-model="slide"
          ref="carousel"
          infinite
          height="100%"
          style="width: 100%; object-fit: contain; border-radius: 5px"
        >
          <q-carousel-slide
            v-for="(frame, index) in newFrames"
            :key="frame.id"
            :name="index + 1"
          >
            <q-img
              :key="frame.id"
              :src="frame.url"
              contain
              :ratio="16 / 9"
              loading="lazy"
              spinner-color="primary"
              style="object-fit: contain"
            />
          </q-carousel-slide>

          <template v-slot:control>
            <q-carousel-control
              position="bottom-left"
              :offset="[0, 0]"
              class="text-white rounded-borders carousel-control row justify-between items-center"
            >
              <div class="row">
                <q-btn
                  push
                  dense
                  size="md"
                  text-color="white"
                  icon="arrow_left"
                  @click="$refs.carousel.previous()"
                />
                <div class="q-px-sm q-pt-xs font-18-22 text-bold">
                  {{ slide }}/{{ frames.length }}
                </div>
                <q-btn
                  push
                  dense
                  size="md"
                  text-color="white"
                  icon="arrow_right"
                  @click="$refs.carousel.next()"
                />
              </div>

              <div class="row q-px-md">
                <q-btn
                  push
                  round
                  dense
                  text-color="white"
                  :icon="fullscreen ? 'fullscreen_exit' : 'fullscreen'"
                  @click="fullscreen = true"
                />
              </div>
            </q-carousel-control>
          </template>
        </q-carousel>
      </div>
    </div> -->
  </div>
  <div class="lt-md">
    <q-list bordered separator class="rounded-borders">
      <q-expansion-item bordered v-for="row in rows" :key="row.id">
        <template v-slot:header>
          <q-item-section class="column">
            <q-item-label class="barlow-bold text-dark fs-16-19">
              {{ row.id }}
            </q-item-label>
            <q-item-label class="fs-14-19 text-grey-3">
              <span class="barlow-semibold fs-15-18">
                {{ formatDateEvent(row.addedDate).date }}
              </span>

              <span class="fs-15-18">
                | {{ formatDateEvent(row.addedDate).time }}</span
              >
            </q-item-label>
          </q-item-section>
        </template>

        <q-card>
          <q-card-section>
            <q-item-label class="text-grey-3 fs-14-19"
              >Confiabilidad:
              <span class="barlow-bold fs-15-18">
                {{ Math.round(row.confidence * 100) }}%
              </span>
            </q-item-label>
            <q-item-label class="text-grey-3 fs-14-19">
              Detectados:
              <q-chip
                v-for="label in row.labelsMissing"
                :key="label.id"
                color="primary"
                text-color="white"
              >
                {{ label.name }}
              </q-chip>
            </q-item-label>
            <q-item-label class="text-grey-3 fs-14-19">
              No encontrados:
              <q-chip
                v-for="label in row.labelsMissing"
                :key="label.id"
                color="primary"
                text-color="white"
              >
                {{ label.name }}
              </q-chip>
            </q-item-label>
          </q-card-section>
          <q-card-section>
            <q-img
              src="https://firebasestorage.googleapis.com/v0/b/eocean-cv-processed-bucket-nonprod/o/268136ca-4ce3-3250-8439-44bb857b6d77%2F2023-07-16%2F376d8cc5-c173-58a5-8b31-591298dbae3e%2F29d34290-bc51-436c-a6ff-76cd548bcf14.png?alt=media&token=c376e83c-a374-465b-9af3-be8e5d1bc564"
            />
          </q-card-section>
        </q-card>
      </q-expansion-item>

      <q-separator />
    </q-list>
  </div>
</template>

<script>
import { ref, computed, nextTick } from "vue";
export default {
  name: "TableEvents",
  props: {
    rows: {
      type: Array,
      default: () => [],
    },
    columns: {
      type: Array,
      default: () => [],
    },
  },
  setup() {
    const nextPage = ref(2);
    const loading = ref(false);
    const rowSelected = ref(null);
    const slide = ref("soft-jazz");
    const fullscreen = ref(false);
    const expanded = ref([]);

    function getRowSelected(row, column, event) {
      if (rowSelected.value?.id === row.id) {
        rowSelected.value = null;
      } else {
        rowSelected.value = row;
      }
    }

    const pagination = computed(() => {
      return {
        rowsPerPage: 10,
      };
    });

    const formatDateEvent = (date) => {
      const dateObj = new Date(date);
      const month =
        dateObj.getMonth() + 1 < 10
          ? `0${dateObj.getMonth() + 1}`
          : dateObj.getMonth() + 1;
      const day =
        dateObj.getDate() < 10 ? `0${dateObj.getDate()}` : dateObj.getDate();
      const year = dateObj.getFullYear();
      const hour = dateObj.getUTCHours();
      const minutes = dateObj.getUTCMinutes();
      const newDate = {
        date: `${day}/${month}/${year}`,
        time: `${hour}:${minutes}`,
      };
      return newDate;
    };

    const colorRowSelected = (row) => {
      if (rowSelected.value?.id === row.id) {
        return "bg-blue-3";
      }
    };

    const checkIfPlural = (row) => {
      console.log("row plural", row);
      return row > 1 ? " labels" : " label";
    };

    return {
      nextPage,
      loading,
      rowSelected,
      pagination,
      getRowSelected,
      formatDateEvent,
      colorRowSelected,
      slide,
      fullscreen,
      expanded,
      checkIfPlural,
    };
  },
};
</script>

<style lang="sass">
.my-sticky-dynamic
  /* height or max-height is important */
  max-height: 410px

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
