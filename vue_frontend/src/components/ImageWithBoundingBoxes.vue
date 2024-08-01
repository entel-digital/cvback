<template>
  <div class="image-container">
    <img :src="imageUrl" ref="img" @load="onImageLoad" style="display: none;">
    <canvas ref="canvas" @mousemove="onMouseMove" @mouseout="onMouseOut" @click="onClick"></canvas>
  </div>
</template>

<script>
import { nextTick } from 'vue'

export default {
  props: ['imageUrl', 'boundingBoxes', 'hideBbox'],
  data() {
    return {
      labelCategories: {
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
      },
      categoryColors: {
        'person': [0, 255, 224],
        'animal': [255, 127, 0],
        'vehicle': [44, 255, 0],
        'id': [211, 145, 249],
        'epp': [255, 255, 0],
        'other': [0, 0, 0]
      },
      hoveredBox: null,
      selectedBox: null,
      labelCoords: [],
      canvasReady: false,
      scale: 1
    }
  },
  watch: {
    hideBbox() {
      this.drawImage();
    },
    boundingBoxes: {
      handler() {
        this.initLabelCoords();
        this.$nextTick(() => {
          if (this.canvasReady) {
            this.drawImage();
          }
        });
      },
      immediate: true
    }
  },
  methods: {
    initLabelCoords() {
      this.labelCoords = this.boundingBoxes.map(() => ({ x: 0, y: 0, width: 0, height: 0 }));
    },
    onImageLoad() {
      this.canvasReady = true;
      this.$nextTick(() => {
        this.drawImage();
      });
    },
    drawImage() {
      const canvas = this.$refs.canvas;
      const img = this.$refs.img;
      if (!canvas || !img) return;

      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      this.scale = canvas.offsetWidth / img.naturalWidth;

      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

      if (!this.hideBbox) {
        this.drawBoundingBoxes(ctx);
      }
    },
    drawBoundingBoxes(ctx) {
      if (!this.boundingBoxes || !ctx) return;

      this.boundingBoxes.forEach((box, index) => {
        const x1 = box.topLeft[0] * ctx.canvas.width;
        const y1 = box.topLeft[1] * ctx.canvas.height;
        const x2 = box.bottomRight[0] * ctx.canvas.width;
        const y2 = box.bottomRight[1] * ctx.canvas.height;

        const label = box.label.toLowerCase();
        const category = this.labelCategories[label] || 'other';
        const color = this.categoryColors[category] || this.categoryColors['other'];

        // Dibujar el bounding box
        ctx.strokeStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
        ctx.lineWidth = this.hoveredBox === index ? 4 : 2; // Línea más gruesa al hacer hover
        ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

        // Resaltar el bounding box al hacer hover
        if (this.hoveredBox === index) {
          ctx.fillStyle = `rgba(${color[0]}, ${color[1]}, ${color[2]}, 0.2)`;
          ctx.fillRect(x1, y1, x2 - x1, y2 - y1);
        }

        let labelText = box.label;
        if (typeof box.confidence === 'number' && !isNaN(box.confidence)) {
          labelText += ` ${(box.confidence * 100).toFixed(2)}%`;
        }

        const isHovered = this.hoveredBox === index;
        const fontSize = isHovered ? 34 : 30; // Aumentar el tamaño de la fuente al hacer hover
        ctx.font = `${fontSize}px 'Roboto', sans-serif`;
        
        const textWidth = ctx.measureText(labelText).width;
        const textHeight = isHovered ? 38 : 34; // Aumentar la altura del fondo al hacer hover

        let labelX, labelY;
        if (label === 'pértiga') {
          labelX = x1 - textWidth - 8 - (isHovered ? 4 : 0);
          labelY = y1 - textHeight - (isHovered ? 4 : 0);
        } else if (label === 'chapulín') {
          labelX = x2 + (isHovered ? 4 : 0);
          labelY = y1 - textHeight - (isHovered ? 4 : 0);
        } else if (label === 'banderín') {
          labelX = x2 + (isHovered ? 4 : 0);
          labelY = y2 + (isHovered ? 4 : 0);
        } else {
          labelX = x1;
          labelY = y1 - textHeight - (isHovered ? 4 : 0);
        }

        // Dibujar el fondo de la etiqueta
        ctx.fillStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
        ctx.fillRect(labelX, labelY, textWidth + 8, textHeight);

        // Dibujar el texto de la etiqueta
        ctx.fillStyle = 'black';
        ctx.fillText(labelText, labelX + 4, labelY + textHeight - 6);

        this.labelCoords[index] = {x: labelX, y: labelY, width: textWidth + 8, height: textHeight};
      });
    },
    onMouseMove(event) {
      if (!this.labelCoords.length) return;

      const rect = this.$refs.canvas.getBoundingClientRect();
      const x = (event.clientX - rect.left) / this.scale;
      const y = (event.clientY - rect.top) / this.scale;

      const hoveredIndex = this.labelCoords.findIndex(coords => {
        return coords && x >= coords.x && x <= coords.x + coords.width &&
               y >= coords.y && y <= coords.y + coords.height;
      });

      if (hoveredIndex !== this.hoveredBox) {
        this.hoveredBox = hoveredIndex;
        this.drawImage();
      }
    },
    onMouseOut() {
      this.hoveredBox = null;
      this.drawImage();
    },
    onClick(event) {
      if (!this.labelCoords.length) return;

      const rect = this.$refs.canvas.getBoundingClientRect();
      const x = (event.clientX - rect.left) / this.scale;
      const y = (event.clientY - rect.top) / this.scale;

      const clickedIndex = this.labelCoords.findIndex(coords => {
        return coords && x >= coords.x && x <= coords.x + coords.width &&
               y >= coords.y && y <= coords.y + coords.height;
      });

      if (clickedIndex !== -1) {
        this.selectedBox = this.selectedBox === clickedIndex ? null : clickedIndex;
        this.drawImage();
        console.log('Clicked on label:', this.boundingBoxes[clickedIndex].label);
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

.image-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

canvas {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
</style>