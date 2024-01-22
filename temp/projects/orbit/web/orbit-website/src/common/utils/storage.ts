import Cookies from "js-cookie";



export default abstract class Storage{

	abstract store(key: string, value: string): Promise<void>;

	abstract get(key: string): Promise<string | null>;

}


export class CookieStorage extends Storage{
	async store(key: string, token: string): Promise<void> {
		await Cookies.set(key, token);
	}
	async get(key: string): Promise<string | null> {
		return Cookies.get(key) ?? null;
	}

}