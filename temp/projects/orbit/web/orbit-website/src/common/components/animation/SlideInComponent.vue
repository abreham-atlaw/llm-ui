<template>
  <div :class="['slide-in-component', direction]" ref="slideInComponent" :style="{ transitionDuration: duration + 's' }">
    <!-- Use slot to allow content to be added -->
    <slot></slot>
  </div>
</template>

<script lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

export default {
  props: {
    direction: {
      type: String,
      default: 'right',
    },
    duration: {
      type: Number,
      default: 2,
    },
  },
  setup() {
    const slideInComponent = ref(null);
    let observer;

    onMounted(() => {
      observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('slide-in');
          } else {
            entry.target.classList.remove('slide-in');
          }
        },
        {
          threshold: 0.1,
        }
      );

      if (slideInComponent.value) {
        observer.observe(slideInComponent.value);
      }
    });

    onUnmounted(() => {
      if (slideInComponent.value) {
        observer.unobserve(slideInComponent.value);
      }
    });

    return { slideInComponent };
  },
};
</script>

<style scoped>
.slide-in-component {
  transform: translateX(-100%);
}
.slide-in-component.right {
  transform: translateX(-100%);
}

.slide-in-component.right.slide-in {
  transform: translateX(0);
}

.slide-in-component.left {
  transform: translateX(100%);
}

.slide-in-component.left.slide-in {
  transform: translateX(0);
}

.slide-in-component.up {
  transform: translateY(100%);
}

.slide-in-component.up.slide-in {
  transform: translateY(0);
}

.slide-in-component.down {
  transform: translateY(-100%);
}

.slide-in-component.down.slide-in {
  transform: translateY(0);
}
</style>
