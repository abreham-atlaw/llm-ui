import Cookies from "js-cookie";



export default abstract class TokenStorage{

	abstract store(token: string): Promise<void>;

	abstract get(): Promise<string | null>;

}


export class CookieTokenStorage extends TokenStorage{
	async store(token: string): Promise<void> {
		await Cookies.set("AUTH_TOKEN", token);
	}
	async get(): Promise<string | null> {
		return Cookies.get("AUTH_TOKEN") ?? null;
	}

}