

export default class BaseState {
    public initState = {
        status: AsyncStatus.none,
        error: null,
    };

}

export enum AsyncStatus{
	none = 0, 
	loading = 1,
	done = 2,
	failed = 3
}

export class AsyncState extends BaseState{

	public status: AsyncStatus;
	public error: Error;

	constructor(status: AsyncStatus = AsyncStatus.none, error: any = null){
		super();
		this.status = status;
		this.error = error;
	}

}
