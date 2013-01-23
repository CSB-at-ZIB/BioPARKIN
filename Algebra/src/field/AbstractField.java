package field;

import java.util.Iterator;
import java.util.Map.Entry;
import java.util.TreeMap;

import module.VectorSpace;
import ring.AbstractCommRing;

public abstract class AbstractField<A extends AbstractField<A>> extends AbstractCommRing<A>
		implements Field<A>, VectorSpace<A,A> {
	
	public AbstractField (){super();}
	public void clear (){}
	public boolean isUnit(){return isZero()?false:true;}
	public boolean equals(AbstractField<A> another){return add(another.addInverse()).isZero()?true:false;}
	public A multiplyLeft(A another){return multiply(another);}
	public A multiplyRight(A another){return multiply(another);}
	public Iterator<Entry<Integer,A>> iterator(){return new AFIterator ();}
	public void setEntry(int i, A coeff){}
	public Integer getIndex (A coeff){return equals(coeff)?0:null;}
	public A ringAct (A scalar){return multiply(scalar);}
	@SuppressWarnings("unchecked")
	public A getValue (int index){return (A) this;}
	public A remove (int index){return null;}
	public abstract A constructOne ();
	protected class AFIterator implements Iterator<Entry<Integer,A>> {
		private TreeMap<Integer,A> map;
		private Iterator<Entry<Integer,A>> it;
		@SuppressWarnings("unchecked")
		protected AFIterator (){
			map = new TreeMap<Integer,A> ();
			map.put(0,(A) A.this);
			it  = map.entrySet().iterator();
		}
		public boolean hasNext (){return it.hasNext()?true:false;}
		public Entry<Integer,A> next(){return it.next();}
		public void remove (){}
	}
	
}
