import AsyncHandler from "./asyncHandler";
import ViewModel from "./viewmodel";
import { AsyncState } from "../state/baseState";
import BaseState from "../state/baseState";


export class FunctionalAsyncHandler<S extends BaseState> extends AsyncHandler<any, S>{

	private onEventCallback: Function;

	constructor(
		viewModel: ViewModel<S>,
		onEvent: Function,
		onError?: Function,
		onDone?: Function,
		onLoading?: Function,
		asyncStateGetter?: Function
	){
		super(viewModel);
		this.onEventCallback = onEvent.bind(this);
		if(onError != undefined){
			this.onError = onError.bind(this);
 		}
		if(onDone != undefined){
			this.onDone = onDone.bind(this);
		} 
		if(onLoading != undefined){
			this.onLoading = onLoading.bind(this);
		}
		if(asyncStateGetter != undefined){
			this.getAsyncState = asyncStateGetter.bind(this);
		}
	}

	protected async onEvent(_viewModel: ViewModel<S>, _event: any, state: S): Promise<void> {
		return await this.onEventCallback(state);
	}
			
}


export default class AsyncViewModel<S extends BaseState> extends ViewModel<S>{
	
	
	protected async asyncCall(
		onEvent: Function,
		asyncState?: AsyncState,
		onError?: Function,
		onDone?: Function,
		onLoading?: Function
	){
		let asyncStateGetter;
		if(asyncState != undefined){
			asyncStateGetter = () => {return asyncState}
		}	
		let handler = new FunctionalAsyncHandler<S>(
			this,
			onEvent,
			onError,
			onDone,
			onLoading,
			asyncStateGetter
		);
		await handler.handle(null);
	}


}