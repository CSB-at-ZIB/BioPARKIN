package topo;

import util.Pair;

public class PairedElement<E extends Element<E>>
		extends Pair<E> implements Element<PairedElement<E>> {

	public PairedElement(E first, E second) {
		super(first, second);
		// TODO Auto-generated constructor stub
	}
	public PairedElement(Pair<E> pair){
		super(pair.getFirst(),pair.getSecond());
	}

	public boolean equals(PairedElement<E> another) {return super.equals(another);}
	
	public Class<?> getElementClass(){
		E first = getFirst(), second = getSecond();
		return first!=null?first.getClass():second!=null?second.getClass():null;
	}

}
