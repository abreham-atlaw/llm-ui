<template>
	<div>
		<input
		:class="`${inputClass} color-${textColor} bg-${bg} border border-${borderWidth} border-${borderColor} text-${textColor} rounded-${borderRadius} focus:outline-none font-medium leading-none py-3 w-full pl-3`"
		:type=type
		:value="(field.getValue() === null) ? '' : field.getValue()"
		:placeholder="placeholder"
		@change="handleInput"
		/>
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
		type: {
			type: String,
			default: "text"
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
			default: "full"
		},
		borderWidth:{
			type: String,
			default: "1"
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
		},
		onChange:{
			type: Function,
			default: null
		}
	},
	methods: {
		handleInput(event: any) {
			console.log("Value Changed")
			this.field.setValue(event.target.value);
			if(this.stateSyncer != null){
				this.stateSyncer();
			}
			if(this.onChange != null){
				this.onChange(event.target.value);
			}
		},
	},
};
</script>