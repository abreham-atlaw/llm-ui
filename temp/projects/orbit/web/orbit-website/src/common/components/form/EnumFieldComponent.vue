<template>
	<div>
		<div v-for="(item, index) in enumValues" :key="index">
			<label class="block mt-5">
                <input
                    class="hidden w-full"
                    :class="`bg-${bg} border border-${borderWidth} border-${borderColor} text-${textColor} rounded-${borderRadius} focus:outline-none font-medium leading-none text-gray-800 py-5 w-full pl-3`"
                    type="radio"
                    :value="item"
                    v-model="selectedValue"
                    @change="handleInput"
                />
                <div class="border-light border rounded-xl flex p-5" :class="(selectedValue === item) ? 'bg-light text-dark' : 'text-light'">
                    
                    <div class="w-10 h-10 rounded-full border border light flex" :class="(selectedValue === item) ? 'bg-primary text-light' : ''">

                        <span v-if="selectedValue === item" class="fas fa-check m-auto"></span>

                    </div>

                    <div class="my-auto ml-5">
                        {{ enumLabels[item] }}
                    </div>

                </div>
            </label>
		</div>
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
		enumClass: {
            type: Object,
            required: true
        },
        bg:{
			type: String,
			default: "primaryDark"
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
			default: "light"
		},
		textColor: {
			type: String,
			default: "light"
		},
        labels: {
            type: Array,
            default: null
        }
        // ... rest of your props
    },
    data() {
        return {
            selectedValue: this.value,
            enumValues: Object.values(this.enumClass).filter(value => !isNaN(Number(value))),
            enumLabels: this.labels ?? Object.values(this.enumClass).filter(value => isNaN(Number(value))),
        }
    },
	methods: {
        // ... rest of your methods
        handleInput() {
            console.log("Value Changed")
            this.field.setValue(this.selectedValue);
            if(this.stateSyncer != null){
                this.stateSyncer();
            }
        },
    },
};
</script>
@/common/forms/fields.js