<template>
  <div class="image-container">
    <img :src="imageUrl" ref="img" @load="onImageLoad" style="display: none;">
    <canvas ref="canvas" @mousemove="onMouseMove" @mouseout="onMouseOut" @click="onClick"></canvas>
  </div>
</template>

<script>
import { defineComponent, ref, computed, watch } from 'vue'

export default defineComponent({
  name: 'ImageWithBoundingBoxes',
  props: ['imageUrl', 'boundingBoxes', 'hideBbox'],
  setup(props) {
    const img = ref(null);
    const canvas = ref(null);
    const hoveredBox = ref(null);
    const selectedBox = ref(null);
    const labelCoords = ref([]);
    const canvasReady = ref(false);
    const scale = ref(1);

    const labelCategories = computed(() => ({
      "buses": "vehicle",
      "baliza": "epp",
      "banderín": "epp",
      "camioneta": "vehicle",
      "camión": "vehicle",
      "placa_patente": "id",
      "vehículos": "vehicle",
      "chapulín": "epp",
      "camiones": "vehicle",
      "pértiga": "epp"
    }));

    const categoryColors = computed(() => ({
      'person': [0, 255, 224],
      'animal': [255, 127, 0],
      'vehicle': [44, 255, 0],
      'id': [211, 145, 249],
      'epp': [255, 255, 0],
      'other': [0, 0, 0]
    }));

    const initLabelCoords = () => {
      labelCoords.value = props.boundingBoxes.map(() => ({ x: 0, y: 0, width: 0, height: 0 }));
    };

    const onImageLoad = () => {
      canvasReady.value = true;
      drawImage();
    };

    const drawImage = () => {
      if (!canvas.value || !img.value) return;

      const ctx = canvas.value.getContext('2d');
      if (!ctx) return;

      canvas.value.width = img.value.naturalWidth;
      canvas.value.height = img.value.naturalHeight;
      scale.value = canvas.value.offsetWidth / img.value.naturalWidth;

      ctx.drawImage(img.value, 0, 0, canvas.value.width, canvas.value.height);

      if (!props.hideBbox) {
        drawBoundingBoxes(ctx);
      }
    };

    const drawBoundingBoxes = (ctx) => {
      if (!props.boundingBoxes || !ctx) return;

      props.boundingBoxes.forEach((box, index) => {
        const x1 = box.topLeft[0] * ctx.canvas.width;
        const y1 = box.topLeft[1] * ctx.canvas.height;
        const x2 = box.bottomRight[0] * ctx.canvas.width;
        const y2 = box.bottomRight[1] * ctx.canvas.height;

        drawBox(ctx, x1, y1, x2, y2, box, index);
        drawLabel(ctx, x1, y1, x2, y2, box, index);
      });
    };

    const drawBox = (ctx, x1, y1, x2, y2, box, index) => {
      const label = box.label.toLowerCase();
      const category = labelCategories.value[label] || 'other';
      const color = categoryColors.value[category] || categoryColors.value['other'];

      ctx.strokeStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
      ctx.lineWidth = hoveredBox.value === index ? 4 : 2;
      ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

      if (hoveredBox.value === index) {
        ctx.fillStyle = `rgba(${color[0]}, ${color[1]}, ${color[2]}, 0.2)`;
        ctx.fillRect(x1, y1, x2 - x1, y2 - y1);
      }
    };

    const drawLabel = (ctx, x1, y1, x2, y2, box, index) => {
      const label = box.label.toLowerCase();
      const category = labelCategories.value[label] || 'other';
      const color = categoryColors.value[category] || categoryColors.value['other'];

      let labelText = box.label;
      if (typeof box.confidence === 'number' && !isNaN(box.confidence)) {
        labelText += ` ${(box.confidence * 100).toFixed(2)}%`;
      }

      const isHovered = hoveredBox.value === index;
      const fontSize = isHovered ? 34 : 30;
      ctx.font = `${fontSize}px 'Roboto', sans-serif`;
      
      const textWidth = ctx.measureText(labelText).width;
      const textHeight = isHovered ? 38 : 34;

      const [labelX, labelY] = getLabelPosition(label, x1, y1, x2, y2, textWidth, textHeight, isHovered);

      ctx.fillStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
      ctx.fillRect(labelX, labelY, textWidth + 8, textHeight);

      ctx.fillStyle = 'black';
      ctx.fillText(labelText, labelX + 4, labelY + textHeight - 6);

      labelCoords.value[index] = {x: labelX, y: labelY, width: textWidth + 8, height: textHeight};
    };

    const getLabelPosition = (label, x1, y1, x2, y2, textWidth, textHeight, isHovered) => {
      const offset = isHovered ? 4 : 0;
      switch(label) {
        case 'pértiga':
          return [x1 - textWidth - 8 - offset, y1 - textHeight - offset];
        case 'chapulín':
          return [x2 + offset, y1 - textHeight - offset];
        case 'banderín':
          return [x2 + offset, y2 + offset];
        default:
          return [x1, y1 - textHeight - offset];
      }
    };

    const onMouseMove = (event) => {
      if (!labelCoords.value.length) return;

      const rect = canvas.value.getBoundingClientRect();
      const x = (event.clientX - rect.left) / scale.value;
      const y = (event.clientY - rect.top) / scale.value;

      const hoveredIndex = labelCoords.value.findIndex(coords => {
        return coords && x >= coords.x && x <= coords.x + coords.width &&
               y >= coords.y && y <= coords.y + coords.height;
      });

      if (hoveredIndex !== hoveredBox.value) {
        hoveredBox.value = hoveredIndex;
        drawImage();
      }
    };

    const onMouseOut = () => {
      hoveredBox.value = null;
      drawImage();
    };

    const onClick = (event) => {
      if (!labelCoords.value.length) return;

      const rect = canvas.value.getBoundingClientRect();
      const x = (event.clientX - rect.left) / scale.value;
      const y = (event.clientY - rect.top) / scale.value;

      const clickedIndex = labelCoords.value.findIndex(coords => {
        return coords && x >= coords.x && x <= coords.x + coords.width &&
               y >= coords.y && y <= coords.y + coords.height;
      });

      if (clickedIndex !== -1) {
        selectedBox.value = selectedBox.value === clickedIndex ? null : clickedIndex;
        drawImage();
        console.log('Clicked on label:', props.boundingBoxes[clickedIndex].label);
      }
    };

    watch(() => props.boundingBoxes, () => {
      initLabelCoords();
      if (canvasReady.value) {
        drawImage();
      }
    }, { immediate: true });

    watch(() => props.hideBbox, drawImage);

    return {
      img,
      canvas,
      onImageLoad,
      onMouseMove,
      onMouseOut,
      onClick
    };
  }
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

.image-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

canvas {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
</style>