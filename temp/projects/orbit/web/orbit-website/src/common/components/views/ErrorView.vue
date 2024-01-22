<script lang="ts">
import { defineComponent } from "vue";
import Cactus from '@/assets/core/images/Cactus.jpg'

export default defineComponent({
	props: {
		error: {
			type: Error,
			required: true
		}
	},

	data() {
		return {
			Cactus
		}
	},
	computed: {
	}
});
</script>

<template>
	<div class="w-full h-screen flex h-full bg-cover bg-center" :style="{ backgroundImage: `url('${Cactus}')` }">
		<div class="h-full w-full flex bg-dark bg-opacity-50">
			<div class="m-auto text-center">
				<h1 class="mt-5 text-7xl font-medium text-white text-center ">Hmmm...</h1>
				<h2 class="mt-5 text-4xl font-medium text-white text-center ">There was supposed to be a Teff farm here...
				</h2>
				<h6 class="mt-5 text-xl text-center text-white pb-[2%]">{{ error ? error.message : '' }}</h6>
				<button class="border py-2 px-5 text-sm rounded-full rounded-tr-none bg-primary text-white">
					<router-link to="/">Go to Home</router-link>
				</button>
			</div>
		</div>
	</div>
</template>

<style scoped>
/* Add your component-specific styles here */
</style>

