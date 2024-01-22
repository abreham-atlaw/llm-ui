<script lang="ts">
import { defineComponent } from 'vue';


export default defineComponent({
	props: {
		label: {
			type: String,
			required: true
		}
	}
})

</script>


<template>

	<label class="block">
		<span class="block">{{ label }}</span>
		<div class="mt-3"> 
			<slot></slot>
		</div>
	</label>

</template>