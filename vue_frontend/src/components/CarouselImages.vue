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
      >
        <q-img
          :key="frame.id"
          :src="getFullImageUrl(frame.image)"
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
          v-for="(frame, index) in frames.value"
          :key="frame.id"
          :name="index + 1"
          id="dialog_carousel-frames"
        >
          <q-img
            :src="getFullImageUrl(frame.image)"
            contain
            loading="lazy"
            spinner-color="primary"
            style="object-fit: contain"
            :ratio="16 / 9"
            class="q-mb-xl"
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

  props: ["frames", "loading", "event_id", "expanded"],

  setup(props) {
    const slide = ref(1);
    const fullscreen = ref(false);
    const newFrames = ref(props.frames);
        const image1Url = ref('')
    //  const   mode: "fill";
    // carousel: false,
    // modalcenter: "center",
    console.log("expanded", props.expanded);

   const getFullImageUrl = (relativePath) => {
      return `http://localhost:8000/media/${relativePath}`;
    };
    return {
      slide,
      fullscreen,
      newFrames,
      getFullImageUrl
    };
  },
});
</script>

<style lang="scss" scoped>
.carousel-control {
  background: #000000b3;
  width: 100%;
  height: 50px;
}
.custom-pt {
  padding-top: 14px;
}
</style>
