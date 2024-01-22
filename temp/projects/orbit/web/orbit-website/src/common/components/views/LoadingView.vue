<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    data() {
        return {};
    },

})
</script>
<template>
    <div className="w-full h-full flex">
        <div class="m-auto">
            <div>
                <h1 class="animate-pulse text-3xl pt-[50%]">Loading...</h1>
            </div>
            <div class='flex space-x-2 justify-center items-center bg-white h-screen'>
                <span class='sr-only'>Loading...</span>
                <div class='h-8 w-8 bg-primary rounded-full animate-bounce [animation-delay:-0.3s]'></div>
                <div class='h-8 w-8 bg-primary rounded-full animate-bounce [animation-delay:-0.15s]'></div>
                <div class='h-8 w-8 bg-primary rounded-full animate-bounce'></div>
            </div>
        </div>

    </div>
</template>