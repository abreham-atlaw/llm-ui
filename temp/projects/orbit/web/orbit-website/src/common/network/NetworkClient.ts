import axios, {AxiosHeaders, type AxiosInstance, type AxiosRequestConfig, type AxiosResponse} from "axios";
import Request from "./Request";


export default class NetworkClient{

	private client?: AxiosInstance;
	private baseUrl: string;

	constructor(baseUrl: string){
		this.baseUrl = baseUrl;
	}

	protected onCreateClient(baseUrl: string): AxiosInstance{
		return axios.create({
			baseURL: baseUrl,
		});
	}

	private getClient(): AxiosInstance{
		if(this.client === undefined){
			this.client = this.onCreateClient(this.baseUrl);
		}
		return this.client!;
	}

	async execute<T>(request: Request<T>): Promise<T>{

		let response: AxiosResponse = await this.getClient()(request.config);
		
		if(response.status >= 400){
			throw new ApiException(response.status, response.data);
		}

		return request.deserializeResponse(response.data);

	}



}


export class ApiException extends Error{

	public statusCode: number;
	public message: string;

	constructor(statusCode: number, message: string){
		super(`${statusCode}: ${message}`);
		this.statusCode = statusCode;
		this.message = message;
	}
}