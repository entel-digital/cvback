<template>
    <div class="video-container">
      <video 
        ref="videoPlayer" 
        :src="videoUrl" 
        class="video-player"
        @click="togglePlay"
        @error="handleVideoError"
        controls
      ></video>
      <div 
        v-if="!isPlaying" 
        class="play-overlay" 
        @click="togglePlay"
        role="button"
        aria-label="Play video"
      >
        <q-icon name="play_circle_outline" size="64px" color="white" />
      </div>
    </div>
  </template>
  
  <script>
  import { defineComponent, ref, onMounted, onBeforeUnmount } from 'vue';
  
  export default defineComponent({
    name: 'VideoPlayer',
    props: {
      videoUrl: {
        type: String,
        required: true
      }
    },
    setup(props) {
      const videoPlayer = ref(null);
      const isPlaying = ref(false);
  
      const togglePlay = () => {
        if (videoPlayer.value.paused) {
          videoPlayer.value.play().catch(handleVideoError);
        } else {
          videoPlayer.value.pause();
        }
      };
  
      const onPlay = () => {
        isPlaying.value = true;
      };
  
      const onPause = () => {
        isPlaying.value = false;
      };
  
      const handleVideoError = (error) => {
        console.error('Error playing video:', error);
        // Aquí podrías implementar alguna lógica adicional,
        // como mostrar un mensaje de error al usuario
      };
  
      onMounted(() => {
        if (videoPlayer.value) {
          videoPlayer.value.addEventListener('play', onPlay);
          videoPlayer.value.addEventListener('pause', onPause);
        }
      });
  
      onBeforeUnmount(() => {
        if (videoPlayer.value) {
          videoPlayer.value.removeEventListener('play', onPlay);
          videoPlayer.value.removeEventListener('pause', onPause);
        }
      });
  
      return {
        videoPlayer,
        isPlaying,
        togglePlay,
        handleVideoError
      };
    }
  });
  </script>
  
  <style scoped>
  .video-container {
    position: relative;
    width: 100%;
    height: 100%;
  }
  
  .video-player {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
  
  .play-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.3);
    cursor: pointer;
  }
  </style>