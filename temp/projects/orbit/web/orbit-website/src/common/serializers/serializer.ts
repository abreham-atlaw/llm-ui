export default abstract class Serializer<F, T>{

	abstract serialize(instance: F): T

	abstract deserialize(data: T): F

	public serializeMany(instances: F[]): T[]{
		return instances.map(
			(instance: F) => {
				return this.serialize(instance);
			}
		)
	}

	public deserializeMany(dataArray: T[]): F[]{
		return dataArray.map(
			(data: T) => {
				return this.deserialize(data);
			}
		)
	}


}