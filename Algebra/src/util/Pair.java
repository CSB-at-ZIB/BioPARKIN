package util;

public class Pair<X> {
	private X first;
	private X second;
	public Pair(X first, X second) {
		this.first  =  first;
		this.second = second;
	}
	public boolean equals(Object o){
		if(this==o) return true;
		if(!(o instanceof Pair)) return false;
		Pair<?> cp = (Pair<?>) o;
		return cp.first.equals(first)&&cp.second.equals(second)?true:false;
	}
	public X getFirst(){return first==null?null:first;}
	public X getSecond(){return second==null?null:second;}
}
