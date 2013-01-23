package topo;

import java.util.Random;

import homomorphism.GenericDual;
import module.GenericVSpace;
import field.DoubleField;

public class DoubleSpace<A extends AbstractRelation<GenericVSpace<DoubleField>,A>> extends AbstractTopo<GenericVSpace<DoubleField>> {
	private A rel;
	private PairedElement<GenericVSpace<DoubleField>> basePoint;
	private boolean isEmpty;
	public DoubleSpace() {}
	
	public DoubleSpace(A rel){
		if(rel!=null){
			this.rel = rel;
			if((basePoint = rel.basePoint())==null) isEmpty = true;			
		}
	}
	
	public DoubleSpace<A> complement(){return new DoubleSpace<A>(rel.inverse());}
	
	public boolean contains(GenericVSpace<DoubleField> element) {
		return rel.isRelated(basePoint.getFirst(),element)||rel.isRelated(basePoint.getSecond(),element);
	}

	
	public DoubleSpace<A> intersect(DoubleSpace<A> another) {
		return new DoubleSpace<A>(rel.intersect(another.rel));
	}

	
	public boolean isEmpty() {isEmpty = rel.isEmpty(); return isEmpty;}

	
	public boolean isOpen() {
		if(isEmpty) return true;
		return rel.isClosed()?false:true;
	}

	
	public DoubleSpace<A> union(DoubleSpace<A> another) {return new DoubleSpace<A>(rel.union(another.rel));}

	
	public boolean isSuperSet(DoubleSpace<A> another) {
		if(!intersect(another).isEmpty()){
			return union(another).equals(another)?true:false;
		}
		return false;
	}

	
	public boolean isSubSet(DoubleSpace<A> another) {
		return another.isSuperSet(this);
	}
	public static void main(String[] args){
	
	}
}
