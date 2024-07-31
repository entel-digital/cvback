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
      :style="{ height: carouselHeight }"
    >
      <q-carousel-slide
        v-for="(frame, index) in newFrames"
        :key="frame.id"
        :name="index + 1"
        class="q-pa-none"
      >
        <ImageWithBoundingBoxes
          :imageUrl="frame.imageUrl"
          :boundingBoxes="frame.boundingBoxes"
          :hideBbox="hideBbox"
        />
      </q-carousel-slide>

      <template v-slot:control>
        <q-carousel-control
          position="bottom"
          :offset="[0, 0]"
          class="text-white carousel-control row justify-between items-center"
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
              {{ slide }}/{{ newFrames.length }}
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
              :label="hideBbox ? 'Mostrar Bbox' : 'Ocultar Bbox'"
              :icon="hideBbox ? 'visibility' : 'visibility_off'"
              @click="toggleBbox"
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
          <ImageWithBoundingBoxes
            :imageUrl="frame.imageUrl"
            :boundingBoxes="frame.boundingBoxes"
            :hideBbox="hideBbox"
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
                {{ slide }}/{{ newFrames.length }}
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
                :label="hideBbox ? 'Mostrar Bbox' : 'Ocultar Bbox'"
                :icon="hideBbox ? 'visibility' : 'visibility_off'"
                @click="toggleBbox"
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
import { defineComponent, ref, computed } from "vue";
import ImageWithBoundingBoxes from './ImageWithBoundingBoxes.vue';

export default defineComponent({
  name: "CarouselImages",
  components: {
    ImageWithBoundingBoxes
  },

  props: {
    frames: {
      type: Array,
      default: () => []
    },
    inferenceDetectionClassification: {
      type: Array,
      default: () => []
    }
  },

  setup(props) {
    const slide = ref(1);
    const fullscreen = ref(false);
    const hideBbox = ref(true);
    const carouselHeight = ref('500px');

    const newFrames = computed(() => {
      if (!props.frames || !props.inferenceDetectionClassification) {
        return [];
      }
      
      return props.frames.map(frame => {
        const frameInferences = props.inferenceDetectionClassification.filter(
          inference => inference.frame.id === frame.id
        );

        const boundingBoxes = frameInferences.flatMap(inference => 
          inference.boundingBoxes.map(box => ({
            ...box,
            label: inference.labels[0]?.name || '',
            confidence: inference.confidence

          }))
        );

        return {
          ...frame,
          boundingBoxes
        };
      });
    });

    const toggleBbox = () => {
      hideBbox.value = !hideBbox.value;
    };

    return {
      slide,
      fullscreen,
      newFrames,
      hideBbox,
      carouselHeight,
      toggleBbox
    };
  },
});
</script>

<style lang="scss" scoped>
.carousel-control {
  z-index: 1000;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0,0,0,0.5);
  padding: 10px;
}

.carousel_slides {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 400px;
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

