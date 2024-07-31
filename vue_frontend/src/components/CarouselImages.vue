<template>
  <div class="container_carousel">
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
        class="q-px-md"
      >
        <q-img
          :key="frame.id"
          :src="getFullImageUrl(frame)"
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
          style="height: 55px;"
        >
          <div class="fit row q-pl-md" style="max-width:200px ;">
            <q-btn
              push
              dense
              size="md"
              text-color="white"
              icon="arrow_left"
              @click="$refs.carousel.previous()"
            />
            <div class="q-px-sm q-pt-xs font-18-22 text-bold" style="max-width: 40px; margin-top: 12px">
              {{ slide }}/{{ frames.length || 0 }}
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

          <div class="fit row q-px-lg" style="max-width: fit-content;">
            <q-btn
              dense
              text-color="white"
              no-caps
              :label="hideBbox ? 'Ocultar Bbox' : 'Mostrar Bbox'"
              :icon="hideBbox ? 'visibility_off' : 'visibility'"
              @click="hideBbox = !hideBbox"
            />

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

    <q-dialog v-model="fullscreen">
      <q-carousel
        class="carousel_slides"
        swipeable
        animated
        v-model="slide"
        ref="carousel"
        infinite
        height="100%"
        style="width: 100%; max-width: 80vw; object-fit: contain"
      >
        <q-carousel-slide
          v-for="(frame, index) in newFrames"
          :key="frame.id"
          :name="index + 1"
          id="dialog_carousel-frames"
        >
          <q-img
            :key="frame.id"
            :src="getFullImageUrl(frame)"
            contain
            loading="lazy"
            spinner-color="primary"
            style="object-fit: contain"
            :ratio="16 / 9"
            class="q-mb-xl"
            @load="initializeCanvas"
          />
        </q-carousel-slide>

        <template v-slot:control>
          <q-carousel-control
            position="bottom-left"
            :offset="[0, 0]"
            class="text-white rounded-borders carousel-control row justify-between items-center"
          >
          <div class="fit row q-pl-md" style="max-width:200px ;">
            <q-btn
                push
                dense
                size="md"
                text-color="white"
                icon="arrow_left"
                @click="$refs.carousel.previous()"
              />
              <div class="q-px-sm q-pt-xs font-18-22 text-bold" style="max-width: 40px; margin-top: 12px">
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

            <div class="fit row q-px-lg" style="max-width: fit-content;">
              <q-btn
              dense
              text-color="white"
              no-caps
              :label="hideBbox ? 'Ocultar Bbox' : 'Mostrar Bbox'"
              :icon="hideBbox ? 'visibility_off' : 'visibility'"
              @click="hideBbox = !hideBbox"
            />
              <q-btn
                push
                round
                dense
                text-color="white"
                :icon="fullscreen ? 'fullscreen_exit' : 'fullscreen'"
                @click="fullscreen = false"
              />
            </div>
          </q-carousel-control>
        </template>
      </q-carousel>
    </q-dialog>
  </div>
</template>

<script>
import { defineComponent, ref, watch } from "vue";

export default defineComponent({
  name: "CarouselImages",

  props: ["frames"],

  setup(props) {
    const slide = ref(1);
    const fullscreen = ref(false);
    const newFrames = ref(props.frames);
    const hideBbox = ref(true);

    const getFullImageUrl = (path) => {
     return  hideBbox.value ? path.imageUrl : path.imageWithBoundingboxesUrl;
    };

    return {
      slide,
      fullscreen,
      newFrames,
      getFullImageUrl,
      hideBbox,
    };
  },
});
</script>

<style lang="scss" scoped>
.carousel-control {
  background: #000000b3;
  width: 100%;
}
.q-img.q-img--menu {
  margin-bottom: 20px;
}

#dialog_carousel-frames {
  padding: 0em 7em 0em 7em;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.q-carousel {
  background-color: #363636 !important;
}
</style>
