import { AxiosHeaders, type AxiosRequestConfig, type AxiosRequestHeaders } from "axios";

export default class Request<T>{

	public config: AxiosRequestConfig;

	constructor(config: AxiosRequestConfig){
		this.config = config;
	}

	deserializeResponse(response: any): T{
		return response;
	}

}