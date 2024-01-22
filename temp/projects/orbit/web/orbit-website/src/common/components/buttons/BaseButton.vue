<script lang="ts">
import { defineComponent } from 'vue';


export default defineComponent({
	props: {
		bg: {
			type: String,
			default: "primary"
		},
		outlineColor: {
			type: String,
			default: "primary"
		},
		textColor:{
			type: String,
			default: "light"
		}
	},
	computed: {
	},
	components: {
	}
});

</script>
<template>

	<button :class="`bg-${bg} text-${textColor} border-${outlineColor}`" class="border py-2 px-5 text-sm rounded-full rounded-tr-none">
		<slot></slot>
	</button>

</template>