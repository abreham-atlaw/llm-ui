<!-- <template>

	<ViewModelView :viewModel="viewModel" :state="state">
		<slot></slot>
	</ViewModelView>

</template>
  
<script lang="ts">
import { defineComponent, ref } from "vue";
import { AsyncState, AsyncStatus } from "@/common/state/baseState";
import AuthenticationStatus from "@/features/auth/data/models/authenticationStatus";
import Role from "@/apps/auth/data/models/roles";
import LoadingView from "./LoadingView.vue";
import ErrorView from "./ErrorView.vue";
import AsyncViewModel from "@/common/viewmodel/asyncViewModel";
import AuthRepository from "@/apps/auth/data/repository/authRepository";
import ViewModelView from "./ViewModelView.vue";


class AuthenticatedComponentState extends AsyncState{
	authenticationStatus?: AuthenticationStatus;
}


class AuthenticatedComponentViewModel extends AsyncViewModel<AuthenticatedComponentState>{

	private authRepository = new AuthRepository();

	public async onInit(): Promise<void> {
		await super.onInit();
		this.state.authenticationStatus = await this.authRepository.getAuthenticationStatus();
	}


}


export default defineComponent({
	props: {
		validStatus: {
			type: Array,
			default: () => [AuthenticationStatus.authenticated]
		},
		redirectionMap: {
			type: Map,
			default: () => new Map()
		},
		redirectTo: {
			type: String,
			default: "/auth/login"
		}
	},
	data() {
		let state = ref(new AuthenticatedComponentState());

		return {
			state: state,
			viewModel: new AuthenticatedComponentViewModel(state.value),
			currentLocation: window.location
		};
	},
	computed: {
		
		isLoading() {
			return (
				this.state.status === AsyncStatus.loading ||
				this.state.status === AsyncStatus.none
			);
		},
		
		isFailed() {
			return this.state.status === AsyncStatus.failed;
		},
		
		isValidStatus() {
			return this.validStatus.includes(this.state.authenticationStatus);
		},
		
		targetLocation() {
			const status = this.state.authenticationStatus;
			let targetLocation = this.redirectionMap.get(status);
			if (targetLocation === undefined) {
				targetLocation = this.redirectTo;
				if (targetLocation === undefined) {
				throw new TargetPathNotFoundException();
				}
			}
			const futureRedirect =
				new URLSearchParams(this.currentLocation.search).get("redirect") ||
				this.currentLocation.pathname;
			return `${targetLocation}?redirect=${futureRedirect}`;
		}
	},

	watch: {
		state: {
			handler(newValue: AuthenticatedComponentState){
				if(newValue.initState.status != AsyncStatus.done){
					return;
				}
				if(!this.isValidStatus){
					window.location.assign(this.targetLocation);
				}
			},
			deep: true
		}
		
	},

	components: {
		LoadingView,
		ErrorView,
		ViewModelView
	}
});

class TargetPathNotFoundException extends Error {}
</script>@/common/state/baseState@/common/viewmodel/asyncViewModel@/common/state/baseState -->