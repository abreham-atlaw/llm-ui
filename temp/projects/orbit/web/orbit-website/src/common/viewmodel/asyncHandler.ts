import { AsyncState, AsyncStatus } from "../state/baseState";
import BaseState from "../state/baseState";
import ViewModel from "./viewmodel";



export default abstract class AsyncHandler<E, S extends BaseState>{


	private viewModel: ViewModel<S>;

	public constructor(viewModel: ViewModel<S>){
		this.viewModel = viewModel;
	}

	private extractError(value: any): Error{
		if(value instanceof Error){
			return value
		}
		let message: string;
		if(value.toString != undefined){
			message = value.toString();
		}
		else{
			message = String(value)
		}
		return new Error(message);
	}

	protected getAsyncState(state: S): AsyncState{
		return state as unknown as AsyncState;
	}


	protected onError(state: S, error: any){
		this.getAsyncState(state).status = AsyncStatus.failed;
		this.getAsyncState(state).error = this.extractError(error);
		this.viewModel.syncState()
	}

	protected onDone(state: S){
		this.getAsyncState(state).status = AsyncStatus.done;
		this.viewModel.syncState()
	}

	protected onLoading(state: S){
		this.getAsyncState(state).status = AsyncStatus.loading;
		this.viewModel.syncState()
	}

	protected abstract onEvent(viewModel: ViewModel<S>, event: E, state: S): Promise<void>;

	public async handle(event: E){
		await this.onLoading(this.viewModel.state);
		try{
			await this.onEvent(this.viewModel, event, this.viewModel.state);
			await this.onDone(this.viewModel.state);
		}
		catch(ex){
			console.log("Caught Exception")
			console.log(ex)
			await this.onError(this.viewModel.state, ex);
		}
	}

}