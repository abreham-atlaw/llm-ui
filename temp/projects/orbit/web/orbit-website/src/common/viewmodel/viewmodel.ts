import BaseState from "../state/baseState";
import { FunctionalAsyncHandler } from "./asyncViewModel";
import { sleep } from "../utils/time";
import { AsyncStatus } from "../state/baseState";


export default class ViewModel<S extends BaseState>{

	public state: S;


	constructor(state: S){
		this.state = state;
	}

	public async onInit(){
		await new Promise( async (resolve, reject) => {
			while(!this.isReady()){
				await sleep(100);
			}
			resolve(true);
		})
	}

	public isReady(): boolean{
		return true;
	}

	public initialize = async () => {
		if(this.state.initState.status != AsyncStatus.none){
			return;
		}
		let initHandler = new FunctionalAsyncHandler<BaseState>(
			this,
			async () => {
				await this.onInit()
			},
			undefined,
			undefined,
			undefined,
			() => {
				return this.state.initState
			}
		)
		await initHandler.handle({});
	}

	public setState(state: S){
		// this.stateSetter(state)
		this.state = state;
	}

	public syncState(){
		this.setState(this.state);
	}

}
