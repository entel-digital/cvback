<template>
    <div class="image-container">
      <img :src="imageUrl" ref="img" @load="onImageLoad" style="display: none;">
      <canvas ref="canvas"></canvas>
    </div>
  </template>
  
  <script>
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
        }
      }
    },
    watch: {
      hideBbox() {
        this.drawImage();
      }
    },
    methods: {
      onImageLoad() {
        this.drawImage();
      },
      drawImage() {
        const canvas = this.$refs.canvas;
        const ctx = canvas.getContext('2d');
        const img = this.$refs.img;
  
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
  
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  
        if (!this.hideBbox) {
          this.drawBoundingBoxes(ctx);
        }
      },
      drawBoundingBoxes(ctx) {
      this.boundingBoxes.forEach(box => {
        const x1 = box.topLeft[0] * ctx.canvas.width;
        const y1 = box.topLeft[1] * ctx.canvas.height;
        const x2 = box.bottomRight[0] * ctx.canvas.width;
        const y2 = box.bottomRight[1] * ctx.canvas.height;

        const label = box.label.toLowerCase();
        const category = this.labelCategories[label] || 'other';
        const color = this.categoryColors[category] || this.categoryColors['other'];

        // Dibujar el rectángulo
        ctx.strokeStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
        ctx.lineWidth = 2;
        ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

        // Preparar el texto
        let labelText = box.label;
        if (typeof box.confidence === 'number' && !isNaN(box.confidence)) {
          labelText += ` ${(box.confidence * 100).toFixed(2)}%`;
        }
        
        ctx.font = '24px Arial';
        const textMetrics = ctx.measureText(labelText);
        const textWidth = textMetrics.width;
        const textHeight = 22;

        const padding = 5;
        const rectWidth = textWidth + (padding * 2);
        const rectHeight = textHeight + (padding * 2);

        // Dibujar el fondo del texto
        ctx.fillStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
        ctx.fillRect(x1, y1 - rectHeight, rectWidth, rectHeight);

        // Dibujar el texto
        ctx.fillStyle = 'rgb(0, 0, 0)';
        ctx.fillText(labelText, x1 + padding, y1 - padding);
      });
    }
  }
}
</script>
  
  <style scoped>
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
