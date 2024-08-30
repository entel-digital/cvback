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
    >
      <q-carousel-slide
        v-for="(frame, index) in newFrames"
        :key="frame.id"
        :name="index + 1"
        class="q-pa-none"
      >
        <template v-if="frame.type === 'image'">
          <ImageWithBoundingBoxes
            :imageUrl="frame.imageUrl"
            :boundingBoxes="frame.boundingBoxes"
            :hideBbox="hideBbox"
          />
        </template>
        <template v-else-if="frame.type === 'video'">
          <VideoPlayer :videoUrl="frame.videoUrl" />
        </template>
      </q-carousel-slide>

      <template v-slot:control>
        <q-carousel-control
          position="bottom"
          :offset="[0, 0]"
          class="text-white carousel-control row justify-between items-center"
        >
          <div class="fit row q-pl-md" style="max-width: 200px">
            <q-btn
              push
              dense
              size="md"
              text-color="white"
              icon="arrow_left"
              @click="$refs.carousel.previous()"
            />
            <div
              class="q-px-sm q-pt-xs font-18-22 text-bold"
              style="max-width: 40px; margin-top: 4px"
            >
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
          <div class="fit row q-px-lg q-gutter-x-md" style="max-width: fit-content">
            <q-btn
              dense
              text-color="white"
              no-caps
              :icon="hideBbox ? 'visibility' : 'visibility_off'"
              @click="toggleBbox"
            >
              <q-tooltip>{{ hideBbox ? 'Ocultar BoundingBox' : 'Ver BoundingBox' }}</q-tooltip>
            </q-btn>
            <q-btn
              push
              round
              dense
              text-color="white"
              :icon="'fullscreen'"
              @click="fullscreen = true"
            >
              <q-tooltip>Ver pantalla completa</q-tooltip>
            </q-btn>
          </div>
        </q-carousel-control>
      </template>
    </q-carousel>

    <q-dialog v-model="fullscreen" full-width full-height>
      <q-carousel
        class="carousel_slides fullscreen"
        swipeable
        animated
        v-model="slide"
        ref="carousel"
        infinite
      >
        <q-carousel-slide
          v-for="(frame, index) in newFrames"
          :key="frame.id"
          :name="index + 1"
          id="dialog_carousel-frames"
        >
          <template v-if="frame.type === 'image'">
            <ImageWithBoundingBoxes
              :imageUrl="frame.imageUrl"
              :boundingBoxes="frame.boundingBoxes"
              :hideBbox="hideBbox"
            />
          </template>
          <template v-else-if="frame.type === 'video'">
            <VideoPlayer :videoUrl="frame.videoUrl" />
          </template>
        </q-carousel-slide>
        <template v-slot:control>
          <q-carousel-control
            position="bottom-left"
            :offset="[0, 0]"
            class="text-white rounded-borders carousel-control row justify-between items-center"
          >
            <div class="fit row q-pl-md" style="max-width: 200px">
              <q-btn
                push
                dense
                size="md"
                text-color="white"
                icon="arrow_left"
                @click="$refs.carousel.previous()"
              />
              <div
                class="q-px-sm q-pt-xs font-18-22 text-bold"
                style="max-width: 40px; margin-top: 4px"
              >
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
            <div class="fit row q-px-lg q-gutter-x-md" style="max-width: fit-content">
              <q-btn
                dense
                text-color="white"
                no-caps
                :icon="hideBbox ? 'visibility' : 'visibility_off'"
                :disable="frame.type === 'video'"
                @click="toggleBbox"
              >
                <q-tooltip>{{ hideBbox ? 'Ocultar BoundingBox' : 'Ver BoundingBox' }}</q-tooltip>
              </q-btn>
              <q-btn
                push
                round
                dense
                text-color="white"
                :icon="'fullscreen_exit'"
                @click="fullscreen = false"
              >
                <q-tooltip>Salir Pantalla completa</q-tooltip>
              </q-btn>
            </div>
          </q-carousel-control>
        </template>
      </q-carousel>
    </q-dialog>
  </div>
</template>

<script>
import { defineComponent, ref, computed, watch } from 'vue'
import ImageWithBoundingBoxes from './ImageWithBoundingBoxes.vue'
import VideoPlayer from './VideoPlayer.vue'

export default defineComponent({
  name: 'CarouselImages',
  components: {
    ImageWithBoundingBoxes,
    VideoPlayer
  },

  props: {
    frames: {
      type: Array,
      default: () => []
    },
    inferenceDetectionClassification: {
      type: Array,
      default: () => []
    },
    videos: {
      type: Array,
      default: () => []
    },
    eventSelected: {
      type: Array,
      default: () => []
    }
  },

  setup(props) {
    const slide = ref(1)
    const fullscreen = ref(false)
    const hideBbox = ref(true)

    const newFrames = computed(() => {
      if (!props.frames || !props.inferenceDetectionClassification) {
        return []
      }

      const imageFrames = props.frames.map((frame) => ({
        ...frame,
        type: 'image',
        boundingBoxes: props.inferenceDetectionClassification
          .filter((inference) => inference.frame.id === frame.id)
          .flatMap((inference) =>
            inference.boundingBoxes.map((box) => ({
              ...box,
              label: inference.labels[0]?.name || '',
              confidence: inference.confidence
            }))
          )
      }))

      const videoFrames = props.videos.map((video) => ({
        id: video.id,
        type: 'video',
        videoUrl: video.videoUrl
      }))
      return [...imageFrames, ...videoFrames]
    })

    const toggleBbox = () => {
      hideBbox.value = !hideBbox.value
    };

    watch(
      () => props.eventSelected,
      (newEvent, oldEvent) => {
        if(newEvent[0] !== oldEvent[0]){
          slide.value = 1
          hideBbox.value = true
        }
      },
    )

    return {
      slide,
      fullscreen,
      newFrames,
      hideBbox,
      toggleBbox
    }
  }
})
</script>

<style lang="scss" scoped>
.carousel-control {
  z-index: 1000;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 10px;
}

.carousel_slides {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 400px;

  &.fullscreen {
    width: 100vw;
    height: 100vh;
  }
}

.q-carousel {
  background-color: #363636 !important;
  width: 100%;
}

:deep(.q-carousel__slide) {
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  width: 100%;
  height: 100%;
}

:deep(img),
:deep(video) {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
</style>
