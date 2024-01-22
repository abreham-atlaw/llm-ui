<template>
	<div>
		<textarea
        class="h-full"
		:class="`${inputClass} color-${textColor} bg-${bg} border border-${borderWidth} border-${borderColor} text-${textColor} rounded-${borderRadius} focus:outline-none font-medium leading-none py-5 w-full pl-3`"
		:value="(field.getValue() === null) ? '' : field.getValue()"
		:placeholder="placeholder"
		@input="handleInput"
		></textarea>
		<div
		v-if="field.error != null"
		class="text-red-500"
		>
		{{ field.error }}
		</div>
	</div>
</template>
	
<script lang="ts">

import Field from "@/common/forms/fields.js"
export default {
	props: {
		value: {
			type: String,
			default: null,
		},
		field: {
			type: Field<string>,
			default: null
		},
		stateSyncer: {
			type: Function,
			default: null
		},
		bg:{
			type: String,
			default: "light"
		},
		inputClass: {
			type: String,
			default: ""
		},
		borderRadius:{
			type: String,
			default: "2xl"
		},
		borderWidth:{
			type: String,
			default: "2"
		},
		borderColor: {
			type: String,
			default: "grey"
		},
		textColor: {
			type: String,
			default: "dark"
		},
		placeholder: {
			type: String,
			default: ""
		}
	},
	methods: {
		handleInput(event: any) {
			console.log("Value Changed")
			this.field.setValue(event.target.value);
			if(this.stateSyncer != null){
				this.stateSyncer();
			}
		},
	},
};
</script>
