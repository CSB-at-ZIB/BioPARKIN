package topo;

import field.DoubleField;
/**
 * The one dimensional double precision floating point topo space
 * @author bzfmuell
 *
 * @param <A>
 */
public class DoubleDim1<A extends AbstractRelation<DoubleField,A>> implements TopoSpace<DoubleDim1<A>,DoubleField> {
	
	public static final Lt LT = new Lt();
	
	public static final Gt GT = new Gt();
	/**The non-negative double precision floating point range: any element in the range <tt>[0,infinity)</tt>
	 * belongs to this set*/
	public static final DoubleDim1<InRange> NON_NEGATIVE = new DoubleDim1<InRange>(new InRange(DoubleField.ZERO,new DoubleField(Double.MAX_VALUE)));
	
	protected A relation;
	
	protected DoubleDim1 (){}
	
	public DoubleDim1 (A relation){
		this.relation = relation;
	}
	
	public boolean contains(DoubleField element){
		if(relation!=null){
			PairedElement<DoubleField> base = relation.basePoint;
			if(base!=null) {
				return relation.isRelated(element, base.getFirst())||relation.isRelated(element, base.getSecond());
			}
			return false;
		}
		return false;
	}
	
	public DoubleDim1<A> complement(){
		return new DoubleDim1<A> (relation.complement());
	}
	
	public DoubleDim1<A> intersect(DoubleDim1<A> another) {
		
		return relation==null||another.relation==null?new DoubleDim1<A>(null): new DoubleDim1<A> (relation.intersect(another.relation));
	}

	
	public boolean isEmpty() {
		return relation==null?true:relation.basePoint==null?true:false;
	}

	
	public boolean isOpen() {
		if(relation==null) return true;
		return !relation.isClosed();
	}

	
	public DoubleDim1<A> union(DoubleDim1<A> another) {
		return relation==null&&another.relation==null?new DoubleDim1<A>(null):new DoubleDim1<A>(relation.union(another.relation));
	}

	
	public boolean isSuperSet(DoubleDim1<A> another) {
		return intersect(another).equals(this);
	}

	
	public boolean isSubSet(DoubleDim1<A> another) {
		return intersect(another).equals(another);
	}
	
	public final static class Lt extends AbstractRelation<DoubleField,Lt> {
		
		private Lt (){
			super();
			basePoint = new PairedElement<DoubleField>(DoubleField.M_ONE,DoubleField.ONE);
		}

		public boolean isEmpty() {
			return false;
		}

		
		public boolean isOpen() {return true;}

		
		public boolean isClosed() {
			return false;
		}

		
		public boolean isRelated(DoubleField first, DoubleField second) {
			return first.compareTo(second)<0?true:false;
		}
		
	}
	
	public final static class Le extends AbstractRelation<DoubleField,Le> {
		
		private Le (){
			super();
		}
		
		public boolean isEmpty() {
			// TODO Auto-generated method stub
			return false;
		}

		
		public boolean isOpen() {
			// TODO Auto-generated method stub
			return false;
		}

		
		public boolean isClosed() {
			// TODO Auto-generated method stub
			return false;
		}

		
		public boolean isRelated(DoubleField first, DoubleField second) {
			// TODO Auto-generated method stub
			return false;
		}
				
	}
	
	public final static class Gt extends AbstractRelation<DoubleField,Gt> {
		
		private Gt (){
			super();
			basePoint = new PairedElement<DoubleField> (DoubleField.ONE,DoubleField.M_ONE);
		}
		
		public boolean isEmpty() {
			return false;
		}

		
		public boolean isOpen() {return true;}

		
		public boolean isClosed() {return false;}

		
		public boolean isRelated(DoubleField first, DoubleField second) {
			return first.compareTo(second)>0?true:false;
		}
		
	}
}
