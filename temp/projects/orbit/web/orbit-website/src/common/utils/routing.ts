import { useRouter, useRoute, type RouteLocationRaw } from "vue-router";



export default class RoutingUtils{

	static redirect(to: string){
		window.location.assign(to);
	}

	static async download(url: string, filename: string = "file"){
		const response = await fetch(url);
		if (!response.ok) 
			throw new Error("Network response was not ok");
		const blob = await response.blob();
		const downloadUrl = window.URL.createObjectURL(blob);
		const link = document.createElement("a");
		link.href = downloadUrl;
		link.download = `${filename}.txt`; // use your desired file name here
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	}

	static getUrlParams(){
		const router = useRoute();
		return router.query;
	}

}