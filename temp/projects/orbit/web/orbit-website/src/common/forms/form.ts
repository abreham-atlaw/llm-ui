import Field  from "./fields";


export default abstract class Form{

	
	abstract getFields(): Array<Field<any>>


	public async validate(throw_error: boolean = false): Promise<boolean>{

		let valid = true;

		for(let field of this.getFields()){
			if(!(await field.isValid())){
				valid = false
			}
		}
		if(throw_error && !valid){
			throw new ValidationException("Error in form");
		}

		return valid;

	}

}

export class ValidationException extends Error{

}