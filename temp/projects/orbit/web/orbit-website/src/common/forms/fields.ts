import { sleep } from "../utils/time";

export default class Field<T>{

	public value :T | null = null;
	public error : string | null = null;
	public required: boolean;
	public validator: Function | null;
	public liveValidate: boolean;

	constructor(required: boolean = true, validator: Function|null = null, liveValidate: boolean = true, validationGap: number = 2000){
		this.required = required;
		this.validator = validator;
		this.liveValidate = liveValidate;
	}

	public async isValid(): Promise<boolean>{
		this.error = await this.validate();
		if(this.error === null){
			return true;
		}
		return false
	}

	public async validate(): Promise<string | null>{
		if(this.required && this.getValue() === null){
			return "This field is required";
		}
		if(this.validator != null){
			return this.validator(this.getValue())
		}
		return null;
	}

	public getValue(): T | null{
		return this.value;
	}

	public async setValue(value: T|null){
		this.value = value;
		if(this.liveValidate){
			await this.isValid()
		}
	}

}

export class TextField extends Field<string>{

	private emptyAsNull: boolean;
	constructor(
		required: boolean = true, 
		validator: Function|null = null, 
		liveValidate: boolean = true,
		emptyAsNull: boolean = true
	){
		super(required, validator, liveValidate)
		this.emptyAsNull = emptyAsNull
	}

	public getValue(): string | null {
		const value = super.getValue()
		if(this.emptyAsNull && value === ""){
			return null;
		}
		return value;
	}

}
