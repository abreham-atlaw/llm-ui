<template>
	<div class="h-full">
	  <slot name="loading" v-if="isLoading"><LoadingView/></slot>
	  <slot name="failed" v-else-if="isFailed" :error="state.initState.error"><ErrorView :error="state.initState.error!"/></slot>
	  <slot v-else></slot>
	</div>
  </template>
  
<script lang="ts">
import { defineComponent } from "vue";
import LoadingView from "./LoadingView.vue";
import ErrorView from "./ErrorView.vue";
import BaseState from "@/common/state/baseState";
import ViewModel from "@/common/viewmodel/viewmodel";
import { AsyncStatus } from "@/common/state/baseState";

export default defineComponent({
	
	props: {
		state: {
			type: BaseState,
			required: true
		},
		viewModel: {
			type: ViewModel,
			required: true
		}
	},
	created() {
		this.viewModel.initialize();
	},

	computed: {
		isLoading() {
			return (
				this.state.initState.status === AsyncStatus.loading ||
				this.state.initState.status === AsyncStatus.none
			);
		},
	
		isFailed() {
			return this.state.initState.status === AsyncStatus.failed;
		}
	},
	
	components: {
		LoadingView,
		ErrorView
	}
});
</script>@/common/state/baseState@/common/viewmodel/viewmodel@/common/state/baseState@/common/state/baseState