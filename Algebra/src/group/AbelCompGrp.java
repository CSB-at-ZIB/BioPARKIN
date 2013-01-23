package group;

public abstract class AbelCompGrp<A extends AbelCompGroup<A>> implements
		AbelCompGroup<A> {

	public AbelCompGrp (){}

	
	public A operate(A another) {return add(another);}
	@SuppressWarnings("unchecked")
	public boolean equals (Object o){
		if(this==o) return true;
		if(!(o instanceof AbelCompGrp)) return false;
		return equals((AbelCompGrp<A>) o)?true:false;
	}
}
