import DataConfigs from "@/configs/dataConfigs";
import AuthenticatedNetworkClient from "@/common/network/AuthenticatedNetworkClient";
import NetworkClient from "@/common/network/NetworkClient";
import type TokenStorage from "@/common/utils/tokenStorage";
import { CookieTokenStorage } from "@/common/utils/tokenStorage";
import type Storage from "@/common/utils/storage";
import { CookieStorage } from "@/common/utils/storage";



export default class CoreProviders{


	static networkClient?: NetworkClient;
	static authenticatedClient?: AuthenticatedNetworkClient;

	static provideNetworkClient(): NetworkClient{
		if(this.networkClient === undefined){
			this.networkClient = new NetworkClient(DataConfigs.API_URL);
		}
		return this.networkClient;
	}

	static async provideAuthenticatedNetworkClient(): Promise<AuthenticatedNetworkClient>{
		if(this.authenticatedClient === undefined){
			const token = await this.provideAuthToken();
			this.authenticatedClient = new AuthenticatedNetworkClient(DataConfigs.API_URL, token!);
		}
		return this.authenticatedClient!;
	}

	static async provideAuthToken(): Promise<string | null>{
		return await this.provideTokenStorage().get();
	}

	static provideTokenStorage(): TokenStorage{
		return new CookieTokenStorage();
	}

	static provideStorage(): Storage{
		return new CookieStorage();
	}

}